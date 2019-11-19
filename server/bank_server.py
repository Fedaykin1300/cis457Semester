import socket
import threading
import netfuncs
import os
import crypt
from accounts import AccountCollection
from user import User

PORT = 31377
private_key = None
base = 105553562181097584568135621478053647945975401896322062466680526006565819715313
mod = 101698025584279479970615281866284275596840877055769356435585637498067885712049
iv = (321).to_bytes(16,byteorder="big")

def new_client(sock,addr):

	session_key = None
	public_key = None
	accounts = None
	username = ""
	user = User()

	print(f"{addr}..............Exchanging Keys..........")
	#get clients session ket and rsa public key
	session_key = netfuncs.keyExchange(sock,base,mod)
	#print(session_key.hex())

	pub_cipher_data = netfuncs.recieveData(sock)
	pub_plain_data = crypt.decryptAES(pub_cipher_data,session_key,iv)
	public_key = crypt.loadPublicKey(pub_plain_data)
	print(f"{addr}## Public Key Recieved ##")

	#send servers public key
	with open("rsa.public","rb") as fp:
		key_data = fp.read()
	key_cipher = crypt.encryptAES(key_data,session_key,iv)
	netfuncs.sendData(sock,key_cipher)
	print(f"{addr}## Pulbic Key Sent ##")
	print(f"{addr}.............Keys Exchanged..............")

	#Get Login Info
	while True:
		login_info = netfuncs.recieveMessage(sock,private_key,public_key)
		print(f"Login: {login_info}")
		un, pwd = login_info[1].split()
		logged_in, info = user.login(un,pwd)
		print(info)
		netfuncs.sendMessage(sock,info.encode(),public_key,private_key)
		if(logged_in):
			break

	user.loadAccounts()
	accounts = user.getAccounts()
	usr_name = user.getUsername()

	#Main Loop - handles deposit/withdrawal/getinfo/transfer/etc
	while True:

		result, msg = netfuncs.recieveMessage(sock,private_key,public_key)
		print(f"Message From _{usr_name}_ : {msg}")

		words = msg.split()

		# "Deposit" <account> <amount>
		if(words[0] == "Deposit"):
			account_num = int(words[1])
			deposit_amount = int(words[2])
			result = accounts.deposit(account_num,deposit_amount)
			if(result):
				netfuncs.sendMessage(sock,b"Success",public_key,private_key)
			else:
				netfuncs.sendMessage(sock,b"Error",public_key,private_key)

		# "Withdrawal" <account> <amount>
		if(words[0] == "Withdrawal"):
			account_num = int(words[1])
			amount_withdrawal = int(words[2])
			result = accounts.withdrawal(account_num,amount_withdrawal)
			if(result):
				netfuncs.sendMessage(sock,b"Success",public_key,private_key)
			else:
				netfuncs.sendMessage(sock,b"Error",public_key,private_key)

		# "Transfer" <from_account> <to_account> <amount>
		if(words[0] == "Transfer"):
			withdrawal_account_number = int(words[1])
			deposit_account_number = int(words[2])
			transfer_amount = int(words[3])
			result = accounts.transfer(withdrawal_account_number,deposit_account_number,transfer_amount)
			if(result):
				netfuncs.sendMessage(sock,b"Success",public_key,private_key)
			else:
				netfuncs.sendMessage(sock,b"Error",public_key,private_key)


		# Returns all account info
		if(words[0] == "GetInfo"):
			json_data = accounts.getInfo().encode()
			data_cipher = crypt.encryptAES(json_data,session_key,iv)
			netfuncs.sendData(sock,data_cipher)

		# Client disconnected
		if(words[0] == "quit"):
			user.saveAccounts()
			break

	sock.close()
	print("Breaked and socket is closed")


def main():
	global private_key

	print("Loading private key")
	fp = open("rsa.private","rb")
	private_key = crypt.loadPrivateKey(fp.read())
	fp.close()

	listening_socket = socket.socket()
	listening_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR, 1)
	listening_socket.bind(('',PORT))
	listening_socket.listen(5)
	print(f"Listening on port {PORT}")

	while True:

		csock, addr = listening_socket.accept()
		print(f"Connection from {addr}")
		client_thread = threading.Thread(target=new_client,args=(csock,addr))
		client_thread.daemon = True
		client_thread.start()

	listening_socket.close()

if __name__ == "__main__":
	main()