//The main javascript file for thechillbar

function updateSignLog() {
    $.getJSON("/signlog", function(data) {
	$("#sign-log-row-template").tmpl(data).appendTo("#sign-log-body");
    });
}

$(function() {
    updateSignLog();
});