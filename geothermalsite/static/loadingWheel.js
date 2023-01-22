
$(document).ready(function () {
    console.log("Please wait 1...");

    $("#tempvstimeform").submit(function (e) {
        e.preventDefault();
        var data = $(this).serialize();
        // Show the loading spinner when the request is being processed
        $("#loading-wheel-box").show();
        console.log("Please wait 2...");

        $.ajax({
            type: "POST",
            url: "/tempvstime/",
            data: data,
            success: function (response) {
                // Do something with the response
                // ...

                // Hide the loading spinner when the request is done
                $("#loading-wheel-box").hide();
            },
            error: function (response) {
                // Handle errors
                // ...
                // Hide the loading spinner when the request is done
                $("#loading-wheel-box").hide();
            }
        });
    });
});
