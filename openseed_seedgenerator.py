#!/usr/bin/python

import hashlib
import sys
sys.path.append("..")
import mysql.connector
import json
import random
import openseed_setup as Settings
import openseed_account as Account

settings = Settings.get_settings()


def generate_userid(name,passphrase,email):
	fullstring = name+passphrase+email
	count1 = 0
	count2 = 0
	mixer1 = ""
	mixer2 = ""
	mixer3 = ""
	for m1 in fullstring:
		if count1 % 2 == 0:
			mixer1 = mixer1+m1
		else:
		     mixer2 = mixer2+m1.upper()
		count1 +=1
	
	hash1 = hashlib.md5(mixer1.encode())
	hash2 = hashlib.md5(mixer2.encode())
	
	count3 = 0
	stir = ""
	if len(str(hash1.hexdigest())) >= len(str(hash2.hexdigest())):
		stir = str(hash1.hexdigest())
	else:
		stir = str(hash2.hexdigest())
	
	while count3 < len(mixer1):
		mixer3 = mixer3+str(hash1.hexdigest()[count3])+str(hash2.hexdigest()[count3])
		count3 += 1

	return mixer3

def generate_userid_new(name,passphrase,email):
	fullstring = name+passphrase+email
	count1 = 0
	count2 = 0
	mixer1 = ""
	mixer2 = ""
	mixer3 = ""
	for m1 in fullstring:
		if count1 % 2 == 0:
			mixer1 = mixer1+m1
		else:
		     mixer2 = mixer2+m1.upper()
		count1 +=1
	
	hash1 = hashlib.md5(mixer1.encode())
	hash2 = hashlib.md5(mixer2.encode())
	
	count3 = 0
	stir = ""
	if len(str(hash1.hexdigest())) >= len(str(hash2.hexdigest())):
		stir = str(hash1.hexdigest())
	else:
		stir = str(hash2.hexdigest())
	
	while count3 < len(stir):
		mixer3 = mixer3+str(hash1.hexdigest()[count3])+str(hash2.hexdigest()[count3])
		count3 += 1

	return mixer3

def generate_id(name,contactname,contactemail,account):
	fullstring = name+contactemail+account+contactname
	count1 = 0
	count2 = 0
	mixer1 = ""
	mixer2 = ""
	mixer3 = ""
	for m1 in fullstring:
		if count1 % 2 == 0:
			mixer1 = mixer1+m1
		else:
		     mixer2 = mixer2+m1.upper()
		count1 +=1
	
	hash1 = hashlib.md5(mixer1.encode())
	hash2 = hashlib.md5(mixer2.encode())

	if len(str(hash1.hexdigest())) >= len(str(hash2.hexdigest())):
		stir = str(hash1.hexdigest())
	else:
		stir = str(hash2.hexdigest())
	
	count3 = 0	
	while count3 < len(stir):
		mixer3 = mixer3+str(hash1.hexdigest()[count3])+str(hash2.hexdigest()[count3])
		count3 += 1

	return mixer3

def generate_publicid(id):
	random.seed()
	fullstring = str(random.random())+id+str(random.random())
	count1 = 0
	count2 = 0
	mixer1 = ""
	mixer2 = ""
	mixer3 = ""
	for m1 in fullstring:
		if count1 % 2 == 0:
			mixer1 = mixer1+m1
		else:
		     mixer2 = mixer2+m1.upper()
		count1 +=1
	
	hash1 = hashlib.md5(mixer1.encode())
	hash2 = hashlib.md5(mixer2.encode())

	count3 = 0	
	while count3 < len(hash1.hexdigest()):
		mixer3 = mixer3+str(hash1.hexdigest()[count3])+str(hash2.hexdigest()[count3])
		count3 += 1

	return mixer3[0:8]

def generate_usertoken(id):
	random.seed()
	fullstring = ""
	while len(fullstring) < 256:
		fullstring = fullstring+str(random.random())+id+str(random.random())
	
	count1 = 0
	count2 = 0
	mixer1 = ""
	mixer2 = ""
	mixer3 = ""
	for m1 in fullstring:
		if count1 % 2 == 0:
			mixer1 = mixer1+m1
		else:
		     mixer2 = mixer2+m1.upper()
		count1 +=1
	
	hash1 = hashlib.md5(mixer1.encode())
	hash2 = hashlib.md5(mixer2.encode())

	count3 = 0	
	while count3 < len(hash1.hexdigest()):
		mixer3 = mixer3+str(hash1.hexdigest()[count3])+str(hash2.hexdigest()[count3])
		count3 += 1

	return mixer3


