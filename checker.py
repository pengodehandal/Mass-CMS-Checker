import requests
import warnings
from urllib3.exceptions import InsecureRequestWarning
from requests.exceptions import RequestException, Timeout, ConnectionError
import os
import threading
import time
import pyfiglet
from colorama import Fore
from urllib.parse import urlparse

warnings.simplefilter('ignore', InsecureRequestWarning)

ascii_art = pyfiglet.figlet_format("CMS CHECKER V1")
print(Fore.CYAN + ascii_art)
print(Fore.YELLOW + "GitHub: https://github.com/pengodehandal/Mass-CMS-Checker/")
print(Fore.GREEN + "Tools ini adalah alat untuk mengecek CMS (Content Management System) website.")
print(Fore.GREEN + "CMS yang dideteksi: WordPress, Joomla, Magento, Drupal, PrestaShop, Laravel, Shopify, dll.")
print(Fore.RED + "Harap gunakan tools ini dengan bijak. 💻🔍")

def add_scheme(url):
    parsed_url = urlparse(url)
    if not parsed_url.scheme:
        return f'http://{url}'
    return url

def check_cms(url):
    url = add_scheme(url)
    
    try:
        response = requests.get(url, timeout=3, verify=False)
        
        if response.status_code == 200:
            print(Fore.GREEN + f"Website {url} berhasil diakses. Deteksi CMS sedang dilakukan...")
            return detect_cms(url, response.text)
        else:
            print(Fore.YELLOW + f"Website {url} mengembalikan status {response.status_code}.")
            return None
    except Timeout:
        print(Fore.RED + f"Website {url} tidak merespons dalam waktu yang ditentukan. Timeout.")
        return None
    except RequestException as e:
        print(Fore.RED + f"Error saat mencoba mengakses {url}: {str(e)}")
        return None
    except ConnectionError:
        print(Fore.RED + f"Website {url} tidak dapat dijangkau. Cek koneksi atau DNS.")
        return None
    except Exception as e:
        print(Fore.RED + f"Terjadi kesalahan saat mencoba mengakses {url}: {str(e)}")
        return None

def detect_cms(url, html_content):
    cms = None
    if '/wp-content/' in html_content:
        cms = 'WordPress'
    elif '/administrator/' in html_content:
        cms = 'Joomla'
    elif '/shop/' in html_content:
        cms = 'Magento'
    elif '/wp-admin/' in html_content:
        cms = 'WordPress'
    elif '/drupal/' in html_content:
        cms = 'Drupal'
    elif '/presta/' in html_content:
        cms = 'PrestaShop'
    elif 'Laravel' in html_content:
        cms = 'Laravel'

    if cms:
        print(Fore.CYAN + f"{url}: {cms}")
        save_to_file(cms, url)
    else:
        print(Fore.RED + f"{url}: Tidak dapat menemukan CMS.")

    return cms

def save_to_file(cms, url):
    filename = f"{cms.lower()}.txt"
    
    if os.path.exists(filename):
        with open(filename, "a") as file:
            file.write(url + "\n")
    else:
        with open(filename, "w") as file:
            file.write(url + "\n")

def process_websites(file_name, threads=10):
    with open(file_name, 'r') as f:
        websites = [line.strip() for line in f.readlines() if line.strip()]
    
    print(Fore.YELLOW + f"Mulai pengecekan {len(websites)} website dengan {threads} threads...")
    
    def check_in_thread(urls):
        for url in urls:
            if url:
                check_cms(url)

    websites_per_thread = len(websites) // threads
    threads_list = []

    for i in range(threads):
        start = i * websites_per_thread
        end = start + websites_per_thread if i < threads - 1 else len(websites)
        thread = threading.Thread(target=check_in_thread, args=(websites[start:end],))
        threads_list.append(thread)
        thread.start()

    for thread in threads_list:
        thread.join()

    print(Fore.GREEN + "Pengecekan CMS selesai.")

def main():
    file_name = input(Fore.YELLOW + "Masukkan nama file daftar website (misal: websites.txt): ")
    threads = input(Fore.YELLOW + "Masukkan jumlah threads (default: 10): ")
    threads = int(threads) if threads else 10
    
    process_websites(file_name, threads)

if __name__ == "__main__":
    main()

