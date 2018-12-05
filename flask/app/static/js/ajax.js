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

                    show(data); 

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
                
                if ($('#ano').val() != 'none') {
                    $("#ano").empty()
                    $('#ano').append($("<option value = 'all' id = 'op'>Todos</option>"));
                } else {
                    $("#ano").empty()
                }
                addSelect(data);

            });
        }
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
                $("#bodySemanal").append(row); 

                if (data.media_semanal.ajuste_atual) {           
                    row.append($("<td>" + data.media_semanal.data[i] + "</td>"));
                }

                if ($('#check1').is(':checked')) {           
                    row.append($("<td>" + parseFloat(Math.round(data.media_semanal.ajuste_atual[i] * 100) / 100).toFixed(2) + "</td>"));
                }

                if ($('#check2').is(':checked')) {
                   row.append($("<td>" + parseFloat(Math.round(data.media_semanal.variacao[i] * 100) / 100).toFixed(2) + "</td>"));
                }

                if ($('#check3').is(':checked')) { 
                    row.append($("<td>" + parseFloat(Math.round(data.media_semanal.contratos[i] * 100) / 100).toFixed(2) + "</td>"));
                }

                if ($('#check4').is(':checked')) { 
                    row.append($("<td>" + parseFloat(Math.round(data.media_semanal.volume[i] * 100) / 100).toFixed(2) + "</td>"));
                }

                if ($('#check5').is(':checked')) {
                    row.append($("<td>" + parseFloat(Math.round(data.media_semanal.preco_abertura[i] * 100) / 100).toFixed(2) + "</td>"));
                }

                if ($('#check6').is(':checked')) { 
                    row.append($("<td>" + parseFloat(Math.round(data.media_semanal.preco_min[i] * 100) / 100).toFixed(2) + "</td>"));
                }

                if ($('#check7').is(':checked')) { 
                    row.append($("<td>" + parseFloat(Math.round(data.media_semanal.preco_max[i] * 100) / 100).toFixed(2) + "</td>"));
                }
            }
}

function drawMediaMovel(data) {

        $("#bodyMovel").empty();

            for (var i = 0; i < data.media_movel.data.length; i++) {
                
                var row = $("<tr />");
                $("#bodyMovel").append(row); 

                if (data.media_movel.data) {           
                    row.append($("<td>" + data.media_movel.data[i] + "</td>"));
                }

                if ($('#check1').is(':checked')) {           
                    if (data.media_movel.ajuste_atual[i] != 'N/A')
                        row.append($("<td>" + parseFloat(Math.round(data.media_movel.ajuste_atual[i] * 100) / 100).toFixed(2) + "</td>"));
                    else
                        row.append($("<td>" + 'N/A' + "</td>"));
                }

            }
}

function drawMediaQuinzenal(data) {

        $("#bodyQuinzenal").empty();

            for (var i = 0; i < data.media_quinzenal.data.length; i++) {
                var row = $("<tr />");
                $("#bodyQuinzenal").append(row); 

                if (data.media_quinzenal.data) {           
                    row.append($("<td>" + data.media_quinzenal.data[i] + "</td>"));
                }

                if ($('#check1').is(':checked')) {           
                    row.append($("<td>" + parseFloat(Math.round(data.media_quinzenal.ajuste_atual[i] * 100) / 100).toFixed(2) + "</td>"));
                }

                if ($('#check2').is(':checked')) {
                   row.append($("<td>" + parseFloat(Math.round(data.media_quinzenal.variacao[i] * 100) / 100).toFixed(2) + "</td>"));
                }

                if ($('#check3').is(':checked')) { 
                    row.append($("<td>" + parseFloat(Math.round(data.media_quinzenal.contratos[i] * 100) / 100).toFixed(2) + "</td>"));
                }

                if ($('#check4').is(':checked')) { 
                    row.append($("<td>" + parseFloat(Math.round(data.media_quinzenal.volume[i] * 100) / 100).toFixed(2) + "</td>"));
                }

                if ($('#check5').is(':checked')) {
                    row.append($("<td>" + parseFloat(Math.round(data.media_quinzenal.preco_abertura[i] * 100) / 100).toFixed(2) + "</td>"));
                }

                if ($('#check6').is(':checked')) { 
                    row.append($("<td>" + parseFloat(Math.round(data.media_quinzenal.preco_min[i] * 100) / 100).toFixed(2) + "</td>"));
                }

                if ($('#check7').is(':checked')) { 
                    row.append($("<td>" + parseFloat(Math.round(data.media_quinzenal.preco_max[i] * 100) / 100).toFixed(2) + "</td>"));
                }
            }
}

