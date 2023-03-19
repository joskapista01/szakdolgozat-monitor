import socket
import json
from flask import Flask, request

socket.setdefaulttimeout(1)

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

    handshake_packet = b''
    handshake_packet += toVarIntBytes(HANDSHAKE_PACKET_ID) + toVarIntBytes(PROTOCOL_VERSION) + toVarIntBytes(server_hostname_length) + bytes(serverHostname,"utf-8") + serverPort.to_bytes(2,"little")+ toVarIntBytes(HANDSHAKE_REQUEST_ENUM)
    handshake_packet_size = len(handshake_packet)
    handshake_packet = toVarIntBytes(handshake_packet_size) + handshake_packet

    status_request_packet = b''
    status_request_packet+= toVarIntBytes(STATUS_REQUEST_PACKET_ID)
    status_request_packet_size = len(status_request_packet)
    status_request_packet = toVarIntBytes(status_request_packet_size) + status_request_packet

    with socket.socket() as client:
        try:
            client.connect(server_addr)
            print('Connected')
            client.sendall(handshake_packet)
            print('Handshake sent')
            client.sendall(status_request_packet)
            print('Status request sent')
            handshake_response = client.recv(8192)
            

            if b'"online"' in handshake_response:
                player_count = handshake_response.split(b'"online":')[1].split(b'}')[0].split(b',')[0].decode()
                return {
                    "alive": True,
                    "playerCount": player_count
                }
            return {
                "alive": False
            }

        except:
            return {
                "alive": False
            }



