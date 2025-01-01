import requests
import warnings
from urllib3.exceptions import InsecureRequestWarning
from requests.exceptions import RequestException, Timeout
import os
import threading
import time
import pyfiglet
from colorama import Fore

# Menonaktifkan InsecureRequestWarning (Peringatan SSL)
warnings.simplefilter('ignore', InsecureRequestWarning)

# ASCII Art dan informasi GitHub
ascii_art = pyfiglet.figlet_format("CMS CHECKER V1")
print(Fore.CYAN + ascii_art)
print(Fore.YELLOW + "GitHub: https://github.com/pengodehandal/Mass-CMS-Checker/")

# Penjelasan tentang tools
print(Fore.GREEN + "Tools ini adalah alat untuk mengecek CMS (Content Management System) website.")
print(Fore.GREEN + "CMS yang dideteksi: WordPress, Joomla, Magento, Drupal, PrestaShop, Laravel, Shopify, dll.")
print(Fore.RED + "Harap gunakan tools ini dengan bijak. 💻🔍")

# Fungsi untuk deteksi CMS
def check_cms(url):
    try:
        # Mengirim request dengan timeout 3 detik dan non-verify SSL
        response = requests.get(url, timeout=3, verify=False)
        
        # Jika status code 200, lanjutkan deteksi CMS
        if response.status_code == 200:
            print(Fore.GREEN + f"Website {url} berhasil diakses. Deteksi CMS sedang dilakukan...")
            return detect_cms(url, response.text)
        else:
            print(Fore.YELLOW + f"Website {url} mengembalikan status {response.status_code}.")
            return None
    except Timeout:
        # Menangani timeout
        print(Fore.RED + f"Website {url} tidak merespons dalam waktu yang ditentukan. Timeout.")
        return None
    except RequestException as e:
        # Menangani exception lain
        print(Fore.RED + f"Error saat mencoba mengakses {url}: {e}")
        return None

# Fungsi deteksi CMS
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
    # Tambahkan logika deteksi CMS lainnya jika diperlukan

    if cms:
        print(Fore.CYAN + f"{url}: {cms}")
        save_to_file(cms, url)
    else:
        print(Fore.RED + f"{url}: Tidak dapat menemukan CMS.")

    return cms

# Fungsi untuk menyimpan hasil ke file sesuai CMS
def save_to_file(cms, url):
    filename = f"{cms.lower()}.txt"
    
    # Membuka file untuk menambahkan URL
    if os.path.exists(filename):
        with open(filename, "a") as file:
            file.write(url + "\n")
    else:
        with open(filename, "w") as file:
            file.write(url + "\n")

# Fungsi untuk memproses daftar website dari file
def process_websites(file_name, threads=10):
    with open(file_name, 'r') as f:
        websites = [line.strip() for line in f.readlines() if line.strip()]
    
    print(Fore.YELLOW + f"Mulai pengecekan {len(websites)} website dengan {threads} threads...")
    
    # Membagi task ke beberapa threads
    def check_in_thread(urls):
        for url in urls:
            if url:
                check_cms(url)

    # Membagi URL menjadi beberapa bagian berdasarkan jumlah thread
    websites_per_thread = len(websites) // threads
    threads_list = []

    for i in range(threads):
        start = i * websites_per_thread
        end = start + websites_per_thread if i < threads - 1 else len(websites)
        thread = threading.Thread(target=check_in_thread, args=(websites[start:end],))
        threads_list.append(thread)
        thread.start()

    # Menunggu semua threads selesai
    for thread in threads_list:
        thread.join()

    print(Fore.GREEN + "Pengecekan CMS selesai.")

# Main function untuk menjalankan tools
def main():
    # Input file dan thread
    file_name = input(Fore.YELLOW + "Masukkan nama file daftar website (misal: websites.txt): ")
    threads = input(Fore.YELLOW + "Masukkan jumlah threads (default: 10): ")
    threads = int(threads) if threads else 10
    
    process_websites(file_name, threads)

# Jalankan tools
if __name__ == "__main__":
    main()
