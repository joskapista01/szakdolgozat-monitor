import socket
import json
from flask import Flask, request

socket.setdefaulttimeout(0.1)

app = Flask(__name__)

@app.get("/")
def getServerInfoRequest():
    if request.is_json:
        body = request.get_json()
        print(body)
        response = getServerInfo(serverHostname=body["serverHostname"], serverPort=body["serverPort"])
        return response
    else:
        return {"error": "Request must be json!"}

# converts an integer into a series if bytes representing the integer in VarInt format
def toVarIntBytes(number):
    numbers = b''
    while(number > 127):
        diff = number - ((number >> 7) << 7)
        numbers+=(diff + 128).to_bytes(1,'little')
        number = number >> 7

    numbers+=number.to_bytes(1,'little')
    return numbers

def getServerInfo(serverHostname, serverPort):

    server_addr = (serverHostname, serverPort)

    PROTOCOL_VERSION = 791
    HANDSHAKE_PACKET_ID = 0
    HANDSHAKE_REQUEST_ENUM = 1

    STATUS_REQUEST_PACKET_ID = 0


    server_hostname_length = len(serverHostname)

    # the packet sent to the minecraft server for handshaking
    handshake_packet = b''
    handshake_packet += toVarIntBytes(HANDSHAKE_PACKET_ID) + toVarIntBytes(PROTOCOL_VERSION) + toVarIntBytes(server_hostname_length) + bytes(serverHostname,"utf-8") + serverPort.to_bytes(2,"little")+ toVarIntBytes(HANDSHAKE_REQUEST_ENUM)
    handshake_packet_size = len(handshake_packet)
    handshake_packet = toVarIntBytes(handshake_packet_size) + handshake_packet

    # the status request packet we send to the server immediately after the handshake packet
    status_request_packet = b''
    status_request_packet+= toVarIntBytes(STATUS_REQUEST_PACKET_ID)
    status_request_packet_size = len(status_request_packet)
    status_request_packet = toVarIntBytes(status_request_packet_size) + status_request_packet

    with socket.socket() as client:
        # try to establish tcp connection with the server recieved in the request parameters
        try:
            client.connect(server_addr)
            # send tha handshake and the status request packets
            client.sendall(handshake_packet)
            client.sendall(status_request_packet)
            handshake_response = client.recv(8192)
            

            if b'"online"' in handshake_response:
                # get the player count from the response
                player_count = handshake_response.split(b'"online":')[1].split(b'}')[0].split(b',')[0].decode()
                return {
                    "alive": True,
                    "playerCount": player_count
                }
            return {
                "alive": False
            }
        # if we can't establish connection, we assume that the server is offline
        except:
            return {
                "alive": False
            }



