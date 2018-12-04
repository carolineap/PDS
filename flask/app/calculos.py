import pandas as pd
import numpy as np
from datetime import datetime
import string


def makeDF(objList):

	df = pd.DataFrame.from_records([s.to_dict() for s in objList])

	return df

def media_movel(data, w):

	
	data = {'m': data}

	df = pd.DataFrame(data)
	df = df.rolling(window=w).mean()

	df = df['m'].values.tolist()

	return df


def media_diaria(df):

	df = df.set_index('data').resample('D').mean().round(2)
	df = df.reset_index()
	df['data'] = df['data'].dt.strftime('%d/%m/%Y')

	df = df.dropna()

	return df


def media_semanal(df):

	df = df.set_index('data').resample('W-SAT').mean().round(2)
	df = df.reset_index()
	df['data'] = df['data'].dt.strftime('%d/%m/%Y') 

	df = df.dropna()

	return df

def media_quinzenal(df):

	df = df.set_index('data').resample('2W-SAT').mean().round(2)
	df = df.reset_index()
	df['data'] = df['data'].dt.strftime('%d/%m/%Y') 

	df = df.dropna()

	return df

def media_mensal(df):
	
	df = df.set_index('data').resample('M').mean().round(2)
	df = df.reset_index()
	df['data'] = df['data'].dt.strftime('%b')
	df = df.dropna()

	return df

def desvio_padrao(df):

	df['ajuste_atual'] = df['ajuste_atual'].std()
	df['ajuste_anterior'] = df['ajuste_anterior'].std() 
	df['variacao'] =  df['variacao'].std() 
	df['contratos'] =  df['contratos'].std()
	df['volume'] =  df['volume'].std()
	df['preco_abertura'] = df['preco_abertura'].std()
	df['preco_min'] = df['preco_min'].std()
	df['preco_max'] =  df['preco_max'].std()
	df['data'] = df['data'].dt.strftime('%d/%m/%Y') 

	return df

def ln(data):

	df = np.log(data)

	return df

def retorno_simples(data):

	data = ln(data)

	data = {'m': data}

	df = pd.DataFrame(data)
	df = df.rolling(window=2).std()

	df = df['m'].values.tolist()

	return df


def retorno_continuo(data):

	data = ln(data)

	data = {'m': data}

	df = pd.DataFrame(data)
	df = df.rolling(window=2).mean()

	df = df['m'].values.tolist()

	return df




def volatilidade(data):

	data = retorno_simples(data)

	data = {'m': data}

	df = pd.DataFrame(data)
	
	df = df.diff()

	df = df['m'].values.tolist()

	return df
	
