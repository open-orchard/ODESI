#!/usr/bin/python
import cgi
import cgitb
import sys
import urllib
sys.path.append("..")
import openseed_account as Account
import openseed_setup as Settings
import openseed_utils as Utils
#import steem_get as Get
#import steem_submit as Submit
#import leaderboard as LeaderBoard
import openseed_seedgenerator as Seeds
import openseed_music as Music
import openseed_connections as Connections
import openseed_chat as Chat
import onetime as OneTime
import io

import json

form = cgi.FieldStorage()

dev_pub = form.getvalue("pub")
read_json = form.getvalue("msg")

get_image = form.getvalue("image")

if get_image != None:
	
	print("Content-type:text/html\r\n\r\n")
	
	get_size = form.getvalue("size")
	get_source_type = form.getvalue("source")
	if get_size != None and get_source_type != None:
		image = Utils.get_image(get_image,get_source_type,get_size)
		print("<html>")
		print("<body>")
		print("<img src=http://openseed.solutions:8080/ipfs/"+image+">")
		print("</body>")
		print("</html>")
		

else:
	print("Content-type:text/html\r\n\r\n")

if dev_pub == None:
	from_client = json.loads(read_json)
else:
	devID = Account.get_priv_from_pub(dev_pub)
	decrypted_message = Seeds.simp_decrypt(devID,read_json)
	from_client = json.loads(decrypted_message)
	
	
action = from_client["act"]

if Account.check_appID(from_client["appPub"],from_client["devPub"]):
	app = from_client["appPub"]
	dev = from_client["devPub"]
	
	
# Account Actions
 
	if action == "accountcheck":
		print(Account.accountCheck(from_client["username"],from_client["passphrase"]))
	if action == "steemcheck":
		print(Account.steem_Check(from_client["steemname"]))
	if action == "create":
		print(Account.create_user(from_client["username"],from_client["passphrase"],from_client["email"]))
	if action == "create_profile":
		print(Account.create_profile(from_client["theid"],from_client["data1"],
			from_client["data2"],from_client["data3"],from_client["data4"],
			from_client["data5"],from_client["type"])
		)
	if action == "link":
		print(Account.steem_link(from_client["username"]))
	if action == "verify":
		print(Account.steem_verify(from_client["username"],from_client["onetime"]))
	if action == "account":
		print(Account.get_account(from_client["theid"]))
	if action == "search":
		print(Account.openseed_search(from_client["username"]))
	if action == "gps":
		print(Account.gps_search(from_client["username"],from_client["cords"]))

# Chat Actions
 
	if action == "requests":
		print(Connections.get_requests(from_client["username"],from_client["data"]))
	if action == "request_status":
		print(Connections.request_status(from_client["username"],from_client["data"]))
	if action == "get_status":
		print(Account.get_status(from_client["username"]))
	if action == "update_status":
		print(Account.set_status(from_client["username"],from_client["appPub"],from_client["data"]))
	if action == "get_chat":
		print(Chat.get_chat(from_client["uid"],from_client["account"],from_client["room"],from_client["last"]))
	if action == "get_chat_history":
		print(Chat.get_chat_history(from_client["uid"],from_client["account"],from_client["room"],from_client["count"],from_client["last"]))
	if action == "conversations":
		print(Chat.chats(from_client["username"]))
	if action == "send_chat":
		print(Chat.send_chat(from_client["uid"],from_client["username"],from_client["othername"],from_client["data"]))
	if action == "check_chat":
		print(Chat.check_chat(from_client["username"],from_client["othername"]))
	if action == "chat":
 		print(Chat.get_chat(from_client["uid"],from_client["username"],from_client["chatroom"],from_client["data"]))

# Key Actions

	if action == "newkey":
		print(OneTime.store_onetime(from_client["type"],from_client["register"],from_client["validusers"]))
	if action == "getkey":
		print(OneTime.update_key(from_client["type"],from_client["register"],from_client["validusers"]))

# Connection Actions

	if action == "steem_connections":
		print(Connections.get_steem_connections(from_client["steem"]))
	if action == "openseed_connections":
		print(Connections.get_openseed_connections(from_client["username"]))
	if action == "profile_small":
		print(Connections.get_account(from_client["steem"]))
	if action == "profile":
		print(Connections.profile(from_client["userid"]))
	if action == "user_profile":
		print(urllib.parse.quote(Connections.user_profile(from_client["username"])))
	if action == "send_request":
		print(Connections.send_request(from_client["username"],from_client["request"],from_client["response"]))

else:
	print("App rejected")
