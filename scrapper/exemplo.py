#author Gabriel Eiji Uema Martin

import scrapper
import json

# Helper que transforma uma instância de uma classe em JSON
def toJSON(self):
    return json.dumps(self, default=lambda o: o.__dict__, indent=4, separators=(',',':'))

# Define a URL alvo das requisições
scrapper.URL = 'http://www2.bmf.com.br/pages/portal/bmfbovespa/lumis/lum-ajustes-do-pregao-ptBR.asp'

# Realiza uma única requisição com a data fornecida
requisicao = scrapper.Requisicao('01/10/2018')

# Realiza requisições entre as datas fornecidas
requisicoes = scrapper.Requisicao.request_batch('01/10/2017', '01/10/2018')

# Salva os resultados em JSON
file1 = open('requisicao.json', 'w')
file1.write(toJSON(requisicao))
file1.close()

file2 = open('requisicoes.json', 'w')
file2.write(toJSON(requisicoes))
file2.close()