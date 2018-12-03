$(document).ready(function() {
	
    var form = $('#fAjuste');

	form.on('submit', function(event) {

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
            localStorage.setItem("tabela", JSON.stringify(data));
            localStorage.setItem("data1", $("#data1").val());
            localStorage.setItem("data2", $("#data2").val());
            localStorage.setItem("vencimento", String(data[0].vencimento)); 

		});

		event.preventDefault();

	});

});

$(document).ready(function() {
    
    var form = $('#fAnalytics');

    form.on('submit', function(event) {
        show();
        var form = $(this);
        $.ajax({
            data : form.serialize(),
            type : 'POST',
            dataType: "json",
            cache: false,
            url : '/requestAnalytics'
        })

        .done(function(data) {

                drawMediaDiaria(data);
                drawMediaMensal(data);
                drawMediaSemanal(data);
                drawDesvio(data);          

        });

        event.preventDefault();

    });

});


$(document).ready(function() {

    $('#ano').on('mouseenter', function(event) {

    if ($('#ano').val() == 'all' || $('#data1').val() != data1 || $('#data2').val() != data2) {     
            
            data1 = $('#data1').val();
            data2 = $('#data2').val();

            $.ajax({
                data : {'data1': data1, 'data2': data2},
                type : 'POST',
                dataType: "json",
                cache: false,
                url : '/requestSelect'
            })
            .done(function(data) {
                $("#ano").empty()
                addSelect(data);

            });
        }
    });
    
});

function addSelect(data) {

    $('#ano').append($("<option value = 'all' id = 'op'>Todos</option>"));

    for (var i = 0; i < data.length; i++) {

        $('#ano').append($("<option value = " + data[i] + ">" + data[i] + "</option>"));
    }

}

function drawMediaSemanal(data) {

        $("#bodySemanal").empty();

            for (var i = 0; i < data.media_semanal.ajuste_atual.length; i++) {
                var row = $("<tr />");
                $("#bodySemanal").append(row); 

                if (data.media_semanal.ajuste_atual) {           
                    row.append($("<td>" + data.media_semanal.data[i] + "</td>"));
                }

                if (data.media_semanal.ajuste_atual) {           
                    row.append($("<td>" + parseFloat(Math.round(data.media_semanal.ajuste_atual[i] * 100) / 100).toFixed(2) + "</td>"));
                }

                if (data.media_semanal.variacao) {
                   row.append($("<td>" + parseFloat(Math.round(data.media_semanal.variacao[i] * 100) / 100).toFixed(2) + "</td>"));
                }

                if (data.media_semanal.contratos) { 
                    row.append($("<td>" + parseFloat(Math.round(data.media_semanal.contratos[i] * 100) / 100).toFixed(2) + "</td>"));
                }

                if (data.media_semanal.volume) { 
                    row.append($("<td>" + parseFloat(Math.round(data.media_semanal.volume[i] * 100) / 100).toFixed(2) + "</td>"));
                }

                if (data.media_semanal.preco_abertura) {
                    row.append($("<td>" + parseFloat(Math.round(data.media_semanal.preco_abertura[i] * 100) / 100).toFixed(2) + "</td>"));
                }

                if (data.media_semanal.preco_min) { 
                    row.append($("<td>" + parseFloat(Math.round(data.media_semanal.preco_min[i] * 100) / 100).toFixed(2) + "</td>"));
                }

                if (data.media_semanal.preco_max) { 
                    row.append($("<td>" + parseFloat(Math.round(data.media_semanal.preco_max[i] * 100) / 100).toFixed(2) + "</td>"));
                }
            }
}

function drawMediaMensal(data) {

        $("#bodyMensal").empty();

            for (var i = 0; i < data.media_mensal.ajuste_atual.length; i++) {
                var row = $("<tr />");
                $("#bodyMensal").append(row); 

                if (data.media_mensal.ajuste_atual) {           
                    row.append($("<td>" + data.media_mensal.data[i] + "</td>"));
                }

                if (data.media_mensal.ajuste_atual) {           
                    row.append($("<td>" + parseFloat(Math.round(data.media_mensal.ajuste_atual[i] * 100) / 100).toFixed(2) + "</td>"));
                }

                if (data.media_mensal.variacao) {
                   row.append($("<td>" + parseFloat(Math.round(data.media_mensal.variacao[i] * 100) / 100).toFixed(2) + "</td>"));
                }

                if (data.media_mensal.contratos) { 
                    row.append($("<td>" + parseFloat(Math.round(data.media_mensal.contratos[i] * 100) / 100).toFixed(2) + "</td>"));
                }

                if (data.media_mensal.volume) { 
                    row.append($("<td>" + parseFloat(Math.round(data.media_mensal.volume[i] * 100) / 100).toFixed(2) + "</td>"));
                }

                if (data.media_mensal.preco_abertura) {
                    row.append($("<td>" + parseFloat(Math.round(data.media_mensal.preco_abertura[i] * 100) / 100).toFixed(2) + "</td>"));
                }

                if (data.media_mensal.preco_min) { 
                    row.append($("<td>" + parseFloat(Math.round(data.media_mensal.preco_min[i] * 100) / 100).toFixed(2) + "</td>"));
                }

                if (data.media_mensal.preco_max) { 
                    row.append($("<td>" + parseFloat(Math.round(data.media_mensal.preco_max[i] * 100) / 100).toFixed(2) + "</td>"));
                }
            }
}

