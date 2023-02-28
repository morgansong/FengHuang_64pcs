from tkinter import *
# creating tkinter window
base = Tk()
#screen's length and width in pixels and mm
length_1= base.winfo_screenheight()
width_1= base.winfo_screenwidth()

length_2 = base.winfo_screenmmheight()
width_2 = base.winfo_screenmmwidth()

#screen Depth
screendepth = base.winfo_screendepth()


Label(base,text='Select the module to connect\n which port of Relay controller', width = int(width_2/8), height= int(length_2/8),bg='green').pack()
Label(base,text='aaaaaaa', width = int(length_2/2), height= int(length_2/2),bg='red').pack()
base.attributes('-fullscreen', True)

print(" width x length (in pixels) =",(width_1,length_1))
print(" width x length (in mm) =", (width_2, length_2))
print(" Screen depth =",screendepth)


mainloop()