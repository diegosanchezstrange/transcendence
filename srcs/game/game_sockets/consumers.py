import json
 
from channels.generic.websocket import WebsocketConsumer
 
class LobbyConsumer(WebsocketConsumer):
 
    # Set to True to automatically port users from HTTP cookies
    # (you don't need channel_session_user, this implies it)
    # http_user = True
 
    # def connection_groups(self, **kwargs):
    #     """
    #     Called to return the list of groups to automatically add/remove
    #     this connection to/from.
    #     """
    #     return ["lobby"]
 
    def connect(self):
        """
        Perform things on connection start
        """
        # self.message.reply_channel.send({"accept": True})
        # pass
        self.accept()
 
    def receive(self, text_data):
        """
        Called when a message is received with either text or bytes
        filled out.
        """
        # http_user = True
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        self.send(text_data=json.dumps({
            'message': message
        }))
 
 
    def disconnect(self, message, **kwargs):
        """
        Perform things on connection close
        """
        pass