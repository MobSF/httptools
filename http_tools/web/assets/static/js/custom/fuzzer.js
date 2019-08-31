$("#fz").submit(function (event) {
  event.preventDefault(); //prevent default action 
  var post_url = $(this).attr("action"); //get form action url
  var request_method = $(this).attr("method"); //get form GET/POST method
  var form_data = $(this).serialize(); //Encode form elements for submission

  $.ajax({
    url: post_url,
    type: request_method,
    data: form_data
  }).done(function (response) {
    if (response.error){
        $.growl({ title: "Send to Fuzzer", message: "Failed to send requests" + response.error, style: "error" });
    } else {
      $.growl({ title: "Send to Fuzzer", message: "Requests queued and repeating...", style: "notice" });
    }
  });
});
