import tkinter as tk
from tkinter import messagebox
# from tkinter import simpledialog
import smtplib
from email.mime.text import MIMEText
from twilio.rest import Client



root=tk.Tk()
root.title("STUDENT PORTAL")
root.geometry("400x400")

accounts=[]
current_account=None
class Student:
    def __init__(self,mname,mstudentid,mdateofbirth,mgender,mbatch,mmail,mphonenumber,mparantmail):
        self.mname=mname
        self.mstudentid=mstudentid
        self.mdateofbirth=mdateofbirth
        self.mgender=mgender
        self.mbatch=mbatch
        self.mmail=mmail
        self.mphonenumber=mphonenumber
        self.mmark={}
        self.mparantmail=mparantmail
        self.maths=0
        self.english=0
        self.statistics=0
        self.python=0
        self.language=0
        

    def info(self):
        return f"Name is :{self.mname}\n DOB:{self.mdateofbirth}\n Gender:{self.mgender}\n Batch{self.mbatch}"
    
    def marks(self, mmaths, menglish, mstatistics,mpython,mlanguage):
        self.mmark["1.Maths"] = mmaths
        self.mmark["2.English"] = menglish
        self.mmark["3.Statistics"] = mstatistics
        self.mmark["4.Python"] = mpython
        self.mmark["5.Language"] = mlanguage
        return str(self.mmark)
    def total(self):
        return sum(self.mmark.values()) if self.mmark else 0


    def calculate_grade(self,score):
        if score >= 90:
            return "A+"
        elif score >= 80:
            return "A"
        elif score >= 70:
            return "B"
        elif score >= 60:
            return "C"
        elif score >= 50:
            return "D"
        else:
            return "F"


def switch_frame(frame):
    frame.tkraise()






frames = {}
for name in ("main", "create", "login", "account","marks"):
    frames[name] = tk.Frame(root)
    frames[name].place(relwidth=1, relheight=1)

main_menu = frames["main"]
create_frame = frames["create"]
login_frame = frames["login"]
account_menu = frames["account"]
mark_frame = frames["marks"]



def on_close():
    root.destroy()




main_label=tk.Label(main_menu,text="STUDENT PORTAL",width=40)
main_label.pack(pady=10)
main_button=tk.Button(main_menu,text="Create Account",width=20,command=lambda: switch_frame(create_frame))
main_button.pack(pady=10)
main_button=tk.Button(main_menu,text="Login",width=20,command=lambda: switch_frame(login_frame))
main_button.pack(pady=10)
main_button=tk.Button(main_menu,text="Exit",width=20,command=root.destroy)
main_button.pack(pady=10)



# ....create fn...



def create_account():
    name= name_textbox.get()
    studentid=studentid_textbox.get()
    dateofbirth=dateofbirth_textbox.get()
    email=email_textbox.get()
    gender=gender_textbox.get()
    batch=batch_textbox.get()
    phonenumber=phonenumber_textbox.get()
    parantemail=parantemail_textbox.get()



    if not name or not studentid or not dateofbirth or not gender or not batch:
        messagebox.showwarning(
            "Missing Data",
            "Please fill all fields."
        )
        return 

    
    if not studentid.isdigit():
        return messagebox.showinfo("ERROR","Student Id must be numeric!")
    
    if "-" not in dateofbirth :
        return messagebox.showinfo("ERROR","Date Of Birth must be DD-MM-YYYY format!")
    if not email:
      return messagebox.showerror("Error", "Email is required!")

    

    if any(acc.mmail == email for acc in accounts):
        return messagebox.showerror("Error", "Email already exists!")
        
   
    if any(sid.mstudentid == studentid for sid in accounts):
        messagebox.showerror("Error", "Student Id already exists!")
        return
    

    if name and studentid and dateofbirth and gender and batch:
        messagebox.showinfo(
        "Information Added",
        f"""Student information has been successfully added.

    Name: {name}
    Student ID: {studentid}
    Date of Birth: {dateofbirth}
    Gender: {gender}
    Batch: {batch}
    email:{email}
    phonenumber:{phonenumber}
    parantemail:{parantemail}

    """
    )
        messagebox.showinfo(
            "Success",
            f"Student Portal of - {name}",
            
            
            
        )
        new_account = Student(name,studentid,dateofbirth,gender,batch,email,phonenumber,parantemail)
        accounts.append(new_account)

   

