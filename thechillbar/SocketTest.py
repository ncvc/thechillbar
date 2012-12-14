import socket
import sys
import os.path

data = " ".join(sys.argv[1:])

socket_name = "/tmp/thechillsocket"
if os.path.exists(socket_name):
# Create a socket (SOCK_STREAM means a TCP socket)
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

    try:
        # Connect to server and send data
        sock.connect(socket_name)
        sock.send(data)

        print "Sent:     {}".format(data)
        
    # Receive data from the server and shut down
#        received = sock.recv(1024)
    except Exception as e:
        print "Error connecting to socket {0}.\nMake sure the server is running and is on this socket".format(socket_name)
    finally:
        sock.close()

else:
    print "Couln't connect to socket."
