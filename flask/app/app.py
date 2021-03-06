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
import config

app = Flask(__name__)
app.secret_key = 'some_secret'

conn = psycopg2.connect("dbname='cpa' user='postgres' host='localhost' password='1234'")
cur = conn.cursor()


class Calculo:			
	def __init__(self, data, ajuste_anterior, ajuste_atual, variacao, contratos, volume, preco_abertura, preco_min, preco_max):
		self.data = data
		self.ajuste_anterior = ajuste_anterior
		self.ajuste_atual = ajuste_atual
		self.variacao = variacao
		self.contratos = contratos
		self.volume = volume
		self.preco_abertura = preco_abertura
		self.preco_min = preco_min
		self.preco_max = preco_max

class Calculoln:			
	def __init__(self, data, ajuste_atual, retorno_simples, ln, retorno_continuo, risco, volatilidade, media_simples, media_continua):
		self.data = data
		self.ajuste_atual = ajuste_atual
		self.retorno_simples = retorno_simples
		self.ln = ln
		self.retorno_continuo = retorno_continuo
		self.risco = risco
		self.volatilidade = volatilidade
		self.media_simples = media_simples
		self.media_continua = media_continua

	
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
		elif (frequencia == 'M'):
			if (dia and dia == 'P'):
				mes = []
				m = None
				
				for row in r:
					
					data = row[0]
					data = str(data).replace('-', '/')
					data = datetime.strptime(data, '%Y/%m/%d')

					mes.append(row)
					
					if not m or m != data.month:
						m = data.month
						if data.day <= 3:
							result.append(mes[0])
						mes = []
						mes.append(row)
					
			elif (dia and dia == 'U'):

				mes = []
				m = 0
				
				for row in r:
					
					data = row[0]
					data = str(data).replace('-', '/')
					data = datetime.strptime(data, '%Y/%m/%d')

					if m == 0:
						m = data.month
					
					if m != data.month:
						m = data.month
						result.append(mes[len(mes) - 1])
						mes = []

					mes.append(row)

				if data.day >= 28:
					result.append(mes[len(mes) - 1])

			else:
				pass					
		else:
			pass
	
	if not result: 
		result = r

	return result

def mediaDiaria(df):

	media_aa = media_at = media_var = media_cont = media_vol = media_abert = media_min = media_max = []
	if request.form.get('medDia'):
	
		df_mediaDiaria = calc.media_diaria(df)

		if request.form.get('check0'):
			media_at = df_mediaDiaria['ajuste_anterior'].tolist()
		if request.form.get('check1'):
			media_aa = df_mediaDiaria['ajuste_atual'].tolist()
		if request.form.get('check2'):
			media_var = df_mediaDiaria['variacao'].tolist()
		if request.form.get('check3'):
			media_cont = df_mediaDiaria['contratos'].tolist()
		if request.form.get('check4'):
			media_vol = df_mediaDiaria['volume'].tolist()
		if request.form.get('check5'):
			media_abert = df_mediaDiaria['preco_abertura'].tolist()
		if request.form.get('check6'):
			media_min = df_mediaDiaria['preco_min'].tolist()
		if request.form.get('check7'):
			media_max = df_mediaDiaria['preco_max'].tolist()
	else:
		return None
			
			
	return Calculo([], media_at, media_aa, media_var, media_cont, media_vol, media_abert, media_min, media_max)

def mediaMovel(df):

	media_aa = []

	if request.form.get('movel'):

		if request.form.get('window'):
			
			w = request.form.get('window')
	
			df_mediaMovel = calc.media_movel(df, w)

			media_aa = df_mediaMovel['ajuste_atual'].values.tolist()

			print(media_aa)
	
	else:
		return None
			
			
	return Calculo(df_mediaMovel['data'].values.tolist(), [], media_aa, [], [], [], [], [], [])

def ln(df):
	ajuste_atual = retorno_simples = ln = retorno_continuo = []

	if request.form.get('ln'):

		df_ln = calc.ln(df)
		ajuste_atual = df_ln['ajuste_atual'].values.tolist()
		retorno_simples =  df_ln['retorno_simples'].values.tolist()
		ln =  df_ln['ln'].values.tolist()
		retorno_continuo =  df_ln['retorno_continuo'].values.tolist()
		media_simples =  df_ln['media_simples'].values[0]
		media_continua =  df_ln['media_continua'].values[0]
		risco =  df_ln['risco'].values[0]
		volatilidade =  df_ln['volatilidade'].values[0]

		#print(risco)

	else:
		return None
			
	return Calculoln(df_ln['data'].values.tolist(), ajuste_atual, retorno_simples, ln, retorno_continuo, risco, volatilidade, media_simples, media_continua)

