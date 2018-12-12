var csv_mediaDiaria;
var csv_mediaSemanal;
var csv_mediaQuinzenal;
var csv_mediaMensal;
var csv_mediaMovel;
var csv_desvioPadrao;
var csv_ln;
var csv;
var data1;
var data2;

$(document).ready(function() {
	
    var form = $('#fAjuste');

	form.on('submit', function(event) {
        
        $(document).ajaxStart(function() {
            $("#loading").show();
        });

        $(document).ajaxStop(function() {
            $("#loading").hide();
        });

		var form = $(this);
		$.ajax({
			data : form.serialize(),
            type : 'POST',
            dataType: "json",
            cache: false,
            url : '/requestTable'
		})
		.done(function(data) {

			$("#ajusteTableB").empty()
            drawTable(data);

            try {
                localStorage.setItem("tabela", JSON.stringify(data));
                localStorage.setItem("data1", $("#data1").val());
                localStorage.setItem("data2", $("#data2").val());
                localStorage.setItem("vencimento", String(data[0].vencimento)); 
            } catch (e) {
                localStorage.clear();
            }

		});

		event.preventDefault();


	});

});

$(document).ready(function() {
    
    var form = $('#fAnalytics');

    form.on('submit', function(event) {

            if ($('#ano').val() == 'none') {
                alert("Selecione um ano de vencimento específico!");
            }

            var form = $(this);
            $.ajax({
                data : form.serialize(),
                type : 'POST',
                dataType: "json",
                cache: false,
                url : '/requestAnalytics'
            })

            .done(function(data) {

                if (data.fail) {
                    alert("Não há resultados para esse intervalo de datas e vencimento! Apenas a rolagem pode ser executada!");
                } else {

                    csv_mediaDiaria = 'Média Diária\n';
                    csv_mediaSemanal = "Média Semanal\n" + "Semana, ";
                    csv_mediaQuinzenal = "Média Quinzenal\n" + "Semana, ";
                    csv_mediaMensal = "Média Mensal\n" + "Mês, ";
                    csv_mediaMovel =   "Média Móvel\n" + "Data, Média Móvel";
                    csv_desvioPadrao = 'Desvio Padrão\n';
                    csv_ln = "Ln\n" + "Data, Ajuste Atual, Retorno Simples, Ln, Retorno Contínuo;"
                    csv = "Análises\n";

                    show(data); 

                }

                var med = $("#rolagem");
        
                if(med.is(':checked')){

                    $.ajax({
                        data : form.serialize(),
                        type : 'POST',
                        cache: false,
                        dataType: "json",
                        url : '/requestRolagem'
                    })

                    .done(function(data) {
                        try {
                            localStorage.setItem("tabelaRolagem", JSON.stringify(data));
                            localStorage.setItem("data1", $("#data1").val());
                            localStorage.setItem("data2", $("#data2").val());
                            var win = window.open('rolagem.html', '_blank');
                        } catch(e) {
                            alert("Não foi possível gerar o gráfico! Tente novamente");
                            localStorage.clear();
                        }
                    
                    });

                    event.preventDefault();


                }

            });

            event.preventDefault();

        });


});

$(document).ready(function() {

    $('#ano').on('mouseenter', function(event) {

        if ($('#ano').val() == 'all' || $('#data1').val() != data1 || $('#data2').val() != data2) {   
            
            data1 = $('#data1').val();
            data2 = $('#data2').val();
            table = $('#commoditie').val();

            if (data1 && data2 && table) {

                $.ajax({
                    data : {'data1': data1, 'data2': data2, 'table': table },
                    type : 'POST',
                    dataType: "json",
                    cache: false,
                    url : '/requestSelect'
                })
                .done(function(data) {
                    
                    if ($('#page').val() != 'none') {
                        $("#ano").empty()
                        $('#ano').append($("<option value = 'all' id = 'op'>Todos</option>"));
                    } else {
                        $("#ano").empty()
                    }
                    addSelect(data);

                });

                event.preventDefault();
            }
        }
    });
    
});

