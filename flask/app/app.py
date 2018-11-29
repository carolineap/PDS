from flask import Flask, redirect, url_for, render_template, session
from flask import Response
import psycopg2
from flask import request
from datetime import datetime
import string
import json

app = Flask(__name__)
app.secret_key = 'some_secret'

conn = psycopg2.connect("dbname='cpa' user='postgres' host='localhost' password='1234'")
cur = conn.cursor()

class Commodity:
	def __init__(self, vencimento, codigo, data, ajuste_anterior, ajuste_atual, contratos, volume, tamanhoContrato):
		self.codigo = str(codigo)
		self.vencimento = str(vencimento)
		data = str(data).replace('-', '/')
		data = datetime.strptime(data, '%Y/%m/%d')
		self.data = str(data.day).zfill(2) + "/" + str(data.month).zfill(2) + "/" + str(data.year)
		self.ajuste_anterior = float(ajuste_anterior)
		self.ajuste_atual = float(ajuste_atual)
		self.variacao = self.ajuste_atual - self.ajuste_anterior
		self.valor_contrato = abs(self.variacao) * tamanhoContrato
		self.contratos = str(contratos)
		self.volume = volume

def filtro(rows, vencimento, frequencia, dia):

	r = []
	if vencimento != 'all':
		for row in rows:
			if row[2][0] == vencimento:
				r.append(row)
	else:
		r = rows

	result = []
	if frequencia != 'D':
		if (frequencia == 'S'):
			for row in r:
				data = row[0]
				data = str(data).replace('-', '/')
				data = datetime.strptime(data, '%Y/%m/%d')
				diaSemana = data.weekday()
				if int(dia) == diaSemana:
					result.append(row)
	else:
		result = r
			
	# 	elif (frequencia == 'M'):
	# 		if (dia == 'P'):
	# 			primeiro = None
	# 			for row in r:
	# 				data = row[0]
	# 				data = str(data).replace('-', '/')
	# 				data = datetime.strptime(data, '%Y/%m/%d')
	# 				if (data.day == 1):
	# 					primeiro = data.month
	# 					result.append(row)
	# 		elif (dia == 'U'):
	# 			ultimo = None
	# 			for row in r:
	# 				data = row[0]
	# 				data = str(data).replace('-', '/')
	# 				data = datetime.strptime(data, '%Y/%m/%d')
	# 				if (data.day == 30 or 31):
	# 					ultimo = data.month
	# 					result.append(row)
	
	return result

@app.route('/')
@app.route('/home.html')
def home():
	return render_template('home.html')

@app.route('/requestTable', methods=['GET', 'POST'])
def requestTable():
	
	if (request.method == 'POST'):
		try:
			table = request.form.get('commoditie')
			data1 = request.form.get('data1')
			data2 = request.form.get('data2')
			vencimento = request.form.get('vencimento')

			frequencia = request.form.get('frequencia')
			if (frequencia == 'S'):
				dia = request.form.get('diaSemana')
			elif (frequencia == 'M'):
				dia = request.form.get('diaMes')
			else:
				dia = None

			if (len(data2) == 0): data2 = data1

			if (table == 'milho'):
				cur.execute("SELECT * FROM milho WHERE data_ajuste >= %s AND data_ajuste <= %s ORDER BY data_ajuste, vencimento", (data1,data2))
				tamanhoContrato = 450
			elif (table == 'boi'):
				cur.execute("SELECT * FROM boi WHERE data_ajuste >= %s AND data_ajuste <= %s ORDER BY data_ajuste, vencimento", (data1,data2))	
				tamanhoContrato = 330		
			elif (table == 'cafe'):
				cur.execute("SELECT * FROM cafe WHERE data_ajuste >= %s AND data_ajuste <= %s ORDER BY data_ajuste, vencimento", (data1,data2))	
				tamanhoContrato = 450		
			elif (table == 'soja'):
				cur.execute("SELECT * FROM soja WHERE data_ajuste >= %s AND data_ajuste <= %s ORDER BY data_ajuste, vencimento", (data1,data2))
				tamanhoContrato = 100			
			else:
				pass

			
			rows = cur.fetchall()
			rows = filtro(rows, vencimento, frequencia, dia)
			response = ''
			data = []
			for row in rows:
				data.append(Commodity(row[2], row[1], row[0], row[9], row[8], row[4], row[3], tamanhoContrato))	

			return json.dumps(data, default=lambda o: o.__dict__, indent=4, separators=(',',':'))

		except:
			pass

	return render_template('/home.html')

@app.route('/milho.html')
def milho():
	return render_template('milho.html')

@app.route('/boi.html', methods=['GET', 'POST'])
def boi():
	return render_template('boi.html')

@app.route('/soja.html', methods=['GET', 'POST'])
def soja():
	return render_template('soja.html')

@app.route('/cafe.html', methods=['GET', 'POST'])
def cafe():
	return render_template('cafe.html')

@app.route('/ajusteTable.html', methods = ['POST'])
def ajusteTable():
	return render_template('ajusteTable.html')

@app.route('/commodities.html')
def commodities():
  return render_template('commodities.html')

@app.route('/analytics.html')  
def analytics():
	return render_template('analytics.html')


@app.route('/login.html', methods=['GET', 'POST'])
def login():
	session['logged_in'] = False
	error = None
	if request.method == 'POST':
		if request.form['cpf'] != '000.000.000-00' or request.form['senha'] != '1234':
			error = True
		else:
			session['logged_in'] = True
			return redirect(url_for('home'))
	return render_template('login.html', error=error)

@app.route('/lines.html', methods=['GET', 'POST'])
def lines():

	if (request.method == 'POST'):
		try:
			linhas = request.form.get('linhas')
			if linhas == 'True':
				return render_template('lines.html')
			else:
				velas = request.form.get('velas')
				if velas == 'True':
					return render_template('candle.html')
		except:
			pass
		
	return render_template('home.html')		
	
@app.route('/painel.html', methods=['GET', 'POST'])
def painel():
	return render_template('painel.html')

if __name__ == '__main__':
  app.run(debug=True)