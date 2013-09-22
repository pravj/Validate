import requests
import json
import re

input_email = 'hackpravj@gmail.com'

def is_grammatical_correct(input_email):

	# here valid email are in form of 'alphanumeric_or_periods(.)'@'alphabate'.'alphabate'

	match = re.match(r'[a-z0-9\.]+@[a-z\.a-z]+',input_email)
	if(match):
		return True
	else:
		return False

atSign_ = input_email.find('@')

username = input_email[:atSign_]

domain_ = input_email[atSign_+1:]

domains = {'gmail':'gmail.com','yahoo':'yahoo.com'}

_which_ = 0

for x in domains:
	if (domains[x] == domain_):
		_which_ = x

if (str(type(_which_))=="<type 'str'>"):
	argument = str(_which_)
else:
	raise Exception("No such supported domain.")

def validate(argument):
	if (argument == 'gmail'):
		# for gmail
		origin_url = 'https://accounts.google.com'
		target_url = origin_url+'/InputValidator'
		_keyValue_ = {'resource':'SignUp','service':'mail'}

		load = {"input01":{"Input":"GmailAddress","GmailAddress":username,"FirstName":"","LastName":""},"Locale":"en"}	

		header = {'host':'accounts.google.com','method':'POST','path':'/InputValidator?resource=SignUp&service=mail','scheme':'https','version':'HTTP/1.1','accpet':'*/*','accept-encoding':'gzip,deflate,sdch','accept-language':'en-US,en;q=0.8','content-length':'106','content-type':'application/json','origin':'https://accounts.google.com','referer':'https://accounts.google.com/SignUp?service=mail&continue=https%3A%2F%2Fmail.google.com%2Fmail%2F&ltmpl=default'}	

		try:
			rq_Gmail = requests.post(target_url,params=_keyValue_,data=json.dumps(load),headers=header)
			
			if (rq_Gmail.status_code == 200):
				if(rq_Gmail.json()['input01']['Valid'] == 'true'):
					print 'this email-address does not exists'
				elif((rq_Gmail.json()['input01']['Errors']['GmailAddress']) == 'Someone already has that username. Try another?'):
					print 'this email-address already exists'
		except:
			raise Exception('Unable to communicate')

	elif (argument == 'yahoo'):
		# for yahoo
		yahoo_url = 'https://na.edit.yahoo.com/reg_json'
		keyValue_ = {'GivenName':'','FamilyName':'','AccountID':input_email,'PartnerName':'yahoo_default','ApiName':'ValidateFields'}

		try:
			rq_Yahoo  = requests.get(yahoo_url,params=keyValue_)

			if(rq_Yahoo.status_code == 200):
				if(rq_Yahoo.json()['ResultCode']=='PERMANENT_FAILURE'):
					print 'this email-address already exists'

				elif(rq_Yahoo.json()['ResultCode']=='SUCCESS'):
					print 'this email-address does not exists'
		except:
			raise Exception('unable to communicate')


if(is_grammatical_correct(input_email)):
	validate(argument)

else:
	raise Exception('entered email is not grammatically correct')