$(document).ready(function() {

    $('#aButton').on('click', function(event) {
        var hiddenElement = document.createElement('a');
        hiddenElement.href = 'data:text/csv;charset=utf-8,' + encodeURI(csv);
        hiddenElement.download = 'analise.csv';

        document.body.appendChild(hiddenElement);
        hiddenElement.click();
        document.body.removeChild(hiddenElement);

    });

});

function addSelect(data) {

    for (var i = 0; i < data.length; i++) {

        $('#ano').append($("<option value = " + data[i] + ">" + data[i] + "</option>"));
    }

}



function drawMediaSemanal(data) {

        $("#bodySemanal").empty();

            for (var i = 0; i < data.media_semanal.data.length; i++) {
                var row = $("<tr />");

                csv_mediaSemanal += "\n";

                $("#bodySemanal").append(row); 

                if (data.media_semanal.ajuste_atual) {           
                    row.append($("<td>" + data.media_semanal.data[i] + "</td>"));
                    csv_mediaSemanal += data.media_semanal.data[i] + ",";
                }

                if ($('#check0').is(':checked')) {           
                    row.append($("<td>" + convert(data.media_semanal.ajuste_anterior[i]) + "</td>"));
                    csv_mediaSemanal += convert(data.media_semanal.ajuste_anterior[i]) + ",";
                }

                if ($('#check1').is(':checked')) {           
                    row.append($("<td>" + convert(data.media_semanal.ajuste_atual[i]) + "</td>"));
                    csv_mediaSemanal += convert(data.media_semanal.ajuste_atual[i]) + ",";
                }

                if ($('#check2').is(':checked')) {
                    row.append($("<td>" + convert(data.media_semanal.variacao[i]) + "</td>"));
                    csv_mediaSemanal += convert(data.media_semanal.variacao[i]) + ",";
                }

                if ($('#check3').is(':checked')) { 
                    row.append($("<td>" + convert(data.media_semanal.contratos[i]) + "</td>"));
                    csv_mediaSemanal += convert(data.media_semanal.contratos[i]) + ",";
                }

                if ($('#check4').is(':checked')) { 
                    row.append($("<td>" + convert(data.media_semanal.volume[i]) + "</td>"));
                    csv_mediaSemanal += convert(data.media_semanal.volume[i]) + ",";
                }

                if ($('#check5').is(':checked')) {
                    row.append($("<td>" + convert(data.media_semanal.preco_abertura[i]) + "</td>"));
                    csv_mediaSemanal += convert(data.media_semanal.preco_abertura[i]) + ",";
                }

                if ($('#check6').is(':checked')) { 
                    row.append($("<td>" + convert(data.media_semanal.preco_min[i]) + "</td>"));
                    csv_mediaSemanal += convert(data.media_semanal.preco_min[i]) + ",";
                }

                if ($('#check7').is(':checked')) { 
                    row.append($("<td>" + convert(data.media_semanal.preco_max[i]) + "</td>"));
                    csv_mediaSemanal += convert(data.media_semanal.preco_max[i]) + ",";
                }
            }

}

function drawMediaMovel(data) {

        $("#bodyMovel").empty();

            for (var i = 0; i < data.media_movel.data.length; i++) {

                csv_mediaMovel += "\n";
                
                var row = $("<tr />");
                $("#bodyMovel").append(row); 

                if (data.media_movel.data) {           
                    row.append($("<td>" + data.media_movel.data[i] + "</td>"));
                    csv_mediaMovel += data.media_movel.data[i] + ", ";
                }

                if (data.media_movel.ajuste_atual[i] != 'N/A') {
                    row.append($("<td>" + convert(data.media_movel.ajuste_atual[i]) + "</td>"));
                    csv_mediaMovel += convert(data.media_movel.ajuste_atual[i]) + ", ";
                } else {
                    row.append($("<td>" + 'N/A' + "</td>"));
                    csv_mediaMovel += 'N/A' + ", ";
                }
               
            }

            localStorage.setItem("tabela", JSON.stringify(data));
            localStorage.setItem("data1", $("#data1").val());
            localStorage.setItem("data2", $("#data2").val());
}

