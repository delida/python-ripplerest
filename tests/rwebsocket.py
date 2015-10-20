# -*- coding:utf-8 -*-
import config
import websocket
import json
from robotbrain import robotbrain

class WebSocketHandler:
    def __init__(self, ws_address):
        websocket.enableTrace(True)
        self.ws = websocket.WebSocketApp(ws_address,
            on_message = self.on_message,
            on_error = self.on_error,
            on_close = self.on_close)
        self.ws.on_open = self.on_open
        #print self.ws.__dict__
        self.ws.run_forever()

    def on_open(self, ws):
        print "on_open:::"

    def on_message(self, ws, message):
        #print "on_message:::", message
        response = json.loads(message.decode('utf-8'))
        robotbrain.receive_socket_data(response)

    def on_error(self, ws, error):
        print "on_error:::", error

    def on_close(self, ws):
        pass

websocket_handler = WebSocketHandler(config.web_socket_address)