function drawMediaDiaria(data) {

      $("#bodyDiaria").empty();

            var row = $("<tr />")
            $("#bodyDiaria").append(row); 

            if (data.media_diaria.ajuste_atual) {           
                row.append($("<td>" + parseFloat(Math.round(data.media_diaria.ajuste_atual * 100) / 100).toFixed(2) + "</td>"));
            }

            if (data.media_diaria.variacao) {
               row.append($("<td>" + parseFloat(Math.round(data.media_diaria.variacao * 100) / 100).toFixed(2) + "</td>"));
            }

            if (data.media_diaria.contratos) { 
                row.append($("<td>" + parseFloat(Math.round(data.media_diaria.contratos * 100) / 100).toFixed(2) + "</td>"));
            }

            if (data.media_diaria.volume) { 
                row.append($("<td>" + parseFloat(Math.round(data.media_diaria.volume * 100) / 100).toFixed(2) + "</td>"));
            }

            if (data.media_diaria.preco_abertura) {
                row.append($("<td>" + parseFloat(Math.round(data.media_diaria.preco_abertura * 100) / 100).toFixed(2) + "</td>"));
            }

            if (data.media_diaria.preco_min) { 
                row.append($("<td>" + parseFloat(Math.round(data.media_diaria.preco_min * 100) / 100).toFixed(2) + "</td>"));
            }

            if (data.media_diaria.preco_max) { 
                row.append($("<td>" + parseFloat(Math.round(data.media_diaria.preco_max * 100) / 100).toFixed(2) + "</td>"));
            }
}

function drawDesvio(data) {

     $("#bodyDesvio").empty();

            var row = $("<tr />")
            $("#bodyDesvio").append(row); 

            if (data.desvio_padrao.ajuste_atual) {           
                row.append($("<td>" + parseFloat(Math.round(data.desvio_padrao.ajuste_atual * 100) / 100).toFixed(2) + "</td>"));
            }

            if (data.desvio_padrao.variacao) {
               row.append($("<td>" + parseFloat(Math.round(data.desvio_padrao.variacao * 100) / 100).toFixed(2) + "</td>"));
            }

            if (data.desvio_padrao.contratos) { 
                row.append($("<td>" + parseFloat(Math.round(data.desvio_padrao.contratos * 100) / 100).toFixed(2) + "</td>"));
            }

            if (data.desvio_padrao.volume) { 
                row.append($("<td>" + parseFloat(Math.round(data.desvio_padrao.volume * 100) / 100).toFixed(2) + "</td>"));
            }

            if (data.desvio_padrao.preco_abertura) {
                row.append($("<td>" + parseFloat(Math.round(data.desvio_padrao.preco_abertura * 100) / 100).toFixed(2) + "</td>"));
            }

            if (data.desvio_padrao.preco_min) { 
                row.append($("<td>" + parseFloat(Math.round(data.desvio_padrao.preco_min * 100) / 100).toFixed(2) + "</td>"));
            }

            if (data.desvio_padrao.preco_max) { 
                row.append($("<td>" + parseFloat(Math.round(data.desvio_padrao.preco_max * 100) / 100).toFixed(2) + "</td>"));
            }
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

$(document).ajaxStart(function(){
 // Show image container
 $("#loading").show();
});
$(document).ajaxComplete(function(){
 // Hide image container
 $("#loading").hide();
});

function show(){
        
        var med = $("#medDia");
        if(med){
            $("#tableMedDia").show();
        }else{
            $("#tableMedDia").hide();
        }

        var med = $("#medSema");
        if(med){
            $("#tableMedSema").show();
        }else{
            $("#tableMedSema").hide();
        }

        var med = $("#medMes");
        if(med){
            $("#tableMedMes").show();
        }else{
            $("#tableMedMes").hide();
        }

        var med = $("#desvio");
        if(med){
            $("#tabledesvio").show();
        }else{
            $("#tabledesvio").hide();
        }
      
}