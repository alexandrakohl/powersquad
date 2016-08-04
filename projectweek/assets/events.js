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
  accomp_array = data.split(',')
  $('#accomp1').text(accomp_array[0]);
  $('#accomp2').text(accomp_array[1]);
  $('#accomp3').text(accomp_array[2]);

}

function associate_events(){
  $('#submit').click(submit_clicked);
}

$(document).ready(associate_events);
