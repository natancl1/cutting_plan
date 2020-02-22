try:
    from Tkinter import *
    from Tkinter import ttk
except ImportError:
    from tkinter import *
    from tkinter import ttk

class Informacoes(Tk):
	def __init__(self,s):
		Tk.__init__(self)
		self.iconbitmap('info_icon.ico')
		self.title('Informações')
		self.geometry('%dx%d+%d+%d' % (200,210,((self.winfo_screenwidth()/2) - (200/2)),((self.winfo_screenheight()/2) - (210/2))))

		self.lb = Label(self, text='Peças Incluídas',font=('Arial',10))
		self.lb.grid(row=0,column=1)

		self.pf = Listbox(self, yscrollcommand=self.yscroll, xscrollcommand=self.xscroll)
		self.pf.grid(row=1,column=1)
		
		x = []
		z = []
		for i in range(len(s)):
			for j in range(len(s[i])):
				for k in range(len(s[i][j])-1):
					x.append(s[i][j][k][:])
		for i in range(len(x)):
			x[i] = [x[i][0],x[i][1]]
		for i in x:
			if i not in z and [i[1],i[0]] not in z:
				z.append(i)
		for i in z:
			self.pf.insert('end',f'{int(x.count([i[0],i[1]])+x.count([i[1],i[0]]))} peça de {i[0]} X {i[1]}')
		x = []
		z = []
		'''
		x=[]
		for i in range(0,len(C)):
			for c in range(0,len(C)):
				if (C[i][0]==C[c][1]) and (C[i][1]==C[c][0]) and (c not in x):
					x.append(i)
		for i in x:
			if C[i][2] == 1:
				self.pf.insert('end',f'{int(C[i][2])} peça de {C[i][0]} X {C[i][1]}')
			else:
				self.pf.insert('end',f'{int(C[i][2])} peças de {C[i][0]} X {C[i][1]}')
		x=[]'''
		self.br = Scrollbar(self, orient='vertical')
		self.br.config(command=self.yview)
		self.br.grid(row=1,column=2,sticky=N+S)

		self.br1 = Scrollbar(self, orient='horizontal')
		self.br1.config(command=self.xview)
		self.br1.grid(row=2,column=1,sticky=W+E)

	def yscroll(self, *args):
		if self.pf.yview():
			self.pf.yview_moveto(args[0])
		self.br.set(*args)

	def yview(self, *args):
		self.pf.yview(*args)

	def xscroll(self, *args):
		if self.pf.xview():
			self.pf.xview_moveto(args[0])
		self.br.set(*args)

	def xview(self, *args):
		self.pf.xview(*args)

if __name__ == "__main__":
	root = Informacoes()
	root.mainloop()		
