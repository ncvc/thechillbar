import SocketServer
import Queue
import threading
import os.path
import socket
import time
import sys

sys.path.append('/home/pi/')
from alphasign import AlphaSign

SOCKET_NAME = "/tmp/thechillsignsocket"
StreamServer = None

try:
    StreamServer = SocketServer.UnixStreamServer
except AttributeError:
    # Probably on a Windows machine
    StreamServer = SocketServer.BaseServer

class SignAnimator(StreamServer, object):
    def __init__(self, handler):
        super(SignAnimator, self).__init__(SOCKET_NAME, handler)
        self.queue = Queue.Queue(1)
        self.message_pusher = MessagePusher(self.queue)
        self.message_pusher.start()

    def shutdown(self):
        self.message_pusher.join()
        super(Animator, self).shutdown()

class SignAnimationRequestHandler(SocketServer.StreamRequestHandler):
    def handle(self):
        try:
            self.server.queue.put(self.rfile.readline().strip(), False)
        except Queue.Full:
            pass

class MessagePusher(threading.Thread, object):
    def __init__(self, queue, poll_time=1.0):
        super(MessagePusher, self).__init__()
        self.stop_request = threading.Event()
        self.queue        = queue
        self.poll_time    = poll_time
        self.sign         = AlphaSign.Sign('/dev/ttyUSB0')
        self.sign.setClock()

    def run(self):
        print 'Message pusher thread started'
        while not self.stop_request.isSet():
            try:
                next_message = self.queue.get(False)
                self.sign.sendText('A', AlphaSign.encodeText(next_message), AlphaSign.MODE_AUTO)
            except Queue.Empty:
                pass
            time.sleep(self.poll_time)
            
    def join(self, timeout=None):
        print 'Message Pusher thread exiting'
        self.stop_request.set()
        super(MessagePusher, self).join(timeout)

def sendMessage(message):
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    try:
        sock.connect(SOCKET_NAME)
        sock.send(message)
    except IOError as e:
        if e.errno == 13:
            print "{0}\nTry again using sudo".format(e)
        elif e.errno == 111:
            print "{0}\nError connecting to socket {1}\nMake sure the server is running and is on this socket".format(e, SOCKET_NAME)
        else:
            print e
    except Exception as e:
        print e
    finally:
        sock.close()

if __name__ == "__main__":

    print "Creating sign animator server"
    if os.path.exists(SOCKET_NAME):
        os.remove(SOCKET_NAME)

    server = SignAnimator(SignAnimationRequestHandler)
    print "Starting sign animation server..."
    print "Sign Animation server is running on socket {0}".format(SOCKET_NAME)
    print "Quit the server with CONTROL-C."
    server.serve_forever()
