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
        let comment = form.find("input[type='text']").val().trim();
        if (comment.length < 10){
            alert("Comment has less than 10 symbols");
            return false;
        }
        else if (comment.length > 100){
            alert("Comment is too long!");
            return false;
        }
        //let data = form.serializeArray();

        $.ajax({
            url : window.location.href,
            type : form.attr("method"),
            dataType: 'json',
            data : {'comment' : comment, "feed_id": button.attr("id")},

            success : function (json) {
                console.log(json);
                if (json.success === false){
                    alert("Incorrect comment. Please fix it")
                }
                else{
                    let feed_id = json.feed_id;
                    // add comments counter + 1
                    let badge = $("button[data-target='#collapse_" + feed_id +"'] span")
                    badge.html(parseInt(badge.text(), 10) + 1)
                    // clean up comment input
                    let form = $("#form_" + feed_id);
                    form.find("input[type='text']").val("");
                    // insert comment in main comments list
                    let div_text = "<div class='card card-body'>" + json.email + "<br>" + json.comment + "</div>";
                    $(div_text).insertBefore(form);
                }
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
                let feed_id = json.feed_id;
                let bookmark = $("a[name='" + feed_id + "']");
                // change bookmark value
                if (bookmark.hasClass("added")){
                    bookmark.html("Add to favorites");
                    bookmark.removeClass("added").addClass("removed");
                }
                else{
                    bookmark.html("Remove from favorites");
                    bookmark.removeClass("removed").addClass("added");
                }

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