function drawMediaMensal(data) {

        $("#bodyMensal").empty();

            for (var i = 0; i < data.media_mensal.data.length; i++) {
                var row = $("<tr />");
                $("#bodyMensal").append(row); 

                if (data.media_mensal.data) {           
                    row.append($("<td>" + data.media_mensal.data[i] + "</td>"));
                }

                if ($('#check1').is(':checked')) {           
                    row.append($("<td>" + parseFloat(Math.round(data.media_mensal.ajuste_atual[i] * 100) / 100).toFixed(2) + "</td>"));
                }

                if ($('#check2').is(':checked')) {
                   row.append($("<td>" + parseFloat(Math.round(data.media_mensal.variacao[i] * 100) / 100).toFixed(2) + "</td>"));
                }

                if ($('#check3').is(':checked')) { 
                    row.append($("<td>" + parseFloat(Math.round(data.media_mensal.contratos[i] * 100) / 100).toFixed(2) + "</td>"));
                }

                if ($('#check4').is(':checked')) { 
                    row.append($("<td>" + parseFloat(Math.round(data.media_mensal.volume[i] * 100) / 100).toFixed(2) + "</td>"));
                }

                if ($('#check5').is(':checked')) {
                    row.append($("<td>" + parseFloat(Math.round(data.media_mensal.preco_abertura[i] * 100) / 100).toFixed(2) + "</td>"));
                }

                if ($('#check6').is(':checked')) { 
                    row.append($("<td>" + parseFloat(Math.round(data.media_mensal.preco_min[i] * 100) / 100).toFixed(2) + "</td>"));
                }

                if ($('#check7').is(':checked')) { 
                    row.append($("<td>" + parseFloat(Math.round(data.media_mensal.preco_max[i] * 100) / 100).toFixed(2) + "</td>"));
                }
            }
}

function drawMediaDiaria(data) {

       $("#bodyDiaria").empty();

                var row = $("<tr />");
                $("#bodyDiaria").append(row); 

                if ($('#check1').is(':checked')) {           
                    row.append($("<td>" + parseFloat(Math.round(data.media_diaria.ajuste_atual * 100) / 100).toFixed(2) + "</td>"));
                }

                if ($('#check2').is(':checked')) {
                   row.append($("<td>" + parseFloat(Math.round(data.media_diaria.variacao * 100) / 100).toFixed(2) + "</td>"));
                }

                if ($('#check3').is(':checked')) { 
                    row.append($("<td>" + parseFloat(Math.round(data.media_diaria.contratos  * 100) / 100).toFixed(2) + "</td>"));
                }

                if ($('#check4').is(':checked')) { 
                    row.append($("<td>" + parseFloat(Math.round(data.media_diaria.volume  * 100) / 100).toFixed(2) + "</td>"));
                }

                if ($('#check5').is(':checked')) {
                    row.append($("<td>" + parseFloat(Math.round(data.media_diaria.preco_abertura * 100) / 100).toFixed(2) + "</td>"));
                }

                if ($('#check6').is(':checked')) { 
                    row.append($("<td>" + parseFloat(Math.round(data.media_diaria.preco_min * 100) / 100).toFixed(2) + "</td>"));
                }

                if ($('#check7').is(':checked')) { 
                    row.append($("<td>" + parseFloat(Math.round(data.media_diaria.preco_max * 100) / 100).toFixed(2) + "</td>"));
                }
}

function drawDesvio(data) {

     $("#bodyDesvio").empty();

            var row = $("<tr />")
            $("#bodyDesvio").append(row); 

            if ($('#check1').is(':checked')) {           
                row.append($("<td>" + parseFloat(Math.round(data.desvio_padrao.ajuste_atual * 100) / 100).toFixed(2) + "</td>"));
            }

            if ($('#check2').is(':checked')) {
               row.append($("<td>" + parseFloat(Math.round(data.desvio_padrao.variacao * 100) / 100).toFixed(2) + "</td>"));
            }

            if ($('#check3').is(':checked')) { 
                row.append($("<td>" + parseFloat(Math.round(data.desvio_padrao.contratos * 100) / 100).toFixed(2) + "</td>"));
            }

            if ($('#check4').is(':checked')) { 
                row.append($("<td>" + parseFloat(Math.round(data.desvio_padrao.volume * 100) / 100).toFixed(2) + "</td>"));
            }

            if ($('#check5').is(':checked')) {
                row.append($("<td>" + parseFloat(Math.round(data.desvio_padrao.preco_abertura * 100) / 100).toFixed(2) + "</td>"));
            }

            if ($('#check6').is(':checked')) { 
                row.append($("<td>" + parseFloat(Math.round(data.desvio_padrao.preco_min * 100) / 100).toFixed(2) + "</td>"));
            }

            if ($('#check7').is(':checked')) { 
                row.append($("<td>" + parseFloat(Math.round(data.desvio_padrao.preco_max * 100) / 100).toFixed(2) + "</td>"));
            }
        
}

