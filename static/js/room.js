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
		var wrapper = JSON.parse(evt.data);
		var msgs = wrapper.messages;
		console.log(wrapper);
		// type checking
		if (wrapper.type == 0) {
			// join
			var msg = msgs[0];
			add_user(msg.user_id, msg.content);
		} else if (wrapper.type == 1) {
			// leaves
			// add message to output area
			var msg = msgs[0];
			remove_user(msg.user_id);
		} else if (wrapper.type == 2) {
			// exist
			for (var i = msgs.length - 1; i >= 0; i--) {
				add_user(msgs[i].user_id, msgs[i].content);
			}
		} else {
			// new chat or cache chat
			// 3 or 4
			for (var i = 0; i < msgs.length; ++i) {
				var msg = msgs[i];
				add_message(msg.user_id, msg.timestamp, msg.content);
			}
		}
	}
	// simulating summit event, 'enter' key press
	msg_input.keypress(function(e) {
		// 13 is the key code for return
		if (e.which == 13) {
			if (msg_input.val() === "") {
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

	function add_message(id, timestamp, content) {
		var date = new Date(timestamp);
		// construct a date string to display
		var dateString = "";
		dateString += (date.getMonth() + 1) + "/" + date.getDate() + " ";
		dateString += date.getHours() + ":" + date.getMinutes();

		msg_output.val(msg_output.val() +
			"\n" + dateString + "\n" +
			users_pool[id].name + ": " + content);
	}

	var users_pool = {};

	function add_user(id, user) {
		if (id in users_pool) {
			// do nothing if already exist
		} else {
			// add to pool
			users_pool[id] = user;
			// add UI
			var div = $("<div/>");
			div.attr("id", id);
			div.addClass("user");
			div.html(user.name);
			user_list.append(div);

		}
	}

	function remove_user(id) {
		if (id in users_pool) {
			// remove from pool
			delete users_pool[id];
			// remove from divs
			user_list.children("#" + id).remove();
		}
	}
});