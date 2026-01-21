import tkinter as tk
from tkinter import messagebox  
from tkinter import simpledialog
import datetime
import json
import os 


accounts=[]
current_account = None 
class Bankaccount:
    def __init__(self,mname,maccount,mpassword,memail,mphonenumber):
        self.mname=mname
        self.maccount=maccount
        self.mpassword=mpassword
        self.balance=0
        self.mhistory=[]
        self.memail=memail
        self.mphonenumber=mphonenumber

    def info(self):
        return f"name :{self.mname}\n account:{self.maccount}"
    
    def deposit(self,depositamount):
        self.balance=self.balance+depositamount
        self.addlog("Deposit", "Cash Deposit", depositamount)
        return f"your deposit {depositamount}\nafter deposit balance : {self.balance}"
    
    def withdraw(self,withdrawamount):
        if withdrawamount > self.balance:
            return "Insufficient balance"
        self.balance=self.balance-withdrawamount
        self.addlog("Withdraw", "Cash Withdraw", withdrawamount)
        return f"withdraw amount:{withdrawamount}\n after withdrawal balance: {self.balance}"
    
    def checkbalance(self):
        return f"your balance amount is:{self.balance}"
    
    def debit(self,debitamount):
        self.balance=self.balance-debitamount
    
    def credit(self,creditamount):
        self.balance=self.balance+creditamount

    def addlog(self,op,dsc,act):
        id=len(self.mhistory)+1
        d = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.mhistory.append([id,op,dsc,act,d])



def accounttodict(dictac):
    return {
        "name": dictac.mname,
        "account": dictac.maccount,
        "password": dictac.mpassword,
        "balance": dictac.balance,
        "history": dictac.mhistory,
        "email": dictac.memail,
        "phone": dictac.mphonenumber
    }

def dicttoaccount(data):
    x = Bankaccount(
        data["name"],
        data["account"],
        data["password"],
        data["email"],
        data["phone"]
    )
    x.balance = data["balance"]
    x.mhistory = data["history"]
    return x


def load():
    if os.path.exists("Bankaccount.json"):
        with open("Bankaccount.json", "r") as file:
            try:
                data = json.load(file)
                for i in data:
                    accounts.append(dicttoaccount(i))
            except json.JSONDecodeError:
                messagebox.showerror("Error", "Data file corrupted")

def save_data():
    data = []
    for i in accounts:
        data.append(accounttodict(i))

    file = open("Bankaccount.json", "w")
    json.dump(data, file, indent=4)
    file.close()
 


load()



root=tk.Tk()
root.title("BANK ACCOUNT MANAGMENT SYSTEM")
root.geometry("300x400")




def switch_frame(frame):
    frame.tkraise()




frames = {}
for name in ("main", "create", "login", "account"):
    frames[name] = tk.Frame(root,bg="#6f72b9")
    frames[name].place(relwidth=1, relheight=1)

main_menu = frames["main"]
create_frame = frames["create"]
login_frame = frames["login"]
account_menu = frames["account"]




def on_close():
    save_data()
    root.destroy()

main_label=tk.Label(main_menu,text="BANK SYSTEM",width=20)
main_label.pack(pady=20)
main_button=tk.Button(main_menu,text="Create Account",width=20, command=lambda: switch_frame(create_frame ))
main_button.pack(pady=10)

main_button=tk.Button(main_menu,text="Login",width=20, command=lambda: switch_frame(login_frame ))
main_button.pack(pady=10)
main_button=tk.Button(main_menu,text="Exit",width=20, command=on_close)
main_button.pack(pady=10) 



# ,,,,createa account bar................

