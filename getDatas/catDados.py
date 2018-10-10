import io
import sys
#print(sys.argv[1])
fArqui = open("DadosFtps/extraidos/"+sys.argv[1], 'r')
data = sys.argv[1]
nome = data[6:8] + '-' + data[4:6] + '-' + data[2:4]
#print(nome)
fArqui2 = open("DadosProntos/2017/"+nome+".txt", 'w')

fArqui2.write("Data;Código do Contrato;Pregão;Vencimento;Volume(R$);Volume(U$);Número de contas em Aberto;Preço de Abertura;Preço Mínimo;Preço Máximo;Último Preço;Preço de Ajuste Atual; Preço de Ajuste Anterior;Valor de Ajuste por Contrato;Variação\n")
while(True):
	
	line = fArqui.read(11)
	if not line:
		print("fim")
		break;
	data = fArqui.read(8)
	
	fArqui.read(2)
	cod_contrato = fArqui.read(3)

	fArqui.read(1)
	pregao = fArqui.read(1)

	vencimento = fArqui.read(4)

	fArqui.read(40)
	volumeReais = str(float(fArqui.read(13))/100)

	volumeDolar = str(float(fArqui.read(13))/100)

	numContAberto = str(float(fArqui.read(8))/100)

	fArqui.read(45)
	preco_aber = str(float(fArqui.read(8))/100)

	fArqui.read(1)
	precoMin = str(float(fArqui.read(8))/100)

	fArqui.read(1)
	precoMax = str(float(fArqui.read(8))/100)

	fArqui.read(15)
	precoUltimo = str(float(fArqui.read(8))/100)

	fArqui.read(33)
	precoAjustAtual = str(float(fArqui.read(13))/100)

	fArqui.read(2)
	precoAjustAnte = str(float(fArqui.read(13))/100)

	fArqui.read(1)
	precoAjustContr = str(float(fArqui.read(13))/100)

	fArqui.read(53)
	variacao = str(float(fArqui.read(8))/100)
	fArqui.read(190)
	if (pregao == '*') and (cod_contrato == "SFI" or cod_contrato == "BGI" or cod_contrato == "ICF" or cod_contrato == "CCM"):
		fArqui2.write(data+";")
		fArqui2.write(cod_contrato+";")
		fArqui2.write(pregao+";")
		fArqui2.write(vencimento+";")
		fArqui2.write(volumeReais+";")
		fArqui2.write(volumeDolar+";")
		fArqui2.write(numContAberto+";")
		fArqui2.write(preco_aber+";")
		fArqui2.write(precoMin+";")  
		fArqui2.write(precoMax+";")
		fArqui2.write(precoUltimo+";")
		fArqui2.write(precoAjustAtual+";")
		fArqui2.write(precoAjustAnte+";")
		fArqui2.write(precoAjustContr+";")
		fArqui2.write(variacao+";\n")
	
	
fArqui.close()
fArqui2.close()	