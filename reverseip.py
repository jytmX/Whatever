#!/usr/bin/env python3
import os, requests, sys, time
from colorama import init, Fore, Style
from concurrent.futures import ThreadPoolExecutor
from socket import gethostbyname

s = requests.Session()

try:
	os.mkdir('Result') #createfolder
except:
    pass

init()
r = Fore.RED + Style.BRIGHT
g = Fore.GREEN + Style.BRIGHT
c = Fore.CYAN + Style.BRIGHT
oo = Fore.YELLOW + Style.BRIGHT
o = Fore.RESET + Style.RESET_ALL

headers = {'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
banner = """
[!] {}KIKO FREE{} - {}REVERSE{}

[+] {}Option{} :    1. {}Reverse IP {}-{} Website List{}
                2. {}Subdomain Finder {}-{} Website List{}
                3. {}Reverse IP & Subdomain Finder {}-{} Website LIst{}

                99. {}Exit{}
""".format(g, o, g, o, g, o, g, o, g, o, g, o, g, o, g, o, g, o, r, o)

def Rev1(i):
    dup = []
    try:
        if i.startswith("http://"):
            i = i.replace("http://", "")
        elif i.startswith("https://"):
            i = i.replace("https://", "")
        iii = i.replace("/", "")
        ii = gethostbyname(iii)
        req = s.get('https://sonar.omnisint.io/reverse/' + ii, headers=headers).json()
        print('[#] {}Reverse {}http://{} {}[{} {} {}Domains ]{}'.format(g, o, i, g, o, len(req), g, o))
        for domain in req:
            hapus = domain.replace("_", "").replace("autodiscover.", "").replace("cpanel.", "").replace("cpcalendars.", "").replace("cpcontacts.", "").replace("error:Invalid IPv4 address","").replace("ftp.", "").replace("mail.", "").replace("ns1.", "").replace("ns2.", "").replace("ns3.","").replace("ns4.","").replace("webdisk.", "").replace("webmail.", "").replace("www.", "").replace("error", "")
            if hapus not in dup:
                dup.append(hapus)
                open("Result/rever.txt", "a+").write(hapus + '\n')
    except:
        pass

def Subdo1(i):
    dup = []
    try:
        if i.startswith("http://"):
            i = i.replace("http://", "")
        elif i.startswith("https://"):
            i = i.replace("https://", "")
        iii = i.replace("/", "")
        req = s.get('https://sonar.omnisint.io/subdomains/' + iii, headers=headers).json()
        print('[#] {}Subdomain {}http://{} {}[{} {} {}Domains ]{}'.format(g, o, i, g, o, len(req), g, o))
        for domain in req:
            hapus = domain.replace("www.", "")
            if hapus not in dup:
                dup.append(hapus)
                open("Result/subdomain.txt", "a+").write(hapus + '\n')
    except:
        pass

def RevSub1(i):
    dup = []
    try:
        if i.startswith("http://"):
            i = i.replace("http://", "")
        elif i.startswith("https://"):
            i = i.replace("https://", "")
        iii = i.replace("/", "")
        ii = gethostbyname(iii)
        req = s.get('https://sonar.omnisint.io/reverse/' + ii, headers=headers).json()
        rq = s.get('https://sonar.omnisint.io/subdomains/' + iii, headers=headers).json()
        print('[#] {}Reverse {}http://{} {}[{} {} {}Domains ]{}'.format(g, o, i, g, o, len(req), g, o))
        print('[#] {}Subdomain {}http://{} {}[{} {} {}Domains ]{}'.format(g, o, i, g, o, len(rq), g, o))
        for domain in req:
            hapus = domain.replace("_", "").replace("autodiscover.", "").replace("cpanel.", "").replace("cpcalendars.", "").replace("cpcontacts.", "").replace("error:Invalid IPv4 address","").replace("ftp.", "").replace("mail.", "").replace("ns1.", "").replace("ns2.", "").replace("ns3.","").replace("ns4.","").replace("webdisk.", "").replace("webmail.", "").replace("www.", "")
            if hapus not in dup:
                dup.append(hapus)
                open("Result/reverseip.txt", "a+").write(hapus + '\n')
        for domain in rq:
            hapus = domain.replace("www.", "")
            if hapus not in dup:
                dup.append(hapus)
                open("Result/subdomain.txt", "a+").write(hapus + '\n')
    except:
        pass

def Main():
    try:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(banner)
        heyyo = input('[?] {}Choose{} > '.format(g, o))

        if heyyo == '1':
            awww = input('\n[+] {}Website List{} > {}'.format(g, o, g))
            thrd = input('{}[+] {}Thread{} > '.format(o, g, o))
            print('')
            try:
                listmu = open(awww, 'r').read().splitlines()
                with ThreadPoolExecutor(max_workers=int(thrd)) as e:
                    [e.submit(Rev1, i) for i in listmu]
            except:
                print('{}[!] {}Incorrect'.format(o, r))
                time.sleep(0.5)
    
        elif heyyo == '2':
            awww = input('\n[+] {}Website List{} > {}'.format(g, o, g))
            thrd = input('{}[+] {}Thread{} > '.format(o, g, o))
            print('')
            try:
                listmu = open(awww, 'r').read().splitlines()
                with ThreadPoolExecutor(max_workers=int(thrd)) as e:
                    [e.submit(Subdo1, i) for i in listmu]
            except:
                print('{}[!] {}Incorrect'.format(o, r))
                time.sleep(0.5)
    
        elif heyyo == '3':
            awww = input('\n[+] {}Website List{} > {}'.format(g, o, g))
            thrd = input('{}[+] {}Thread{} > '.format(o, g, o))
            print('')
            try:
                listmu = open(awww, 'r').read().splitlines()
                with ThreadPoolExecutor(max_workers=int(thrd)) as e:
                    [e.submit(RevSub1, i) for i in listmu]
            except:
                print('[!] {}Incorrect'.format(r))
                time.sleep(0.5)
    
        elif heyyo == '99':
            print('\n[+] {}Thanks For Download My Tool'.format(g))
            time.sleep(0.5)
            sys.exit()

        else:
            print('{}\n[!] {}Incorrect{},{} Please Choose Number {}1 - 3,{} and Number {}99{} For {}Exit'.format(o, g, o, g, o, g, o, g, r))
            time.sleep(0.5)
    
    except KeyboardInterrupt:
        print('{}\n\n[!] {}CTRL {}+{} C'.format(o, r, o, r))
        time.sleep(0.5)

if __name__ == '__main__':
    Main()
    
    
    
    
    