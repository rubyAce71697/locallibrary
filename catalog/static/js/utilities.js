function checkIfBookmarked(book){
console.log("checking if bookmarked")
    console.log($.cookie("csrftoken"));

$.ajax({
    url: "../ajax/bookmarked/",
    type: "POST",
    data: {csrfmiddlewaretoken:  $.cookie("csrftoken"),
            "book" : book},
    success :function(json){
        
        console.log("chcking if bookmarked " + json);
        if (json == true){
            $("#bookmarkme").text("Bookmarked");
            console.log(" Changing the bookmark text");
        }
    }

})
}
function checkIfIssued(book){
console.log("fetching ifIssued")
$.ajax({
    url: "../ajax/issued/",
    type: "POST",
    data: {csrfmiddlewaretoken: $.cookie("csrftoken"),
            "book": book},

    success :function(json){
        console.log("printing object in ifIssued " );
        
       
        if (json.status == true){
            $("#issueme").text("Issued");
            $("#issueme").removeAttr("hidden");
            $("#dueback").text(json.due_back);
            console.log(" Changing the issued text");
        }

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
    console.log("fetching bookmarks in fetch_bookmarks function")
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