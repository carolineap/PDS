import requests
from bs4 import BeautifulSoup
import datetime

start = datetime.datetime.strptime("2017-08-26", '%Y-%m-%d')
end = datetime.datetime.strptime("2017-09-26", '%Y-%m-%d')
step = datetime.timedelta(days=1)

while start <= end:
	r = requests.post('http://www2.bmf.com.br/pages/portal/bmfbovespa/lumis/lum-ajustes-do-pregao-ptBR.asp', data = {'dData1': str(start.day).zfill(2) + "/" + str(start.month).zfill(2) + "/" + str(start.year)})
	soup = BeautifulSoup(r.text, 'html.parser')

	table = soup.find('table', attrs={'id':'tblDadosAjustes'})
	if (table):
		file = open(str(start.day) + "-" + str(start.month) + "-" + str(start.year) + '.txt', 'w') 
		table_body = table.find('tbody')
		table_rows = table_body.find_all('tr')
		for tr in table_rows:
			td = tr.find_all('td')
			row = [i.text for i in td]
			if (len(row[0])):
				mercadoria = row[0]
			vencimento = row[1]
			precoAnterior = row[2]
			precoAtual = row[3]
			if (mercadoria[:3] == 'BGI' or mercadoria[:3] == 'ACF' or mercadoria[:3] == 'ICF' or mercadoria[:3] == 'CCM'):
				file.write(mercadoria[:3] + '; ' + vencimento[:3] + '; ' + precoAnterior + '; ' + precoAtual + '\n')

		file.close()

	start += step