def to_char(thecode):
	code = ""
	num = 0
	while num < len(thecode):
		try:
			test = int(thecode[num:num+2])
		except:
			pass
		else:
			code = code+chr(test)
		num = num + 2

	return code

def crypt_key():
	fullstring = ""
	while len(fullstring) < 256:
		fullstring = fullstring+str(random.random()).split(".")[1]\
			+to_char(str(random.random()).split(".")[1])\
			+str(random.random()).split(".")[1]\
			+to_char(str(random.random()).split(".")[1])


	count1 = 0
	count2 = 0
	mixer1 = ""
	mixer2 = ""
	mixer3 = ""

	for m1 in fullstring:
		if count1 % 2 == 0:
			mixer1 = mixer1+m1
		else:
			mixer2 = mixer2+m1.upper()
		count1 +=1

	hash1 = hashlib.md5(mixer1.encode())
	hash2 = hashlib.md5(mixer2.encode())
	mixer3 = str(mixer1.encode())+str(hash1.hexdigest())+str(mixer2.encode())+str(hash2.hexdigest()).replace(" ","2").replace("/","1").replace("'","0").replace(",","5").replace('"',"6").replace(':',"C").replace('#',"P").replace('\!',"p")
	mixer3 = mixer3.replace("`","A").replace("&","Q").replace("=","E").replace("(","T").replace(")","t")
	mixer3 = mixer3.replace("[","3").replace("]","9").replace("-","H").replace("+","h").replace("*","W").replace("%","w").replace("^","K")
	mixer3 = mixer3.replace("@","3").replace("$","9").replace("_","H").replace(";","h").replace("|","W").replace("{","w").replace("}","K")
	mixer3 = mixer3.replace("<","3").replace(">","9").replace("!","H").replace("~","h").replace('\?',"p").replace('\.',"p").replace('.',"p")
	mixer3 = mixer3.replace("\'","3").replace('\"',"9").replace("\,","H").replace("\~","h").replace('\:',"p").replace('\#',"p").replace('.',"p").replace("\\","F")
 
	return mixer3

def store_onetime(thetype,register,validusers):
	code = crypt_key()
	openseed = mysql.connector.connect(
		host = "localhost",
		user = settings["dbuser"],
		password = settings["dbpassword"],
		database = "openseed"
		)
	mysearch = openseed.cursor()
	check = "SELECT codenum FROM onetime WHERE code = %s"
	val = (code,)
	mysearch.execute(check,val)
	result = mysearch.fetchall()
	if len(result) < 1:
		insert = "INSERT INTO `onetime` (type,code,registered,validusers) VALUES (%s,%s,%s,%s)"
	vals = (thetype,code,register,validusers)
	mysearch.execute(insert,vals)
	openseed.commit()

	mysearch.close()
	openseed.close()

	return code

def update_key(thetype,register,validusers):
	reg = ""
	code = ""
	openseed = mysql.connector.connect(
		host = "localhost",
		user = settings["dbuser"],
		password = settings["dbpassword"],
		database = "openseed"
		)
	mysearch = openseed.cursor()
	check = "SELECT registered,code FROM onetime WHERE validusers = %s AND type = %s"
	val1 = (validusers,thetype)
	val2 = (validusers.split(",")[1]+","+validusers.split(",")[0],thetype)
	mysearch.execute(check,val1)
	result1 = mysearch.fetchall()
	mysearch.execute(check,val2)
	result2 = mysearch.fetchall()

	if validusers.find(Account.user_from_id(register)) != -1: 
		if len(result1) == 1:
			reg = result1[0][0].decode()

			if reg != register:
				code = result1[0][1].decode()
			else:
				code = result1[0][1].decode()
 
		if len(result2) == 1:
			reg = result2[0][0].decode()

			if reg != register:
				code = result2[0][1].decode()
			else:
				code = result2[0][1].decode()
	else:
  		code = "denied"   
   
	openseed.commit()
	mysearch.close()
	openseed.close()

	return str(code)

def get_room_key(token,room):
	reg = ""
	code = ""
	openseed = mysql.connector.connect(
		host = "localhost",
		user = settings["dbuser"],
		password = settings["dbpassword"],
		database = "openseed"
		)
	mysearch = openseed.cursor()
	username = json.loads(Account.user_from_id(token))["user"]
	check = "SELECT code FROM onetime WHERE validusers LIKE %s AND room = %s"
	val1 = ("%"+username+"%",room)
	mysearch.execute(check,val1)
	result = mysearch.fetchall()
	if len(result) == 1:
		code = result[0][0]
	
	openseed.commit()
	mysearch.close()
	openseed.close()

	return str(code)
	
	
