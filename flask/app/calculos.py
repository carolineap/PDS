import pandas as pd
import numpy as np
from datetime import datetime

def media_movel(data, w):

	
	data = {'m': data}

	df = pd.DataFrame(data)
	df = df.rolling(window=w).mean()

	df = df['m'].values.tolist()

	return df


def media_diaria(data):

	df = np.mean(data)

	return df


def media_semanal(data, dates):

	i = 0
	while (i < len(dates)): 
		dates[i] = datetime.strptime(dates[i], '%d/%m/%Y')
		i += 1

	dates = pd.DataFrame(dates)

	week = dates[0].isocalendar()[1]

	print(week)

	values = []
	means = []

	i = 0
	while(i < len(dates)):
		if dates[i].isocalendar()[1] == week:
			values.append(data[i])
		
		if (dates[i].isocalendar()[1] != week) or (i == (len(dates) - 1)):
			means.append(np.mean(values))
			values = []
			week = dates[i].isocalendar()[1]
			values.append(data[i])

		

		i += 1
	print(means)
	return means

def media_quinzenal(data, dates):

	i = 0
	while (i < len(dates)): 
		dates[i] = datetime.strptime(dates[i], '%d/%m/%Y')
		i += 1

	week = dates[0].isocalendar()[1]
	values = []
	means = []

	cont = 0
	i = 0
	while(i < len(dates)):

		if dates[i].isocalendar()[1] != week:
			cont += 1
			week = dates[i].isocalendar()[1]

		if cont < 2:
			values.append(data[i])
		
			
		if i == (len(dates) - 1) or cont == 2:
			means.append(np.mean(values))
			values = []
			values.append(data[i])
			cont = 0

		# print(dates[i])
		# print(week)
		# print("--------------------")
		
		i += 1

	return means

def meses():
	pass

def semanas():
	pass

def quinzenas():
	pass

def media_mensal(data, datesM):
	
	meses =[]
	dates = []
	i = 0
	while (i < len(datesM)): 
		dates.append(datetime.strptime(datesM[i], '%d/%m/%Y'))
		i += 1

	month = dates[0].month
	values = []
	means = []
	i = 0
	while(i < len(dates)):

		if dates[i].month == month:
			values.append(data[i])
		
		if (dates[i].month != month) or (i == (len(dates) - 1)):
			means.append(np.mean(values))
			meses.append(month)
			values = []
			month = dates[i].month
			values.append(data[i])

		i += 1

	#print(means)

	return {'meses': meses, 'medias': means}

def desvio_padrao(data):

	df = np.std(data)

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
	
