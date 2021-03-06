function checkIfBookmarked(book){
console.log('checking if bookmarked')
    console.log($.cookie('csrftoken'));

$.ajax({
    url: '../ajax/bookmarked/',
    type: 'POST',
    data: {csrfmiddlewaretoken:  $.cookie('csrftoken'),
            'book' : book},
    success :function(json){
        
        console.log('chcking if bookmarked ' + json.status);
         if (json.status == true){
            
            $('#bookmarkicon').css('color', ''); 
            $('#bookmarkicon').css('text-shadow', ''); 

            
            console.log(' Changing the bookmark: bookmarked');
        }
        else{
                       
            $('#bookmarkicon').css('color', 'white'); 
            $('#bookmarkicon').css('text-shadow', ' -1px 0 black, 0 1px black, 1px 0 black, 0 -1px black'); 

            
            console.log(' Changing the bookmark: removed');

        }
    }

})
}
function checkIfIssued(book){
console.log('fetching ifIssued')
$.ajax({
    url: '../ajax/issued/',
    type: 'POST',
    data: {csrfmiddlewaretoken: $.cookie('csrftoken'),
            'book': book},

    success :function(json){
        console.log('printing object in ifIssued ' );
        
       
        if (json.status == true){
            $('#issueme').text('Issued');
            $('#issueme').removeAttr('hidden');
            $('#dueback').text('Due on: '   + json.due_back);
            console.log(' Changing the issued text');
        }

    }

})
}
function bookmarkme(book){
console.log('bookmark me is clicked', book)

$.ajax({
    url: '../ajax/bookmarkme/',
    type: 'POST',
    data: {csrfmiddlewaretoken: $.cookie('csrftoken'),
            'book': book},

    success :function(json){
        console.log('printing object in bookmarkme ' + json.status );
        
       
        if (json.status == 'bookmarked'){
            
            $('#bookmarkicon').css('color', ''); 
            $('#bookmarkicon').css('text-shadow', ''); 

            
            console.log(' Changing the bookmark: bookmarked');
        }
        else{
                       
            $('#bookmarkicon').css('color', 'white'); 
            $('#bookmarkicon').css('text-shadow', ' -1px 0 black, 0 1px black, 1px 0 black, 0 -1px black'); 

            
            console.log(' Changing the bookmark: removed');

        }

    }

    

})
$(document).ajaxComplete(
    fetch_bookmarks())




}

function openCity(cityName) {
    console.log('one of the buttons clicked')
    var i;
    var x = document.getElementsByClassName('city');
    for (i = 0; i < x.length; i++) {
        x[i].style.display = 'none'; 
    }
    document.getElementById(cityName).style.display = 'block'; 
    fetch_bookmarks()
    
}    

function fetch_bookmarks(){
    console.log('fetching bookmarks in fetch_bookmarks function')
    $.ajax({
        url: '../ajax/bookmarks/',
        type: 'POST',
        data: {csrfmiddlewaretoken: $.cookie('csrftoken')},

        success :function(json){
            
            console.log(json);
            var data1 ;
            $('#bookmarks').empty();
            $.each(json, function(index,data1){
                console.log(data1);
                var str = '<li><a href=' + data1['url'] + '>' + data1['title']
                str += "<a id='bookmarkme' href='javascript:void(0)' onclick='bookmarkme( '{{ book }}' )' title='bookmark'>"
                //str += "<span id='bookmarkicon' class='glyphicon glyphicon-bookmark' style='font-size: 10px;color:white;text-shadow: -1px 0 black, 0 1px black, 1px 0 black, 0 -1px black;'></span>"
                //str += "hello"
                str += "</a><li>"
                str += "<hr style='margin:0.05px; border-color:#3d3d29'>"
                
                console.log(str)
                $('#bookmarks').append(str);
            });
        }

    })
}

function query_text(){
    var q = $('#query').val();

    $.ajax({
        url: '../search',
        method: 'GET',
        data: {
            'q': q},
        success: function(json){
            console.log(json);
            var str = "";
            $.each(json['book'],function(index,data1){
                str += "<option value=\"" + data1['title'] + "\">" + data1['title'] + "</option>"
            });
            console.log(str);
            $('#search-items').innerHTML = str.toString();
            $('#search-items').selectedIndex=0;
            console.log($('#search-items'))
        }


    })
}

