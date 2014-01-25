$(document).ready(function() {
	var ws = new WebSocket("ws://localhost:8888/chat");
	ws.onopen = function() {
		ws.send("Hello World");
	};

	ws.onmessage = function(evt) {
		alert(evt.data);
	}
});