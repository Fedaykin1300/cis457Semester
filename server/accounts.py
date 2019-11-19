import os
import json
import datetime
import crypt

class Account:

	type_ = ""		#checkings/savings/etc
	num = 0			#account id
	ammount = 0		#number (int) of cents in account
	activity = []	#list [date action ammount comment]

	#Constructor
	def __init__(self,type_,num,ammount,activity):
		self.type_ = type_
		self.num = num
		self.ammount = ammount
		self.activity = activity

	#puts info into a dictionary
	def getDict(self):
		dict = {}
		dict["account number"] = self.num
		dict["account type"] = self.type_
		dict["ammount"] = self.ammount
		dict["activity"] = self.activity
		return dict

	#Overrides form print,etc. commands
	def __str__(self):
		return f"{self.num} {self.type_} {self.ammount} Activity: {len(self.activity)}"

	#Withdrawal an amount from account
	#returns false if overdrawn
	def withdrawal(self,ammount):
		if(ammount > self.ammount):
			return False
		else:
			self.ammount -= ammount
			date = str(datetime.datetime.now()).split()[0]
			print(date)
			#self.activity.insert(0,f"{date} Withdrawal {ammount}")
			line = "{:15}{:15}{:>12}".format(date,"Withdrawal",ammount).rstrip()
			self.activity.insert(0,line)
			return True

	#Deposits ammount into account
	#Should always work
	def deposit(self,ammount):
		self.ammount += ammount
		date = str(datetime.datetime.now()).split()[0]
		#self.activity.insert(0,f"{date} Deposit {ammount}")
		line = "{:15}{:15}{:>12}".format(date,"Deposit",ammount).rstrip()
		self.activity.insert(0,line)
		return True

#Collection of accounts
class AccountCollection:

	#dictionary with account id as key and account as value
	accounts = {}

	#constructor
	def __init__(self,json_string):

		accounts_list = json.loads(json_string)

		for acnt in accounts_list:
			key_ = acnt["account number"]
			self.accounts[key_] = Account(acnt["account type"],acnt["account number"],acnt["ammount"],acnt["activity"])

	#Overrides srt for printing purposes
	def __str__(self):
		return "\n".join(list(str(self.accounts[k]) for k in self.accounts))

	#Withdrawal amnt from act_num
	#False if error, true if good
	def withdrawal(self,act_num,amnt):
		result = self.accounts[act_num].withdrawal(amnt)
		return result

	#Deposit amount in account number
	#Should always be true return
	def deposit(self,act_num,amnt):
		result = self.accounts[act_num].deposit(amnt)
		return result

	#Transfers amount from one account to another
	#returns False if not enouch money
	def transfer(self,with_act,dep_act,amnt):
		with_result = self.accounts[with_act].withdrawal(amnt)
		if(not with_result):
			return False
		dep_result = self.accounts[dep_act].deposit(amnt)
		return True

	#Retrieves accounts information for user to save
	def getInfo(self):
		acts = []
		for value in self.accounts.values():
			acts.append(value.getDict())
		return json.dumps(acts,indent=4)


if __name__ == "__main__":
	pass