def mediaMensal(df):

	media_aa = media_at = media_var = media_cont = media_vol = media_abert = media_min = media_max = []
	
	if request.form.get('medMes'):
	
		df_mediaMensal = calc.media_mensal(df)

		if request.form.get('check0'):
			media_at = df_mediaMensal['ajuste_anterior'].values.tolist()
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
			
	return Calculo(df_mediaMensal['data'].values.tolist(), media_at, media_aa, media_var, media_cont, media_vol, media_abert, media_min, media_max)

def mediaSemanal(df):

	media_aa = media_at = media_var = media_cont = media_vol = media_abert = media_min = media_max = datas = []
	
	if request.form.get('medSema'):
	
		df_mediaSemanal = calc.media_semanal(df)

		if request.form.get('check0'):
			media_at = df_mediaSemanal['ajuste_anterior'].values.tolist()
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
			
	return Calculo(datas, media_at, media_aa, media_var, media_cont, media_vol, media_abert, media_min, media_max)

def mediaQuinzenal(df):


	media_aa = media_at = media_var = media_cont = media_vol = media_abert = media_min = media_max = datas = []

	if request.form.get('medQuinze'):
	

		df_mediaQuinzenal= calc.media_quinzenal(df)

		if request.form.get('check0'):
			media_at = df_mediaQuinzenal['ajuste_anterior'].values.tolist()
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
			
	return Calculo(datas, media_at, media_aa, media_var, media_cont, media_vol, media_abert, media_min, media_max)

