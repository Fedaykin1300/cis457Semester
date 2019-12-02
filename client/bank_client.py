import netfuncs
import crypt
from bankguis import ConnectGUI, LoginGUI, MainGUI
import socket
import json
import os
import base64

class Client:

	base = 105553562181097584568135621478053647945975401896322062466680526006565819715313
	mod = 101698025584279479970615281866284275596840877055769356435585637498067885712049
	iv = (321).to_bytes(16,byteorder="big")

	bank_public_key = None
	private_key = None
	session_key = None

	is_connected = False
	is_logged_in = False

	bank_socket = socket.socket()

	username = ""

	accounts = None

	def __init__(self):
		pass

	def connect(self,ip,port):
		
		if(self.is_connected):
			(False,"Already connected")

		result = self.bank_socket.connect_ex((ip,port))
		
		if(result == 0):
			self.is_connected = True
			return (True,"Connected to Server")
			
		return (False,"Error connectinTransactWindowg to server")

	def createKeys(self):
		crypt.createKeyPair()
		fp = open("rsa.private","rb")
		self.private_key = crypt.loadPrivateKey(fp.read())
		fp.close()

	def exchangeKeys(self):
		
		self.createKeys()

		print(".................Exchanging Keys..........................")
		
		#session key
		self.session_key = netfuncs.keyExchange(self.bank_socket,self.base,self.mod)
		print(self.session_key.hex())

		#Send public key
		fp = open("rsa.public","rb")
		key_data = fp.read()
		fp.close()
		key_cipher = crypt.encryptAES(key_data,self.session_key,self.iv)
		netfuncs.sendData(self.bank_socket,key_cipher)
		print("###Public Key Sent###")

		#Recieve Bank Key
		bank_cipher = netfuncs.recieveData(self.bank_socket)
		bank_key_data = crypt.decryptAES(bank_cipher,self.session_key,self.iv)
		self.bank_public_key = crypt.loadPublicKey(bank_key_data)
		fp = open("shouldbebankpem","wb")
		fp.write(bank_key_data)
		fp.close()
		print("###Public Key Recieved###")

		print("............Keys should bey exchanged................")

	def login(self,username,password):
		msg = (f"{username} {password}").encode()
		netfuncs.sendMessage(self.bank_socket,msg,self.bank_public_key,self.private_key)
		answer = netfuncs.recieveMessage(self.bank_socket,self.private_key,self.bank_public_key)
		msg = answer[1]
		if(msg == "Verified!"):
			self.is_logged_in = True
			self.username = username
			return (True,msg)
		else:
			return (False,msg)

	def deposit(self,account,amount):
		msg = f"Deposit {account} {amount}"
		netfuncs.sendMessage(self.bank_socket,msg.encode(),self.bank_public_key,self.private_key)
		result, msg = netfuncs.recieveMessage(self.bank_socket,self.private_key,self.bank_public_key)
		return msg

	def withdrawal(self,account,amount):
		msg = f"Withdrawal {account} {amount}"
		netfuncs.sendMessage(self.bank_socket,msg.encode(),self.bank_public_key,self.private_key)
		result, msg = netfuncs.recieveMessage(self.bank_socket,self.private_key,self.bank_public_key)
		return msg

	def transfer(self,from_account,to_account,amount):
		s = f"{from_account} -> {to_account} : {amount}"
		msg = f"Transfer {from_account} {to_account} {amount}"
		netfuncs.sendMessage(self.bank_socket,msg.encode(),self.bank_public_key,self.private_key)
		result, msg = netfuncs.recieveMessage(self.bank_socket,self.private_key,self.bank_public_key)
		return msg

	def close(self):
		netfuncs.sendMessage(self.bank_socket,b"quit",self.bank_public_key,self.private_key)

	def updateAccountInfo(self):
		netfuncs.sendMessage(self.bank_socket,b"GetInfo",self.bank_public_key,self.private_key)
		msg_cipher = netfuncs.recieveData(self.bank_socket)
		msg_plain = crypt.decryptAES(msg_cipher,self.session_key,self.iv)
		self.accounts = json.loads(msg_plain)

	def getAccountLines(self):
		lines = []
		for account in self.accounts:
			fmt = "{:<13} {:<13} {:>10.2f}"
			line = fmt.format(account['account number'],account['account type'],account['ammount']/100)
			lines.append(line)
		return lines

	def getAccount(self,account_num):
		for account in self.accounts:
			if(account_num == account["account number"]):
				return account
		return None

	def getUsername(self):
		return self.username

	def getKeys(self):
		keys_ = {}
		keys_["Session Key"] = base64.b64encode(self.session_key).decode("ascii")
		keys_["Private Key"] = crypt.pemPrivateKey(self.private_key).decode("ascii")
		keys_["Bank Key"] = crypt.pemPublicKey(self.bank_public_key).decode("ascii")
		return keys_

if __name__ == "__main__":
	client = Client()
	
	connect_gui = ConnectGUI(client)
	if(not client.is_connected):
		os._exit()

	client.exchangeKeys()

	login_gui = LoginGUI(client)
	if(not client.is_logged_in):
		os._exit()

	main_gui = MainGUI(client)