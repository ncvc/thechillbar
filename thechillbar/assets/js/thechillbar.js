//The main javascript file for thechillbar

function showSuccessAlert() {
    var data = {"type" : "alert alert-success",
		"id" : "led-sign-alert-success",
		"primary" : "Success!",
		"secondary" : "Your message has been sent to the sign."}
    var a = $("#alert-template").tmpl(data);
    a.appendTo("#led-sign-alert-placeholder");
    setTimeout(function() { a.alert('close'); }, 3000);
}

function showErrorAlert() {
    var data = {"type" : "alert alert-error",
	    "id" : "led-sign-alert-error",
	    "primary" : "Error!",
	    "secondary" : "Oops, spomething went wrong. Please try again."}
    var a = $("#alert-template").tmpl(data);
    a.appendTo("#led-sign-alert-placeholder");
    setTimeout(function() { a.alert('close'); }, 3000);
}

function showOverLimitAlert() {
    var data = {"type" : "alert alert-error",
		"id" : "led-sign-alert-error",
		"primary" : "Limit Reached!",
		"secondary" : "Come back in a few minutes and try again."}
    var a = $("#alert-template").tmpl(data); 
    a.appendTo("#led-sign-alert-placeholder");
    setTimeout(function() { a.alert('close'); }, 3000);
}


$(function() {

    //Bar display code
    $("#blackout-button").click(
	function(){
	    $.post("/display", { command : "blackout",
				 'csrfmiddlewaretoken' : $.cookie('csrftoken') } );
	}
    );

    $("#wipe-button").click(
	function(){
	    $.post("/display", { command : "colorwipe",
				 'csrfmiddlewaretoken' : $.cookie('csrftoken') } );
	}
    );

    $("#fade-button").click(
	function(){
	    $.post("/display", { command : "rainbow",
				 'csrfmiddlewaretoken' : $.cookie('csrftoken') } );
	}
    );

    $("#rainbow-button").click(
	function(){
	    $.post("/display", { command : "rainbowcycle",
				 'csrfmiddlewaretoken' : $.cookie('csrftoken') } );
	}
    );

    $("#color-cycle-button").click(
	function(){
	    $.post("/display", { command : "colorrotate", 
				 'csrfmiddlewaretoken' : $.cookie('csrftoken') } );
	}
    );

    $("#color-chase-button").click(
	function(){
	    $.post("/display", { command : "colorchase",
				 'csrfmiddlewaretoken' : $.cookie('csrftoken') } );
	}
    );

    $("#additive-button").click(
	function(){
	    $.post("/display", { command : "additivecycle", 
			       'csrfmiddlewaretoken' : $.cookie('csrftoken') } );
	}
    );

    $("#droplets-button").click(
	function(){
	    $.post("/display", { command : "droplets",
			       'csrfmiddlewaretoken' : $.cookie('csrftoken') } );
	}
    );

    $("#random-choice-button").click(
	function(){
	    $.post("/display", { command : "randomchoice",
			       'csrfmiddlewaretoken' : $.cookie('csrftoken') } );
	}
    );

    //LED sign code
    $("#publish-button").click(
        function(){
            $.post("/sign", { 'message' : $("#message-textarea").val(),
			      'csrfmiddlewaretoken' : $.cookie('csrftoken')})
		.done(function() { showSuccessAlert(); })
		.error(function(jqXHR, status, error) { 
		    if (jqXHR.status == 403){
			showOverLimitAlert();
		    } else {
			showErrorAlert();
		    }
		});
        }
    );

    $("#reset-button").click(
        function(){
	    $.post("/sign", { 'message' : '',
			      'csrfmiddlewaretoken' : $.cookie('csrftoken') })
		.done(function() { showSuccessAlert(); })
		.error(function(jqXHR, status, error){
		    if (jqXHR.status == 403){
			showOverLimitAlert();
		    } else {
			showErrorAlert();
		    }
		});
        }
    );
});