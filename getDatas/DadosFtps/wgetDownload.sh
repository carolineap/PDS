#!/bin/sh
ano=17
um=1
for mes in $(seq -f "%02g" 1 12 ); do
	for dia in $(seq -f "%02g" 1 31 ); do
		

		url="ftp://ftp.bmf.com.br/ContratosPregaoAjuste/AJ$ano"
		url="$url$mes"
		url="$url$dia.ex_"
		
		wget $url
	
	done
done


