from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, landscape
import os
from reportlab.lib.colors import Color, black, snow


width = 791
height = 611

def gerarpdf(x,r,p,solucao,esp,count,sens):
	x0 = 36
	y0 = 17
	
	p.setFillColorRGB(0.68,0.85,0.9)
	p.rect(x0,y0,count*x[0],count*x[1],stroke=1,fill=1)
	p.setFillColor(black)
	p.setFont('Helvetica',12)
	p.drawString(x0+count*x[0]/2,y0-12,text='{}'.format(round(x[0],3)))
	p.drawString(x0-32,y0+count*x[1]/2,text='{}'.format(round(x[1],3)))
	p.drawString(x0,count*x[1]+30,text=f'Chapa: {x[4]}')

	for j in range(len(solucao[r])): # Strip
		if 'h' in solucao[r][j]:
			a = x0
			for k in range(len(solucao[r][j])-1): # Parts
				p.setFillColor(snow)
				p.rect(x0,y0,solucao[r][j][k][0]*count,solucao[r][j][k][1]*count,stroke=1,fill=1)
				p.setFillColor(black)
				p.drawString(x0+(solucao[r][j][k][0]*count)/2-10,y0+2,text='{}'.format(round(solucao[r][j][k][0],3)))
				p.drawString(x0+2,y0+(solucao[r][j][k][1]*count)/2-5,text='{}'.format(round(solucao[r][j][k][1],3)))
				x0 += (solucao[r][j][k][0]+esp)*count
			y0 += (solucao[r][j][0][1]+esp)*count
			x0 = a
		else:
			b = y0
			for k in range(len(solucao[r][j])-1): # Parts
				p.setFillColor(snow)
				p.rect(x0,y0,solucao[r][j][k][0]*count,solucao[r][j][k][1]*count,stroke=1,fill=1)
				p.setFillColor(black)
				p.drawString(x0+(solucao[r][j][k][0]*count)/2-10,y0+2,text='{}'.format(round(solucao[r][j][k][0],3)))
				p.drawString(x0+2,y0+(solucao[r][j][k][1]*count)/2-5,text='{}'.format(round(solucao[r][j][k][1],3)))
				y0 += (solucao[r][j][k][1]+esp)*count
			x0 += (solucao[r][j][0][0]+esp)*count
			y0 = b
	p.showPage()

def ifgerarpdf(solucao,chapas,r,esp,count,sens):
	p = canvas.Canvas("Plano de Corte.pdf",pagesize=landscape(letter))
	chapas.sort(key=lambda x: x[0]*x[1])
	for i in range(0,min(len(chapas),len(solucao))):
		if solucao != [] and len(chapas) > 1:
			gerarpdf(chapas[r],r,p,solucao,esp,count,sens)
			r+=1
		elif solucao != [] and len(chapas) == 1:
			gerarpdf(chapas[r],r,p,solucao,esp,count,sens)
	p.save()
	os.startfile('Plano de Corte.pdf')