function drawMediaQuinzenal(data) {

        $("#bodyQuinzenal").empty();

            for (var i = 0; i < data.media_quinzenal.data.length; i++) {
                var row = $("<tr />");
                $("#bodyQuinzenal").append(row); 

                 csv_mediaQuinzenal += "\n";

                if (data.media_quinzenal.data) {           
                    row.append($("<td>" + data.media_quinzenal.data[i] + "</td>"));
                    csv_mediaQuinzenal += data.media_quinzenal.data[i] + ", ";
                }

                if ($('#check0').is(':checked')) {           
                    row.append($("<td>" + convert(data.media_quinzenal.ajuste_anterior[i]) + "</td>"));
                    csv_mediaQuinzenal += convert(data.media_quinzenal.ajuste_anterior[i]) + ", ";
                }

                if ($('#check1').is(':checked')) {           
                    row.append($("<td>" + convert(data.media_quinzenal.ajuste_atual[i]) + "</td>"));
                    csv_mediaQuinzenal += convert(data.media_quinzenal.ajuste_atual[i]) + ", ";
                }

                if ($('#check2').is(':checked')) {
                   row.append($("<td>" + convert(data.media_quinzenal.variacao[i]) + "</td>"));
                   csv_mediaQuinzenal += convert(data.media_quinzenal.variacao[i]) + ", ";
                }

                if ($('#check3').is(':checked')) { 
                    row.append($("<td>" + convert(data.media_quinzenal.contratos[i]) + "</td>"));
                    csv_mediaQuinzenal += convert(data.media_quinzenal.contratos[i]) + ", ";
                }

                if ($('#check4').is(':checked')) { 
                    row.append($("<td>" + convert(data.media_quinzenal.volume[i]) + "</td>"));
                    csv_mediaQuinzenal += convert(data.media_quinzenal.volume[i]) + ", ";
                }

                if ($('#check5').is(':checked')) {
                    row.append($("<td>" + convert(data.media_quinzenal.preco_abertura[i]) + "</td>"));
                    csv_mediaQuinzenal += convert(data.media_quinzenal.preco_abertura[i]) + ", ";
                }

                if ($('#check6').is(':checked')) { 
                    row.append($("<td>" + convert(data.media_quinzenal.preco_min[i]) + "</td>"));
                    csv_mediaQuinzenal += convert(data.media_quinzenal.preco_min[i]) + ", ";
                }

                if ($('#check7').is(':checked')) { 
                    row.append($("<td>" + convert(data.media_quinzenal.preco_max[i]) + "</td>"));
                    csv_mediaQuinzenal += convert(data.media_quinzenal.preco_max[i]) + ", ";
                }
            }
}

