function submit_clicked(event){
  console.log("CLICKED");
  event.preventDefault();
  var content = $('#accomp_text').val();
  $.post_accomp(
    "post_1",
    content,
    handle_response
  );
}

function handle_response(data){
  console.log(data);
  $('#accomp').text(data);
  $('#accomp').show();
}

function associate_events(){
  $('#submit').click(submit_clicked);
}

$(document).ready(associate_events);
