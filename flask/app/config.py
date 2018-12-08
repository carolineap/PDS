from flask import Flask, redirect, url_for, render_template, session
from flask import Response
import psycopg2
from flask import request
from datetime import datetime
from datetime import timedelta
import string

def configMain():
	if (request.method == 'POST'):
		try:
			table = request.form.get('commoditie')
			data1 = request.form.get('data1')
			data2 = request.form.get('data2')

			if table == 'all':
				pass
			elif table == 'B':
				cur.execute("DELETE FROM boi WHERE data_ajuste >= '%s' AND data_ajuste <= '%s';", (data1,data2))

			elif table == 'C':
				pass
			elif table == 'M':
				pass
			elif table == 'S':
				pass
			else:
				pass	
				
		except:
			pass	
	return		
			