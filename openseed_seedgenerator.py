#!/usr/bin/python

import hashlib
import sys
sys.path.append("..")
import mysql.connector
import json
import random
import openseed_setup as Settings

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

def generate_id(name,account,contactname,contactemail):
	fullstring = name+passphrase+contactemail+account+contactname
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


def to_char(thecode):
	code = ""
	num = 0
	while num < len(thecode):
		code = code+chr(int(thecode[num:num+2]))
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

def simp_crypt(key,raw_data):
	key = key.replace("0","q")\
			.replace("1","a").replace("2","b")\
			.replace("3","c").replace("4","d")\
			.replace("5","F").replace("6","A")\
			.replace("7","Z").replace("8","Q")\
			.replace("9","T").replace("#","G")\
			.replace("!","B").replace(",","C")\
			.replace(" ","!").replace("/","S")\
			.replace("=","e").replace(":","c")\
			.replace("\n","n")
	secret = ""
	datanum = 0
	digits = ""
	#//lets turn it into integers first//
	for t in raw_data.replace("%", ":percent:").replace("&", ":ampersand:"):
		c = t.ord_at(0)
		digits += str(c)+" "
		
	data = digits+str(str(" ").ord_at(0))
	while datanum < len(data):
		keynum = 0
		while keynum < len(key):
			salt = int(round(randf() * 40))
			if keynum < len(data) and salt % 3 == 0 and datanum < len(data):
				if data[datanum] == key[keynum]:
					num = keynum
					while num < len(key) -1:
						secret = secret + key[num]
						num += 1
						if data[datanum] != key[num]:
							keynum = num
							secret = secret+data[datanum]
							break
						else:
							secret = secret + key[num]
				else:
					secret = secret+data[datanum]
				datanum += 1
			else:
				if keynum < len(key) and key[keynum]:
					secret = secret + key[keynum]
				else:
					keynum = 0
					secret = secret + key[keynum]
			keynum += 1
	return secret.replace(" ","zZz")

def simp_decrypt(key,raw_data):
	key = key.replace("0","q")\
			.replace("1","a").replace("2","b")\
			.replace("3","c").replace("4","d")\
			.replace("5","F").replace("6","A")\
			.replace("7","Z").replace("8","Q")\
			.replace("9","T").replace("#","G")\
			.replace("!","B").replace(",","C")\
			.replace(" ","!").replace("/","S")\
			.replace("=","e").replace(":","c")\
			.replace("\n","n")
			
	key_stretch = key
	message = ""
	datanum = 0
	decoded = ""

	data = raw_data.replace("zZz"," ")

	if key_stretch != "":
		if len(data) > len(key_stretch):
			while len(key_stretch) < len(data):
				key_stretch = key_stretch + key

		while datanum < len(data):
			if key_stretch[datanum] != data[datanum]:
				if data[datanum]:
					message = message + data[datanum]
				else:break
			datanum = datanum + 1
			
		for c in message.split(" "):
			if len(c) <= 4 and len(c) > 0:
				if int(c) < 255:
					decoded += chr(int(c))
				else:
					decoded = "Unable to Decrypt"

	return decoded.replace(":percent:","%").replace(":ampersand:","&")
	