import tkinter as tk 

root = tk.Tk()

letter = ['A','B','C','D','E']

for i in letter:
    tk.Label(root, text=i, relief='groove').pack(fill='both', expand=True)
for i in letter:
    tk.Label(root, text=i+i, relief='groove').pack(side='left', fill='both', expand=True)
for i in letter:
    tk.Label(root, text=i+i+i, relief='groove').pack(side='bottom', fill='both', expand=True)
for i in letter:
    tk.Label(root, text=i+i+i+i, relief='groove').pack(side='right',fill='both', expand=True)
 
root.mainloop()
