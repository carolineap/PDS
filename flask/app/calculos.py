import pandas as pd
import numpy as np
from datetime import datetime
import string


def makeDF(objList):

	df = pd.DataFrame.from_records([s.to_dict() for s in objList])

	return df

def media_movel(df, w):

	df = df[['ajuste_atual','data']]
	df = df.set_index('data')
	df = df.rolling(window=int(w)).mean() 
	df = df.reset_index()
	df['data'] = df['data'].dt.strftime('%d/%m/%Y') 
	df = df.replace(np.NaN, 'N/A')
	return df


def media_diaria(df):


	df = df.mean() 

	#print(df['ajuste_atual'].tolist())

	return df


def media_semanal(df):

	df = df.set_index('data').resample('W-SAT').mean() 
	df = df.reset_index()
	df['data'] = df['data'].dt.strftime('%d/%m/%Y') 

	df = df.dropna()


	return df

def media_quinzenal(df):

	df = df.set_index('data').resample('2W-SAT').mean() 
	df = df.reset_index()
	
	df['data'] = df['data'].dt.strftime('%d/%m/%Y') 

	df = df.dropna()


	return df

def media_mensal(df):
	
	df = df.set_index('data').resample('M').mean() 
	df = df.reset_index()
	df['data'] = df['data'].dt.strftime('%b')
	df = df.dropna()

	return df

def desvio_padrao(df):

	df = df.std() 

	return df

def ln(df):

	df = df[['ajuste_atual','data']]
	df = df.set_index('data')
	df['retorno_simples'] = df.diff()
	df['ln'] = np.log(df['ajuste_atual'])
	df['retorno_continuo'] = df['ln'].diff()
	df = df.reset_index()
	df['data'] = df['data'].dt.strftime('%d/%m/%Y') 
	df = df.replace(np.NaN, 'N/A')


	return df
	#print(df['ajuste_atual'].values)
	#print(df['ajuste_atual'].mean())

	#print(df['ln'].mean())

	#print(df)

	
