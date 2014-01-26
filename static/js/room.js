$(document).ready(function() {
	var chat_panel = $("#chat_panel");
	var user_list = $("#user_list");

	var ws = new WebSocket("ws://127.0.0.1:8888/chat");
	var msg_input = $("#msg_input");
	var msg_output = $("#msg_output");
	ws.onopen = function() {
		// after sucessfully connection, enable message input for users
		msg_input.prop('disabled', false);
	};

	ws.onmessage = function(evt) {
		var msg = JSON.parse(evt.data);
		console.log(msg);
		msg.date = new Date(msg.timestamp);
		// construct a date string to display
		var dateString = "";
		dateString += (msg.date.getMonth() + 1) + "/" + msg.date.getDate() + " ";
		dateString += msg.date.getHours() + ":" + msg.date.getMinutes();
		// type checking
		if (msg.type == 0) {
			// join
			add_user(msg.user_id, msg.content);
		} else if (msg.type == 1) {
			// chat
			// add message to output area
			msg_output.val(msg_output.val() + "\n" + dateString + "\n" + msg.content);			
		} else if (msg.type == 2) {
			// leave
		} else {
			// exist
			for (var i = msg.content.length - 1; i >= 0; i--) {
				add_user(msg.user_id[i], msg.content[i]);
			}
		}
	}
	// simulating summit event, 'enter' key press
	msg_input.keypress(function(e) {
		// 13 is the key code for return
		if (e.which == 13) {
			if(msg_input.val() === "") {
				alert("No Empty Message");
			} else {
				// contrust a message object
				var message = {};
				message.content = msg_input.val();
				message.timestamp = Date.now();
				// send in a form of JSON
				ws.send(JSON.stringify(message));
				// clear the input
				msg_input.val("");
			}
			// prevent form from submitting
			e.preventDefault();
		}
	});

	var users_pool = {};
	function add_user(id, user) {
		if (id in users_pool) {
			// do nothing if already exist
		} else {
			// add to pool
			users_pool[id] = user;
			// add UI
			var div = $("<div/>");
			div.addClass("user");
			div.html(user.name);
			user_list.append(div);

		}
	}
});