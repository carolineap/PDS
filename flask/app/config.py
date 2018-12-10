from flask import Flask, flash, redirect, url_for, render_template, session
from flask import Response
import psycopg2
from flask import request
from datetime import datetime
from datetime import timedelta
import string
import subprocess
import crawler

conn = psycopg2.connect("dbname='cpa' user='postgres' host='localhost' password='1234'")
cur = conn.cursor()

def configMain():

	if (request.method == 'POST'):
		try:
			table = request.form.get('commoditie')
			data1 = request.form.get('data1')
			data2 = request.form.get('data2')

			subprocess.call(['bash static/backup/backup.sh'], shell=True)

			if table == 'all':
				cur.execute("DELETE FROM boi WHERE data_ajuste >= %s AND data_ajuste <= %s", (data1,data2))
				rows_deleted = cur.rowcount
				cur.execute("DELETE FROM cafe WHERE data_ajuste >= %s AND data_ajuste <= %s", (data1,data2))
				rows_deleted += cur.rowcount
				cur.execute("DELETE FROM milho WHERE data_ajuste >= %s AND data_ajuste <= %s", (data1,data2))
				rows_deleted += cur.rowcount
				cur.execute("DELETE FROM soja WHERE data_ajuste >= %s AND data_ajuste <= %s", (data1,data2))
				rows_deleted += cur.rowcount
			elif table == 'B':
				cur.execute("DELETE FROM boi WHERE data_ajuste >= %s AND data_ajuste <= %s", (data1,data2))
				rows_deleted = cur.rowcount
				conn.commit()
			elif table == 'C':
				cur.execute("DELETE FROM cafe WHERE data_ajuste >= %s AND data_ajuste <= %s", (data1,data2))
				rows_deleted = cur.rowcount
				conn.commit()
			elif table == 'M':
				cur.execute("DELETE FROM milho WHERE data_ajuste >= %s AND data_ajuste <= %s", (data1,data2))
				rows_deleted = cur.rowcount
				conn.commit()
			elif table == 'S':
				cur.execute("DELETE FROM soja WHERE data_ajuste >= %s AND data_ajuste <= %s", (data1,data2))
				rows_deleted = cur.rowcount
				conn.commit()

			print("numero de linhas deletadas = " + str(rows_deleted))	
			return rows_deleted			
		except (Exception, psycopg2.DatabaseError) as error:
			print(error)	

def updateData():

	if (request.method == 'POST'):
		try:
			atualizacao = request.form.get('atualizacao')
			if atualizacao == 'T':
				cur.execute("SELECT ultima_atualizacao FROM info_geral WHERE cpf = '00000000000'")
				rows = cur.fetchall()
				start = rows[0][0]

				end = datetime.today()
				
				crawler.update(start, end)
				
		except (Exception, psycopg2.DatabaseError) as error:
			print(error)
		except:
			pass
		



	 		
			