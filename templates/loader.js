
$( document ).ready(function() {
    console.log( "ready now!" );
    $.ajax({
        url: "/data",
        cache: false,
        success: function(resp){
            console.log('success');
            var response = $.parseJSON(resp);
            var table = $('<table id="dynatable"></table>');
            var header =$('<th>Serial</th><th>state</th><th>cases</th><th>cured</th><th>death</th>');
            table.append(header);
            $.each(response, function(i, item){
                var row = $('<tr>').append(
                    $('<td>').text(item.serial),
                    $('<td>').text(item.state),
                    $('<td>').text(item.cases),
                    $('<td>').text(item.cured),
                    $('<td>').text(item.death)
                    );
                console.log('adding: '+item.state);
                table.append(row);
            });
            $('#optable').append(table);
        },
        failure: function(e){
            console.error(e);
        }
      });
});