def create_account():
    name= name_textbox.get()
    accountnumber=accountnumber_textbox.get()
    password=password_textbox.get()
    email=email_textbox.get()
    phonenumber=phonenumber_textbox.get()


    if not name or not accountnumber or not password:
        messagebox.showwarning(
            "Missing Data",
            "Please fill all fields."
        )
        return 

    
    if not accountnumber.isdigit():
        return messagebox.showinfo("ERROR","Account number must me numeric!")
    
    if len(password)<4 :
        return messagebox.showinfo("ERROR","password must be graeter than four!")
   
    if any(acc.maccount == accountnumber for acc in accounts):
        messagebox.showerror("Error", "Account number already exists!")
        return
    
    

    if name and accountnumber and password:
        messagebox.showinfo(
            "Account Created",
            f"Name:{name}\nAccount Number: {accountnumber}"

            
        )
        messagebox.showinfo(
            "Success",
            f"{name}, Your Account has been created successfully!..",
            
            
            
        )
        new_account = Bankaccount(name, accountnumber, password, email, phonenumber)
        accounts.append(new_account)

   
        import smtplib
        from email.mime.text import MIMEText

        subject = "Account Created"
        body =f"""Your Account has been created successfully....",
        "These are the details of your account. Please keep your password private to prevent misuse.,
        Name:{ new_account.mname},
        Account Number: { new_account.maccount},
        Balance:{new_account.balance}"""
        sender = "asahila590@gmail.com"
        recipients = [new_account.memail]
        password = "dpgcpevlracnkkwy"


        def send_email(subject, body, sender, recipients, password):
            msg = MIMEText(body)
            msg['Subject'] = subject
            msg['From'] = sender
            msg['To'] = ', '.join(recipients)
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
                smtp_server.login(sender, password)
                smtp_server.sendmail(sender, recipients, msg.as_string())
            print("Message sent!")


        send_email(subject, body, sender, recipients, password)
        from twilio.rest import Client
        account_sid = 'ACb989b8ba477dd200b066337952ccb771'
        auth_token = 'd5ecfb5f1d8714949707dd45f58e2ba8'
        client = Client(account_sid, auth_token)
        message = client.messages.create(
        messaging_service_sid='MG34371a979ba31016c37dc47140543b41',
        body=f"""Your Account has been created successfully....",
        "These are the details of your account. Please keep your password private to prevent misuse.,
        Name:{ new_account.mname},
        Account Number: { new_account.maccount},
        Balance:{new_account.balance}""",
        to=new_account.mphonenumber
        )
        print(message.sid)
        print("Account successfully created!..")
   
        # new_account = Bankaccount(name, accountnumber, password,email,phonenumber)
        # accounts.append(new_account)
        for e in (name_textbox,accountnumber_textbox,password_textbox):
            e.delete(0, tk.END)
        save_data()
        switch_frame(main_menu)
        
        
   
# ....create account........

createaccount_label=tk.Label(create_frame,text="CREATE ACCOUNT",width=20)
createaccount_label.pack(pady=10)
name_label=tk.Label(create_frame,text="Name")
name_label.pack(pady=5)
name_textbox=tk.Entry(create_frame)
name_textbox.pack()

accountnumber_label=tk.Label(create_frame,text="Account Number")
accountnumber_label.pack(pady=5)
accountnumber_textbox=tk.Entry(create_frame)
accountnumber_textbox.pack()

password_label=tk.Label(create_frame,text="Password")
password_label.pack(pady=5)
password_textbox=tk.Entry(create_frame,show="*")
password_textbox.pack()


email_label=tk.Label(create_frame,text="Email")
email_label.pack(pady=5)
email_textbox=tk.Entry(create_frame)
email_textbox.pack()


phonenumber_label=tk.Label(create_frame,text="Phone Number")
phonenumber_label.pack(pady=5)
phonenumber_textbox=tk.Entry(create_frame)
phonenumber_textbox.pack()

create_button=tk.Button(create_frame,text="CREATE",width=10,command= create_account)
create_button.pack(pady=10)

back_button=tk.Button(create_frame,text="BACK",width=10,command=lambda: switch_frame(main_menu))
back_button.pack()





# ...login bar.....



def login_account():
    global current_account
    laccountnumber=laccountnumber_textbox.get()
    lpassword=lpassword_textbox.get()
    if not laccountnumber or not lpassword:
       return messagebox.showerror("Error", "Please fill all fields")
    

    if not laccountnumber.isdigit():
            return messagebox.showinfo("ERROR","Account number must be numeric!")
    
    if len(lpassword)<4 :
            return messagebox.showinfo("ERROR","password must be graeter than four characters!")
       



    for loginaccount in accounts:
        if loginaccount.maccount == laccountnumber and loginaccount.mpassword == lpassword:
            current_account = loginaccount 
            messagebox.showinfo("Logged in", f"Welcome {loginaccount.mname}")
            switch_frame(account_menu)
            return

    messagebox.showerror("Login Failed", "Invalid account number or password")

            

        
   

# # .....login.....


loginaccount_label=tk.Label(login_frame ,text="LOGIN ACCOUNT",width=20)
loginaccount_label.pack(pady=10)

laccountnumber_label=tk.Label(login_frame,text="Account Number")
laccountnumber_label.pack(pady=5)

