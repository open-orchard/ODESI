#!/usr/bin/python

import sys
import mysql.connector
import hashlib
import json
import urllib.parse
sys.path.append("..")
from steem import Steem
import openseed_account as Account
import onetime as OneTime
import openseed_setup as Settings

settings = Settings.get_settings()

s = Steem()

def check_onetime(username,room):
	openseed = mysql.connector.connect(
		host = "localhost",
		user = settings["dbuser"],
		password = settings["dbpassword"],
		database = "openseed"
		)
	mysearch = openseed.cursor()
	check = "SELECT codenum FROM onetime WHERE room = %s"
	val1 = (room.split("[")[1].split("]")[0],)
	mysearch.execute(check,val1)
	result1 = len(mysearch.fetchall())

	if result1 == 1:
		return 1
	else:
		return 0

def create_chatroom(creator,title,room,userlist):
	openseed = mysql.connector.connect(
		host = "localhost",
		user = settings["dbuser"],
		password = settings["dbpassword"],
		database = "openseed"
		)
	chatcreator = openseed.cursor()
	newchat = "INSERT INTO chat (room,title,attendees,record,speaker) VALUES (%s,%s,%s,%s,'server')"
	vals = (room.split("[")[1].split("]")[0],title,userlist.split("[")[1].split("]")[0],'new')
	chatcreator.execute(newchat,vals)
	openseed.commit()
	chatcreator.close()	
	openseed.close()
	newkey = OneTime.store_onetime(1,creator,userlist.split("[")[1].split("]")[0],room.split("[")[1].split("]")[0])
	return '{"type":"server","key":"'+newkey+'"}'


	

def check_chat(username,room):
	openseed = mysql.connector.connect(
		host = "localhost",
		user = settings["dbuser"],
		password = settings["dbpassword"],
		database = "openseed"
		)
	mysearch = openseed.cursor()
	check = "SELECT Id FROM chat WHERE room = %s"
	val1 = (room.split("[")[1].split("]")[0],)
	val2 = (room.split("[")[1].split("]")[0],)
	mysearch.execute(check,val1)
	result1 = len(mysearch.fetchall())
	mysearch.execute(check,val2)
	result2 = len(mysearch.fetchall())
	mysearch.close()
	openseed.close()
	# Below are the 3 states that any chat can be in. 
	# 0 = No key No chat 
	# 1 = Key exists but not chat has started and registration is open
	# 2 = Key exists and Chat has started but registration is open
	# 3 = Chat exists and has started but registration is closed
	if result1 > 0:
		if check_onetime(username,room) == 1:
			return 2
		else:
			return 3
	elif result2 > 0:
		if check_onetime(username,room) == 1:
			return 2
		else:
			return 3
	else:
		if check_onetime(username,room) == 1:
			return 1
		else:
   			return 0
	

	


def chats(username):
	chatlist = ""
	convolist = []
	openseed = mysql.connector.connect(
		host = "localhost",
		user = settings["dbuser"],
		password = settings["dbpassword"],
		database = "openseed"
		)
	mysearch = openseed.cursor()
	chat = "SELECT attendees,record FROM chat WHERE attendees LIKE %s ORDER BY Id DESC"
	val1 = ("%"+username+"%",)
	mysearch.execute(chat,val1)
	result = mysearch.fetchall()
	for r in result:
		if convolist.count != 0:
			if str(r[0]) not in convolist:
				reverse = str(r[0]).split(",")[1]+","+str(r[0]).split(",")[0]
				if reverse not in convolist:
					convolist.append(str(r[0]))
					chatlist = '{"conversation":"'+str(r[0])+'","message":'+json.dumps(r[1].decode())+'}\n'+chatlist
		else:
			convolist.append(str(r[0]))
			chatlist = '{"conversation":"'+str(r[0])+'","message":'+json.dumps(r[1])+'}\n'+chatlist

	mysearch.close()
	openseed.close()
	return chatlist

