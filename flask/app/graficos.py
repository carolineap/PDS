from datetime import datetime
import string
import json
import plotly
import plotly.plotly as py
import plotly.graph_objs as go

def candle_stick():

	open_data = [33.0, 33.3, 33.5, 33.0, 34.1]
	high_data = [33.1, 33.3, 33.6, 33.2, 34.8]
	low_data = [32.7, 32.7, 32.8, 32.6, 32.8]
	close_data = [33.0, 32.9, 33.3, 33.1, 33.1]
	dates = [datetime(year=2013, month=10, day=10),
						 datetime(year=2013, month=11, day=10),
						 datetime(year=2013, month=12, day=10),
						 datetime(year=2014, month=1, day=10),
						 datetime(year=2014, month=2, day=10)]
 	
	trace = go.Candlestick(x=dates,
		                       open=open_data,
		                       high=high_data,
		                       low=low_data,
		                       close=close_data)
	graph = [trace]

	graphJSON = json.dumps(graph, cls=plotly.utils.PlotlyJSONEncoder)


	return graphJSON


def lines():

	x = [datetime(year=2013, month=10, day=10),
						 datetime(year=2013, month=11, day=10),
						 datetime(year=2013, month=12, day=10),
						 datetime(year=2014, month=1, day=10),
						 datetime(year=2014, month=2, day=10)]

	trace1 = go.Scatter(
		x = x,
		y = [10, 20, 55, 14, 15],
		mode = 'lines+markers',
		name = 'V18'
	)


	trace2 = go.Scatter(
		x = x,
		y = [2, 30, 40, 50, 60],
		mode = 'lines+markers',
		name = 'F19'
	)


	trace3 = go.Scatter(
		x = x,
		y = [12, 13, 16, 75, 23],
		mode = 'lines+markers',
		name = 'X20'
	)

	graph = [trace1, trace2, trace3]

	graphJSON = json.dumps(graph, cls=plotly.utils.PlotlyJSONEncoder)

	return graphJSON


def points():

	x = [15, 30, 40, 50, 60, 10, 20, 55, 14, 15]
		
	y = [10, 20, 55, 14, 15, 15, 30, 40, 50, 60]				 

	trace = go.Scatter(
		x = x,
		y = y,
		mode = 'markers',
	)

	graph = [trace]

	graphJSON = json.dumps(graph, cls=plotly.utils.PlotlyJSONEncoder)

	return graphJSON




	