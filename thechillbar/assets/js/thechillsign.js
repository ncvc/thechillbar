//The main javascript file for thechillsign

$(function() {
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