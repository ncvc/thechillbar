//The main javascript file for thechillbar
function banIP(ip) {
    $.post("/ban", { "ip" : ip })
}

function unbanIP(ip) {
    $.post("/unban", { "ip" : ip });
}

function showAdminSuccessAlert() {
    $("#admin-update-alert-placeholder").empty();
    data = {"type" : "alert alert-success",
            "id" : "admin-update-alert-success",
            "primary" : "Refreshed!",
            "secondary" : ""}
    $("#alert-template").tmpl(data).appendTo("#admin-update-alert-placeholder");
    setTimeout(function() { $(".alert").alert('close'); }, 3000);
}

function updateSignLog() {
    $.getJSON("/signlog", function(data) {
	$("#sign-log-table-body").empty();
	$.each(data, function(index, object) {
	    object['index'] = index;
	    var populated_template;
	    
	    if (object.banned) {
		populated_template = $("#banned-sign-log-row-template").tmpl(object).appendTo("#sign-log-table-body");
		var unban_button = $("#ip-entry-" + index + "-unban-button");	
		unban_button.click(function() {
		    unban_button.button('toggle');
		    $.post("/unban", {"ip" : object.ip})
			.done(function() { updateBannedIPList(); })
			.always(function() { unban_button.button('toggle');
				             updateAll(); });
		});
	    }
	    else {
		populated_template = $("#sign-log-row-template").tmpl(object).appendTo("#sign-log-table-body");
		var ban_button = $("#ip-entry-" + index + "-ban-button");
		ban_button.click(function() {
		    ban_button.button('toggle');
		    $.post("/ban", {"ip" : object.ip})
			.done(function() { updateBannedIPList(); })
			.always(function() { ban_button.button('toggle');
				             updateAll(); });
		});
		if (object.self) {
		    ban_button.hide();
		}
	    }
	});
    });
}

function updateBannedIPList() {
    $.getJSON("/bannedips", function(data) {
	$("#banned-ip-table-body").empty();
	$.each(data, function(index, object) {
	    object['index'] = index;
	    $("#banned-ip-row-template").tmpl(object).appendTo("#banned-ip-table-body");
	    var button = $("#banned-ip-entry-" + index + "-unban-button");
	    button.click(function() {
		button.button('toggle');
		$.post("/unban", {"ip" : object.ip})
		    .done(function() { updateBannedIPList(); })
		    .always(function() { button.button('toggle');
				         updateAll(); });
	    });
	});
    });
}

function updateAll() {
    updateSignLog();
    updateBannedIPList();
}

$(function() {
    updateAll();
    $("#refresh-sign-log-button").click(function(){ updateAll();
						    showAdminSuccessAlert();});
});