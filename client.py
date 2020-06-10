import socket
import threading
import json
import os
import time

class Signal:
    REGISTER_AND_WAIT = 'register' # register and wait for peer to connect to you
    REGISTER_AND_CONNECT = 'connect' # register and send the peername you want to connect to
    ACK_REGISTER = 'ack_register'
    PEER_INFO = 'peer_info'
    PUNCH = 'punch'
    ACK_PUNCH = 'ack_punch'
    PING = 'ping'
    CHAT = 'chat_msg'


class State:

    def __init__(self, client):
        self.client = client

    def handle(self, message):
        raise NotImplementedError

    def log_unhandled_signal(self, signal: str):
        print(f"[Warning] Ignoring signal: {signal} recieved in state: {type(self).__name__} ")


class InitialState(State):
    def __init__(self, client):
        super().__init__(client)

    def handle(self, message):
        signal = message.get('signal')
        if signal == Signal.ACK_REGISTER: # client is the initiator of connection
            self.client.change_state(RegisteredState)
        elif signal == Signal.PEER_INFO: # client is not the initiator 
            self.client.set_peer(peername=message.get('peer'), peer_addr=message.get('peer_addr'))
            self.client.change_state(PeerConnectingState)
        else:
            self.log_unhandled_signal(signal)

class RegisteredState(State):

    def __init__(self, client):
        super().__init__(client)
        self.client.set_ping_addr(self.client.server_addr)
        self.client.enable_ping_activity(True) # start server pings

    def handle(self, message):
        signal = message.get('signal')
        if signal == Signal.PEER_INFO:
            self.client.set_peer(peername=message.get('peer'), peer_addr=message.get('peer_addr'))
            self.client.change_state(PeerConnectingState)
        else:
            self.log_unhandled_signal(signal)

class PeerConnectingState(State):

    def __init__(self, client):
        super().__init__(client)
        self.client.enable_ping_activity(False) # stop server pings
        self.client.enable_punch_activity(True) # start UDP hole punching

    def handle(self, message):
        signal = message.get('signal')
        if signal == Signal.ACK_PUNCH: # punch cycle complete
            self.client.change_state(PeerConnectedState)
        elif signal == Signal.PUNCH: # hole punching successful
            self.client.send_msg(signal=Signal.ACK_PUNCH)
            self.client.change_state(PeerConnectedState)
        else:
            self.log_unhandled_signal(signal)

class PeerConnectedState(State):
    '''
    This is the final state the client needs to be in
    '''
    def __init__(self, client):
        super().__init__(client)
        self.client.enable_punch_activity(False) # stop UDP hole punching
        self.client.set_ping_addr(self.client.peer_addr, interval=10)
        self.client.enable_ping_activity(True) # start peer pings

    def handle(self, message):
        '''
        Client handles the messages
        '''
        pass


class Client:
    peer_addr = None
    ping_addr = None
    perform_ping = False
    perform_punch = False

    def __init__(self, username, server_addr, peername=None):
        self.state = InitialState(self)
        self.username = username
        self.server_addr = server_addr
        self.peername = peername
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        if self.peername:
            self.sock.sendto(
                self._create_message(
                    signal = Signal.REGISTER_AND_CONNECT,
                    user = self.username,
                    peer = self.peername,
                ),
                self.server_addr
            )          
        else:
            self.sock.sendto(
                self._create_message(
                    signal = Signal.REGISTER_AND_WAIT,
                    user = self.username
                ),
                self.server_addr
            )

        while type(self.state) != PeerConnectedState:
            message = self.__get_response()
            self.state.handle(message)

        print(f'Connection Established Between users {self.username}:{self.peername}')

    def _create_message(self, signal, **kwargs):
        return json.dumps(dict( signal=signal, **kwargs)).encode('utf-8')

    def __get_response(self, buff_size=1024):
        response = self.sock.recv(buff_size)
        return json.loads(response.decode('utf-8'))

    def __ping(self):
        self.sock.sendto(
            self._create_message(signal=Signal.PING),
            self.ping_addr
        )
        if self.perform_ping:
            threading.Timer(self.ping_interval, self.__ping).start()

    def __punch(self):
        self.sock.sendto(
            self._create_message(signal=Signal.PUNCH),
            self.peer_addr
        )
        if self.perform_punch:
            threading.Timer(interval=0.5, function=self.__punch).start()
    
    def change_state(self, state: State):
        # DEBUG: print(f'Changing state {type(self.state).__name__} -> {state.__name__}')
        self.state = state(client=self)

    def get_state(self):
        return self.state

    def set_peer(self, peername, peer_addr: tuple):
        self.peername = peername
        self.peer_addr = tuple(peer_addr)

    def set_ping_addr(self, addr: tuple, interval: int=5):
        self.ping_addr = addr
        self.ping_interval = interval
    
    def enable_ping_activity(self, perform: bool):
        self.perform_ping = perform
        if self.perform_ping:
            self.__ping()

    def enable_punch_activity(self, perform: bool):
        self.perform_punch = perform
        if self.perform_punch:
            self.__punch()
    
    def send_msg(self, signal=Signal.CHAT, msg=''): # Send msg to peer
        self.sock.sendto(
            self._create_message(signal=signal, msg=msg),
            self.peer_addr
        )
