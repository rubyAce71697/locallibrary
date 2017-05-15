    function checkIfBookmarked(){
      console.log("fetching bookmarks")
          console.log($.cookie("csrftoken"));
      
      $.ajax({
          url: "../ajax/bookmarked/",
          type: "POST",
          data: {csrfmiddlewaretoken:  $.cookie("csrftoken")},
          success :function(json){
              
              console.log(json);
 
          }

      })
    }
    function checkIfIssued(){
      console.log("fetching bookmarks")
      $.ajax({
          url: "../ajax/issued/",
          type: "POST",
          data: {csrfmiddlewaretoken: $.cookie("csrftoken")},

          success :function(json){
              console.log(json);
          }

      })
    }

      function openCity(cityName) {
            console.log("one of the buttons clicked")
            var i;
            var x = document.getElementsByClassName("city");
            for (i = 0; i < x.length; i++) {
                x[i].style.display = "none"; 
            }
            document.getElementById(cityName).style.display = "block"; 
            fetch_bookmarks()
            
        }    

        function fetch_bookmarks(){
            console.log("fetching bookmarks")
            $.ajax({
                url: "../ajax/bookmarks/",
                type: "POST",
                data: {csrfmiddlewaretoken: $.cookie("csrftoken")},

                success :function(json){
                    
                    console.log(json);
                    var data1 ;
                    $("#bookmarks").empty();
                    $.each(json, function(index,data1){
                        console.log(data1);
                        $("#bookmarks").append("<li><a href=" + data1['url'] + ">" + data1['title'] + "</li>");
                    });
                }

            })
        }