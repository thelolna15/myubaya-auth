import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs, urljoin
import time
import sys
import getpass
from colorama import Fore, Style, init

# Inisialisasi colorama
init(autoreset=True)

def print_colored(message, color="white", end="\n"):
    """
    Fungsi untuk mencetak pesan dengan warna tertentu.
    """
    colors = {
        "red": Fore.RED,
        "green": Fore.GREEN,
        "yellow": Fore.YELLOW,
        "blue": Fore.BLUE,
        "magenta": Fore.MAGENTA,
        "cyan": Fore.CYAN,
        "white": Fore.WHITE
    }
    color_code = colors.get(color.lower(), Fore.WHITE)
    print(f"{color_code}{message}{Style.RESET_ALL}", end=end)

def get_credentials():
    """
    Meminta pengguna untuk memasukkan username dan password dengan validasi.
    Password akan dimasukkan secara tersembunyi.
    Menangani KeyboardInterrupt untuk keluar dengan bersih jika pengguna menekan Ctrl+C.
    """
    try:
        while True:
            username = input("Masukkan Username: ").strip()
            if not username:
                print_colored("Username tidak boleh kosong. Silakan coba lagi.", "red")
                continue
            break

        while True:
            password = getpass.getpass("Masukkan Password: ").strip()
            if not password:
                print_colored("Password tidak boleh kosong. Silakan coba lagi.", "red")
                continue
            break
    except KeyboardInterrupt:
        print_colored("\n[INFO] Program dihentikan oleh pengguna.", "yellow")
        sys.exit(0)

    return username, password

def logout(session, headers):
    """
    Fungsi melakukan logout dengan mengakses endpoint logout.
    """
    logout_url = 'https://my.ubaya.ac.id/index2.php/login_detail/action~logout/'
    try:
        print_colored("\n[INFO] Melakukan logout...", "cyan")
        response = session.get(logout_url, headers=headers, allow_redirects=False)
        
        if response.status_code in [200, 302]:
            if response.status_code == 302:
                redirect_location = response.headers.get('Location')
                if redirect_location:
                    redirect_full = urljoin('https://my.ubaya.ac.id', redirect_location)
                    session.get(redirect_full, headers=headers)
            print_colored("[SUCCESS] Logout berhasil.", "green")
        else:
            print_colored("[WARNING] Gagal melakukan logout.", "yellow")
    except requests.exceptions.RequestException as e:
        print_colored(f"[ERROR] Terjadi kesalahan saat logout: {e}", "red")

def perform_logout_after_delay(session, headers, delay):
    """
    Fungsi untuk menunggu selama 'delay' detik sebelum melakukan logout.
    Jika ada interupsi (Ctrl+C), segera melakukan logout.
    """
    try:
        for remaining in range(delay, 0, -1):
            sys.stdout.write(f"\r[INFO] Logout otomatis dalam {remaining} detik. Tekan Ctrl+C untuk logout segera.")
            sys.stdout.flush()
            time.sleep(1)
        print()
        print_colored("[INFO] Waktu logout otomatis telah tiba.", "cyan")
        logout(session, headers)
    except KeyboardInterrupt:
        print_colored("\n[INFO] Interupsi manual diterima. Melakukan logout segera...", "yellow")
        logout(session, headers)
        sys.exit(0)

