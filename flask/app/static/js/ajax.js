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
			
		});

		event.preventDefault();

	});

});

function drawTable(data) {

    if (data.length == 0) {
         $("#ajusteTableB").append($("<p style='text-align: center'>Não há resultados.</p>")); 
    } else {

        for (var i = 0; i < data.length; i++) {
            drawRow(data[i]);
        }

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