
  //Flow Selection Event Handler
  $('#jstree_div').on("changed.jstree", function (e, data) {
    var selected_nodes = data.selected
    for (var i = 0; i < selected_nodes.length; i++) {
        if (selected_nodes[i].startsWith("http")){
        console.log("Domain: " + selected_nodes[i]);
        } else {
          get_flow_meta(selected_nodes[i]);
        }
    }
  });

  function get_flow_meta(flow_id){
      //Returns Request Response Details
      $.ajax({
          type: 'POST',
          url: "/flow_meta",
          headers: {
              'X-Flow-ID': flow_id,
          },
          data: {
              'project': $('meta[name=project]').attr("content"),
          },
          error: function(xhr, status, error) {
            console.log("[ERROR]")
            console.log(status);
            console.log(xhr.responseText);
          },
          success: function(flow) { 
            //Request Meta
            var request = flow.request.method + " " + flow.request.url + " " + flow.request.http_version + "\n"
            for (var key in flow.request.headers) {
                request += key + ": " +  flow.request.headers[key] + "\n"; 
            }
            if (flow.request.content){
                request += "\n\n" + flow.request.content
            }
            $("#request").val(request);
            //Response Meta
            var response = flow.response.http_version + " " + flow.response.status_code + " " + flow.response.reason + "\n"
            for (var key in flow.response.headers) {
                response += key + ": " +  flow.response.headers[key] + "\n"; 
            }
            if (flow.response.content){
                response += "\n\n" + flow.response.content
            }
            $("#response").val(response);
          }
        });
  }
  $( document ).ready(function() {
    // Tree View and Context menu
    $(function () { $('#jstree_div').jstree({
    "plugins" : [
      "state", "wholerow"
    ]
    });});
  });


  function load_project(){
    var uri = $("#project_name option:selected").val();
    localStorage.clear();
    location.href = "/dashboard/" + uri;
  }
  function show_projects(){
    $("#projects").modal("show");
  }
  