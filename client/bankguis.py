import tkinter as tk

#Connects to server
class ConnectGUI:

	client = None

	def __init__(self,client):
		self.client = client

		self.root = tk.Tk()
		self.root.title("Connect to Bank")

		self.server_label = tk.Label(self.root,text="Server:")
		self.server_label.grid(row=0,column=0,padx=5,pady=5)

		self.server_entry = tk.Entry(self.root)
		self.server_entry.grid(row=0,column=1)

		self.port_label = tk.Label(self.root,text="Port:")
		self.port_label.grid(row=0,column=2)

		self.port_entry = tk.Entry(self.root)
		self.port_entry.grid(row=0,column=3)

		self.connect_button = tk.Button(self.root,text="Connect",command=self.connect)
		self.connect_button.grid(row=0,column=4,padx=5,pady=5)

		self.log_label = tk.Label(self.root,text="Connect to Bank Server",bg="cyan",width=57)
		self.log_label.grid(row=1,column=0,columnspan=5,sticky="W")

		self.root.mainloop()

	def connect(self):
		ip = self.server_entry.get()
		port_str = self.port_entry.get()
		port = int(port_str)
		result, meta = self.client.connect(ip,port)

		if(not result):
			self.log_label.config(text="Error")
		else:
			self.root.destroy()

class LoginGUI:

	client = None

	def __init__(self,client):
		self.client = client

		self.root = tk.Tk()
		self.root.title("Login")

		self.username_label = tk.Label(self.root,text="Username:")
		self.username_label.grid(row=0,column=0,padx=10,pady=5,sticky="E")

		self.username_entry = tk.Entry(self.root)
		self.username_entry.grid(row=0,column=1,padx=10,pady=5,sticky="W")

		self.password_label = tk.Label(self.root,text="Password:")
		self.password_label.grid(row=1,column=0,pady=5,padx=10,sticky="E")

		self.password_entry = tk.Entry(self.root,show="*")
		self.password_entry.grid(row=1,column=1,padx=10,pady=5,sticky="W")

		self.login_button = tk.Button(self.root,text="Login",command=self.login)
		self.login_button.grid(row=2,column=0,columnspan=2,pady=10)

		self.log_label = tk.Label(self.root,text="Login Credentials",bg="cyan",width=40)
		self.log_label.grid(row=3,column=0,columnspan=2,pady=5)

		self.root.mainloop()

	def login(self):
		un = self.username_entry.get()
		pwd = self.password_entry.get()
		result, msg = self.client.login(un,pwd)
		if(result):
			self.root.destroy()
		else:
			self.log_label.config(text=msg,bg="coral1")


class MainGUI:

	client = None

	def __init__(self,client):
		self.client = client
		self.updateClientInfo()

		self.root = tk.Tk()
		self.root.title("Banking")

		username = self.client.getUsername()
		self.banner_label = tk.Label(self.root,text=f"{username} - Secure Banking",font=("courier new",24,"bold"))
		self.banner_label.grid(row=0,column=0,columnspan=5,pady=15)

		self.accounts_listbox = tk.Listbox(self.root,width=50,font=("courier new",12))
		self.accounts_listbox.grid(row=1,column=0,columnspan=5,rowspan=4,padx=20,pady=15)
		self.updateListBox()

		self.deposit_button = tk.Button(self.root,text="Deposit",command=self.deposit)
		self.deposit_button.grid(row=5,column=0,pady=20)

		self.withdrawal_button = tk.Button(self.root,text="Withdrawal",command=self.withdrawal)
		self.withdrawal_button.grid(row=5,column=1,pady=20)

		self.transfer_button = tk.Button(self.root,text="Transfer",command=self.transfer)
		self.transfer_button.grid(row=5,column=2,pady=20)

		self.keys_button = tk.Button(self.root,text="Keys",command=self.show_keys)
		self.keys_button.grid(row=5,column=3,pady=20)

		self.details_button = tk.Button(self.root,text="Account Details",command=self.account_details)
		self.details_button.grid(row=5,column=4,pady=20)

		self.log_label = tk.Label(self.root,text="Log",width=110,bg="cyan")
		self.log_label.grid(row=6,column=0,columnspan=5)

		self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

		self.root.mainloop()

	def account_details(self):
		selected = self.accounts_listbox.curselection()
		if(selected == ()):
			self.setLog("No Selection","firebrick1")
			return
		ac_id = int(self.accounts_listbox.get(selected).split()[0])
		AccountDetailsGUI(self.client.getAccount(ac_id))

	def updateClientInfo(self):
		self.client.updateAccountInfo()

	def updateListBox(self):
		self.accounts_listbox.delete(0,tk.END)
		lines = self.client.getAccountLines()
		for line in lines:
			self.accounts_listbox.insert(tk.END,line)

	def on_closing(self):
		self.client.close()
		self.root.destroy()

	def deposit(self):
		depo_gui = TransactWindow(self.client,self,"Deposit")

	def withdrawal(self):
		with_window = TransactWindow(self.client,self,"Withdrawal")

	def transfer(self):
		trans_window = TransferWindow(self.client,self)

	def setLog(self,msg,color):
		self.log_label.config(text=msg,bg=color)

	def show_keys(self):
		keys_ = self.client.getKeys()
		ShowKeysGUI(keys_)


