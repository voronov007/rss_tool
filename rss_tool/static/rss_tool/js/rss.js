$(document).ready(function() {
    console.log( "ready!" );
    // Setup AJAX
    $(function () {
        $.ajaxSetup({
            headers: { "X-CSRFToken": getCookie("csrftoken") }
        });
    });

    $(".add_comment").click(function(){
        let button = $(this);
        let form = button.closest("form");
        let data = form.serializeArray();
        console.log(data);
        console.log(button.attr("id"));
        console.log(window.location.href);

        $.ajax({
            url : window.location.href,
            type : form.attr("method"),
            dataType: 'json',
            data : {'form' : data, "feed_id": button.attr("id")},

            success : function (json) {
                console.log(json);
            }
        });

        return false;
    });

     $(".bookmark").click(function(){
        $.ajax({
            url : window.location.href,
            type : "POST",
            dataType: 'json',
            data : {'bookmark' : true, "feed_id": $(this).attr("name")},

            success : function (json) {
                console.log(json);
            }
        });

        return false;
    });
});

// Getting a cookie by name
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

