# Helps you to Validate emails in Real Time
# Copyright (c) 2013 Pravendra Singh <hackpravj@yahoo.com,hackpravj@gmail.com>


# ----------------------------------------------source file portion------------------------------------------

#['requests' for making http-requests, 're' for local-grammatical-email-verification, 'json' for encoding data in json]
import requests
import json
import re

# sample email-address to check
# paste here yours by input field or via any mean
# I'm pasting mine addresses
input_email = 'hackpravj@gmail.com' # 'hackpravj@yahoo.com'

# local-verification of emails
def is_grammatical_correct(input_email):

	# here valid email are in form of 'alphanumeric_or_periods(.)'@'alphabate'.'alphabate'

	match = re.match(r'[a-z0-9\.]+@[a-z\.a-z]+',input_email)
	if(match):
		return True
	else:
		return False

# position of '@' sign
atSign_ = input_email.find('@')

# username portion 
username = input_email[:atSign_]

# domain portion
domain_ = input_email[atSign_+1:]

# currently supported domains
domains = {'gmail':'gmail.com','yahoo':'yahoo.com'}

# tracking a particular domain
_which_ = 0

for x in domains:
	if (domains[x] == domain_):
		_which_ = x

if (str(type(_which_))=="<type 'str'>"):
	argument = str(_which_)
else:
	raise Exception("No such supported domain.")
# argument will have particular domain type ['yahoo' or 'gmail']

# processing ahead
def validate(argument):
	if (argument == 'gmail'):
		# for gmail
		origin_url = 'https://accounts.google.com'
		target_url = origin_url+'/InputValidator'
		_keyValue_ = {'resource':'SignUp','service':'mail'}

		# data, to be sent there
		load = {"input01":{"Input":"GmailAddress","GmailAddress":username,"FirstName":"","LastName":""},"Locale":"en"}	

		# required headers
		header = {'host':'accounts.google.com','method':'POST','path':'/InputValidator?resource=SignUp&service=mail','scheme':'https','version':'HTTP/1.1','accpet':'*/*','accept-encoding':'gzip,deflate,sdch','accept-language':'en-US,en;q=0.8','content-length':'106','content-type':'application/json','origin':'https://accounts.google.com','referer':'https://accounts.google.com/SignUp?service=mail&continue=https%3A%2F%2Fmail.google.com%2Fmail%2F&ltmpl=default'}	

		# making http-requests and showing results
		# gmail use "POST" request for this mean
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

		# making http-requests and showing results
		# yahoo use "GET" request for this mean
		try:
			rq_Yahoo  = requests.get(yahoo_url,params=keyValue_)

			if(rq_Yahoo.status_code == 200):
				if(rq_Yahoo.json()['ResultCode']=='PERMANENT_FAILURE'):
					print 'this email-address already exists'

				elif(rq_Yahoo.json()['ResultCode']=='SUCCESS'):
					print 'this email-address does not exists'
		except:
			raise Exception('unable to communicate')


# -------------------------------------------------test file portion-------------------------------------------------

if(is_grammatical_correct(input_email)):
	validate(argument)

else:
	raise Exception('entered email is not grammatically correct')
