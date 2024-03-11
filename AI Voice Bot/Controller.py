from tkinter import *
window = Tk()



discordEnabled = False

interactionsOpt = Frame(window)
interactionsOpt.pack()
opt1 = Checkbutton( variable = discordEnabled, text='Discord', bg= 'purple')
opt1.pack()


window.mainloop()
#exec("discordInteract.py")