def desvioPadrao(df):

	desvio_aa = desvio_at = desvio_var = desvio_cont = desvio_vol = desvio_abert = desvio_min = desvio_max = []
	
	
	if request.form.get('desvio'):

		df_desvioPadrao = calc.desvio_padrao(df)

		if request.form.get('check0'):
			desvio_at = df_desvioPadrao['ajuste_anterior'].tolist()
		if request.form.get('check1'):
			desvio_aa = df_desvioPadrao['ajuste_atual'].tolist()
		if request.form.get('check2'):
			desvio_var = df_desvioPadrao['variacao'].tolist()
		if request.form.get('check3'):
			desvio_cont = df_desvioPadrao['contratos'].tolist()
		if request.form.get('check4'):
			desvio_vol = df_desvioPadrao['volume'].tolist()
		if request.form.get('check5'):
			desvio_abert = df_desvioPadrao['preco_abertura'].tolist()
		if request.form.get('check6'):
			desvio_min = df_desvioPadrao['preco_min'].tolist()
		if request.form.get('check7'):
			desvio_max = df_desvioPadrao['preco_max'].tolist()
			
	else:
		return None
			


	return Calculo([], desvio_at, desvio_aa, desvio_var, desvio_cont, desvio_vol, desvio_abert, desvio_min, desvio_max)

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
			table = request.form.get('table')

			if (table == 'milho'):
				cur.execute("SELECT DISTINCT SUBSTRING(vencimento, 2, 3) FROM milho WHERE data_ajuste >= %s AND data_ajuste <= %s ORDER BY SUBSTRING(vencimento, 2, 3);", (data1, data2))
			elif (table == 'boi'):
				cur.execute("SELECT DISTINCT SUBSTRING(vencimento, 2, 3) FROM boi WHERE data_ajuste >= %s AND data_ajuste <= %s ORDER BY SUBSTRING(vencimento, 2, 3);", (data1, data2))
			elif (table == 'cafe'):
				cur.execute("SELECT DISTINCT SUBSTRING(vencimento, 2, 3) FROM cafe WHERE data_ajuste >= %s AND data_ajuste <= %s ORDER BY SUBSTRING(vencimento, 2, 3);", (data1, data2))
			elif (table == 'soja'):
				cur.execute("SELECT DISTINCT SUBSTRING(vencimento, 2, 3) FROM soja WHERE data_ajuste >= %s AND data_ajuste <= %s ORDER BY SUBSTRING(vencimento, 2, 3);", (data1, data2))
			else:
				pass


			rows = cur.fetchall()

			for row in rows:
				anos.append(row[0])
				
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
			vencimento = request.form.get('vencimento')
			ano = request.form.get('ano')

			vencimento = vencimento + ano

			if (len(data2) == 0): data2 = data1

			if (table == 'milho'):
				cur.execute("SELECT * FROM milho WHERE data_ajuste >= %s AND data_ajuste <= %s AND vencimento = %s ORDER BY data_ajuste, vencimento", (data1,data2, vencimento))
				tamanhoContrato = 450
			elif (table == 'boi'):
				cur.execute("SELECT * FROM boi WHERE data_ajuste >= %s AND data_ajuste <= %s  AND vencimento = %s ORDER BY data_ajuste, vencimento", (data1,data2, vencimento))
				tamanhoContrato = 330		
			elif (table == 'cafe'):
				cur.execute("SELECT * FROM cafe WHERE data_ajuste >= %s AND data_ajuste <= %s  AND vencimento = %s ORDER BY data_ajuste, vencimento", (data1,data2, vencimento))	
				tamanhoContrato = 450		
			elif (table == 'soja'):
				cur.execute("SELECT * FROM soja WHERE data_ajuste >= %s AND data_ajuste <= %s  AND vencimento = %s ORDER BY data_ajuste, vencimento", (data1,data2, vencimento))
				tamanhoContrato = 100			
			else:
				pass

			rows = cur.fetchall()
			commodities = []
			response = ''
			for row in rows:
				commodities.append(Commodity(row[0], row[1], row[2], row[9], row[8], row[5], row[6], row[7], row[4], row[3], tamanhoContrato))	
			
			df = calc.makeDF(commodities)	

			if df.empty:
				return json.dumps({'fail': True})

			data = {
				'media_diaria': mediaDiaria(df),
				'media_mensal': mediaMensal(df),
				'media_semanal': mediaSemanal(df),
				'media_quinzenal': mediaQuinzenal(df),
				'desvio_padrao': desvioPadrao(df),
				'media_movel': mediaMovel(df),
				'ln': ln(df)			
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

@app.route('/rolagem.html', methods=['GET', 'POST'])
def rolagem():
	return render_template('rolagem.html')

@app.route('/mediaMovel.html', methods=['GET', 'POST'])
def graphMediaMovel():
	return render_template('mediaMovel.html')

@app.route('/requestRolagem', methods=['GET', 'POST'])
def requestRolagem():

	vencimento = None

	if (request.method == 'POST'):
		
		try:
			
			table = request.form.get('commoditie')
			data1 = request.form.get('data1')
			data2 = request.form.get('data2')

			if (len(data2) == 0): data2 = data1
			

			if (table == 'milho'):
				cur.execute("SELECT * FROM rolagem_milho(%s, %s) ORDER BY data_ajuste", (data1, data2))
				tamanhoContrato = 450
			elif (table == 'boi'):
				cur.execute("SELECT * FROM rolagem_boi(%s, %s) ORDER BY data_ajuste", (data1, data2))
				tamanhoContrato = 330
			elif (table == 'cafe'):
				cur.execute("SELECT * FROM rolagem_cafe(%s, %s) ORDER BY data_ajuste", (data1, data2))
				tamanhoContrato = 450
			elif (table == 'soja'):
				cur.execute("SELECT * FROM rolagem_soja(%s, %s) ORDER BY data_ajuste", (data1, data2))
				tamanhoContrato = 100
			else:
				pass

			rows = cur.fetchall()
			commodities = []

			response = ''

			for row in rows:
				commodities.append(Commodity(row[0], row[1], row[2], row[9], row[8], row[5], row[6], row[7], row[4], row[3], tamanhoContrato))	

			
			return(json.dumps(commodities, default=lambda o: o.__dict__, indent=4, separators=(',',':')))

		except:
			pass

	return render_template('/home.html')

@app.route('/painel.html', methods=['GET', 'POST'])
def painel():
	
	try:
		if (request.method == 'POST'):
			table = request.form.get('commoditie')
			data1 = request.form.get('data1')
			data2 = request.form.get('data2')
			
			if data1 and data2 and table:
				row = config.configMain()
				return render_template('painel.html', row=row)
			
			atualizacao = request.form.get('atualizacao')
			if atualizacao == 'T':
				config.updateData()

			backup = request.form.get('backup')
			if backup == 'T':
				foi = config.backup()
				return render_template('painel.html', foi=foi)

	except:
		pass

	return render_template('painel.html')

if __name__ == '__main__':
  app.run(debug=True, threaded=True)

 