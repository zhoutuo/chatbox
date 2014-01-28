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
		if (id in users_pool) {
			// construct a date string to display
			var dateString = moment(timestamp).format("MM/DD HH:mm");

			var chat_div = $("<div/>");
			chat_div.addClass("chat_message");
			// 
			var name_span = $("<span/>");
			name_span.addClass("chat_name");
			name_span.html(users_pool[id].name);
			// 
			var timestamp_span = $("<span/>");
			timestamp_span.addClass("chat_time");
			timestamp_span.html(dateString);			
			// 
			var content_div = $("<div/>");
			content_div.addClass("chat_content");
			content_div.html(content);

			chat_div.append(name_span);
			chat_div.append(timestamp_span);			
			chat_div.append(content_div);

			msg_output.append(chat_div);
			// scroll to bottm
			msg_output.scrollTop(msg_output[0].scrollHeight);
		}
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
			// add profile information to Bootstrap popover
			div.attr("data-placement", "auto");
			div.attr("data-toggle", "popover");
			div.attr("data-original-title", "Profile");
			div.attr("data-content", function() {
				var gender = "Gender: " + user.gender + "<br>";
				var birthday = "Birthday: " + user.birthday + "<br>";
				var country = "Country: " + user.country;
				return gender + birthday + country;
			});
			// enable popover feature
			div.popover({
				html: true,
				trigger: "hover",
				container: "body"				
			});

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