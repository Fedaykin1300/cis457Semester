import json
import datetime
import random
import crypt
import os

actions = ["Deposit","Withdrawal"]
types = ["Checking","Savings","Credit Card","Mortgage","IRA","Money Market"]

accounts = []

username = input("Username: ")
password = input("Password: ")

key_username = crypt.md5(password.encode()).encode()
key_password = crypt.md5(username.encode()).encode()

key = bytes([a^b for (a,b) in zip(key_username,key_password)])
iv = (123456).to_bytes(16,byteorder='big')

num_accounts_str = input("Number of Accounts: ")
n = int(num_accounts_str)

for i in range(n):

	#account number
	ac = random.randint(100000,1000000)

	#account type
	at = types[i%len(types)]

	#ammount
	ammount = random.randint(100,10000)

	#create activities
	activity = []
	for year in range(2000,2020):
		date = str(datetime.datetime(year,random.randint(1,12),random.randint(1,28))).split()[0]
		amnt = random.randint(100,100000)
		type_ = random.choice(actions)
		line = "{:15}{:15}{:>12}".format(date,type_,amnt).rstrip()
		activity.append(line)

	accounts.append({"account number":ac,"account type":at,"ammount":ammount,"activity":activity})


json_str = json.dumps(accounts,indent=4)
json_data = json_str.encode()
cipher_text = crypt.encryptAES(json_data,key,iv)
dir_name = crypt.md5(username[::-1].encode())[5:25]

if(not os.path.exists(f"./Server/{dir_name}")):
	os.makedirs(f"./Server/{dir_name}")

path = f"./Server/{dir_name}/accounts.json"
fp = open(path,"wb+")
fp.write(cipher_text)
fp.close()

#write password to hash and put on file
pass_hash = crypt.hash(password.encode())
pass_path = f"./Server/{dir_name}/pass.hash"
fp = open(pass_path,"w+")
fp.write(pass_hash)
fp.close()