def main():
    # Inisialisasi sesi
    session = requests.Session()
    
    # Header Request
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:133.0) Gecko/20100101 Firefox/133.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }
    
    # Banner
    print_colored("="*35, "magenta")
    print_colored("Authentication - My UBAYA".center(35), "magenta")
    print_colored("By TheLoLNA15".center(35), "magenta")
    print_colored("="*35, "magenta")
    
    username, password = get_credentials()
    
    # Langkah 1: GET halaman login untuk mendapatkan CSRF token
    login_url = 'https://ws.ubaya.ac.id/oauth2/login'
    try:
        response = session.get(login_url, headers=headers)
        response.raise_for_status()
        print_colored(f"\n[INFO] Mengakses halaman login: {login_url}", "cyan")
    except requests.exceptions.RequestException as e:
        print_colored(f"[ERROR] Gagal mengakses halaman login: {e}", "red")
        sys.exit(1)
    
    # Parsing CSRF token
    soup = BeautifulSoup(response.text, 'html.parser')
    csrf_input = soup.find('input', {'name': '_token'})
    if not csrf_input:
        print_colored("[ERROR] CSRF token tidak ditemukan.", "red")
        sys.exit(1)
    csrf_token = csrf_input['value']
    print_colored("[INFO] CSRF token ditemukan.", "cyan")
    
    # Langkah 2: POST data login
    login_data = {
        '_token': csrf_token,
        'intendedpage': '',
        'username': username,
        'password': password,
    }
    
    try:
        response = session.post(login_url, data=login_data, headers=headers, allow_redirects=False)
        print_colored(f"[INFO] Melakukan POST data login ke: {login_url}", "cyan")
        
        if response.status_code == 302:
            redirect_url = response.headers.get('Location')
            print_colored("[INFO] Mengarahkan ke halaman home...", "cyan")
            response = session.get(redirect_url, headers=headers)
        elif response.status_code == 200:
            print_colored("[SUCCESS] Login berhasil atau diarahkan ke halaman home.", "green")
        else:
            print_colored("[ERROR] Gagal login. Periksa kembali kredensial Anda.", "red")
            sys.exit(1)
    except requests.exceptions.RequestException as e:
        print_colored(f"[ERROR] Gagal melakukan POST data login: {e}", "red")
        sys.exit(1)
    
    # Langkah 3: Akses halaman home
    home_url = 'https://ws.ubaya.ac.id/oauth2/home'
    try:
        response = session.get(home_url, headers=headers)
        response.raise_for_status()
        print_colored(f"[INFO] Mengakses halaman home: {home_url}", "cyan")
    except requests.exceptions.RequestException as e:
        print_colored(f"[ERROR] Gagal mengakses halaman home: {e}", "red")
        sys.exit(1)
    
    # Langkah 4: Akses endpoint OAuth dengan handle redirect manual
    authorize_url = (
        'https://ws.ubaya.ac.id/oauth2/oauth/authorize'
        '?response_type=code'
        '&client_id=e73fc503-83de-11ec-af57-664866c1a16d'
        '&redirect_uri=https%3A%2F%2Fmy.ubaya.ac.id%2Findex2.php%2Flogin_detail%2Faction~oauth2_callback%2F'
        '&state=532e0b32caeae31c40248f14791ff2cfbef1fcb0b14b7e1b2ee6483fa3494b2a'
        '&scope=user.info'
    )
    
    try:
        response = session.get(authorize_url, headers=headers, allow_redirects=False)
        
        if response.status_code == 302:
            redirect_location = response.headers.get('Location')
            
            # Parsing URL redirect untuk mendapatkan 'code' dan 'state'
            parsed_url = urlparse(redirect_location)
            query_params = parse_qs(parsed_url.query)
            code = query_params.get('code', [None])[0]
            state = query_params.get('state', [None])[0]
            
            if not code or not state:
                print_colored("[ERROR] LOGIN GAGAL.", "red")
                sys.exit(1)
            
            print_colored("[SUCCESS] Login berhasil.", "green")
            
            # Langkah 5: Akses callback OAuth dengan 'code' dan 'state' yang diperoleh
            callback_url = (
                'https://my.ubaya.ac.id/index2.php/login_detail/action~oauth2_callback/'
                f'?code={code}&state={state}'
            )
            try:
                response = session.get(callback_url, headers=headers, allow_redirects=False)
                
                if response.status_code == 302:
                    final_redirect = response.headers.get('Location')
                    final_redirect_full = urljoin('https://my.ubaya.ac.id', final_redirect)
                    response = session.get(final_redirect_full, headers=headers)
                    print_colored("[SUCCESS] Mengakses callback OAuth dan redirect akhir.", "green")
                elif response.status_code == 200:
                    print_colored("[SUCCESS] Callback diakses dengan sukses.", "green")
                else:
                    print_colored("[ERROR] Gagal mengakses callback URL.", "red")
                    sys.exit(1)
            except requests.exceptions.RequestException as e:
                print_colored(f"[ERROR] Terjadi kesalahan saat mengakses callback OAuth: {e}", "red")
                sys.exit(1)
        else:
            print_colored("[ERROR] Respons tidak diharapkan selama otorisasi OAuth.", "red")
            sys.exit(1)
    except requests.exceptions.RequestException as e:
        print_colored(f"[ERROR] Gagal mengakses endpoint OAuth: {e}", "red")
        sys.exit(1)
    
    # Langkah 6: Akses root untuk mendapatkan cookie
    root_url = 'https://my.ubaya.ac.id/'
    try:
        response = session.get(root_url, headers=headers)
        response.raise_for_status()
        print_colored(f"[INFO] Mengakses root URL: {root_url}", "cyan")
        print()
    except requests.exceptions.RequestException as e:
        print_colored(f"[ERROR] Gagal mengakses root URL: {e}", "red")
        sys.exit(1)
    
    # Ambil cookie neoweb
    neoweb_cookie = session.cookies.get('neoweb')
    if neoweb_cookie:
        print_colored(f"[SUCCESS] Cookie 'neoweb' ditemukan: {neoweb_cookie}", "green")
    else:
        print_colored("[WARNING] Cookie 'neoweb' tidak ditemukan. Tidak perlu logout.", "yellow")
        sys.exit(0)
    
    # Langkah 7: Delay sebelum logout dengan countdown
    delay_seconds = 120
    try:
        print_colored(f"\n[INFO] Program akan logout otomatis dalam {delay_seconds} detik.", "cyan")
        for remaining in range(delay_seconds, 0, -1):
            sys.stdout.write(f"\r[INFO] Logout otomatis dalam {remaining} detik. Tekan Ctrl+C untuk logout segera.")
            sys.stdout.flush()
            time.sleep(1)
        print()
        print_colored("[INFO] Waktu logout otomatis telah tiba.", "cyan")
        logout(session, headers)
    except KeyboardInterrupt:
        print_colored("\n[INFO] Interupsi manual diterima. Melakukan logout segera...", "yellow")
        logout(session, headers)
        sys.exit(0)

if __name__ == "__main__":
    main()
