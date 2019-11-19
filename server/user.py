from accounts import AccountCollection
import crypt
import os
import json

class User:

	#used to decrypt/encrypt account info,same for all users
	#the key however is different for each user
	iv = (123456).to_bytes(16,byteorder='big')

	def __init__(self):
		self.username = None
		self.password = None
		self.directory_name = None
		self.key = None
		self.account_collection = None

	#Verify Username and Passwrod
	def login(self,username,password):

		self.username = username
		self.password = password
		self.directory_name = dir_name = crypt.md5(username[::-1].encode())[5:25]

		#Check if username exists
		isdir = os.path.isdir(self.directory_name)
		if(not isdir):
			return (False,"No Such Username on File")

		pass_hash = crypt.hash(password.encode())

		pass_path = f"./{self.directory_name}/pass.hash"
		with open(pass_path,"r") as fp:
			pass_on_file = fp.read()

		#See if inputted passwords matches the one on file
		if(pass_hash != pass_on_file):
			return (False,"Password doesn't match")

		#Generate Key to read account information from json
		key_username = crypt.md5(password.encode()).encode()
		key_password = crypt.md5(username.encode()).encode()
		self.key = bytes([a^b for (a,b) in zip(key_username,key_password)])

		return (True,"Verified!")

	#Decrypt account info from encrypted json
	def loadAccounts(self):
		account_path = f"./{self.directory_name}/accounts.json"
		with open(account_path,"rb") as fp:
			cipher_data = fp.read()
		plain_data = crypt.decryptAES(cipher_data,self.key,self.iv)
		plain_text = plain_data.decode("ascii")
		self.account_collection = AccountCollection(plain_text)
		return True

	#return account collection
	def getAccounts(self):
		return self.account_collection

	#encrypt and save accounts
	def saveAccounts(self):
		json_str = self.account_collection.getInfo()
		json_cipher = crypt.encryptAES(json_str.encode(),self.key,self.iv)
		save_path = f"./{self.directory_name}/accounts.json"
		with open(save_path,"wb") as fp:
			fp.write(json_cipher)

	#return username
	def getUsername(self):
		return self.username