from flask import Flask, redirect, url_for, render_template, session
from flask import Response
import psycopg2
from flask import request
from datetime import datetime
from datetime import timedelta
import string
import json
import calculos as calc
import pandas as pd

app = Flask(__name__)
app.secret_key = 'some_secret'

conn = psycopg2.connect("dbname='cpa' user='postgres' host='localhost' password='1234'")
cur = conn.cursor()


class Calculo:			
	def __init__(self, data, ajuste_atual, variacao, contratos, volume, preco_abertura, preco_min, preco_max):
		self.data = data
		self.ajuste_atual = ajuste_atual
		self.variacao = variacao
		self.contratos = contratos
		self.volume = volume
		self.preco_abertura = preco_abertura
		self.preco_min = preco_min
		self.preco_max = preco_max
		

class Commodity:
	def __init__(self, data, codigo, vencimento, ajuste_anterior, ajuste_atual, preco_abertura, preco_min, preco_max, contratos, volume, tamanhoContrato):
		self.codigo = str(codigo)
		self.vencimento = str(vencimento)
		data = str(data).replace('-', '/')
		data = datetime.strptime(data, '%Y/%m/%d')
		self.data = str(data.day).zfill(2) + "/" + str(data.month).zfill(2) + "/" + str(data.year)
		self.ajuste_anterior = float(ajuste_anterior)
		self.ajuste_atual = float(ajuste_atual)
		self.preco_abertura = float(preco_abertura)
		self.preco_min = float(preco_min)
		self.preco_max = float(preco_max)
		self.variacao = self.ajuste_atual - self.ajuste_anterior
		self.valor_contrato = abs(self.variacao) * tamanhoContrato
		self.contratos = contratos
		self.volume = str("{:,}".format(int(volume))).replace(',', '.')

	def to_dict(self):
		return {
			'data': datetime.strptime(self.data, '%d/%m/%Y'),
            'ajuste_atual': self.ajuste_atual,
            'ajuste_anterior': self.ajuste_anterior,
            'variacao': self.variacao,
            'contratos': self.contratos,
            'volume': int(self.volume.replace('.', '')),
            'preco_abertura': self.preco_abertura,
            'preco_min': self.preco_min,
            'preco_max': self.preco_max
        }

def filtro(rows, vencimento, frequencia, dia, ano):

	r = []
	if vencimento != 'all':
		for row in rows:
			if ano != 'all':
				if row[2][0] == vencimento and row[2][1:] == ano:
					r.append(row)
			else:
				if row[2][0] == vencimento:
					r.append(row)
	elif ano != 'all':
		for row in rows:
			if row[2][1:] == ano:
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

def mediaDiaria(df):

	media_aa = media_var = media_cont = media_vol = media_abert = media_min = media_max = []
	
	if request.form.get('medDia'):
	
	 	df_mediaDiaria = calc.media_diaria(df)

	 	if request.form.get('check1'):
			media_aa = df_mediaDiaria['ajuste_atual'].values.tolist()
		if request.form.get('check2'):
			media_var = df_mediaDiaria['variacao'].values.tolist()
		if request.form.get('check3'):
			media_cont = df_mediaDiaria['contratos'].values.tolist()
		if request.form.get('check4'):
			media_vol = df_mediaDiaria['volume'].values.tolist()
		if request.form.get('check5'):
			media_abert = df_mediaDiaria['preco_abertura'].values.tolist()
		if request.form.get('check6'):
			media_min = df_mediaDiaria['preco_min'].values.tolist()
		if request.form.get('check7'):
			media_max = df_mediaDiaria['preco_max'].values.tolist()
			
	else:
	 	return None
			
	return Calculo(df_mediaDiaria['data'].values.tolist(), media_aa, media_var, media_cont, media_vol, media_abert, media_min, media_max)

