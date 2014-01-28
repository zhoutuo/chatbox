import time
import json
import tornado.web
import tornado.websocket
from forms import RegistrationForm
from models.user import User
from models.room import Room
from models.message import Message, MessageType, MessageWrapper, MessageWrapperType
from ext import TornadoMultiDict

# this global variable will act as a pseudo-db
registeredUsers = {}


class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        """
            This method will return None if user_id is not presented
            Or the id cannot be found inside the room.
        """
        id = self.get_secure_cookie('user_id')
        if id in registeredUsers:
            return registeredUsers[id]


class RoomHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render('room.html')


class RegisterHandler(BaseHandler):
    def get(self):
        # feed new registration form to users
        form = RegistrationForm()
        self.render('register.html', form=form)

    def post(self):
        form = RegistrationForm(TornadoMultiDict(self.request.arguments))
        if form.validate():
            # generate new user in the memory from POST data
            user = User(form.name.data, form.birthday.data, form.gender.data, form.country.data)
            # save the user in the memory, supposingly save it in the db of sorts
            registeredUsers[user.id] = user
            # set the client cookie, since no expires_days, it is a session cookie
            self.set_secure_cookie('user_id', user.id, expires_days=30)
            # redirect to room page
            self.redirect('/')
        else:
            # return the populated form back to users with corresponding errors
            self.render('register.html', form=form)


class ChatHandler(tornado.websocket.WebSocketHandler):
    # class variable
    room = Room()

    def __init__(self, *args, **kwargs):
        super(ChatHandler, self).__init__(*args, **kwargs)
        self._user = None

    def open(self):
        id = self.get_secure_cookie('user_id')
        self._user = registeredUsers[id]
        # passing web socket ref to user
        self._user.ws = self
        # generate a list excluding the user's id
        ids = ChatHandler.room.users.keys()
        # Add the new user into the room
        ChatHandler.room.users.join(self._user)
        # send existing users to the new user
        ChatHandler.room.messages.enque(MessageWrapper(
            MessageWrapperType.Exist,
            messages=[Message(
                MessageType.User,
                id,
                time.time(),
                ChatHandler.room.users[id].profile()
            ) for id in ids],
            target=[self._user.id]
        )
        )
        # send join message to users about the joining
        ChatHandler.room.messages.enque(MessageWrapper(
            MessageWrapperType.Join,
            [Message(MessageType.User, self._user.id, time.time(), self._user.profile())]
        ))
        # send existing messages to the new user
        ChatHandler.room.messages.enque(MessageWrapper(
            MessageWrapperType.CacheChat,
            messages=[message for message in ChatHandler.room.messages.cache()],
            target=[self._user.id]
        ))

    def on_message(self, message):
        # receive front end messages
        msg = json.loads(message)
        ChatHandler.room.messages.enque(MessageWrapper(
            MessageWrapperType.NewChat,
            [Message(MessageType.Chat, self._user.id, msg['timestamp'], msg['content'])]
        ))

    def on_close(self):
        # once on leave, kick user out of the room
        if self._user:
            # make it leave the room first
            ChatHandler.room.users.leave(self._user)
            # send the leave message
            ChatHandler.room.messages.enque(MessageWrapper(
                MessageWrapperType.Leave,
                [Message(MessageType.User, self._user.id, time.time())]
            ))