def get_key(thetype,register,room):
	result = ""
	#cleanroom = room.split("[")[1].split("]")[0]
	#wharoom = cleanroom.split(",")[0]+', '+cleanroom.split(",")[1]
	#reverseroom = cleanroom.split(",")[1]+', '+cleanroom.split(",")[0]
	reg = ""
	code = ""
	openseed = mysql.connector.connect(
		host = "localhost",
		user = settings["dbuser"],
		password = settings["dbpassword"],
		database = "openseed"
		)
	mysearch = openseed.cursor()
	check = "SELECT registered,code,validusers FROM onetime WHERE room = %s AND type = %s"
	val1 = (room,thetype)
	#val2 = (reverseroom,thetype)
	mysearch.execute(check,val1)
	result1 = mysearch.fetchall()
	#mysearch.execute(check,val2)
	#result2 = mysearch.fetchall()
	if len(result1) == 1:
		result = result1
	#elif len(result2) == 1:
	#	result = result2
	else:
		result = 0

	if result != 0:
		validusers = result[0][2]
		vuser = json.loads(Account.user_from_id(register))["user"]
		
		if validusers.find(vuser) != -1: 
			if len(result1) == 1:
				reg = result[0][0]
			if reg != register:
				code = '{"room":"'+room+'","key":"'+result[0][1]+'"}'
			else:
				code = '{"room":"'+room+'","key":"'+result[0][1]+'"}'
		else:
			code = '{"room":"denied","key":"denied"}'
	else:
		code = '{"room":"denied","key":"denied"}'

	openseed.commit()
	mysearch.close()
	openseed.close()
	return '{"lock":'+str(code)+'}'


def simp_crypt(key,raw_data):
	num_array = []
	
	for c in key:
		if c in ["2","4","6","8"]:
			num_array.append(c)
				
	while len(num_array) < len(raw_data):
		num_array += num_array
	num_array += num_array
	
	secret = ""
	datanum = 0
	digits = ""
	key_digits = ""
	key_stretch = key
	keystring = "" 

	#//lets turn it into integers first//
	for t in raw_data:
		c = ord(t)
		digits += str(c)+" "
		
	data = digits
	
	if key_stretch != "":
		if len(data)> len(key_stretch):
			while len(key_stretch) < len(data):
				key_stretch = key_stretch + key
				
	key_stretch = key_stretch[0:len(data)]
	
	data = data.split(" ")
	
	for b in key_stretch:
		i = ord(b)
		key_digits += str(i)+" "
	key_digits = key_digits.split(" ")
	keynum = 0
	for d in data:
		if d:
			if int(d) == int(key_digits[keynum]):
				#if int(num_array[keynum]) % 2 == 0:
				#	secret = secret + chr(int(d) - int(num_array[keynum]))
				#else:
				#	secret = secret + chr(int(d) + int(num_array[keynum]))
				secret += chr(int(d))
			else:
				combine = 0
				if int(num_array[keynum]) % 2 == 0:
					combine = int(d) + int(key_digits[keynum])
				else:
					combine =int(d) * int(num_array[keynum])
					
				secret = secret + chr(combine)
		keynum += 1

	return secret.replace(" ","zZz")

def simp_decrypt(key,raw_data):
	#print("using key "+key) 
	#print("on "+raw_data)
	num_array = []
	for c in key:
		if c in ["2","4","6","8",]:
			num_array.append(c)
				
	while len(num_array) < len(raw_data):
		num_array += num_array
	num_array += num_array
	
	#print(num_array)
		
	key_stretch = key
	message = ""
	datanum = 0
	decoded = ""
	key_digits = ""
	digits = ""
	
	for t in raw_data.replace("zZz"," "):
		c = ord(t)
		digits += str(c)+" "
		
	data = digits
	
	if key_stretch != "":
		if len(data)> len(key_stretch):
			while len(key_stretch) < len(data):
				key_stretch = key_stretch + key
	key_stretch = key_stretch[0:len(data)]
	
	
	data = data.split(" ")
	
	#print("data in digits ",data)
	
	for b in key_stretch:
		i = ord(b)
		key_digits += str(i)+" "
	
	key_digits = key_digits.split(" ")	
	
	#print("key in digits",key_digits)
	
	keynum = 0
	for d in data:
		if d != '' and key_digits[keynum] != '':
			if int(d) == int(key_digits[keynum]):
				message += chr(int(d))
			else:
				combine = 0
				if int(num_array[keynum]) % 2 == 0:
					combine = int(d) - int(key_digits[keynum])
				else:
					combine = int(d) / int(num_array[keynum])
				try:
					chr(int(combine))
				except:
					pass
				else:	
					message += chr(int(combine))
		keynum += 1
			
	return message.strip()
	