def mediaMensal(df):

	media_aa = media_var = media_cont = media_vol = media_abert = media_min = media_max = []
	
	if request.form.get('medMes'):
	
	 	df_mediaMensal = calc.media_mensal(df)

	 	if request.form.get('check1'):
			media_aa = df_mediaMensal['ajuste_atual'].values.tolist()
		if request.form.get('check2'):
			media_var = df_mediaMensal['variacao'].values.tolist()
		if request.form.get('check3'):
			media_cont = df_mediaMensal['contratos'].values.tolist()
		if request.form.get('check4'):
			media_vol = df_mediaMensal['volume'].values.tolist()
		if request.form.get('check5'):
			media_abert = df_mediaMensal['preco_abertura'].values.tolist()
		if request.form.get('check6'):
			media_min = df_mediaMensal['preco_min'].values.tolist()
		if request.form.get('check7'):
			media_max = df_mediaMensal['preco_max'].values.tolist()
			
	else:
	 	return None
			
	return Calculo(df_mediaMensal['data'].values.tolist(), media_aa, media_var, media_cont, media_vol, media_abert, media_min, media_max)

def mediaSemanal(df):

	media_aa = media_var = media_cont = media_vol = media_abert = media_min = media_max = datas = []
	
	if request.form.get('medSema'):
	
	 	df_mediaSemanal = calc.media_semanal(df)

	 	if request.form.get('check1'):
			media_aa = df_mediaSemanal['ajuste_atual'].values.tolist()
		if request.form.get('check2'):
			media_var = df_mediaSemanal['variacao'].values.tolist()
		if request.form.get('check3'):
			media_cont = df_mediaSemanal['contratos'].values.tolist()
		if request.form.get('check4'):
			media_vol = df_mediaSemanal['volume'].values.tolist()
		if request.form.get('check5'):
			media_abert = df_mediaSemanal['preco_abertura'].values.tolist()
		if request.form.get('check6'):
			media_min = df_mediaSemanal['preco_min'].values.tolist()
		if request.form.get('check7'):
			media_max = df_mediaSemanal['preco_max'].values.tolist()

		datas_iniciais = []
		datas_finais = df_mediaSemanal['data'].values.tolist()


		for d in datas_finais:
			data = datetime.strptime(d, '%d/%m/%Y')
			data = data - timedelta(days=6)		
			data = str(data.day).zfill(2) + "/" + str(data.month).zfill(2) + "/" + str(data.year)
			datas_iniciais.append(data)

		i = 0
		while i < len(datas_iniciais):
			d = str(datas_iniciais[i]) + " - " + str(datas_finais[i])
			datas.append(d)
			i += 1

	else:
	 	return None
			
	return Calculo(datas, media_aa, media_var, media_cont, media_vol, media_abert, media_min, media_max)

def mediaQuinzenal(df):


	media_aa = media_var = media_cont = media_vol = media_abert = media_min = media_max = datas = []

	if request.form.get('medQuinze'):
	

	 	df_mediaQuinzenal= calc.media_quinzenal(df)

	 	if request.form.get('check1'):
			media_aa = df_mediaQuinzenal['ajuste_atual'].values.tolist()
		if request.form.get('check2'):
			media_var = df_mediaQuinzenal['variacao'].values.tolist()
		if request.form.get('check3'):
			media_cont = df_mediaQuinzenal['contratos'].values.tolist()
		if request.form.get('check4'):
			media_vol = df_mediaQuinzenal['volume'].values.tolist()
		if request.form.get('check5'):
			media_abert = df_mediaQuinzenal['preco_abertura'].values.tolist()
		if request.form.get('check6'):
			media_min = df_mediaQuinzenal['preco_min'].values.tolist()
		if request.form.get('check7'):
			media_max = df_mediaQuinzenal['preco_max'].values.tolist()

		datas_iniciais = []
		datas_finais = df_mediaQuinzenal['data'].values.tolist()


		for d in datas_finais:
			data = datetime.strptime(d, '%d/%m/%Y')
			data = data - timedelta(days=13)		
			data = str(data.day).zfill(2) + "/" + str(data.month).zfill(2) + "/" + str(data.year)
			datas_iniciais.append(data)

		i = 0
		while i < len(datas_iniciais):
			d = str(datas_iniciais[i]) + " - " + str(datas_finais[i])
			datas.append(d)
			i += 1

	else:
	 	return None
			
	return Calculo(datas, media_aa, media_var, media_cont, media_vol, media_abert, media_min, media_max)

