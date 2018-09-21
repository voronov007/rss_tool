$(document).ready(function() {
    console.log( "ready!" );
    // Setup AJAX
    $(function () {
        $.ajaxSetup({
            headers: { "X-CSRFToken": getCookie("csrftoken") }
        });
    });

    $(".remove_bookmark").click(function(){
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