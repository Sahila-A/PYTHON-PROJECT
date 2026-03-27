import tkinter as tk

root=tk.Tk()
root.title("Calculator")
root.geometry("400x300")
root.configure(bg="#545050")
def click(event):
    global expression
    expression += str(event.widget.cget("text"))
    input_text.set(expression)
# Function to clear input field
def clear():
    global expression
    expression = ""
    input_text.set("")

# Function to calculate expression
def calculate():
    global expression
    try:
        result = str(eval(expression))
        input_text.set(result)
        expression = result
    except:
        input_text.set("Error")
        expression = ""
expression = ""
input_text = tk.StringVar()

# # Input field
input_frame=tk.Frame(root,width=500,height=40,bd=0,highlightbackground="black", highlightcolor="black", highlightthickness=1)
input_frame.pack()

input_field = tk.Entry(input_frame, font=('arial', 18, 'bold'), textvariable=input_text, width=50, bg="#eee", bd=0, justify=tk.RIGHT)
input_field.grid(row=0, column=0)
input_field.pack(ipady=10)  # internal padding

# Buttons
button_frame = tk.Frame(root, width=500, height=272.5, bg="grey")
button_frame.pack()



buttons=[
    ['7','8','9','/'],
    ['4','5','6','*'],
    ['1','2','3','-'],
    ['0','.','=','+'],
    

]
for i in range(4):
    for j in range(4):
        btn_text = buttons[i][j]
        if btn_text == "=":
            btn = tk.Button(button_frame, text=btn_text, fg="black", width=10, height=3, bd=0, bg="#eee", cursor="hand2", command=calculate)
        else:
            btn = tk.Button(button_frame, text=btn_text, fg="black", width=10, height=3, bd=0, bg="#fff", cursor="hand2")
            btn.bind("<Button-1>", click)
        btn.grid(row=i, column=j, padx=1, pady=1)

# Clear button
clear_btn = tk.Button(root, text='C', fg="black", width=34, height=3, bd=0, bg="#f2a33c", cursor="hand2", command=clear)
clear_btn.pack(side=tk.TOP, pady=1)

root.mainloop()