# ..........create account.............





createaccount_label=tk.Label(create_frame,text="CREATE ACCOUNT",width=20)
createaccount_label.pack(pady=10)
name_label=tk.Label(create_frame,text="Name")
name_label.pack(pady=5)
name_textbox=tk.Entry(create_frame)
name_textbox.pack()

studentid_label=tk.Label(create_frame,text="Student Id")
studentid_label.pack(pady=5)
studentid_textbox=tk.Entry(create_frame)
studentid_textbox.pack()

dateofbirth_label=tk.Label(create_frame,text="Date Of Birth")
dateofbirth_label.pack(pady=5)
dateofbirth_textbox=tk.Entry(create_frame)
dateofbirth_textbox.pack()


gender_label=tk.Label(create_frame,text="Gender")
gender_label.pack(pady=5)
gender_textbox=tk.Entry(create_frame)
gender_textbox.pack()


batch_label=tk.Label(create_frame,text="Batch")
batch_label.pack(pady=5)
batch_textbox=tk.Entry(create_frame)
batch_textbox.pack()



email_label=tk.Label(create_frame,text="Email")
email_label.pack(pady=5)
email_textbox=tk.Entry(create_frame)
email_textbox.pack()



phonenumber_label=tk.Label(create_frame,text="Phone Number")
phonenumber_label.pack(pady=5)
phonenumber_textbox=tk.Entry(create_frame)
phonenumber_textbox.pack()


parantemail_label=tk.Label(create_frame,text="Parant_Email")
parantemail_label.pack(pady=5)
parantemail_textbox=tk.Entry(create_frame)
parantemail_textbox.pack()

create_button=tk.Button(create_frame,text="CREATE",width=10,command= create_account)
create_button.pack(pady=10)

back_button=tk.Button(create_frame,text="BACK",width=10,command=lambda: switch_frame(main_menu))
back_button.pack()




# ...login account............






def login_account():
    global current_account
    lstudentid=lstudentid_textbox.get()
    ldateofbirth=ldateofbirth_textbox.get()
    if not ldateofbirth or not lstudentid:
       return messagebox.showerror("Error", "Please fill all fields")
    

    if not lstudentid.isdigit():
            return messagebox.showinfo("ERROR","Student Id must be numeric!")
    
    
       



    for loginaccount in accounts:
        if loginaccount.mstudentid == lstudentid and loginaccount.mdateofbirth == ldateofbirth:
            current_account = loginaccount 
            messagebox.showinfo("Logged in", f"Welcome {loginaccount.mname}")
            switch_frame(account_menu)
            return

    messagebox.showerror("Login Failed", "Invalid Student Id or Date Of Birth")

            
loginaccount_label=tk.Label(login_frame ,text="LOGIN ACCOUNT",width=20)
loginaccount_label.pack(pady=10)

lstudentid_label=tk.Label(login_frame,text="Student Id")
lstudentid_label.pack(pady=5)
lstudentid_textbox=tk.Entry(login_frame)
lstudentid_textbox.pack()

ldateofbirth_label=tk.Label(login_frame,text="Password")
ldateofbirth_label.pack(pady=5)
ldateofbirth_textbox=tk.Entry(login_frame,show="*")
ldateofbirth_textbox.pack()





login_button=tk.Button(login_frame,text="LOGIN",width=10,command= login_account)
login_button.pack(pady=10)

lback_button=tk.Button(login_frame,text="BACK",width=10,command=lambda: switch_frame(main_menu))
lback_button.pack()


# ....account menu .....




accountmenu_label=tk.Label(account_menu,text="Student Details",width=20)
accountmenu_label.pack(pady=10)
def show_account_info():
    if current_account:
        messagebox.showinfo("Account Info", current_account.info())
    else:
        messagebox.showerror("Error", "No account is currently logged in!")

accountinfo_button = tk.Button(account_menu, text="Student Details", width=15, command=show_account_info)
accountinfo_button.pack(pady=10)





# ....marks.....






