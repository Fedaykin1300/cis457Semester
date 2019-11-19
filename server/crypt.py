from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import padding as aespadding
from cryptography.exceptions import InvalidSignature

### ^^^^^^^^^^^^ That's a lot of imports ^^^^^^^^^^^^^^^^^^^^

#create prime number for use in diffie/helman exchage
def createPrime():
	pk = rsa.generate_private_key(public_exponent=7,key_size=512,backend=default_backend())
	num = pk.private_numbers().p
	return num

#Creates a rsa key pair
#saves pem to rsa.private and rsa.public
def createKeyPair():

	#Private Key
	private_key = rsa.generate_private_key(public_exponent=65537,key_size=2048,backend=default_backend())
	pem1 = private_key.private_bytes(
		encoding=serialization.Encoding.PEM,
		format=serialization.PrivateFormat.PKCS8,
		encryption_algorithm=serialization.NoEncryption()
	)
	fp = open("rsa.private","wb")
	fp.write(pem1)
	fp.close()

	#Public key
	public_key = private_key.public_key()
	pem2 = public_key.public_bytes(
		encoding=serialization.Encoding.PEM,
		format=serialization.PublicFormat.SubjectPublicKeyInfo
	)
	fp = open("rsa.public","wb")
	fp.write(pem2)
	fp.close()

#loads pem for a public key
def loadPublicKey(data):
	public_key = serialization.load_pem_public_key(data,backend=default_backend())
	return public_key

#loads a pen for a private key
def loadPrivateKey(data):
	private_key = serialization.load_pem_private_key(data,password=None,backend=default_backend())
	return private_key

#encrypt message using rsa public key
def encryptRSA(msg,public_key):
	cipher_text = public_key.encrypt(
		msg,
		padding.OAEP(
			mgf=padding.MGF1(algorithm=hashes.SHA256()),
			algorithm=hashes.SHA256(),
			label=None
		)
	)
	return cipher_text

#decrypt messge using rsa private key
def decryptRSA(msg,private_key):
	plain_text = private_key.decrypt(
		msg,
		padding.OAEP(
			mgf=padding.MGF1(algorithm=hashes.SHA256()),
			algorithm=hashes.SHA256(),
			label=None
		)
	)
	return plain_text

#hash item using sha256 hash function
def hash(item):
	digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
	digest.update(item)
	return digest.finalize().hex()

def md5(item):
	digest = hashes.Hash(hashes.MD5(), backend=default_backend())
	digest.update(item)
	return digest.finalize().hex()

#create signature for a message with
#private rsa key
def signMessage(msg,private_key):
	signature = private_key.sign(
		msg,
		padding.PSS(
			mgf=padding.MGF1(hashes.SHA256()),
			salt_length=padding.PSS.MAX_LENGTH
			),
		hashes.SHA256()
	)
	return signature

#Verify message matches a signature with
#an rsa public key
def verifySignature(msg,signature,public_key):
	try:
		verified = public_key.verify(
			signature,
			msg,
			padding.PSS(
				mgf=padding.MGF1(hashes.SHA256()),
				salt_length=padding.PSS.MAX_LENGTH
				),
			hashes.SHA256()
		)
	except InvalidSignature:
		return False
	return True

#Encrypt data using aes and given key and iv
def encryptAES(data,key,iv):
	aesCipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend = default_backend())
	aesEncryptor = aesCipher.encryptor()
	padder = aespadding.PKCS7(128).padder()
	padded_msg = padder.update(data)
	cipher = aesEncryptor.update(padded_msg)
	cipher += aesEncryptor.update(padder.finalize())
	return cipher

#decrypt data using aes with key and iv given
def decryptAES(data,key,iv):
	aesCipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend = default_backend())
	aesDecryptor = aesCipher.decryptor()
	unpadder = aespadding.PKCS7(128).unpadder()
	plain_padder = aesDecryptor.update(data)
	plain_unpadded = unpadder.update(plain_padder)
	plain = plain_unpadded + unpadder.finalize()
	return plain

#serialize private key into pem format in base64
def pemPrivateKey(private_key):
	pem1 = private_key.private_bytes(
    	encoding=serialization.Encoding.PEM,
    	format=serialization.PrivateFormat.PKCS8,
    	encryption_algorithm=serialization.NoEncryption()
	)
	return pem1

#serialize public key into pem formate in base64
def pemPublicKey(public_key):
	pem2 = public_key.public_bytes(
		encoding=serialization.Encoding.PEM,
		format=serialization.PublicFormat.SubjectPublicKeyInfo
	)
	return pem2