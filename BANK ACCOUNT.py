import datetime
accounts=[]
class Bankaccount:
    def __init__(self,mname,maccountno,mpassword,memail,mphonenumber):
        self.mname=mname
        self.maccountno=maccountno
        self.balance=0
        self.mpassword=mpassword
        self.mhistory=[]
        self.memail=memail
        self.mphonenumber=mphonenumber


    def info(self):
        return f"Name : {self.mname}\nAccount number : {self.maccountno}"
    

    def deposit(self,amount):
        
        self.balance= self.balance+amount
        return f"your deposit amount is : {amount}\nYour current balance : {self.balance}"


    def withdrawal(self,withdrawalamount):
        
        self.balance=self.balance-withdrawalamount
        return f"your withdeawal amount is : {withdrawalamount}\nAfter withdrawal your balance is: {self.balance}"
    

    def checkbalance(self):
        return f"Now your balance amount is: {self.balance}"
    

    def debit(self,debitamount):
        self.balance=self.balance-debitamount


    def credit(self,creditamount):
        self.balance=self.balance+creditamount

    def addlog(self,op,dsc,act):
        id=len(self.mhistory)+1
        d=datetime.datetime.now()
        self.mhistory.append([id,op,dsc,act,d])  #op=opration(deit,credit....) #dsc=description(detailed information)# act=yeth account kk credit ayi debit ayi nokke# d=time and date of transaction
        
        


def menu1():
    options=int(input("""1.Createaccount
2.Login account
3.List all elements
4.Exit
select any option: """))
    

    if options==1:
        print("Create account")
        cname=input("Enter Name: ")
        caccountnumber=int(input("Account Number: "))
        cpassword=input("Enter Password:")
        cmail=input("Enter Mail Id: ")
        cphonenumber=input("Phone Number: ")
        newaccount=Bankaccount(cname,caccountnumber,cpassword,cmail,cphonenumber)
        import smtplib
        from email.mime.text import MIMEText

        subject = "Account Created"
        body =f"""Your Account has been created successfully....",
        "These are the details of your account. Please keep your password private to prevent misuse.,
        Name:{newaccount.mname},
        Account Number: {newaccount.maccountno},
        Balance:{newaccount.balance}"""
        sender = "asahila590@gmail.com"
        recipients = [newaccount.memail]
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
        Name:{cname},
        Account Number: {caccountnumber}
        Balance:{newaccount.balance}""",
        to=newaccount.mphonenumber
        )
        print(message.sid)
        print("Accont successfully created!..")
        accounts.append(newaccount)
        newaccount.addlog("Account created","your accound has been created","by self")
        print(newaccount.info())
        menu1()

    elif options==2:
        print("Login account")
        laccountnumber=int(input("enter your account number: "))
        lpassword=input("enter your password")

        for loginaccount in accounts:
            if loginaccount.maccountno==laccountnumber and loginaccount.mpassword==lpassword :
                print(f"{loginaccount.mname} welcome to your account!..your account number:{loginaccount.maccountno}")
                def menu2():
                    choice2=int(input("""
                1.Account detials
                2.Deposit
                3.Withdraw
                4.Transfer
                5.Check balance
                6.Transaction history
                7.Log out
                select any option: """))
                    if choice2==1:
                        print("Account details")
                        print(loginaccount.info())
                        menu2()
                    elif choice2==2:
                        print("Deposit")
                        damount=int(input("how much you want to deposit"))
                        print(loginaccount.deposit(damount))
                        loginaccount.addlog("deposited,",f"you deposit {damount} ","by self")
                        menu2()
                    elif choice2==3:
                        print("Withdraw")
                        wamount=int(input("how much you want to withdrawal"))
                        print(loginaccount.withdrawal(wamount))
                        loginaccount.addlog("withdrawal",f"you withraw {wamount} from  your account ","by self")
                        menu2()
                    elif choice2==4:
                        print("Transfer")
                        transferaccountnum=int(input("enter account number"))
                        for transferaccount in accounts:
                            if transferaccount.maccountno==transferaccountnum:
                                    print(f"transfer amount from {transferaccount.mname} his ac number: {transferaccount.maccountno}..")
                                    tamount=int(input("how much you want transfer to other account"))
                                    loginaccount.debit(tamount)
                                    transferaccount.credit(tamount)
                                    print(f" ( {loginaccount.maccountno}) {loginaccount.mname}  debited ;{tamount}")
                                    print(f"({transferaccount.maccountno}) {transferaccount.mname} credited ;{tamount}")
                                    loginaccount.addlog("debit",f"{tamount} has been debited from your ac to ",f"{transferaccount.maccountno} {transferaccount.mname}")
                                    transferaccount.addlog("credit",f"{tamount}has been credited to your account from ",f"{loginaccount.mname} {loginaccount.maccountno}")



                        menu2()
                    elif choice2==5:
                        print("Check balance")
                        print(loginaccount.checkbalance())
                        menu2()
                    elif choice2==6:
                        print("Transaction history")
                        for tr in loginaccount.mhistory:
                            print(tr[0],tr[1],tr[2],tr[3],tr[4])

                        menu2()
                    elif choice2==7:
                        print("Log out")
                    else:
                        print("Incorrect option...please receck your option!...")
                        menu2()
                menu2()  
                            

        menu1()


    elif options==3:
        print("List all account")
        for i in accounts:
            print(i.info())
        print("your all list are printed!....")
        menu1()


    elif options==4:
        print("Exit")
        
    else:
        print("Incorrect option...please receck your option!...")
        menu1()
menu1()


# dpgc pevl racn kkwy
# A5T4L6QNUW7RT5US2JJ7XHNY
# 25f1002109@ds.study.iitm.ac.in