def addmark():
    mathsmark = maths_textbox.get()
    englishmark = english_textbox.get()
    statisticsmark = statistics_textbox.get()
    pythonmark = python_textbox.get()
    languagemark = language_textbox.get()

    if not current_account:
        messagebox.showerror("Error", "No account is logged in!")
        return

    if (not mathsmark.isdigit() or int(mathsmark) > 100 or
        not englishmark.isdigit() or int(englishmark) > 100 or
        not statisticsmark.isdigit() or int(statisticsmark) > 100 or
        not pythonmark.isdigit() or int(pythonmark) > 100 or
        not languagemark.isdigit() or int(languagemark) > 100):
        
        messagebox.showerror("Error", "Marks must be numeric and ≤ 100")
        return

   
    current_account.marks(
        int(mathsmark),
        int(englishmark),
        int(statisticsmark),
        int(pythonmark),
        int(languagemark)
    )

    messagebox.showinfo(
    "Success",
    "Marks saved successfully\n\n"
    f"1.Maths: {mathsmark}\n"
    f"2.English: {englishmark}\n"
    f"3.Statistics: {statisticsmark}\n"
    f"4.Python: {pythonmark}\n"
    f"5.Language: {languagemark}"
)





maths_label=tk.Label(mark_frame ,text="Maths")
maths_label.pack(pady=5)
maths_textbox=tk.Entry(mark_frame )
maths_textbox.pack()


english_label=tk.Label(mark_frame,text="English")
english_label.pack(pady=5)
english_textbox=tk.Entry(mark_frame)
english_textbox.pack()


statistics_label=tk.Label(mark_frame,text="Statistics")
statistics_label.pack(pady=5)
statistics_textbox=tk.Entry(mark_frame)
statistics_textbox.pack()


python_label=tk.Label(mark_frame,text="Python")
python_label.pack(pady=5)
python_textbox=tk.Entry(mark_frame)
python_textbox.pack()


language_label=tk.Label(mark_frame,text="Language")
language_label.pack(pady=5)
language_textbox=tk.Entry(mark_frame)
language_textbox.pack()

marks_button = tk.Button(account_menu, text="Marks", width=15, command=lambda: switch_frame(mark_frame))
marks_button.pack(pady=10)

submit_button=tk.Button(mark_frame,text="SUBMIT",width=15,command=addmark)
submit_button.pack(pady=10)

back_button=tk.Button(mark_frame,text="BACK",width=10,command=lambda: switch_frame(account_menu))
back_button.pack()



# .....report card.....


def show_report_card():
    if not current_account:
        messagebox.showerror("Error", "No account logged in!")
        return

    if not current_account.mmark:
        messagebox.showerror("Error", "Marks not entered yet!")
        return

    total_marks = current_account.total()
    subject_count = len(current_account.mmark)
    max_total = subject_count * 100
    overall_percentage = round((total_marks / max_total) * 100, 2)
    average_marks = round(total_marks / subject_count, 2)
    overall_grade = current_account.calculate_grade(overall_percentage)


    result_status = "PASS" if overall_percentage >= 50 else "FAIL"

   
    subject_card = ""
    for subject, mark in current_account.mmark.items():
        subject_percentage = (mark / 100) * 100
        subject_grade = current_account.calculate_grade(mark)

        subject_card += (
            f"{subject}\n"
            f"  Marks      : {mark} / 100\n"
            f"  Percentage : {subject_percentage}%\n"
            f"  Grade      : {subject_grade}\n"
            f"-----------------------------\n"
        )
   
    messagebox.showinfo(
        "REPORT CARD",
        f"""STUDENT REPORT CARD

STUDENT DETAILS
-----------------------------
Name       : {current_account.mname}
Student ID : {current_account.mstudentid}
DOB        : {current_account.mdateofbirth}
Gender     : {current_account.mgender}
Batch      : {current_account.mbatch}

SUBJECT PERFORMANCE
-----------------------------
{subject_card}

OVERALL RESULT
-----------------------------
Total Marks : {total_marks} / {max_total}
Percentage  : {overall_percentage} %
Average     : {average_marks}
Grade       : {overall_grade}
Result      : {result_status}
"""
    )


reportcard_button = tk.Button(account_menu, text="Report Card", width=15, command=show_report_card)
reportcard_button.pack(pady=10)




# ....update mark....



