try:
    from Tkinter import *
    from Tkinter import ttk
except ImportError:
    from tkinter import *
    from tkinter import ttk
import sqlite3

class config(Tk):
	def __init__(self):
		Tk.__init__(self)
		ttk.Style(self).configure('TButton', font=('Arial', 10))

		self.lb1 = Label(self,text='Iterações',font=('Arial',10))
		self.lb2 = Label(self,text='Alfa',font=('Arial',10))
		self.lb3 = Label(self,text='Aproveitamento Mínimo (%)',font=('Arial',10))
		self.lb4 = Label(self,text='Tempo Mínimo (min)',font=('Arial',10))
		self.lb5 = Label(self,text='Espessura de Lâmina (mm)',font=('Arial',10))
		self.lb6 = Label(self,text='Proporção inicial',font=('Arial',10))
		self.lb7 = Label(self,text='Sensibilidade do scroll',font=('Arial',10))
		self.lb1.grid(row=0,column=0)
		self.lb2.grid(row=1,column=0)
		self.lb3.grid(row=2,column=0)
		self.lb4.grid(row=3,column=0)
		self.lb5.grid(row=4,column=0)
		self.lb6.grid(row=5,column=0)
		self.lb7.grid(row=6,column=0)

		self.ent1 = Entry(self,width=10)
		self.ent2 = Entry(self,width=10)
		self.ent3 = Entry(self,width=10)
		self.ent4 = Entry(self,width=10)
		self.ent5 = Entry(self,width=10)
		self.ent6 = Entry(self,width=10)
		self.ent7 = Entry(self,width=10)
		self.ent1.grid(row=0,column=1)
		self.ent2.grid(row=1,column=1)
		self.ent3.grid(row=2,column=1)
		self.ent4.grid(row=3,column=1)
		self.ent5.grid(row=4,column=1)
		self.ent6.grid(row=5,column=1)
		self.ent7.grid(row=6,column=1)

		self.bt = ttk.Button(self,text='Salvar',command=self.save)
		self.bt.grid(row=7,column=0)

		self.cconfig = sqlite3.connect('configuracoes.db')
		self.cco = self.cconfig.cursor()
		self.cco.execute('CREATE TABLE IF NOT EXISTS configuracoes (iteracoes int, alfa real, aprovmin real, tempo real, esp real, count int, sens int)')

		for row in self.cco.execute('SELECT * FROM configuracoes'):
			self.ent1.insert('end',row[0])
			self.ent2.insert('end',row[1])
			self.ent3.insert('end',row[2]*100)
			self.ent4.insert('end',row[3])
			self.ent5.insert('end',row[4])
			self.ent6.insert('end',row[5])
			self.ent7.insert('end',row[6])

	def save(self):
		self.cco.execute('UPDATE configuracoes SET iteracoes=?, alfa=?, aprovmin=?, tempo=?, esp=?, count=?, sens=?',(int(self.ent1.get()),float(self.ent2.get()),float(self.ent3.get())/100,float(self.ent4.get()),float(self.ent5.get()),float(self.ent6.get()),float(self.ent7.get())))
		self.cconfig.commit()

if __name__=='__main__':
	w=config()
	w.iconbitmap('iconfiguracoes_icon.ico')
	w.title('Configurações')
	w.geometry('%dx%d+%d+%d' % (232,180,((w.winfo_screenwidth()/2) - (232/2)),((w.winfo_screenheight()/2) - (180/2))))
	w.mainloop()