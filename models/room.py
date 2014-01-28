import json
from user import UserPool
from message import MessageQueue


class Room(object):
    """
        The class for a chat room, keeping track of the current in-room users in a normal dict using users' IDs as keys.
        It provides methods when a user joins or leaves the room and provides users search by IDs.
        It also saves latest messages sent by users, push them back to users.
    """
    def __init__(self):
        self.users = UserPool()
        self.messages = MessageQueue(self.push)

    def push(self, new_msg):
        """
            This is a callback function for message queue variable
            Push new messages back to current users in this room if any message available.
        """
        target = new_msg.target or self.users
        for user_id in target:
            self.users[user_id].ws.write_message(json.dumps(new_msg.to_dict()))