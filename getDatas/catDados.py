import io
import sys
import os

#lista apenas os arquivos txt da pasta
pasta = "DadosFtps/extraidos/"
caminhos = [os.path.join(pasta, nome) for nome in os.listdir(pasta)]
arquivos = [arq for arq in caminhos if os.path.isfile(arq)]
arquivos_txt = [arq for arq in arquivos if arq.lower().endswith(".txt")]

fMilho = open("DadosProntos/2017/Milho.txt", 'w')
fBoi = open("DadosProntos/2017/Boi.txt", 'w')
fSoja = open("DadosProntos/2017/Soja.txt", 'w')
fCafe = open("DadosProntos/2017/Cafe.txt", 'w')

#fMilho.write("Data;Código do Contrato;Vencimento;Volume(R$);Volume(U$);Número de contas em Aberto;Preço de Abertura;Preço Mínimo;Preço Máximo;Último Preço;Preço de Ajuste Atual; Preço de Ajuste Anterior;Valor de Ajuste por Contrato;Variação\n")
#fBoi.write("Data;Código do Contrato;Vencimento;Volume(R$);Volume(U$);Número de contas em Aberto;Preço de Abertura;Preço Mínimo;Preço Máximo;Último Preço;Preço de Ajuste Atual; Preço de Ajuste Anterior;Valor de Ajuste por Contrato;Variação\n")
#fSoja.write("Data;Código do Contrato;Vencimento;Volume(R$);Volume(U$);Número de contas em Aberto;Preço de Abertura;Preço Mínimo;Preço Máximo;Último Preço;Preço de Ajuste Atual; Preço de Ajuste Anterior;Valor de Ajuste por Contrato;Variação\n")
#fCafe.write("Data;Código do Contrato;Vencimento;Volume(R$);Volume(U$);Número de contas em Aberto;Preço de Abertura;Preço Mínimo;Preço Máximo;Último Preço;Preço de Ajuste Atual; Preço de Ajuste Anterior;Valor de Ajuste por Contrato;Variação\n")

#percorre os arquivos
for arq in arquivos_txt:

	#print(sys.argv[1])
	fArqui = open(arq)
	#data = sys.argv[1]
	#nome = data[6:8] + '-' + data[4:6] + '-' + data[2:4]
	#print(nome)
	#nome = 'teste' + str(i)
	#i += 1


	while(True):

		line = fArqui.read(11)
		if not line:
			print("fim")
			break;
		data = fArqui.read(4)+"-"+fArqui.read(2)+"-"+fArqui.read(2)

		fArqui.read(2)
		cod_contrato = fArqui.read(3)

		fArqui.read(1)
		pregao = fArqui.read(1)

		vencimento = fArqui.read(4)

		fArqui.read(40)
		volumeReais = str(float(fArqui.read(13))/100)

		volumeDolar = str(float(fArqui.read(13))/100)

		numContAberto = str(int(fArqui.read(8)))

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

		if (pregao == '*'):
			if (cod_contrato == "SFI"):
				fSoja.write(data+";")
				fSoja.write(cod_contrato+";")
				#fSoja.write(pregao+";")
				fSoja.write(vencimento+";")
				#fSoja.write(volumeReais+";")
				fSoja.write(volumeDolar+";")
				fSoja.write(numContAberto+";")
				fSoja.write(preco_aber+";")
				fSoja.write(precoMin+";")
				fSoja.write(precoMax+";")
				fSoja.write(precoUltimo+";")
				fSoja.write(precoAjustAtual+";")
				fSoja.write(precoAjustAnte+";")
				fSoja.write(precoAjustContr+";")
				fSoja.write(variacao+"\n")
			elif (cod_contrato == "BGI"):
				fBoi.write(data+";")
				fBoi.write(cod_contrato+";")
				#fBoi.write(pregao+";")
				fBoi.write(vencimento+";")
				fBoi.write(volumeReais+";")
				#fBoi.write(volumeDolar+";")
				fBoi.write(numContAberto+";")
				fBoi.write(preco_aber+";")
				fBoi.write(precoMin+";")
				fBoi.write(precoMax+";")
				fBoi.write(precoUltimo+";")
				fBoi.write(precoAjustAtual+";")
				fBoi.write(precoAjustAnte+";")
				fBoi.write(precoAjustContr+";")
				fBoi.write(variacao+"\n")
			elif (cod_contrato == "ICF"):
				fCafe.write(data+";")
				fCafe.write(cod_contrato+";")
				#fCafe.write(pregao+";")
				fCafe.write(vencimento+";")
				#fCafe.write(volumeReais+";")
				fCafe.write(volumeDolar+";")
				fCafe.write(numContAberto+";")
				fCafe.write(preco_aber+";")
				fCafe.write(precoMin+";")
				fCafe.write(precoMax+";")
				fCafe.write(precoUltimo+";")
				fCafe.write(precoAjustAtual+";")
				fCafe.write(precoAjustAnte+";")
				fCafe.write(precoAjustContr+";")
				fCafe.write(variacao+"\n")
			elif (cod_contrato == "CCM"):
				fMilho.write(data+";")
				fMilho.write(cod_contrato+";")
				#fMilho.write(pregao+";")
				fMilho.write(vencimento+";")
				fMilho.write(volumeReais+";")
				#fMilho.write(volumeDolar+";")
				fMilho.write(numContAberto+";")
				fMilho.write(preco_aber+";")
				fMilho.write(precoMin+";")
				fMilho.write(precoMax+";")
				fMilho.write(precoUltimo+";")
				fMilho.write(precoAjustAtual+";")
				fMilho.write(precoAjustAnte+";")
				fMilho.write(precoAjustContr+";")
				fMilho.write(variacao+"\n")

	fArqui.close()

fSoja.close()
fCafe.close()
fMilho.close()
fBoi.close()
