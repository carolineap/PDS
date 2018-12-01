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

    $('#ano').on('mouseenter', function(event) {

    var data1 = $('#data1').val();
    var data2 = $('#data2').val();

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
    });

});

function addSelect(data) {

    $('#ano').append($("<option value = 'all' id = 'op'>Todos</option>"));

    for (var i = 0; i < data.length; i++) {

        $('#ano').append($("<option value = " + data[i] + ">" + data[i] + "</option>"));
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