def update_marks():
    if not current_account:
        messagebox.showerror("Error", "No account logged in!")
        return

    if not current_account.mmark:
        messagebox.showerror("Error", "Marks not entered yet!")
        return


    maths_textbox.delete(0, tk.END)
    maths_textbox.insert(0, current_account.mmark["Maths"])

    english_textbox.delete(0, tk.END)
    english_textbox.insert(0, current_account.mmark["English"])

    statistics_textbox.delete(0, tk.END)
    statistics_textbox.insert(0, current_account.mmark["Statistics"])

    python_textbox.delete(0, tk.END)
    python_textbox.insert(0, current_account.mmark["Python"])

    language_textbox.delete(0, tk.END)
    language_textbox.insert(0, current_account.mmark["Language"])

    switch_frame(mark_frame)
 


updatemark_button = tk.Button(account_menu, text="Update Mark", width=15, command=update_marks)
updatemark_button.pack(pady=10)


# .....emial....




def generate_report_card_text():
    total_marks = current_account.total()
    subject_count = len(current_account.mmark)
    max_total = subject_count * 100
    percentage = round((total_marks / max_total) * 100, 2)
    grade = current_account.calculate_grade(percentage)

    report = f"""STUDENT REPORT CARD

Name       : {current_account.mname}
Student ID : {current_account.mstudentid}
DOB        : {current_account.mdateofbirth}
Gender     : {current_account.mgender}
Batch      : {current_account.mbatch}

MARKS
"""
    for subject, mark in current_account.mmark.items():
        report += f"{subject}: {mark}/100\n"

    report += f"""
-----------------------------
Total      : {total_marks}/{max_total}
Percentage : {percentage} %
Grade      : {grade}
"""
    return report


def send_report_card():
    if not current_account:
        messagebox.showerror("Error", "No account logged in!")
        return

    if not current_account.mmark:
        messagebox.showerror("Error", "Marks not entered yet!")
        return

    try:
        # -------- EMAIL --------
        subject = "Student Progress Report"
        body =generate_report_card_text()
        sender = "asahila590@gmail.com"
        password = "dpgcpevlracnkkwy"

        recipients = [
            current_account.mmail,
            current_account.mparantmail
        ]

        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = sender
        msg["To"] = ", ".join(recipients)

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender, password)
            server.sendmail(sender, recipients, msg.as_string())

        # -------- SMS --------
        client = Client(
            'ACb989b8ba477dd200b066337952ccb771',
            'd5ecfb5f1d8714949707dd45f58e2ba8'
        )

        total = current_account.total()
        percentage = round((total / (len(current_account.mmark) * 100)) * 100, 2)
        grade = current_account.calculate_grade(percentage)

        sms_body = (
            f"Progress Report\n"
            f"Name: {current_account.mname}\n"
            f"Percentage: {percentage}%\n"
            f"Grade: {grade}"
        )

        client.messages.create(
            messaging_service_sid='MG34371a979ba31016c37dc47140543b41',
            body=sms_body,
            to=current_account.mphonenumber
        )

        messagebox.showinfo(
            "Success",
            "Report card sent to Parent via Email and SMS"
        )

    except Exception as e:
        messagebox.showerror("Error", str(e))

send_report_button = tk.Button(
    account_menu,
    text="Send Report Card",
    width=20,
    command=send_report_card
)
send_report_button.pack(pady=10)


# ....delete account....




def delete_account():
    global current_account

    if not current_account:
        messagebox.showerror("Error", "No account logged in!")
        return

    confirm = messagebox.askyesno(
        "Confirm Delete",
        "Are you sure you want to delete this account?"
    )

    if confirm:
        accounts.remove(current_account)
        current_account = None
        messagebox.showinfo("Deleted", "Account deleted successfully!")
        switch_frame(main_menu)


delete_button = tk.Button(account_menu, text="Delete Account", width=15, command=delete_account)
delete_button.pack(pady=10)




# ...logout.....

def logout():
    global current_account
    current_account = None
    switch_frame(main_menu)

logout_button = tk.Button(account_menu, text="Logout", width=15, command=logout)
logout_button.pack(pady=10)



root.protocol("WM_DELETE_WINDOW", on_close)
switch_frame(main_menu)
root.mainloop()


# 25f1002109@ds.study.iitm.ac.in