laccountnumber_textbox=tk.Entry(login_frame)
laccountnumber_textbox.pack()


lpassword_label=tk.Label(login_frame,text="password")
lpassword_label.pack(pady=5)
lpassword_textbox=tk.Entry(login_frame,show="*")
lpassword_textbox.pack()


login_button=tk.Button(login_frame,text="LOGIN",width=10,command= login_account)
login_button.pack(pady=10)

lback_button=tk.Button(login_frame,text="BACK",width=10,command=lambda: switch_frame(main_menu))
lback_button.pack()

# ....account menu........

accountmenu_label=tk.Label(account_menu,text="ACCOUNT MENU",width=20)
accountmenu_label.pack(pady=10)
def show_account_info():
    if current_account:
        messagebox.showinfo("Account Info", current_account.info())
    else:
        messagebox.showerror("Error", "No account is currently logged in!")

accountinfo_button = tk.Button(account_menu, text="Account Info", width=15, command=show_account_info)
accountinfo_button.pack(pady=10)

# ....deposit......

def deposit():
    if not current_account:
        messagebox.showerror("Error", "No account is logged in!")
        return
    amount = simpledialog.askinteger("Deposit", "Enter amount:", minvalue=1)
    if amount:
        messagebox.showinfo("Deposit", current_account.deposit(amount))
    save_data()

deposit_button = tk.Button(account_menu,text="Deposit",width=15,command=deposit)
deposit_button.pack(pady=10)



# ..withdrew...

def withdraw():
    if not current_account:
        messagebox.showerror("Error", "No account is logged in!")
        return
    amount=simpledialog.askinteger("Withraw","Enter amount:",minvalue=1)
    if amount:
        messagebox.showinfo("withdraw",current_account.withdraw(amount))
    save_data()

withdraw_button = tk.Button(account_menu,text="Withdraw",width=15,command=withdraw)
withdraw_button.pack(pady=10)


# ....transfer.............
def transfer():
    if not current_account:
        messagebox.showerror("Error", "No account is logged in!")
        return
    transferaccount=simpledialog.askinteger("Transfer","Recipient Account Number:")
    transferamount=simpledialog.askinteger("Transfer","Amount:",minvalue=1)

    if not transferaccount or not transferamount:
        return
    
    if not current_account:
        messagebox.showerror("Error", "No account is logged in!")
        return
    
    if current_account.balance <transferamount:
        return messagebox.showinfo("Error", "Insufficient balance!")
    
    for acc in accounts:
        if acc.maccount==str(transferaccount):
            current_account.debit(transferamount)
            acc.credit(transferamount) 
            messagebox.showinfo("Success","Transaction successfully completed!..")
            messagebox.showinfo("Transfer Details",f"{transferamount} debited from Account{current_account.maccount}\nBalance of the current account is:{current_account.balance}\n{transferamount} credited to Account{acc.maccount}\nBalance of the Recipient is: {acc.balance}")
            current_account.addlog("Transfer", f"To {acc.maccount}", transferamount)
            acc.addlog("Transfer", f"From {current_account.maccount}", transferamount)
            save_data()        
            return 
    
    messagebox.showerror("Error", "Recipient account not found!")
    

transfer_button = tk.Button(account_menu,text="Transfer",width=15,command=transfer)
transfer_button.pack(pady=10)


# ...transaction history.........

def history():
    if not current_account:
        messagebox.showerror("Error", "No account is logged in!")
        return

    if not current_account.mhistory:
        messagebox.showinfo("History", "No transactions yet")
    else:
        text = ""
        for h in current_account.mhistory:
            text =text+ f"{h[0]} | {h[1]} | {h[2]} | {h[3]} | {h[4]}\n"
        messagebox.showinfo("History", text)
    save_data()

history_button = tk.Button(account_menu,text="History",width=15,command=history)
history_button.pack(pady=10)

# ....check balance....

def checkbalance():
    messagebox.showinfo("Balance",f"balance is:{current_account.balance}")


balance_button = tk.Button(account_menu,text="Check balance",width=15,command=checkbalance)
balance_button.pack(pady=10)                   



# ..logout....
def logout():
    global current_account
    current_account = None
    save_data()
    switch_frame(main_menu)

logout_button = tk.Button(account_menu, text="Logout", width=15, command=logout)
logout_button.pack(pady=10)








root.protocol("WM_DELETE_WINDOW", on_close)


switch_frame(main_menu)
root.mainloop()