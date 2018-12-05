import tkinter as tk
import math

LARGE_FONT = ('Helvetica',14)
SMALL_FONT = ('Helvetica',12)

def popUpMsg(msg):

	popup = tk.Tk()

	popup.wm_title('!')

	label = tk.Label(popup,text=msg,font=LARGE_FONT)

	label.pack(side='top',fill='x',pady=10)

	B1 = tk.Button(popup,text='Ok',command=lambda:popup.destroy())

	B1.pack()

	popup.mainloop()

class PVcalcApp(tk.Tk):

	def __init__(self,*args,**kwargs):

		tk.Tk.__init__(self,*args,**kwargs)

		tk.Tk.wm_title(self,'PV Calculator')

		container = tk.Frame(self)
		container.pack(side='top',fill='both',expand=True)
		container.grid_rowconfigure(0,weight=1)
		container.grid_columnconfigure(0,weight=1)

		self.frames = {}

		for F in (StartPage,LumpSumPage,AnnuityPage):

			frame = F(container,self)

			self.frames[F] = frame

			frame.grid(row=0,column=0,sticky='nsew')

		self.showFrame(StartPage)

	def showFrame(self,cont):

		frame = self.frames[cont]
		frame.tkraise()


class StartPage(tk.Frame):

	def __init__(self,parent,controller):

		tk.Frame.__init__(self,parent)

		label = tk.Label(self,text='Select:',font=LARGE_FONT)
		label.pack(pady=10,padx=10)

		button1 = tk.Button(self,text='Lump Sum',command=lambda:controller.showFrame(LumpSumPage))
		button1.pack()

		button2 = tk.Button(self,text='Annuity',command=lambda:controller.showFrame(AnnuityPage))
		button2.pack()

		button3 = tk.Button(self,text='Perpituity')
		button3.pack()

		button4 = tk.Button(self,text='Quit',command=lambda:quit())
		button4.pack()

class LumpSumPage(tk.Frame):

	def __init__(self,parent,controller):

		tk.Frame.__init__(self,parent)

		label1 = tk.Label(self,text='Lump Sum',font=LARGE_FONT)
		label2 = tk.Label(self,text='Future Value:',font=SMALL_FONT)
		label3 = tk.Label(self,text='No. of Periods:',font=SMALL_FONT)
		label4 = tk.Label(self,text='Interest Rate (%):',font=SMALL_FONT)
		label5 = tk.Label(self,text='Present Value:',font=SMALL_FONT)

		label1.grid(row=0)
		label2.grid(row=1)
		label3.grid(row=2)
		label4.grid(row=3)
		label5.grid(row=4)

		vcmd = (parent.register(self.validate),'%d','%i','%P','%s','%S','%v','%V','%W')

		self.FVEntry = tk.Entry(self)
		self.tEntry = tk.Entry(self)
		self.rEntry = tk.Entry(self)
		self.PVEntry = tk.Entry(self)

		self.FVEntry.grid(row=1,column=1,columnspan=3)
		self.tEntry.grid(row=2,column=1,columnspan=3)
		self.rEntry.grid(row=3,column=1,columnspan=3)
		self.PVEntry.grid(row=4,column=1,columnspan=3)

		button1 = tk.Button(self,text='Back',command=lambda:controller.showFrame(StartPage))
		button2 = tk.Button(self,text='Show',command=self.calculate)
		button3 = tk.Button(self,text='Clear',command=self.clearall)
		button4 = tk.Button(self,text='Quit',command=lambda:quit())

		button1.grid(row=5,column=0,sticky='W',pady=4)
		button2.grid(row=5,column=1,sticky='W',pady=4)
		button3.grid(row=5,column=2,sticky='W',pady=4)
		button4.grid(row=5,column=3,sticky='W',pady=4)

	def calculate(self):

		try:
			FV = float(self.FVEntry.get())
		except ValueError:
			FV = None
		try:
			t = float(self.tEntry.get())
		except ValueError:
			t = None
		try:
			r = float(self.rEntry.get())/100
		except ValueError:
			r = None
		try:
			PV = float(self.PVEntry.get())
		except ValueError:
			PV = None

		empty = [i for i,x in enumerate([FV,t,r,PV]) if x == None]

		if len(empty) == 0:
			popUpMsg('Please remove one field to calculate.')
		elif len(empty) > 1:
			popUpMsg('Please enter a minimum of 3 fields.')
		else:
			if FV == None:
				FV = PV*(1+r)**t
				self.FVEntry.insert(0,str(round(FV,2)))

			if t == None:
				t = math.log10(FV/PV)/math.log10(1+r)
				self.tEntry.insert(0,str(round(t,2)))

			if r == None:
				r = ((FV/PV)**(1/t))-1
				self.rEntry.insert(0,str(round(r,4)*100))

			if PV == None:
				PV = FV/(1+r)**t
				self.PVEntry.insert(0,str(round(PV,2)))

	def clearall(self):

		self.FVEntry.delete(0,'end')
		self.tEntry.delete(0,'end')
		self.rEntry.delete(0,'end')
		self.PVEntry.delete(0,'end')

	def validate(self,action,index,value_if_allowed,prior_value,text,validation_type,trigger_type,widget_name):

		if text in '0123456789.-+':
			try:
				float(value_if_allowed)
				return True
			except ValueError:
				return False
		else:
			return False

