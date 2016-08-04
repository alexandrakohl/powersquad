function submit_clicked(event){
  console.log("CLICKED");
  event.preventDefault();
  var content = $('#content').val();
  $.post_accomp(
    "post_1",
    content,
    handle_response
  );
}

function handle_response(data){
  console.log(data);
  $('#result').text(data);
  $('#result').show();
}

function associate_events(){
  $('#submit').click(submit_clicked);
}

$(document).ready(associate_events);