function drawMediaMensal(data) {

        $("#bodyMensal").empty();

            for (var i = 0; i < data.media_mensal.data.length; i++) {
                var row = $("<tr />");
                $("#bodyMensal").append(row); 

                csv_mediaMensal += "\n";

                if (data.media_mensal.data) {           
                    row.append($("<td>" + data.media_mensal.data[i] + "</td>"));
                    csv_mediaMensal += data.media_mensal.data[i] + ", ";
                }

                if ($('#check0').is(':checked')) {           
                    row.append($("<td>" +convert(data.media_mensal.ajuste_anterior[i]) + "</td>"));
                    csv_mediaMensal += convert(data.media_mensal.ajuste_anterior[i]) + ", ";
                }

                if ($('#check1').is(':checked')) {           
                    row.append($("<td>" +convert(data.media_mensal.ajuste_atual[i]) + "</td>"));
                    csv_mediaMensal += convert(data.media_mensal.ajuste_atual[i]) + ", ";
                }

                if ($('#check2').is(':checked')) {
                   row.append($("<td>" + convert(data.media_mensal.variacao[i]) + "</td>"));
                   csv_mediaMensal += convert(data.media_mensal.variacao[i]) + ", ";
                }

                if ($('#check3').is(':checked')) { 
                    row.append($("<td>" + convert(data.media_mensal.contratos[i]) + "</td>"));
                    csv_mediaMensal += convert(data.media_mensal.contratos[i]) + ", ";
                }

                if ($('#check4').is(':checked')) { 
                    row.append($("<td>" + convert(data.media_mensal.volume[i]) + "</td>"));
                    csv_mediaMensal += convert(data.media_mensal.volume[i]) + ", ";
                }

                if ($('#check5').is(':checked')) {
                    row.append($("<td>" + convert(data.media_mensal.preco_abertura[i]) + "</td>"));
                    csv_mediaMensal += convert(data.media_mensal.preco_abertura[i]) + ", ";
                }

                if ($('#check6').is(':checked')) { 
                    row.append($("<td>" + convert(data.media_mensal.preco_min[i]) + "</td>"));
                    csv_mediaMensal+= convert(data.media_mensal.preco_min[i]) + ", ";
                }

                if ($('#check7').is(':checked')) { 
                    row.append($("<td>" + convert(data.media_mensal.preco_max[i]) + "</td>"));
                    csv_mediaMensal += convert(data.media_mensal.preco_max[i]) + ", ";
                }
            }
}

function drawMediaDiaria(data) {

       $("#bodyDiaria").empty();

                var row = $("<tr />");
                $("#bodyDiaria").append(row); 

                csv_mediaDiaria += "\n";

                 if ($('#check0').is(':checked')) {           
                    row.append($("<td>" + convert(data.media_diaria.ajuste_anterior) + "</td>"));
                    csv_mediaDiaria += convert(data.media_diaria.ajuste_anterior) + ", ";
                }

                if ($('#check1').is(':checked')) {           
                    row.append($("<td>" + convert(data.media_diaria.ajuste_atual) + "</td>"));
                    csv_mediaDiaria += convert(data.media_diaria.ajuste_atual) + ", ";
                }

                if ($('#check2').is(':checked')) {
                   row.append($("<td>" + convert(data.media_diaria.variacao) + "</td>"));
                   csv_mediaDiaria += convert(data.media_diaria.variacao) + ", ";
                }

                if ($('#check3').is(':checked')) { 
                    row.append($("<td>" + convert(data.media_diaria.contratos) + "</td>"));
                    csv_mediaDiaria += convert(data.media_diaria.contratos) + ", ";
                }

                if ($('#check4').is(':checked')) { 
                    row.append($("<td>" + convert(data.media_diaria.volume) + "</td>"));
                    csv_mediaDiaria += convert(data.media_diaria.volume) + ", ";
                }

                if ($('#check5').is(':checked')) {
                    row.append($("<td>" + convert(data.media_diaria.preco_abertura) + "</td>"));
                    csv_mediaDiaria += convert(data.media_diaria.preco_abertura) + ", ";
                }

                if ($('#check6').is(':checked')) { 
                    row.append($("<td>" + convert(data.media_diaria.preco_min) + "</td>"));
                    csv_mediaDiaria += convert(data.media_diaria.preco_min) + ", ";
                }

                if ($('#check7').is(':checked')) { 
                    row.append($("<td>" + convert(data.media_diaria.preco_max) + "</td>"));
                    csv_mediaDiaria += convert(data.media_diaria.preco_max) + ", ";
                }
}