def get_chat_history(userid,room,count,last):
	history = []
	response = '{"chat":"none"}'
	username = json.loads(Account.user_from_id(userid))["user"]
	if check_chat(username,room) != 0:
		while len(history) < int(count):
			from_chat = get_chat(userid,room,last)
			check = json.loads(from_chat)
			if "type" in check:
				if check["index"] != "-1":
					history.append(from_chat)
					#message = json.loads(history[len(history) -1])
					last = check["index"]
				else:
					break
		if len(history) > 0:
			response = '{"chat":'+json.dumps(history)+'}'
		else:
			response = '{"chat":[none]}'
	else:
		response = create_chatroom(username,"chat",room,room)

	return response

def get_chat(userid,chatroom,last):
	theRoom = find_chatroom(chatroom)[0]
	chat = '{"type":"server","room":"'+theRoom+'","message":"none","index":"-1"}'
	jsoned = chat
	room = ""
	index1 = 0
	status1 = ""
	username = json.loads(Account.user_from_id(userid))["user"]
	openseed = mysql.connector.connect(
		host = "localhost",
		user = settings["dbuser"],
		password = settings["dbpassword"],
		database = "openseed"
		)
	mysearch = openseed.cursor()
	search = "SELECT Id,record,attendees,date,speaker FROM chat WHERE room = %s AND Id > %s ORDER BY Id ASC"
	val1 = (theRoom,str(last))
	mysearch.execute(search,val1)
	result1 = mysearch.fetchall()
	if len(result1) != 0:
		status1 = result1[0][1]
		index1 = result1[0][0]
		jsoned = '{"type":"'+str(result1[0][4])+'","room":"'+theRoom+'","message":"'+status1.decode()+'","index":"'+str(index1)+'","date":"'+str(result1[0][3])+'"}'
	mysearch.close()
	openseed.close() 

	if status1 != None:
		chat = jsoned 
	else:
		chat = '{"type":"server","room":"'+theRoom+'","message":"none","index":"-1"}'
	return chat	

def find_chatroom(chatroom):
	cleanroom = chatroom.split("[")[1].split("]")[0]
	wharoom = cleanroom.split(",")[0].strip()+', '+cleanroom.split(",")[1].strip()
	reverseroom = cleanroom.split(",")[1].strip()+', '+cleanroom.split(",")[0].strip()
	room = ""
	title = ""
	attendees = ""
	openseed = mysql.connector.connect(
		host = "localhost",
		user = settings["dbuser"],
		password = settings["dbpassword"],
		database = "openseed"
		)
	mysearch = openseed.cursor()
	search = "SELECT Id,record,title,attendees,date,speaker FROM chat WHERE room = %s"
	val1 = (wharoom,)
	val2 = (reverseroom,)
	mysearch.execute(search,val1)
	result1 = mysearch.fetchall()
	mysearch.execute(search,val2)
	result2 = mysearch.fetchall()

	mysearch.close()
	openseed.close() 

	if len(result1) != 0:
		room = wharoom
		title = result1[0][2]
		attendees = result1[0][3]
	if len(result2) != 0:
		room = reverseroom
		title = result2[0][2]
		attendees = result2[0][3]
	return [room,title,attendees]	



def send_chat(userid,chatroom,data):
	
	roomInfo = find_chatroom(chatroom)
	theRoom = roomInfo[0]
	
	username = json.loads(Account.user_from_id(userid))["user"]
	response = '{"type":"server","message":"denied"}'
	if username:
		response = '{"type":"server","message":"No data"}'
		openseed = mysql.connector.connect(
			host = "localhost",
			user = settings["dbuser"],
			password = settings["dbpassword"],
			database = "openseed"
		)
		mysearch = openseed.cursor()
		if len(data) > 0:
			chat = "INSERT INTO chat (room,title,attendees,record,speaker) VALUES (%s,%s,%s,%s,%s)"
			val1 = (theRoom,roomInfo[1],roomInfo[2],data,username)
			mysearch.execute(chat,val1)
			openseed.commit()
			mysearch.close()
			openseed.close()
			response = '{"type":"server","message":"updated"}'
	else:
		response = '{"type":"server","message":"denied"}'

	return response