function submit_clicked(event){
  console.log("CLICKED");
  event.preventDefault();
  var content = $('#accomp_text').val();
  $.post(
    "post_accomp",
    content,
    handle_response
  );
}

function handle_response(data){
  console.log(data);
  $('#accomp1').text(data);
  $('#accomp2').text('accomp1');
  $('#accomp3').text('accomp2');

}

function associate_events(){
  $('#submit').click(submit_clicked);
}

$(document).ready(associate_events);
