Chat Box
=======

A chat web app based on Tornado Web Framework and WebSocket.
[Tornado](https://github.com/facebook/tornado), as a non-blocking web server framework, provides an esay WebSocket interface for realtime apps like chating.

Front End
-------------
1. jQuery: DOM manipulations.
2. Bootstrap: UI.
3. Mousetrap: Keyboard bindings.
4. Moment.js: Time formating.


Back End
-------------
1. Tornado 3.2
2. WTForm 1.0.5: form validations.


Install
-------------
You have to install [pip](https://github.com/pypa/pip) first. Then use the requirements.txt in the root directory to install dependencies.
```
pip install -r requirements.txt
```


Feature
------------
1. Authentication based on secure cookies.
2. Message buffer for new users.
3. Realtime user list in a chat room.
4. There is no restriction on what language to chat in.
