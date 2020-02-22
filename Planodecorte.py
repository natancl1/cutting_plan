try:
    from Tkinter import *
    from Tkinter import ttk
except ImportError:
    from tkinter import *
    from tkinter import ttk
from functools import partial
import math, Gerarpdf, Info
r1=0
class pcorte(Tk):
	def __init__(self,s,c,ap,qi,t,C,espessura,count,sens):
		Tk.__init__(self)

		self.state('zoomed')
		self.iconbitmap('gerarplanocorte_icon.ico')
		self.title('Plano de Corte')
		self.r = 0
		self.esp = espessura
		self.count=count
		self.sens=sens
		self.bind('<MouseWheel>', self.Mouse_wheel)

		self.lb = Label(self,font=('Arial',10))
		self.lb2 = Label(self,text=f'          Aproveitamento: {round(ap*100,2)}%',font=('Arial',10))
		self.lb4 = Label(self,text=f'          Iterações: {qi}',font=('Arial',10))
		self.lb6 = Label(self,font=('Arial',10))
		if t >= 60 and t < 3600:
			if t/60 == 1:
				self.lb6['text'] = (f'          Tempo: {t/60} minuto')
			else:
				self.lb6['text'] = (f'          Tempo: {round(t/60,2)} minutos')
		elif t >= 3600 and t < 86400:
			if t/3600 == 1:
				self.lb6['text'] = (f'          Tempo: {t/3600} hora')
			else:
				self.lb6['text'] = (f'          Tempo: {round(t/3600,2)} horas')
		elif t >= 86400:
			if t/86400 == 1:
				self.lb6['text'] = (f'          Tempo: {t/86400} dia')
			else:
				self.lb6['text'] = (f'          Tempo: {round(t/86400,2)} dias')
		else:
			if t == 1:
				self.lb6['text'] = (f'          Tempo: {t} segundo')
			else:
				self.lb6['text'] = (f'          Tempo: {round(t,2)} segundos')

		self.lb.grid(row=0,column=4)
		self.lb2.grid(row=0,column=6)
		self.lb4.grid(row=0,column=8)
		self.lb6.grid(row=0,column=10)

		self.iv=PhotoImage(file='voltar.png',master=self)
		self.ia=PhotoImage(file='avancar.png',master=self)
		self.ipdf=PhotoImage(file='pdf.png',master=self)
		self.iinf=PhotoImage(file='info.png',master=self)

		self.bt3 = ttk.Button(self,command=self.voltar,image=self.iv)
		self.bt4 = ttk.Button(self,command=self.avancar,image=self.ia)
		self.bt5 = ttk.Button(self,command=partial(Gerarpdf.ifgerarpdf,s,c,0,self.esp,self.count,self.sens),image=self.ipdf)
		self.bt6 = ttk.Button(self,command=partial(self.Inform,s),image=self.iinf)

		self.bt3.grid(row=0,column=0)
		self.bt4.grid(row=0,column=1)
		self.bt5.grid(row=0,column=2)
		self.bt6.grid(row=0,column=3)

		self.ca = Canvas(self,height=(self.winfo_screenheight())*0.85,width=(self.winfo_screenwidth())*0.95,bg="white")
		self.ca.place(relx=0.5,rely=0.5,anchor=CENTER)
		self.solucao = s
		self.chapas = c
		self.ifdesenho(self.r)

	def Mouse_wheel(self,event):
		global r1
		if event.delta==-120 and self.count>=0:
			self.count-=self.sens
			self.desenho(self.chapas[r1],r1)
			self.bt5.grid_forget()
			self.bt5 = ttk.Button(self,command=partial(Gerarpdf.ifgerarpdf,self.solucao,self.chapas,0,self.esp,self.count,self.sens),image=self.ipdf)
			self.bt5.grid(row=0,column=2)
		if event.delta==120:
			self.count+=self.sens
			self.desenho(self.chapas[r1],r1)
			self.bt5.grid_forget()
			self.bt5 = ttk.Button(self,command=partial(Gerarpdf.ifgerarpdf,self.solucao,self.chapas,0,self.esp,self.count,self.sens),image=self.ipdf)
			self.bt5.grid(row=0,column=2)

	def Inform(self,s):
		Info.Informacoes(s)

	def voltar(self):
		global r1
		if r1 > 0:
			r1-=1
			if self.solucao[r1] != []:
				self.desenho(self.chapas[r1],r1)

	def avancar(self):
		global r1
		if r1 < (len(self.chapas)-1) and r1 < (len(self.solucao)-1):
			r1 += 1
			if self.solucao[r1] != []:
				self.desenho(self.chapas[r1],r1)

	def ifdesenho(self,r):
		self.chapas.sort(key=lambda x: x[0]*x[1])
		if self.solucao != [] and self.solucao[r] != []:
			self.desenho(self.chapas[r],r)
		elif self.solucao != [] and len(self.chapas) > 1:
			r+=1
			self.desenho(self.chapas[r],r)

	def desenho(self,x,r):
		self.ca.delete('all')
		x0 = 36
		y0 = 17                

		self.ca.create_rectangle(x0,y0,x0+self.count*x[0],y0+self.count*x[1],fill='light blue')
		self.ca.create_text(x0+self.count*x[0]/2,y0,text='{}'.format(round(x[0],3)),anchor=S,font=("Arial",10,"bold"))
		self.ca.create_text(x0,y0+self.count*x[1]/2,text='{}'.format(round(x[1],3)),anchor=E,font=("Arial",10,"bold"))
		self.lb['text']=(f'          Chapa: {x[4]}')
		f = 'snow'
		for j in range(len(self.solucao[r])): # Strips
			if 'h' in self.solucao[r][j]:
				a = x0
				for k in range(len(self.solucao[r][j])-1): # Parts
					self.ca.create_rectangle(x0, y0, x0+(self.solucao[r][j][k][0]*self.count), y0+(self.solucao[r][j][k][1]*self.count), fill=f)
					self.ca.create_text(x0+(self.solucao[r][j][k][0]*self.count)/2,y0,text='{}'.format(round(self.solucao[r][j][k][0],3)),anchor=N,font=("Arial",10,"bold"))
					self.ca.create_text(x0+2,y0+(self.solucao[r][j][k][1]*self.count)/2,text='{}'.format(round(self.solucao[r][j][k][1],3)),anchor=W,font=("Arial",10,"bold"))
					x0 += ((self.solucao[r][j][k][0]+self.esp)*self.count)
				x0 = a
				y0 += ((self.solucao[r][j][0][1]+self.esp)*self.count)
			else:
				b = y0
				for k in range(len(self.solucao[r][j])-1): # Parts
					self.ca.create_rectangle(x0, y0, x0+(self.solucao[r][j][k][0]*self.count), y0+(self.solucao[r][j][k][1]*self.count), fill=f)
					self.ca.create_text(x0+(self.solucao[r][j][k][0]*self.count)/2,y0,text='{}'.format(round(self.solucao[r][j][k][0],3)),anchor=N,font=("Arial",10,"bold"))
					self.ca.create_text(x0+2,y0+(self.solucao[r][j][k][1]*self.count)/2,text='{}'.format(round(self.solucao[r][j][k][1],3)),anchor=W,font=("Arial",10,"bold"))
					y0 += ((self.solucao[r][j][k][1]+self.esp)*self.count)
				x0 += ((self.solucao[r][j][0][0]+self.esp)*self.count)
				y0 = b

if __name__=="__main__":
	w=pcorte()
	w.mainloop()
