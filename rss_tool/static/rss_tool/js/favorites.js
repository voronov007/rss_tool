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
                if (json.removed === true)
                {
                    location.reload();
                }
                else{
                    alert("Error occurred!");
                }

            }
        });

        return false;
    });
});