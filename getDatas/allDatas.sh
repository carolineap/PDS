#!/bin/sh
ano=17
um=1
for mes in $(seq -f "%02g" 1 12 ); do
	for dia in $(seq -f "%02g" 1 31 ); do
		name="AJ$ano$mes$dia.txt"
		python3 "catDados.py" $name
	done
done