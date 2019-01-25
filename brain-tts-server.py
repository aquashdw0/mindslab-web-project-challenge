import socket
import sys
import json
import re


class stt_sock():
    def __init__(self):
        self.host = "127.0.0.1"
        self.port = 8000
        self.socket = ""

    def start(self):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print("Starting TTS server on {host}:{port}".format(host=self.host, port=self.port))
            self.socket.bind((self.host, self.port))
            print("TTS Server started on port {port}.".format(port=self.port))
        except Exception:
            print("Error: Could not bind to port {port}".format(port=self.port))
            self.shutdown()
            sys.exit(-1)
        self.listen_(10)

    def listen_(self, backlog):
        self.socket.listen(backlog)
        while True:
            (conn, address) = self.socket.accept()
            conn.settimeout(60)
            print("Recieved connection from {addr}".format(addr=address))
            data = conn.recv(4096)

            succ_ = verify(data)
            print(succ_)
            if not succ_:
                send_ = json.dumps({"success": True})
                conn.send(str.encode(send_))
            else:
                send_ = json.dumps({"success": False})
                conn.send(str.encode(send_))

    def shutdown(self):
        self.socket.shutdown(socket.SHUT_RDWR)


def verify(data):
    jdata = json.loads(data.decode('utf-8'))
    ret = False
    if "lang" not in jdata.keys():
        return ret
    else:
        if jdata["lang"] == "kor":
            pass
        elif jdata["lang"] == "eng":
            pass
        else:
            return False
    if "voice" not in jdata.keys():
        return False
    else:
        if jdata["voice"] < 0 or jdata["voice"] > 122:
            return False
    return True


if __name__ == "__main__":
    server = stt_sock()
    try:
        print("Press Ctrl+C to shut down server.")
        server.start()
    except Exception as e:
        print("Error")
        print(e)
        server.shutdown()