class AnnuityPage(tk.Frame):

	def __init__(self,parent,controller):

		tk.Frame.__init__(self,parent)

		label1 = tk.Label(self,text='Annuity',font=LARGE_FONT)
		label2 = tk.Label(self,text='Future Value:',font=SMALL_FONT)
		label3 = tk.Label(self,text='No. of Periods:',font=SMALL_FONT)
		label4 = tk.Label(self,text='Interest Rate (%):',font=SMALL_FONT)
		label5 = tk.Label(self,text='Payment:',font=SMALL_FONT)
		label6 = tk.Label(self,text='Present Value:',font=SMALL_FONT)

		label1.grid(row=0)
		label2.grid(row=1)
		label3.grid(row=2)
		label4.grid(row=3)
		label5.grid(row=4)
		label6.grid(row=5)

		vcmd = (parent.register(self.validate),'%d','%i','%P','%s','%S','%v','%V','%W')

		self.FVEntry = tk.Entry(self)
		self.tEntry = tk.Entry(self)
		self.rEntry = tk.Entry(self)
		self.CEntry = tk.Entry(self)
		self.PVEntry = tk.Entry(self)

		self.FVEntry.grid(row=1,column=1,columnspan=3)
		self.tEntry.grid(row=2,column=1,columnspan=3)
		self.rEntry.grid(row=3,column=1,columnspan=3)
		self.CEntry.grid(row=4,column=1,columnspan=3)
		self.PVEntry.grid(row=5,column=1,columnspan=3)

		button1 = tk.Button(self,text='Back',command=lambda:controller.showFrame(StartPage))
		button2 = tk.Button(self,text='Show',command=self.calculate)
		button3 = tk.Button(self,text='Clear',command=self.clearall)
		button4 = tk.Button(self,text='Quit',command=lambda:quit())

		button1.grid(row=5,column=0,sticky='W',pady=4)
		button2.grid(row=5,column=1,sticky='W',pady=4)
		button3.grid(row=5,column=2,sticky='W',pady=4)
		button4.grid(row=5,column=3,sticky='W',pady=4)

	def calculate(self):

		try:
			FV = float(self.FVEntry.get())
		except ValueError:
			FV = None
		try:
			t = float(self.tEntry.get())
		except ValueError:
			t = None
		try:
			r = float(self.rEntry.get())/100
		except ValueError:
			r = None
		try:
			C = floar(self.CEntry.get())
		except ValueError:
			C = None
		try:
			PV = float(self.PVEntry.get())
		except ValueError:
			PV = None

		empty = [i for i,x in enumerate([FV,t,r,C,PV]) if x == None]

		if len(empty) == 0:
			popUpMsg('Please remove one field to calculate.')
		elif len(empty) == 2 and FV != None and PV != None:
			popUpMsg('Please enter a minimum of 4 fields to calculate future value.')
		elif len(empty) > 2:
			popup
		else:
			if FV == None and PV == None:
				#Calculate PV and FV
			elif FV == None:
				#Calculate FV
			elif PV == None:
				#Calculate PV

			if t == None:
				t = math.log10(FV/PV)/math.log10(1+r)
				self.tEntry.insert(0,str(round(t,2)))

			if r == None:
				r = ((FV/PV)**(1/t))-1
				self.rEntry.insert(0,str(round(r,4)*100))

			if PV == None:
				PV = FV/(1+r)**t
				self.PVEntry.insert(0,str(round(PV,2)))

	def clearall(self):

		self.FVEntry.delete(0,'end')
		self.tEntry.delete(0,'end')
		self.rEntry.delete(0,'end')
		self.PVEntry.delete(0,'end')

	def validate(self,action,index,value_if_allowed,prior_value,text,validation_type,trigger_type,widget_name):

		if text in '0123456789.-+':
			try:
				float(value_if_allowed)
				return True
			except ValueError:
				return False
		else:
			return False

app = PVcalcApp()
app.mainloop()























