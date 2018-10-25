from flask import Flask, redirect, url_for, render_template
from flask import Response
import psycopg2
from flask import request
from datetime import datetime
import string

app = Flask(__name__)

conn = psycopg2.connect("dbname='cpa' user='postgres' host='localhost' password='1234'")
cur = conn.cursor()


class Commodity:
	def __init__(self, vencimento, codigo, data, ajuste_anterior, ajuste_atual, contratos, volume, tamanhoContrato):
		self.codigo = str(codigo)
		self.vencimento = str(vencimento)
		data = str(data).replace('-', '/')
		data = datetime.strptime(data, '%Y/%m/%d')
		self.data = str(data.day).zfill(2) + "/" + str(data.month).zfill(2) + "/" + str(data.year)
		self.ajuste_anterior = str(ajuste_anterior)
		self.ajuste_atual = str(ajuste_atual)
		self.variacao = ajuste_atual - ajuste_anterior
		self.valor_contrato = abs(self.variacao) * tamanhoContrato
		self.contratos = str(contratos)
		self.volume = str(volume)

@app.route('/home.html')
def home():
  return render_template('home.html')

@app.route('/milho.html', methods=['GET', 'POST'])
def milho():
	if (request.method == 'POST'):
		try:
			data1 = request.form.get('data1')
			data2 = request.form.get('data2')
			cur.execute("SELECT * FROM milho WHERE data_ajuste >= %s AND data_ajuste <= %s ORDER BY data_ajuste, vencimento", (data1,data2))
			rows = cur.fetchall()
			response = ''
			milho = []
			for row in rows:
				milho.append(Commodity(row[2], row[1], row[0], row[9], row[8], row[4], row[3], 450))
			return render_template('milho.html', data=milho)
		except:
			pass
		
	return render_template('milho.html')

@app.route('/boi.html')
def boi():
  return render_template('boi.html')

@app.route('/soja.html')
def soja():
  return render_template('soja.html')

@app.route('/cafe.html')
def cafe():
  return render_template('cafe.html')


@app.route('/commodities.html')
def commodities():
  return render_template('commodities.html')



if __name__ == '__main__':
  app.run(debug=True)