function drawDesvio(data) {

     $("#bodyDesvio").empty();

            var row = $("<tr />")
            $("#bodyDesvio").append(row); 

            csv_desvioPadrao += "\n";

            if ($('#check0').is(':checked')) {           
                row.append($("<td>" + convert(data.desvio_padrao.ajuste_anterior) + "</td>"));
                csv_desvioPadrao += convert(data.desvio_padrao.ajuste_anterior) + ", ";
            }

            if ($('#check1').is(':checked')) {           
                row.append($("<td>" + convert(data.desvio_padrao.ajuste_atual) + "</td>"));
                csv_desvioPadrao += convert(data.desvio_padrao.ajuste_atual) + ", ";
            }

            if ($('#check2').is(':checked')) {
               row.append($("<td>" + convert(data.desvio_padrao.variacao) + "</td>"));
               csv_desvioPadrao += convert(data.desvio_padrao.variacao) + ", ";
            }

            if ($('#check3').is(':checked')) { 
                row.append($("<td>" + convert(data.desvio_padrao.contratos) + "</td>"));
                csv_desvioPadrao += convert(data.desvio_padrao.contratos) + ", ";
            }

            if ($('#check4').is(':checked')) { 
                row.append($("<td>" + convert(data.desvio_padrao.volume) + "</td>"));
                csv_desvioPadrao += convert(data.desvio_padrao.volume) + ", ";
            }

            if ($('#check5').is(':checked')) {
                row.append($("<td>" + convert(data.desvio_padrao.preco_abertura) + "</td>"));
                csv_desvioPadrao += convert(data.desvio_padrao.preco_abertura) + ", ";
            }

            if ($('#check6').is(':checked')) { 
                row.append($("<td>" + convert(data.desvio_padrao.preco_min) + "</td>"));
                csv_desvioPadrao += convert(data.desvio_padrao.preco_min) + ", ";
            }

            if ($('#check7').is(':checked')) { 
                row.append($("<td>" + convert(data.desvio_padrao.preco_max) + "</td>"));
                csv_desvioPadrao += convert(data.desvio_padrao.preco_max) + ", ";
            }
        
}
function drawln(data) {

        $("#bodyln").empty();
       

            for (var i = 0; i < data.ln.ajuste_atual.length; i++) {
                var row = $("<tr />");
                $("#bodyln").append(row); 

                csv_ln += "\n";

                if (data.ln.data) {           
                    row.append($("<td>" + data.ln.data[i] + "</td>"));
                    csv_ln += data.ln.data[i] + ", ";
                }          
                
                row.append($("<td>" + convert(data.ln.ajuste_atual[i]) + "</td>"));
                csv_ln += convert(data.ln.ajuste_atual[i]) + ", ";
           
                if (data.ln.retorno_simples[i] != 'N/A') {
                    row.append($("<td>" + convert(data.ln.retorno_simples[i]) + "</td>"));
                    csv_ln += convert(data.ln.retorno_simples[i]) + ", ";
                } else {
                    row.append($("<td>" + 'N/A' + "</td>"));
                    csv_ln += 'N/A' + ", ";
                }

                row.append($("<td>" + convert(data.ln.ln[i]) + "</td>"));
                csv_ln += convert(data.ln.ln[i]) + ", ";
            
                if (data.ln.retorno_continuo[i] != 'N/A') {
                    row.append($("<td>" + parseFloat(data.ln.retorno_continuo[i]).toFixed(6) + "</td>"));
                    csv_ln += parseFloat(data.ln.retorno_continuo[i]).toFixed(6) + ", ";
                } else {
                    row.append($("<td>" + 'N/A' + "</td>"));
                    csv_ln += 'N/A' + ", ";
                }
            }

            csv_ln += '\n';
            
            $("#bodylnaux").empty();

            var row = $("<tr />");
            $("#bodylnaux").append(row); 

            csv_ln += "Média Retorno Simples, Risco, Média Retorno Contínuo, Volatilidade\n";

            row.append($("<td>" + parseFloat(data.ln.media_simples).toFixed(6) + "</td>"));
            csv_ln += parseFloat(data.ln.media_simples).toFixed(6) + ", ";
            row.append($("<td>" + parseFloat(data.ln.risco).toFixed(6) + "</td>"));
            csv_ln += parseFloat(data.ln.risco).toFixed(6) + ", ";
            row.append($("<td>" + parseFloat(data.ln.media_continua).toFixed(6) + "</td>"));
            csv_ln += parseFloat(data.ln.media_continua).toFixed(6) + ", ";
            row.append($("<td>" + parseFloat(data.ln.volatilidade).toFixed(6) + "</td>"));
            csv_ln += parseFloat(data.ln.volatilidade).toFixed(6) + ", ";
}



