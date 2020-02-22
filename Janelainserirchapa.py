try:
    from Tkinter import *
    from Tkinter import ttk
    from Tkinter import filedialog
except ImportError:
    from tkinter import *
    from tkinter import ttk
    from tkinter import filedialog
import sqlite3, xlrd

class ListboxExe(Tk):
    def __init__(self):
        Tk.__init__(self)
        ttk.Style(self).configure('TButton', font=('Arial', 10))

        self.cchapas = sqlite3.connect('chapas.db')
        self.cc = self.cchapas.cursor()
        self.cc.execute('CREATE TABLE IF NOT EXISTS chapas (id text, comprimento real, largura real, quantidade real, area real)')

        self.label1 = Label(self,text='Id',font=('Arial',10))
        self.label2 = Label(self,text='Comprimento',font=('Arial',10))
        self.label3 = Label(self,text='Largura',font=('Arial',10))
        self.label4 = Label(self,text='Quantidade',font=('Arial',10))
        self.label5 = Label(self,text='Área',font=('Arial',10))
        self.label6 = Label(self,font=('Arial',10))
        self.label7 = Label(self,font=('Arial',10))
        self.label1.grid(row=0,column=0)
        self.label2.grid(row=0,column=1)
        self.label3.grid(row=0,column=2)
        self.label4.grid(row=0,column=3)
        self.label5.grid(row=0,column=4)
        self.label6.grid(row=4,column=0,columnspan=2,sticky=W)
        self.label7.grid(row=4,column=2,columnspan=2,sticky=W)

        self.br1 = Scrollbar(self, orient='vertical')
        self.br2 = Scrollbar(self, orient='horizontal')

        self.list1 = Listbox(self, yscrollcommand=self.yscroll1,width=15)
        self.list1.bind('<Button-3>',self.popup)
        self.list1.grid(row=2,column=0)

        self.list2 = Listbox(self, yscrollcommand=self.yscroll2,width=15)
        self.list2.bind('<Button-3>',self.popup)
        self.list2.grid(row=2,column=1)

        self.list3 = Listbox(self, yscrollcommand=self.yscroll3,width=15)
        self.list3.bind('<Button-3>',self.popup)
        self.list3.grid(row=2,column=2)

        self.list4 = Listbox(self, yscrollcommand=self.yscroll4,width=15)
        self.list4.bind('<Button-3>',self.popup)
        self.list4.grid(row=2,column=3)

        self.list5 = Listbox(self, yscrollcommand=self.yscroll5,width=15)
        self.list5.bind('<Button-3>',self.popup)
        self.list5.grid(row=2,column=4)

        y=0
        z=0
        for row in self.cc.execute('SELECT * FROM chapas'):
            self.list1.insert('end',row[0])
            self.list2.insert('end',row[1])
            self.list3.insert('end',row[2])
            self.list4.insert('end',row[3])
            self.list5.insert('end',round(row[4],3))
            y+=row[3]
            z+=(row[3]*row[4])
        self.label6['text']=(f'Quantidade: {int(y)}')
        self.label7['text']=(f'M²: {round(z,3)}')
        y=0
        z=0

        self.br1.config(command=self.yview)
        self.br1.grid(row=2,column=5,sticky=N+S)

        self.br2.config(command=self.xview)
        self.br2.grid(row=3,column=0,sticky=W+E,columnspan=5)

        self.mc = Menu(self, tearoff=0)
        self.mc.add_command(label="Inserir Valores", command=self.inserir)
        self.mc.add_command(label="Excluir", command=self.excluirunit)

        self.bt1 = ttk.Button(self,text='Inserir',command=self.inserir)
        self.bt2 = ttk.Button(self,text='Excluir Tudo',command=self.excluir)
        self.bt3 = ttk.Button(self,text='Salvar',command=self.salvar)
        self.iex=PhotoImage(file='excel.png',master=self)
        self.bt4 = ttk.Button(self,image=self.iex,command=self.dialog)
        self.bt2.grid(row=2,column=6)
        self.bt1.grid(row=3,column=6)
        self.bt3.grid(row=4,column=6)
        self.bt4.grid(row=0,column=6,sticky=E)

    def dialog(self):
        c=0
        j=0
        xl=Tk()
        xl.fileName=filedialog.askopenfilename(filetypes=(("xlsx files", "*.xlsx"),("xls files","*.xls")))
        workbook=xlrd.open_workbook(xl.fileName)
        worksheet=workbook.sheet_by_index(0)
        for i in range(0,worksheet.nrows):
            if worksheet.cell(i,0).value != "" and worksheet.cell(i,1).value != "" and worksheet.cell(i,2).value != "" and worksheet.cell(i,3).value != "":
                self.list1.insert('end',worksheet.cell(i,0).value)
                self.list2.insert('end',round(worksheet.cell(i,1).value,3))
                self.list3.insert('end',round(worksheet.cell(i,2).value,3))
                self.list4.insert('end',worksheet.cell(i,3).value)
                self.list5.insert('end',round(worksheet.cell(i,1).value*worksheet.cell(i,2).value,3))
        for i in range(0,self.list4.size()):
            c+=self.list4.get(i)
            j+=(self.list4.get(i)*self.list5.get(i))
        self.label6['text']=(f'Quantidade: {int(c)}')
        self.label7['text']=(f'M²: {round(j,3)}')
        c=0
        j=0

    def excluirunit(self):
        d=0
        e=0
        x = (self.list1.curselection(),self.list2.curselection(),self.list3.curselection(),self.list4.curselection(),self.list5.curselection())
        for i in x:
            if i != ():
                self.list1.delete(i[0])
                self.list2.delete(i[0])
                self.list3.delete(i[0])
                self.list4.delete(i[0])
                self.list5.delete(i[0])
        for i in range(0,self.list4.size()):
            d+=self.list4.get(i)
            e+=(self.list4.get(i)*self.list5.get(i))
        self.label6['text']=(f'Quantidade: {int(d)}')
        self.label7['text']=(f'M²: {round(e,3)}')
        d=0
        e=0

    def salvar(self):
        self.cc.execute('DELETE FROM chapas')
        self.cchapas.commit()
        for i in range(0,min(self.list1.size(),self.list2.size(),self.list3.size(),self.list4.size(),self.list5.size())):
            self.cc.execute('INSERT INTO chapas (id,comprimento,largura,quantidade,area) VALUES (?,?,?,?,?)',(self.list1.get(i),self.list2.get(i),self.list3.get(i),self.list4.get(i),self.list5.get(i)))
        self.cchapas.commit()

    def excluir(self):
        g=0
        h=0
        if self.list1.size()!=0:

            self.list1.selection_set(0, 'end')
            for i in self.list1.curselection()[::-1]:
                self.list1.delete(i)

            self.list2.selection_set(0, 'end')
            for i in self.list2.curselection()[::-1]:
                self.list2.delete(i)

            self.list3.selection_set(0, 'end')
            for i in self.list3.curselection()[::-1]:
                self.list3.delete(i)

            self.list4.selection_set(0, 'end')
            for i in self.list4.curselection()[::-1]:
                self.list4.delete(i)

            self.list5.selection_set(0, 'end')
            for i in self.list5.curselection()[::-1]:
                self.list5.delete(i)
        for i in range(0,self.list4.size()):
            g+=self.list4.get(i)
            h+=(self.list4.get(i)*self.list5.get(i))
        self.label6['text']=(f'Quantidade: {int(g)}')
        self.label7['text']=(f'M²: {round(h,3)}')
        g=0
        h=0

    def inserir(self):
        self.janelainserir=Tk()
        self.janelainserir.iconbitmap('cadastrarchapas_icon.ico')
        self.janelainserir.title('Inserir Chapas')
        self.janelainserir.geometry('%dx%d+%d+%d' % (410,50,((self.janelainserir.winfo_screenwidth()/2) - (410/2)),((self.janelainserir.winfo_screenheight()/2) - (50/2))))
        self.janelainserir.label1 = Label(self.janelainserir,text='Id',font=('Arial',10))
        self.janelainserir.label2 = Label(self.janelainserir,text='Comprimento',font=('Arial',10))
        self.janelainserir.label3 = Label(self.janelainserir,text='Largura',font=('Arial',10))
        self.janelainserir.label4 = Label(self.janelainserir,text='Quantidade',font=('Arial',10))
        self.janelainserir.label1.grid(row=0,column=0)
        self.janelainserir.label2.grid(row=0,column=1)
        self.janelainserir.label3.grid(row=0,column=2)
        self.janelainserir.label4.grid(row=0,column=3)
        self.janelainserir.cx1 = Entry(self.janelainserir,width=13)
        self.janelainserir.cx2 = Entry(self.janelainserir,width=13)
        self.janelainserir.cx3 = Entry(self.janelainserir,width=13)
        self.janelainserir.cx4 = Entry(self.janelainserir,width=13)
        self.janelainserir.cx1.grid(row=1,column=0)
        self.janelainserir.cx2.grid(row=1,column=1)
        self.janelainserir.cx3.grid(row=1,column=2)
        self.janelainserir.cx4.grid(row=1,column=3)
        self.janelainserir.bt=ttk.Button(self.janelainserir,text='OK',command=self.inserirval)
        self.janelainserir.bt.grid(row=1,column=5)
        self.janelainserir.mainloop()

    def inserirval(self):
        a=0
        b=0
        self.list1.insert('end',self.janelainserir.cx1.get())
        self.list2.insert('end',float(self.janelainserir.cx2.get()))
        self.list3.insert('end',float(self.janelainserir.cx3.get()))
        self.list4.insert('end',float(self.janelainserir.cx4.get()))
        self.list5.insert('end',round(float(self.janelainserir.cx2.get())*float(self.janelainserir.cx3.get()),3))
        self.janelainserir.cx1.delete(0,'end')
        self.janelainserir.cx2.delete(0,'end')
        self.janelainserir.cx3.delete(0,'end')
        self.janelainserir.cx4.delete(0,'end')
        for i in range(0,self.list4.size()):
            a+=self.list4.get(i)
            b+=(self.list4.get(i)*self.list5.get(i))
        self.label6['text']=(f'Quantidade: {int(a)}')
        self.label7['text']=(f'M²: {round(b,3)}')
        a=0
        b=0

    def popup(self,event):
        self.mc.post(self.winfo_pointerx(), self.winfo_pointery())

    def yscroll1(self, *args):
        if self.list1.yview() != self.list2.yview() and self.list1.yview() != self.list3.yview() and self.list1.yview() != self.list4.yview() and self.list1.yview() != self.list5.yview():
            self.list2.yview_moveto(args[0])
            self.list3.yview_moveto(args[0])
            self.list4.yview_moveto(args[0])
            self.list5.yview_moveto(args[0])
        self.br1.set(*args)

    def yscroll2(self, *args):
        if self.list2.yview() != self.list1.yview() and self.list2.yview() != self.list3.yview() and self.list2.yview() != self.list4.yview() and self.list2.yview() != self.list5.yview():
            self.list1.yview_moveto(args[0])
            self.list3.yview_moveto(args[0])
            self.list4.yview_moveto(args[0])
            self.list5.yview_moveto(args[0])
        self.br1.set(*args)

    def yscroll3(self, *args):
        if self.list3.yview() != self.list2.yview() and self.list3.yview() != self.list1.yview() and self.list3.yview() != self.list4.yview() and self.list3.yview() != self.list5.yview():
            self.list1.yview_moveto(args[0])
            self.list2.yview_moveto(args[0])
            self.list4.yview_moveto(args[0])
            self.list5.yview_moveto(args[0])
        self.br1.set(*args)

    def yscroll4(self, *args):
        if self.list4.yview() != self.list2.yview() and self.list4.yview() != self.list3.yview() and self.list4.yview() != self.list1.yview() and self.list4.yview() != self.list5.yview():
            self.list1.yview_moveto(args[0])
            self.list2.yview_moveto(args[0])
            self.list3.yview_moveto(args[0])
            self.list5.yview_moveto(args[0])
        self.br1.set(*args)

    def yscroll5(self, *args):
        if self.list5.yview() != self.list2.yview() and self.list5.yview() != self.list3.yview() and self.list5.yview() != self.list4.yview() and self.list5.yview() != self.list1.yview():
            self.list1.yview_moveto(args[0])
            self.list2.yview_moveto(args[0])
            self.list3.yview_moveto(args[0])
            self.list4.yview_moveto(args[0])
        self.br1.set(*args)

    def yview(self, *args):
        self.list1.yview(*args)
        self.list2.yview(*args)
        self.list3.yview(*args)
        self.list4.yview(*args)
        self.list5.yview(*args)

    def xview(self, *args):
        self.list1.xview(*args)
        self.list2.xview(*args)
        self.list3.xview(*args)
        self.list4.xview(*args)
        self.list5.xview(*args)

if __name__ == "__main__":
    root = ListboxExe()
    root.iconbitmap('cadastrarchapas_icon.ico')
    root.title('Cadastrar Chapas')
    root.geometry('%dx%d+%d+%d' % (575,240,((root.winfo_screenwidth()/2) - (575/2)),((root.winfo_screenheight()/2) - (240/2))))
    root.mainloop()