class TransactWindow:

	client = None
	parent = None
	type_ = ""
	accounts = []

	def __init__(self,client,parent,type_):

		self.client = client
		self.parent = parent
		self.type_ = type_

		self.root = tk.Tk()
		self.root.title(type_)

		self.accounts = self.client.getAccountLines()
		self.account_selected = tk.StringVar(self.root)
		self.account_selected.set(self.accounts[0])
		self.account_menu = tk.OptionMenu(self.root,self.account_selected,*self.accounts)
		self.account_menu.grid(row=0,column=0,columnspan=2,pady=10)

		self.amount_label = tk.Label(self.root,text="Amount:")
		self.amount_label.grid(row=1,column=0,padx=15,pady=5,sticky="E")

		self.amount_entry = tk.Entry(self.root)
		self.amount_entry.grid(row=1,column=1,padx=20,sticky="W")

		self.deposit_button = tk.Button(self.root,text=type_,command=self.transact)
		self.deposit_button.grid(row=2,column=0,columnspan=2,pady=10)

		self.root.mainloop()

	def transact(self):
		amnt_str = self.amount_entry.get()
		amnt = 0
		try:
			amnt = int(100 * float(amnt_str))
		except ValueError:
			self.parent.setLog("Error Parsing Input","firebrick1")
			return

		account = self.account_selected.get().split()[0]

		if(self.type_ == "Deposit"):
			result = self.client.deposit(account,amnt)
			if(result == "Success"):
				self.parent.setLog(result,"green2")
			else:
				self.parent.setLog(result,"firebrick1")
			self.parent.updateClientInfo()
			self.parent.updateListBox()

		if(self.type_ == "Withdrawal"):
			result = self.client.withdrawal(account,amnt)
			if(result == "Success"):
				self.parent.setLog(result,"green2")
			else:
				self.parent.setLog(result,"firebrick1")
			self.parent.updateClientInfo()
			self.parent.updateListBox()

		self.root.destroy()

