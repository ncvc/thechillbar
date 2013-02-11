//The main javascript file for thechillbar

$(function() {

    //Bar display code
    $("#blackout-button").click(
	function(){
	    $.post("/", { command : "blackout" } );
	}
    );

    $("#set-color-button").click(
	function(){
	    var red    = $("#red").val()
	    var green  = $("#green").val()
	    var blue   = $("#blue").val()
	    var commandString = "r:" + red + ",g:" + green + ",b:" + blue
	    $.post("/", { command : commandString });
	}
    );

    $("#color-wipe-button").click(
	function(){
	    $.post("/", { command : "colorwipe" } );
	}
    );

    $("#rainbow-button").click(
	function(){
	    $.post("/", { command : "rainbow" } );
	}
    );

    $("#rainbow-cycle-button").click(
	function(){
	    $.post("/", { command : "rainbowcycle" } );
	}
    );

    $("#droplets-button").click(
	function(){
	    $.post("/", { command : "droplets" } );
	}
    );

    $("#additive-cycle-button").click(
	function(){
	    $.post("/", { command : "additivecycle" } );
	}
    );

    $("#additive-fade-button").click(
	function(){
	    $.post("/", { command : "additivefade" } );
	}
    );

    $("#random-choice-button").click(
	function(){
	    $.post("/", { command : "randomchoice" } );
	}
    );

    //LED sign code
    $("#publish-button").click(
        function(){
            $.post("/sign", { message : $("#message-textarea").val() } );
        }
    );
    $("#reset-button").click(
        function(){
            var defualt_msg = "<red><7><speed3>welcome to\
<hold><green><7shadow><speed1><flash>thechillbar</flash>\
<rotate><amber><7><speed3><\\n>check us out at thechillbar.mit.edu"
            $.post("/sign", { message : defualt_msg } );
        }
    );
});