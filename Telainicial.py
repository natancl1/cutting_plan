try:
    from Tkinter import *
    from Tkinter import ttk
except ImportError:
    from tkinter import *
    from tkinter import ttk
from functools import partial
import Janelainserirpeca, Janelainserirchapa, Grasp, sqlite3, Planodecorte, Configuracoes

class tela(Tk):
	def __init__(self):
		Tk.__init__(self)
		ttk.Style(self).configure('TButton',font=('Arial', 12), anchor=W)

		self.icp=PhotoImage(file='cadastrarpecas.png',master=self)
		self.icc=PhotoImage(file='cadastrarchapas.png',master=self)
		self.ico=PhotoImage(file='iconfiguracoes.png',master=self)
		self.ipc=PhotoImage(file='gerarplanocorte.png',master=self)

		self.botao1 = ttk.Button(self,text=' Cadastrar Peças',width=17,command=self.inserirpecas,image=self.icp,compound=LEFT)
		self.botao2 = ttk.Button(self,text=' Cadastrar Chapas',width=17,command=self.inserirchapas,image=self.icc,compound=LEFT)
		self.botao3 = ttk.Button(self,text=' Configurações',width=17,command=self.conf,image=self.ico,compound=LEFT)
		self.botao4 = ttk.Button(self,text=' Gerar Plano de Corte',width=17,command=self.plano,image=self.ipc,compound=LEFT)

		self.botao1.grid(row=0,column=0)
		self.botao2.grid(row=1,column=0)
		self.botao3.grid(row=2,column=0)
		self.botao4.grid(row=3,column=0)

		self.cpecas = sqlite3.connect('pecas.db')
		self.cp = self.cpecas.cursor()
		self.cp.execute('CREATE TABLE IF NOT EXISTS pecas (id text, comprimento real, largura real, quantidade real, area real)')
		self.cchapas = sqlite3.connect('chapas.db')
		self.cc = self.cchapas.cursor()
		self.cc.execute('CREATE TABLE IF NOT EXISTS chapas (id text, comprimento real, largura real, quantidade real, area real)')
		self.cconfig = sqlite3.connect('configuracoes.db')
		self.cco = self.cconfig.cursor()
		self.cco.execute('CREATE TABLE IF NOT EXISTS configuracoes (iteracoes int, alfa real, aprovmin real, tempo real, esp real)')

	def inserirpecas(self):
		x = Janelainserirpeca.ListboxExe()
		x.iconbitmap('cadastrarpecas_icon.ico')
		x.title('Cadastrar Peças')
		x.geometry('%dx%d+%d+%d' % (575,240,((x.winfo_screenwidth()/2) - (575/2)),((x.winfo_screenheight()/2) - (240/2))))
		x.mainloop()

	def inserirchapas(self):
		x = Janelainserirchapa.ListboxExe()
		x.iconbitmap('cadastrarchapas_icon.ico')
		x.title('Cadastrar Chapas')
		x.geometry('%dx%d+%d+%d' % (575,240,((x.winfo_screenwidth()/2) - (575/2)),((x.winfo_screenheight()/2) - (240/2))))
		x.mainloop()

	def conf(self):
		x = Configuracoes.config()
		x.iconbitmap('iconfiguracoes_icon.ico')
		x.title('Configurações')
		x.geometry('%dx%d+%d+%d' % (232,180,((x.winfo_screenwidth()/2) - (232/2)),((x.winfo_screenheight()/2) - (180/2))))
		x.mainloop()

	def plano(self):
		self.pecas = []
		self.chapas = []
		for row in self.cco.execute('SELECT * FROM configuracoes'):
			self.iteracoes = row[0]
			self.alfa = row[1]
			self.aprov_min = row[2]
			self.tempo = row[3]
			self.esp = row[4]/1000
			self.count = row[5]
			self.sens = row[6]
		for row in self.cp.execute('SELECT * FROM pecas'):
			self.pecas.append([row[1],row[2],row[3],row[4]])
			if row[1]!=row[2]:
				self.pecas.append([row[2],row[1],row[3],row[4]])
		for row in self.cc.execute('SELECT * FROM chapas'):
			self.chapas.append([row[1],row[2],row[3],row[4],row[0]])
		self.resultado = list(Grasp.grasp_2d(self.pecas, self.chapas, self.alfa, self.iteracoes, self.aprov_min, self.tempo, self.esp))[:]
		self.solucao = self.resultado[0][:]
		self.aproveitamento = self.resultado[1]
		self.qi = self.resultado[2]
		self.t = self.resultado[3]
		self.C = self.resultado[4]
		Planodecorte.pcorte(self.solucao,self.chapas,self.aproveitamento,self.qi,self.t,self.C,self.esp,self.count,self.sens)

if __name__ == "__main__":
	w=tela()
	w.iconbitmap('corte.ico')
	w.title('Plano de Corte')
	w.geometry('+%d+%d' % (((w.winfo_screenwidth()/2) - (w.winfo_reqwidth()/2)),((w.winfo_screenheight()/2) - (w.winfo_reqheight()/2))))
	w.mainloop()