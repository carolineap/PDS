function makeCSV() {

	var d = localStorage.getItem('tabela');
    var data = JSON.parse(d);

    if (data) {
		var csv = 'Data,  Código, Vencimento, Ajuste Anterior, Ajuste Atual, Variação, Valor do Contrato, Preço de Abertura, Preço Mínimo, Preço Máximo, Número de Contratos, Volume\n';

		for (var i = 0; i < data.length; i++) {

			csv += data[i].data + "," + data[i].codigo + "," + data[i].vencimento + "," + convert(data[i].ajuste_anterior) + "," + convert(data[i].ajuste_atual) + "," + convert(data[i].variacao) + "," + convert(data[i].valor_contrato) + "," + convert(data[i].preco_abertura) + "," + convert(data[i].preco_min) + "," + convert(data[i].preco_max) + "," + data[i].contratos + "," + data[i].volume + "\n";
		}

	   	var hiddenElement = document.createElement('a');
	    hiddenElement.href = 'data:text/csv;charset=utf-8,' + encodeURI(csv);
	    hiddenElement.download = 'dados.csv';

	    document.body.appendChild(hiddenElement);
		hiddenElement.click();
		document.body.removeChild(hiddenElement);
	}
}

function makeCSVRolagem() {

	var d = localStorage.getItem('tabelaRolagem');
    var data = JSON.parse(d);

    if (data) {
		var csv = 'Data,  Código, Vencimento, Ajuste Anterior, Ajuste Atual, Variação, Valor do Contrato, Preço de Abertura, Preço Mínimo, Preço Máximo, Número de Contratos, Volume\n';

		for (var i = 0; i < data.length; i++) {

			csv += data[i].data + "," + data[i].codigo + "," + data[i].vencimento + "," + convert(data[i].ajuste_anterior) + "," + convert(data[i].ajuste_atual) + "," + convert(data[i].variacao) + "," + convert(data[i].valor_contrato) + "," + convert(data[i].preco_abertura) + "," + convert(data[i].preco_min) + "," + convert(data[i].preco_max) + "," + data[i].contratos + "," + data[i].volume + "\n";
		}

	   	var hiddenElement = document.createElement('a');
	    hiddenElement.href = 'data:text/csv;charset=utf-8,' + encodeURI(csv);
	    hiddenElement.download = 'rolagem.csv';

	    document.body.appendChild(hiddenElement);
		hiddenElement.click();
		document.body.removeChild(hiddenElement);
	}

}

function convert(s) {


	n = String(parseFloat(Math.round(s * 100) / 100).toFixed(2));

	return n;

}