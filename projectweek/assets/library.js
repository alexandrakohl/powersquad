console.log("hello")

$(document).ready(function() {
	var win = $(window);
	var doc = $(document);

	win.scroll(function() {
		// Vertical end reached?
    if($('#loading').is(':visible')){

      // New row
			var tr = $('<tr />').append($('<td class="date">Date</td>')).append($('<td class="textlib">Text</td>')).append($('<td class="star2">Star</td>')).append($('<td class="trash">Trash</td>')).appendTo($('#tableid'));

			// Current number of columns to create
			for (var i = 0; i < 3; ++i)
				tr.append($('<td />'));
		}
	});
});
$('#nomoreresults').hide()
