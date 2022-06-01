import tkinter as tk

OPTIONS = [
    "Market Breadth",
    "Single Ticker",
    "Automated SP500 Analysis"
]


def center(win):
    """
    centers a tkinter window
    :param win: the main window or Toplevel window to center
    """
    win.update_idletasks()
    width = win.winfo_width()
    frm_width = win.winfo_rootx() - win.winfo_x()
    win_width = width + 2 * frm_width
    height = win.winfo_height()
    titlebar_height = win.winfo_rooty() - win.winfo_y()
    win_height = height + titlebar_height + frm_width
    x = win.winfo_screenwidth() // 2 - win_width // 2
    y = win.winfo_screenheight() // 2 - win_height // 2
    win.geometry('{}x{}+{}+{}'.format(width, height, x, y))
    win.deiconify()


root = tk.Tk()
root.title("Analysis")
root.geometry("1000x500")
root.attributes('-alpha', 0.0)
menubar = tk.Menu(root)
filemenu = tk.Menu(menubar, tearoff=0)
filemenu.add_command(label="Exit", command=root.destroy)
menubar.add_cascade(label="File", menu=filemenu)
root.config(menu=menubar)
frm = tk.Frame(root, bd=4, relief='raised')
frm.pack(fill='x')
lab = tk.Label(frm, text='Technical Analysis', bd=4, background="#333", foreground="#fff", relief="sunken")
lab.pack(ipadx=4, padx=4, ipady=4, pady=4, fill='both')
center(root)

variable = tk.StringVar(root)
# Default value
variable.set(OPTIONS[0])
action_select = tk.OptionMenu(root, variable, *OPTIONS)
action_select.pack(ipadx=4, padx=4, ipady=4, pady=10)


def get_selection_choice():
    selection = variable.get()
    label = tk.Label(text=selection)
    label.pack()


confirm_selection = tk.Button(root, text="Confirm", bg="green", fg="white", activebackground='green',
                              activeforeground="white", command=get_selection_choice)
confirm_selection.pack(ipadx=4, padx=4, ipady=4, pady=4)

root.attributes('-alpha', 1.0)
root.mainloop()
