import crypt
import socket
import time
import os

#sock = socket
#msg = message
#encrypt_key = reciever's public key
#sign_key = sender private key
def sendMessage(sock,msg,encrypt_key,sign_key):
	signature = crypt.signMessage(msg,sign_key)
	cipher_text = crypt.encryptRSA(msg,encrypt_key)
	sock.send(cipher_text)
	sock.send(signature)

#sock = socket
#msg_key = recievers private_key 
#sig_key = sender's public key
def recieveMessage(sock,msg_key,sig_key):
	cipher_text = sock.recv(4000)
	plain_text = crypt.decryptRSA(cipher_text,msg_key)
	signature = sock.recv(4000)
	verified = crypt.verifySignature(plain_text,signature,sig_key)
	if(verified):
		return (True,plain_text.decode())
	else:
		return (False,"Error matching signatures")

#Send data by chunks
def sendData(sock,data):
	tosend = data[:512]
	left = data[512:]
	while tosend:
		sock.send(tosend)
		tosend = left[:512]
		left = left[512:]
	time.sleep(0.3)
	sock.send(b"DONE")

#recieve data by chunks
def recieveData(sock):
	result = b''
	while True:
		data = sock.recv(512)
		if(data == b"DONE"):
			break
		result += data
	return result

#Server diffie/helman key exchange
def keyExchange(sock,base,mod):
	a = crypt.createPrime()
	biga = pow(base,a,mod)
	sock.send(str(biga).encode())
	bigb_str = sock.recv(1024).decode()
	bigb = int(bigb_str)
	key = pow(bigb,a,mod)
	return key.to_bytes(32,byteorder="big")
	