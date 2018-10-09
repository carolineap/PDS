import io
fArqui = open("BDAjuste.txt", 'r')
fArqui2 = open("Ajuste.txt", 'w')
i = 0
fArqui2.write("Data;Código do Contrato;Pregão;Vencimento;Volume(R$);Volume(U$);Número de contas em Aberto;Preço de Abertura;Preço Mínimo;Preço Máximo;Último Preço;Preço de Ajuste Atual; Preço de Ajuste Anterior;Valor de Ajuste por Contrato;Variação\n")
while(True):
	
	line = fArqui.read(11)
	if not line:
		print("fim")
		break;
	data = fArqui.read(8)
	fArqui2.write(data+";")
	
	fArqui.read(2)
	cod_contrato = fArqui.read(3)
	fArqui2.write(cod_contrato+";")

	fArqui.read(1)
	pregao = fArqui.read(1)
	fArqui2.write(pregao+";")

	vencimento = fArqui.read(4)
	fArqui2.write(vencimento+";")

	fArqui.read(40)
	volumeReais = float(fArqui.read(13))/100
	fArqui2.write(str(volumeReais)+";")

	volumeDolar = fArqui.read(13)
	fArqui2.write(volumeDolar+";")

	numContAberto = fArqui.read(8)
	fArqui2.write(numContAberto+";")

	fArqui.read(45)
	preco_aber = fArqui.read(8)
	fArqui2.write(preco_aber+";")

	fArqui.read(1)
	precoMin = fArqui.read(8)
	fArqui2.write(precoMin+";")  

	fArqui.read(1)
	precoMax = fArqui.read(8)
	fArqui2.write(precoMax+";")

	fArqui.read(15)
	precoUltimo = fArqui.read(8)
	fArqui2.write(precoUltimo+";")

	fArqui.read(33)
	precoAjustAtual = fArqui.read(13)
	fArqui2.write(precoAjustAtual+";")

	fArqui.read(2)
	precoAjustAnte = fArqui.read(13)
	fArqui2.write(precoAjustAnte+";")

	fArqui.read(1)
	precoAjustContr = fArqui.read(13)
	fArqui2.write(precoAjustContr+";")

	fArqui.read(53)
	variacao = fArqui.read(8)
	fArqui2.write(variacao+";\n")
	fArqui.read(190)
		
fArqui.close()
fArqui2.close()	