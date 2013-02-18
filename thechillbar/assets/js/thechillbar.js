//The main javascript file for thechillbar

function showSuccessAlert() {
    data = {"type" : "alert alert-success",
	    "id" : "led-sign-alert-success",
	    "primary" : "Success!",
	    "secondary" : "Your message has been sent to the sign."}
    $("#alert-template").tmpl(data).appendTo("#led-sign-alert-placeholder");
    setTimeout(function() { $(".alert").alert('close'); }, 3000);
}

function showErrorAlert() {
    data = {"type" : "alert alert-error",
	    "id" : "led-sign-alert-error",
	    "primary" : "Error!",
	    "secondary" : "Oops, spomething went wrong. Please try again."}
    $("#alert-template").tmpl(data).appendTo("#led-sign-alert-placeholder");
    setTimeout(function() { $(".alert").alert('close'); }, 3000);
}

$(function() {

    //Bar display code
    $("#blackout-button").click(
	function(){
	    $.post("/display", { command : "blackout" } );
	}
    );

    $("#wipe-button").click(
	function(){
	    $.post("/display", { command : "colorwipe" } );
	}
    );

    $("#fade-button").click(
	function(){
	    $.post("/display", { command : "rainbow" } );
	}
    );

    $("#rainbow-button").click(
	function(){
	    $.post("/display", { command : "rainbowcycle" } );
	}
    );

    $("#color-cycle-button").click(
	function(){
	    $.post("/display", { command : "colorrotate" } );
	}
    );

    $("#color-chase-button").click(
	function(){
	    $.post("/display", { command : "colorchase" } );
	}
    );

    $("#additive-button").click(
	function(){
	    $.post("/display", { command : "additivecycle" } );
	}
    );

    $("#droplets-button").click(
	function(){
	    $.post("/display", { command : "droplets" } );
	}
    );

    $("#random-choice-button").click(
	function(){
	    $.post("/display", { command : "randomchoice" } );
	}
    );

    //LED sign code
    $("#publish-button").click(
        function(){
            $.post("/sign", { message : $("#message-textarea").val() })
		.done(function() { showSuccessAlert(); })
		.error(function() { showErrorAlert(); });
        }
    );

    $("#reset-button").click(
        function(){
            var defualt_msg = "<red><7><speed3>welcome to\
<hold><green><7shadow><speed1><flash>thechillbar</flash>\
<rotate><amber><7><speed3><\\n>check us out at thechillbar.mit.edu"
            $.post("/sign", { message : defualt_msg } )
		.done(function() { showSuccessAlert(); })
		.error(function() { showErrorAlert(); });
        }
    );
});