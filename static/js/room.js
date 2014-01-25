$(document).ready(function() {
	var ws = new WebSocket("ws://localhost:8888/chat");
	var msg_input = $("#msg_input");
	var msg_output = $("#msg_output");
	ws.onopen = function() {
		// after sucessfully connection, enable message input for users
		msg_input.prop('disabled', false);
	};

	ws.onmessage = function(evt) {
		var msg = JSON.parse(evt.data);
		msg.date = new Date(msg.timestamp);
		// add message to output area
		msg_output.val(msg_output.val() + "\n" + msg.date.toString() + "\n" + msg.content);
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
});