function drawTable(data) {

    if (data.length == 0) {
         $("#ajusteTableB").append($("<p style='text-align: center;'>Não há resultados.</p>")); 
    } else {

        for (var i = 0; i < data.length; i++) {
            drawRow(data[i]);
        }

        $("#graphDown").show();

    }
}

function drawRow(rowData) {
    
    var row = $("<tr />")
    $("#ajusteTableB").append(row); 
    row.append($("<td style='text-align: center'>" + rowData.codigo + "</td>"));
    row.append($("<td style='text-align: center'>" + rowData.data + "</td>"));
    row.append($("<td style='text-align: center'>" + rowData.vencimento + "</td>"));
    row.append($("<td>" + parseFloat(Math.round(rowData.ajuste_anterior * 100) / 100).toFixed(2) + "</td>"));
    row.append($("<td>" + parseFloat(Math.round(rowData.ajuste_atual * 100) / 100).toFixed(2) + "</td>"));
    row.append($("<td>" + parseFloat(Math.round(rowData.variacao * 100) / 100).toFixed(2) + "</td>"));
    row.append($("<td>" + parseFloat(Math.round(rowData.valor_contrato * 100) / 100).toFixed(2) + "</td>"));
    row.append($("<td>" + rowData.contratos + "</td>"));
    row.append($("<td>" + rowData.volume + "</td>"));

}

function show(data){

        removeColumn();

        $("#ADown").show();
        
        var med = $("#medDia");
        if(med.is(':checked')){
            $("#tableMedDia").show();
            drawMediaDiaria(data);
            csv += "\n" + csv_mediaDiaria + "\n";
        }else{
            $("#tableMedDia").hide();
        }

        var med = $("#medSema");
        if(med.is(':checked')){
            $("#tableMedSema").show();
            drawMediaSemanal(data);
            csv +=  "\n" + csv_mediaSemanal + "\n";
        }else{
            $("#tableMedSema").hide();
        }
        var med = $("#medMes");
        if(med.is(':checked')){
            $("#tableMedMes").show();
            drawMediaMensal(data);
            csv += "\n" + csv_mediaMensal + "\n";
        }else{
            $("#tableMedMes").hide();
        }

        var med = $("#medQuinze");
        if(med.is(':checked')){
            $("#tableMedQuinze").show();
            drawMediaQuinzenal(data);
            csv += "\n" + csv_mediaQuinzenal + "\n";
        }else{
            $("#tableMedQuinze").hide();
        }

        var med = $("#desvio");
        if(med.is(':checked')){
            $("#tabledesvio").show();
            drawDesvio(data);
            csv += "\n" + csv_desvioPadrao + "\n";
        }else{
            $("#tabledesvio").hide();
        }

        var med = $("#movel");
        if(med.is(':checked')){
            if ($('#check1').is(':checked')) {    
                $("#tablemovel").show();
                drawMediaMovel(data);
                csv += "\n" + csv_mediaMovel + "\n";
            } else {
                alert("Os cálculos de média móvel são realizados somente com o preço de ajuste atual!");
            }
        }else{
            $("#tablemovel").hide();
        }

        var med = $("#ln");
        if(med.is(':checked')){
            if ($('#check1').is(':checked')) {    
                $("#tableln").show();
                $("#bodyln").empty();
                drawln(data);
                csv += "\n" + csv_ln + "\n";
            } else {
                alert("Os cálculos de ln são realizados somente com o preço de ajuste atual!");
            }
        }else{
            $("#tableln").hide();
        }
}

