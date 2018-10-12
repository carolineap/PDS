import requests
from bs4 import BeautifulSoup
import datetime
import string
import re

class Dados():
	def __init__(self, mercadoria, data, vencimento, ajusteAtual, ajusteAnterior, contratosAbertos, volume, abertura, fechamento, minimo, maximo):
		self.mercadoria = mercadoria
		self.data = data
		self.vencimento = vencimento
		self.ajusteAtual = ajusteAtual
		self.ajusteAnterior = ajusteAnterior
		self.contratosAbertos = contratosAbertos
		self.volume = volume
		self.abertura = abertura
		self.fechamento = fechamento
		self.minimo = minimo
		self.maximo = maximo

class DadosFuturo():
	def __init__(self, contratosAbertos, volume, abertura, fechamento, minimo, maximo):
		self.contratosAbertos = contratosAbertos
		self.volume = volume
		self.abertura = abertura
		self.fechamento = fechamento
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
	table = requestAjuste(data)
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
		fechamento = table[i + 10]
		minimo = table[i + 7]
		maximo = table[i + 8]
	except:
		print("vencimento nao encontrado!")

	return DadosFuturo(contratosAbertos, volume, abertura, fechamento, minimo, maximo)

def main():	

	start = datetime.datetime.strptime("2018-10-11", '%Y-%m-%d')
	end = datetime.datetime.strptime("2018-10-11", '%Y-%m-%d')
	step = datetime.timedelta(days=1)

	dados = []

	while start <= end:

		dadosAjuste = parseAjuste(str(start.day).zfill(2) + "/" + str(start.month).zfill(2) + "/" + str(start.year))

		mercadoria = dadosAjuste[0].mercadoria
		data = dadosAjuste[0].data
		
		table = requestFuturo(data, mercadoria)

		for d in dadosAjuste:	
			if (d.mercadoria != mercadoria):
				mercadoria = d.mercadoria
				table = requestFuturo(d.data, mercadoria)

			f = parseFuturo(table, d.vencimento) 

			dados.append(Dados(d.mercadoria, d.data, d.vencimento.strip(' '), d.ajusteAtual, d.ajusteAnterior, f.contratosAbertos, f.volume, f.abertura, f.fechamento, f.minimo, f.maximo))

		start += step

if __name__ == "__main__": main()