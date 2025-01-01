import requests
import threading
import os
from concurrent.futures import ThreadPoolExecutor
from colorama import init, Fore
import pyfiglet

init(autoreset=True)

ascii_art = pyfiglet.figlet_format("CMS CHECKER V1")
print(Fore.CYAN + ascii_art + Fore.YELLOW + "GitHub: https://github.com/pengodehandal/Mass-CMS-Checker/")

print(Fore.GREEN + "\nTools ini adalah tools untuk mengecek CMS seperti:")
print(Fore.GREEN + "WordPress, Joomla, Magento, Drupal, PrestaShop, Laravel, Shopify, Wix, SquareSpace, Ghost, Typo3, Craft CMS, Hugo.")
print(Fore.YELLOW + "Harap gunakan tools ini dengan bijak ya!\n")

cms_dict = {
    'WordPress': ['/wp-content/', '/wp-includes/', '/wp-admin/'],
    'Joomla': ['/administrator/', '/components/com_'],
    'Magento': ['/admin/'],
    'Drupal': ['/user/login', '/node/add'],
    'PrestaShop': ['/modules/'],
    'Laravel': ['/vendor/', '/artisan'],
    'Shopify': ['/collections/'],
    'Wix': ['/static/'],
    'Squarespace': ['/config/'],
    'Ghost': ['/ghost/'],
    'Typo3': ['/typo3/'],
    'Craft CMS': ['/craft/'],
    'Hugo': ['/index.html'],
}

cms_count = {cms: 0 for cms in cms_dict}
cms_count['No CMS'] = 0

def detect_cms(website):
    try:
        if not website.startswith('http://') and not website.startswith('https://'):
            website = 'http://' + website

        response = requests.get(website, timeout=3, verify=False)

        if response.status_code != 200:
            print(f"{Fore.RED}{website}: {Fore.YELLOW}Error - Status Code {response.status_code}")
            save_to_file('No CMS', website)
            return

        for cms_name, paths in cms_dict.items():
            for path in paths:
                if path in response.text:
                    print(f"{Fore.GREEN}{website}: {Fore.CYAN}{cms_name} Detected")
                    save_to_file(cms_name, website)
                    cms_count[cms_name] += 1
                    return

        print(f"{Fore.RED}{website}: {Fore.YELLOW}No CMS detected or site might be custom-built.")
        save_to_file('No CMS', website)
        cms_count['No CMS'] += 1
    except requests.exceptions.RequestException as e:
        print(f"{Fore.RED}{website}: {Fore.YELLOW}Error - {e}")

def save_to_file(cms_name, website):
    file_name = cms_name.lower().replace(" ", "_") + '.txt'

    if not is_duplicate(file_name, website):
        with open(file_name, 'a') as f:
            f.write(website + '\n')

def is_duplicate(file_name, website):
    if not os.path.exists(file_name):
        return False

    with open(file_name, 'r') as f:
        existing_websites = f.readlines()

    return website + '\n' in existing_websites

def check_websites_from_file(file_name, threads):
    with open(file_name, 'r') as f:
        websites = f.readlines()

    websites = list(set(website.strip() for website in websites))

    with ThreadPoolExecutor(max_workers=threads) as executor:
        executor.map(detect_cms, websites)

def main():
    print(f"{Fore.GREEN}Welcome to the CMS Checker Tool!")
    print(f"{Fore.GREEN}Please provide the list of websites to check in a text file.")
    file_name = input(f"{Fore.YELLOW}Enter the file name (e.g., websites.txt): ")
    threads = input(f"{Fore.YELLOW}Enter number of threads (default 10): ")
    
    if not threads:
        threads = 10
    else:
        threads = int(threads)

    if os.path.exists(file_name):
        print(f"{Fore.GREEN}Starting the CMS detection process...")
        check_websites_from_file(file_name, threads)
        print(f"{Fore.GREEN}CMS detection completed.")

        print(f"\n{Fore.GREEN}Total CMS Detection Summary:")
        for cms_name, count in cms_count.items():
            print(f"{Fore.CYAN}{cms_name}: {Fore.YELLOW}{count}")
    else:
        print(f"{Fore.RED}File '{file_name}' not found. Please provide a valid file.")

if __name__ == '__main__':
    main()
