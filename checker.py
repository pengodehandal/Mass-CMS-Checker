import requests
import warnings
from urllib3.exceptions import InsecureRequestWarning
from requests.exceptions import RequestException, Timeout, ConnectionError
import os
import concurrent.futures
import time
import pyfiglet
from colorama import Fore
from urllib.parse import urlparse
import sys

# Mengabaikan peringatan terkait SSL (InsecureRequestWarning)
warnings.simplefilter('ignore', InsecureRequestWarning)

# ASCII art dan intro
ascii_art = pyfiglet.figlet_format("CMS CHECKER V1")
print(Fore.CYAN + ascii_art)
print(Fore.YELLOW + "GitHub: https://github.com/pengodehandal/Mass-CMS-Checker/")
print(Fore.GREEN + "Tools ini adalah alat untuk mengecek CMS (Content Management System) website.")
print(Fore.GREEN + "CMS yang dideteksi: WordPress, Joomla, Magento, Drupal, PrestaShop, Laravel, Shopify, ZBlog, dll.")
print(Fore.RED + "Harap gunakan tools ini dengan bijak.")

# Menambahkan skema 'http://' jika tidak ada
def add_scheme(url):
    parsed_url = urlparse(url)
    if not parsed_url.scheme:
        return f'http://{url}'
    return url

# Fungsi utama untuk memeriksa CMS
def check_cms(url, session):
    url = add_scheme(url)
    
    try:
        response = session.get(url, timeout=3, verify=False)  # Timeout set to 3 seconds
        if response.status_code == 200:
            detect_cms(url, response.text)
        else:
            print(Fore.RED + f"{url} > Tidak Dapat Menemukan CMS")
    except (Timeout, RequestException, ConnectionError, Exception):
        print(Fore.RED + f"{url} > Tidak Dapat Menemukan CMS")

# Fungsi untuk mendeteksi CMS
def detect_cms(url, html_content):
    cms = None
    color = None

    # Deteksi CMS yang umum
    if '/wp-content/' in html_content:
        cms = 'WordPress'
        color = Fore.BLUE
    elif '/administrator/' in html_content:
        cms = 'Joomla'
        color = Fore.GREEN
    elif '/shop/' in html_content:
        cms = 'Magento'
        color = Fore.MAGENTA
    elif '/wp-admin/' in html_content:
        cms = 'WordPress'
        color = Fore.BLUE
    elif '/drupal/' in html_content:
        cms = 'Drupal'
        color = Fore.CYAN
    elif '/presta/' in html_content:
        cms = 'PrestaShop'
        color = Fore.YELLOW
    elif 'Laravel' in html_content:
        cms = 'Laravel'
        color = Fore.RED
    elif 'Shopify' in html_content:
        cms = 'Shopify'
        color = Fore.BLUE
    elif 'ghost' in html_content:
        cms = 'Ghost'
        color = Fore.MAGENTA
    elif 'hubspot' in html_content:
        cms = 'HubSpot'
        color = Fore.LIGHTGREEN_EX
    # Deteksi ZBlog
    elif '/zb_system/' in html_content:
        cms = 'ZBlog'
        color = Fore.CYAN

    # Menampilkan hasil deteksi CMS
    if cms:
        print(f"{color}{url} > CMS > {cms}")
        save_to_file(cms, url)
    else:
        print(Fore.RED + f"{url} > Tidak Dapat Menemukan CMS")

# Menyimpan hasil ke dalam file
def save_to_file(cms, url):
    filename = f"{cms.lower()}.txt"
    
    with open(filename, "a") as file:
        file.write(url + "\n")

# Fungsi untuk memproses daftar website
def process_websites(file_name, threads=10):
    with open(file_name, 'r') as f:
        websites = [line.strip() for line in f.readlines() if line.strip()]
    
    print(Fore.YELLOW + f"Mulai pengecekan {len(websites)} website dengan {threads} threads...")
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
        session = requests.Session()  # Reuse connection
        executor.map(lambda url: check_cms(url, session), websites)

    print(Fore.GREEN + "Pengecekan CMS selesai.")

# Fungsi utama
def main():
    file_name = input(Fore.YELLOW + "Masukkan nama file daftar website (misal: websites.txt): ")
    threads = input(Fore.YELLOW + "Masukkan jumlah threads (default: 10): ")
    threads = int(threads) if threads else 10
    
    process_websites(file_name, threads)

# Menjalankan program
if __name__ == "__main__":
    main()
