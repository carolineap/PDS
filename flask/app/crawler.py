import requests
from bs4 import BeautifulSoup
import datetime
import string
import re
import sys
import psycopg2

conn = psycopg2.connect("dbname='cpa' user='postgres' host='localhost' password='1234'")
cur = conn.cursor()

class Dados():
	def __init__(self, mercadoria, data, vencimento, ajusteAtual, ajusteAnterior, contratosAbertos, volume, abertura, minimo, maximo):
		self.mercadoria = mercadoria
		self.data = data
		self.vencimento = vencimento
		self.ajusteAtual = ajusteAtual.replace('.', '').replace(',', '.')
		self.ajusteAnterior = ajusteAnterior.replace('.', '').replace(',', '.')
		self.contratosAbertos = contratosAbertos.replace('.', '').replace(',', '.')
		self.volume = volume.replace('.', '').replace(',', '.')
		self.abertura = abertura.replace('.', '').replace(',', '.')
		self.minimo = minimo.replace('.', '').replace(',', '.')
		self.maximo = maximo.replace('.', '').replace(',', '.')

class DadosFuturo():
	def __init__(self, contratosAbertos, volume, abertura, minimo, maximo):
		self.contratosAbertos = contratosAbertos
		self.volume = volume
		self.abertura = abertura
		self.minimo = minimo
		self.maximo = maximo

class DadosAjuste():
	def __init__(self, mercadoria, data, vencimento, ajusteAtual, ajusteAnterior):
		self.mercadoria = mercadoria
		self.data = data
		self.vencimento = vencimento
		self.ajusteAtual = ajusteAtual
		self.ajusteAnterior = ajusteAnterior

def requestAjuste(data):
	rAjuste = requests.post('http://www2.bmf.com.br/pages/portal/bmfbovespa/lumis/lum-ajustes-do-pregao-ptBR.asp', data = {'dData1': data})
	soupAjuste = BeautifulSoup(rAjuste.text, 'html.parser')
	table = soupAjuste.find('table', attrs={'id':'tblDadosAjustes'})
	table_body = table.find('tbody')

	return table_body
	
def parseAjuste(data):
	try:
		table = requestAjuste(data)
	except:
		return -1;
	ajuste = []
	tr = table.find_all('tr')
	for rows in tr:
		td = rows.find_all('td')
		row = [i.text for i in td]
		if (len(row[0])):
			mercadoria = row[0]
		vencimento = row[1]
		precoAnterior = row[2]
		precoAtual = row[3]
		if mercadoria[:3] == 'BGI' or mercadoria[:3] == 'SFI' or mercadoria[:3] == 'ICF' or mercadoria[:3] == 'CCM':			
			ajuste.append(DadosAjuste(mercadoria[:3], data, vencimento, precoAtual, precoAnterior))

	return ajuste

def requestFuturo(data, mercadoria):

	rFuturo = requests.post('http://www2.bmf.com.br/pages/portal/bmfbovespa/boletim1/SistemaPregao1.asp', data = {'txtData': data, 'cboMercadoria': mercadoria})
	soupFuturo = BeautifulSoup(rFuturo.text, 'html.parser')
	table = soupFuturo.findAll('script', attrs={'language':'JavaScript'})
	matchObj = re.findall(r'>([0-9]|[0-9][0-9,.]+|[A-Z]\d\d )<', str(table[6]))

	return matchObj

def parseFuturo(table, vencimento):

	try:
		i = table.index(vencimento)
		contratosAbertos = table[i + 1]
		volume = table[i + 5]
		abertura = table[i + 6]
		minimo = table[i + 7]
		maximo = table[i + 8]
	except:
		print("vencimento nao encontrado!")

	return DadosFuturo(contratosAbertos, volume, abertura, minimo, maximo)

def update(start, end):	

	step = datetime.timedelta(days=1)
	dados = []


	start = datetime.datetime.strftime(start, '%Y-%m-%d')
	end = datetime.datetime.strftime(end, '%Y-%m-%d')
	start = datetime.datetime.strptime(start, '%Y-%m-%d')
	end = datetime.datetime.strptime(end, '%Y-%m-%d')

	start += step
	max_date = start
	while start <= end:

		dadosAjuste = parseAjuste(str(start.day).zfill(2) + "/" + str(start.month).zfill(2) + "/" + str(start.year))

		if (dadosAjuste != -1):

			dataFormat = str(start.year).zfill(2) + "-" + str(start.month).zfill(2) + "-" + str(start.day).zfill(2) 

			print("Starting request day " + dataFormat) 

			mercadoria = dadosAjuste[0].mercadoria
			data = dadosAjuste[0].data
			
			table = requestFuturo(data, mercadoria)

			for d in dadosAjuste:	

				if (d.mercadoria != mercadoria):
					mercadoria = d.mercadoria
					table = requestFuturo(d.data, mercadoria)

				f = parseFuturo(table, d.vencimento) 
				dados.append(Dados(d.mercadoria, dataFormat, d.vencimento.strip(' '), d.ajusteAtual, d.ajusteAnterior, f.contratosAbertos, f.volume, f.abertura, f.minimo, f.maximo))

				print(d.data)

				if datetime.datetime.strptime(d.data, '%d/%m/%Y') > max_date:
					max_date = datetime.datetime.strptime(d.data, '%d/%m/%Y')

				print(datetime.datetime.strptime(d.data, '%d/%m/%Y'))

		start += step
	
	for d in dados:
		if (d.mercadoria == 'BGI'):
			cur.execute("INSERT INTO boi VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (d.data, d.mercadoria, d.vencimento, d.volume, d.contratosAbertos, d.abertura, d.minimo, d.maximo, d.ajusteAtual, d.ajusteAnterior)) 
		elif (d.mercadoria == 'ICF'):
			cur.execute("INSERT INTO cafe VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (d.data, d.mercadoria, d.vencimento, d.volume, d.contratosAbertos, d.abertura, d.minimo, d.maximo, d.ajusteAtual, d.ajusteAnterior)) 
		elif d.mercadoria == 'CCM':
			cur.execute("INSERT INTO milho VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (d.data, d.mercadoria, d.vencimento, d.volume, d.contratosAbertos, d.abertura, d.minimo, d.maximo, d.ajusteAtual, d.ajusteAnterior)) 
		else:			
			cur.execute("INSERT INTO soja VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (d.data, d.mercadoria, d.vencimento, d.volume, d.contratosAbertos, d.abertura, d.minimo, d.maximo, d.ajusteAtual, d.ajusteAnterior)) 
	
	if len(dados):
		max_date = str(max_date.day).zfill(2) + "/" + str(max_date.month).zfill(2) + "/" + str(max_date.year)
		cur.execute("UPDATE info_geral SET ultima_atualizacao = %s WHERE cpf='00000000000';", (max_date, ))
		conn.commit()