function drawln(data) {

        $("#bodyln").empty();



            for (var i = 0; i < data.ln.ajuste_atual.length; i++) {
                var row = $("<tr />");
                $("#bodyln").append(row); 

                if (data.ln.data) {           
                    row.append($("<td>" + data.ln.data[i] + "</td>"));
                }

                if ($('#check1').is(':checked')) {           
                    
                    row.append($("<td>" + parseFloat(Math.round(data.ln.ajuste_atual[i] * 100) / 100).toFixed(2) + "</td>"));

               
                    if (data.ln.retorno_simples[i] != 'N/A')
                        row.append($("<td>" + parseFloat(Math.round(data.ln.retorno_simples[i] * 100) / 100).toFixed(2) + "</td>"));
                    else
                        row.append($("<td>" + 'N/A' + "</td>"));
                

                    row.append($("<td>" + parseFloat(Math.round(data.ln.ln[i] * 100) / 100).toFixed(2) + "</td>"));
                
                    if (data.ln.ajuste_atual[i] != 'N/A')
                        row.append($("<td>" + parseFloat(data.ln.retorno_continuo[i]).toFixed(6) + "</td>"));
                    else
                        row.append($("<td>" + 'N/A' + "</td>"));

                } else {
                    alert("Os cálculos de ln são realizados somente com o preço de ajuste atual!");
                }
                

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

function show(data){

        removeColumn();
        
        var med = $("#medDia");
        if(med.is(':checked')){
            $("#tableMedDia").show();
            drawMediaDiaria(data);     
        }else{
            $("#tableMedDia").hide();
        }

        var med = $("#medSema");
        if(med.is(':checked')){
            $("#tableMedSema").show();
            drawMediaSemanal(data);
        }else{
            $("#tableMedSema").hide();
        }
        var med = $("#medMes");
        if(med.is(':checked')){
            $("#tableMedMes").show();
            drawMediaMensal(data);
        }else{
            $("#tableMedMes").hide();
        }

        var med = $("#medQuinze");
        if(med.is(':checked')){
            $("#tableMedQuinze").show();
            drawMediaQuinzenal(data);
        }else{
            $("#tableMedQuinze").hide();
        }

        var med = $("#desvio");
        if(med.is(':checked')){
            $("#tabledesvio").show();
            drawDesvio(data);
        }else{
            $("#tabledesvio").hide();
        }

        var med = $("#movel");
        if(med.is(':checked')){
            $("#tablemovel").show();
            drawMediaMovel(data);
            $("#graphDown").show();
        }else{
            $("#tablemovel").hide();
        }

        var med = $("#ln");
        if(med.is(':checked')){
            $("#tableln").show();
            drawln(data);
        }else{
            $("#tableln").hide();
        }

        var med = $("#rolagem");
        if(med.is(':checked')){
            
            var win = window.open('rolagem.html', '_blank');

            var form = $('#fAnalytics');
            $.ajax({
                data : form.serialize(),
                type : 'POST',
                cache: false,
                url : '/rolagem.html'
            })

            .done(function(data) {

               

            });

            event.preventDefault();


        }
}

function removeColumn(){

    var check = $("#check1");  
    if(check.is(':checked')){
        $(".ajuste_atual").show();
    } else {
        $(".ajuste_atual").hide();
    }

    var check = $("#check2");  
    if(check.is(':checked')){
        $(".variacao").show();
    } else {
         $(".variacao").hide();
    }

    var check = $("#check3");  
    if(check.is(':checked')){
        $(".contratos").show();
    } else {
        $(".contratos").hide();
    }

    var check = $("#check4");  
    if(check.is(':checked')){
        $(".volume").show();
    } else {
        $(".volume").hide();

    }

    var check = $("#check5");  
    if(check.is(':checked')){
        $(".abertura").show();
    } else {
        $(".abertura").hide();
    }

    var check = $("#check6");  
    if(check.is(':checked')){
        $(".minimo").show();
    } else {
        $(".minimo").hide();

    }

    var check = $("#check7");  
    if(check.is(':checked')){
        $(".maximo").show();
    } else {
        $(".maximo").hide();
    }

}