class TransferWindow:

	client = None
	parent = None
	accounts = []
	
	def __init__(self,client,parent):
		self.client = client
		self.parent = parent

		self.accounts = self.client.getAccountLines()

		self.root = tk.Tk()
		self.root.title("Transfer")

		self.from_label = tk.Label(self.root,text="From:")
		self.from_label.grid(row=0,column=0)

		self.from_selection = tk.StringVar(self.root)
		self.from_selection.set(self.accounts[0])
		self.from_menu = tk.OptionMenu(self.root,self.from_selection,*self.accounts)
		self.from_menu.grid(row=0,column=1)

		self.to_label = tk.Label(self.root,text="To:")
		self.to_label.grid(row=1,column=0)

		self.to_selection = tk.StringVar(self.root)
		self.to_selection.set(self.accounts[0])
		self.to_menu = tk.OptionMenu(self.root,self.to_selection,*self.accounts)
		self.to_menu.grid(row=1,column=1)

		self.amount_label = tk.Label(self.root,text="Amount:")
		self.amount_label.grid(row=2,column=0)

		self.amount_entry = tk.Entry(self.root)
		self.amount_entry.grid(row=2,column=1)

		self.transfer_button = tk.Button(self.root,text="Transfer",command=self.transfer)
		self.transfer_button.grid(row=3,column=0,columnspan=2)

		self.root.mainloop()

	def transfer(self):
		account1 = self.from_selection.get().split()[0]
		account2 = self.to_selection.get().split()[0]
		amnt = int(float(self.amount_entry.get())*100)
		result = self.client.transfer(account1,account2,amnt)
		if(result == "Success"):
			self.parent.setLog(result,"green2")
		else:
			self.parent.setLog(result,"firebrick1")
		self.parent.updateClientInfo()
		self.parent.updateListBox()
		self.root.destroy()

class ShowKeysGUI:

	def __init__(self,keys_):

		root = tk.Tk()
		root.title("Keys")

		session_label = tk.Label(root,text="Session Key")
		session_label.grid(row=0,column=0,sticky="W",pady=10)

		session_text = tk.Text(root,width=100,height=1)
		session_text.grid(row=1,column=0,padx=10)
		session_text.insert(tk.END,keys_["Session Key"])

		private_label = tk.Label(root,text="Private Key")
		private_label.grid(row=2,column=0,sticky="W",pady=10)

		private_text = tk.Text(root,width=100,height=20)
		private_text.grid(row=3,column=0,padx=10)
		private_txt = keys_["Private Key"]
		private_txt = "".join(private_txt.splitlines()[1:-1])
		private_text.insert(tk.END,private_txt)

		public_label = tk.Label(root,text="Bank's Public Key")
		public_label.grid(row=4,column=0,pady=10,sticky="W")

		public_text = tk.Text(root,width=100,height=10)
		public_text.grid(row=5,column=0,padx=10)
		public_txt = keys_["Bank Key"]
		public_txt = "".join(public_txt.splitlines()[1:-1])
		public_text.insert(tk.END,public_txt)

		root.mainloop()

class AccountDetailsGUI:

	def __init__(self,account):

		ac_id = account["account number"]
		ac_type = account["account type"]
		ac_amount = account["ammount"]

		root = tk.Tk()
		root.title(f"Account {ac_id} Details")

		fmt = "{:17} {:>17}"

		ac_num_str = fmt.format("Account Number",ac_id)
		account_number_label = tk.Label(root,text=ac_num_str,font=("courier new",12,"bold"))
		account_number_label.grid(row=0,column=0,padx=10,pady=5)

		ac_type_str = fmt.format("Account Type",ac_type)
		account_type_label = tk.Label(root,text=ac_type_str,font=("courier new",12,"bold"))
		account_type_label.grid(row=1,column=0,padx=10,pady=5)

		ac_amount_str = fmt.format("Amount",ac_amount)
		account_amount_label = tk.Label(root,text=ac_amount_str,font=("courier new",12,"bold"))
		account_amount_label.grid(row=2,column=0,padx=10,pady=5)

		ac_activity = account["activity"]
		account_activity_listbox = tk.Listbox(root,width=50,height=10,font=("courier new",8))
		account_activity_listbox.grid(row=3,column=0,padx=20,pady=5)
		list_scrollbar = tk.Scrollbar(root,orient="vertical")
		list_scrollbar.grid(row=3,column=0,sticky="NES")
		list_scrollbar.config(command=account_activity_listbox.yview)
		account_activity_listbox.config(yscrollcommand=list_scrollbar.set)
		for activity in ac_activity:
			account_activity_listbox.insert(tk.END,activity)

		root.mainloop()