function removeColumn(){

    var check = $("#check0");  
    if(check.is(':checked')){
        $(".ajuste_anterior").show();
        csv_mediaDiaria += "Ajuste Anterior, ";
        csv_mediaSemanal += "Ajuste Anterior, ";
        csv_mediaQuinzenal += "Ajuste Anterior, ";
        csv_mediaMensal += "Ajuste Anterior, ";
        csv_desvioPadrao += "Ajuste Anterior, ";

    } else {
        $(".ajuste_anterior").hide();
    }

    var check = $("#check1");  
    if(check.is(':checked')){
        $(".ajuste_atual").show();
        csv_mediaDiaria += "Ajuste Atual, ";
        csv_mediaSemanal += "Ajuste Atual, ";
        csv_mediaQuinzenal += "Ajuste Atual, ";
        csv_mediaMensal += "Ajuste Atual, ";
        csv_desvioPadrao += "Ajuste Atual, ";

    } else {
        $(".ajuste_atual").hide();
    }

    var check = $("#check2");  
    if(check.is(':checked')){
        $(".variacao").show();
        csv_mediaDiaria += "Variação, ";
        csv_mediaSemanal += "Variação, ";
        csv_mediaQuinzenal += "Variação, ";
        csv_mediaMensal += "Variação, ";
        csv_desvioPadrao += "Variação, ";
    } else {
        $(".variacao").hide();
    }

    var check = $("#check3");  
    if(check.is(':checked')){
        $(".contratos").show();
        csv_mediaDiaria += "Contratos, ";
        csv_mediaSemanal += "Contratos, ";
        csv_mediaQuinzenal += "Contratos, ";
        csv_mediaMensal += "Contratos, ";
        csv_desvioPadrao += "Contratos, ";
    } else {
        $(".contratos").hide();
    }

    var check = $("#check4");  
    if(check.is(':checked')){
        $(".volume").show();
        csv_mediaDiaria += "Volume, ";
        csv_mediaSemanal += "Volume, ";
        csv_mediaQuinzenal += "Volume, ";
        csv_mediaMensal += "Volume, ";
        csv_desvioPadrao += "Volume, ";
    } else {
        $(".volume").hide();

    }

    var check = $("#check5");  
    if(check.is(':checked')){
        $(".abertura").show();
        csv_mediaDiaria += "Preço Abertura, ";
        csv_mediaSemanal += "Preço Abertura, ";
        csv_mediaQuinzenal += "Preço Abertura, ";
        csv_mediaMensal += "Preço Abertura, ";
        csv_desvioPadrao += "Preço Abertura, ";
    } else {
        $(".abertura").hide();
    }

    var check = $("#check6");  
    if(check.is(':checked')){
        $(".minimo").show();
        csv_mediaDiaria += "Preço Mínimo, ";
        csv_mediaSemanal += "Preço Mínimo, ";
        csv_mediaQuinzenal += "Preço Mínimo, ";
        csv_mediaMensal += "Preço Mínimo, ";
        csv_desvioPadrao += "Preço Mínimo, ";
    } else {
        $(".minimo").hide();

    }

    var check = $("#check7");  
    if(check.is(':checked')){
        $(".maximo").show();
        csv_mediaDiaria += "Preço Máximo, ";
        csv_mediaSemanal += "Preço Máximo, ";
        csv_mediaQuinzenal += "Preço Máximo, ";
        csv_mediaMensal += "Preço Máximo, ";
        csv_desvioPadrao += "Preço Máximo, ";
    } else {
        $(".maximo").hide();
    }

}

function convert(s) {

    n = String(parseFloat(Math.round(s * 100) / 100).toFixed(2));

    return n;

}