def desvioPadrao(df):

	desvio_aa = desvio_var = desvio_cont = desvio_vol = desvio_abert = desvio_min = desvio_max = []
	
	
	if request.form.get('desvio'):

		df_desvioPadrao = calc.desvio_padrao(df)

	 	if request.form.get('check1'):
			desvio_aa = df_desvioPadrao['ajuste_atual'].values.tolist()
		if request.form.get('check2'):
			desvio_var = df_desvioPadrao['variacao'].values.tolist()
		if request.form.get('check3'):
			desvio_cont = df_desvioPadrao['contratos'].values.tolist()
		if request.form.get('check4'):
			desvio_vol = df_desvioPadrao['volume'].values.tolist()
		if request.form.get('check5'):
			desvio_abert = df_desvioPadrao['preco_abertura'].values.tolist()
		if request.form.get('check6'):
			desvio_min = df_desvioPadrao['preco_min'].values.tolist()
		if request.form.get('check7'):
			desvio_max = df_desvioPadrao['preco_max'].values.tolist()
			
	else:
		return None
			


	return Calculo(df_desvioPadrao['data'].values.tolist(), desvio_aa, desvio_var, desvio_cont, desvio_vol, desvio_abert, desvio_min, desvio_max)

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
			ano = request.form.get('ano')

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
			rows = filtro(rows, vencimento, frequencia, dia, ano)
			response = ''
			data = []
			for row in rows:
				data.append(Commodity(row[0], row[1], row[2], row[9], row[8], row[5], row[6], row[7], row[4], row[3], tamanhoContrato))	

			return json.dumps(data, default=lambda o: o.__dict__, indent=4, separators=(',',':'))

		except:
			pass

	return render_template('/home.html')

@app.route('/requestSelect', methods=['GET', 'POST'])
def requestSelect():

	if (request.method == 'POST'):
		try:

			anos = []
			
			data1 = request.form.get('data1')
			data2 = request.form.get('data2')

			if (len(data2) == 0): data2 = data1

			ano1 = data1[2:4]
			ano2 = data2[2:4]			

			ano1 = int(ano1) 
			ano2 = int(ano2)

			if ano1 == ano2:
				anos.append(ano1)
				anos.append(ano1 + 1)
			else:
				while ano1 <= ano2 + 1:
					anos.append(ano1)
					ano1 = ano1 + 1


				
			return json.dumps(anos)
		except:
			pass

	return render_template('/home.html')	


@app.route('/requestAnalytics', methods=['GET', 'POST'])
def requestAnalytics():
	
	if (request.method == 'POST'):
		try:
			
			table = request.form.get('commoditie')
			data1 = request.form.get('data1')
			data2 = request.form.get('data2')
			if (len(data2) == 0): data2 = data1

			if (table == 'M'):
				cur.execute("SELECT * FROM milho WHERE data_ajuste >= %s AND data_ajuste <= %s ORDER BY data_ajuste, vencimento", (data1,data2))
				tamanhoContrato = 450
			elif (table == 'B'):
				cur.execute("SELECT * FROM boi WHERE data_ajuste >= %s AND data_ajuste <= %s ORDER BY data_ajuste, vencimento", (data1,data2))
				tamanhoContrato = 330		
			elif (table == 'C'):
				cur.execute("SELECT * FROM cafe WHERE data_ajuste >= %s AND data_ajuste <= %s ORDER BY data_ajuste, vencimento", (data1,data2))	
				tamanhoContrato = 450		
			elif (table == 'S'):
				cur.execute("SELECT * FROM soja WHERE data_ajuste >= %s AND data_ajuste <= %s ORDER BY data_ajuste, vencimento", (data1,data2))
				tamanhoContrato = 100			
			else:
				pass

			rows = cur.fetchall()
			commodities = []

			for row in rows:
				commodities.append(Commodity(row[0], row[1], row[2], row[9], row[8], row[5], row[6], row[7], row[4], row[3], tamanhoContrato))	
			
			df = calc.makeDF(commodities)	

			data = {
				'media_diaria': mediaDiaria(df),
				'media_mensal': mediaMensal(df),
				'media_semanal': mediaSemanal(df),
				'media_quinzenal': mediaQuinzenal(df),
				'desvio_padrao': desvioPadrao(df)
				# ''
			}


			return(json.dumps(data, default=lambda o: o.__dict__, indent=4, separators=(',',':')))

			#return render_template('/analytics.html')

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


@app.route('/graph.html', methods=['GET', 'POST'])
def graph():

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