
#!/usr/bin/python3
import socket
import ssl
import pprint
import json

listen_address = '212.201.8.88'
listen_port = 9093
server_cert = '/home/john/john_05_02/server_org/server.crt'
server_key = '/home/john/john_05_02/server_org/server.key'
ca_cert = '/home/john/john_05_02/intermediate_authority/Intermediate_CA.crt'

context = ssl.create_default_context()
context.verify_mode = ssl.CERT_REQUIRED
context.load_cert_chain(certfile=server_cert, keyfile=server_key)
context.load_verify_locations(cafile=ca_cert)
context.check_hostname = False
sock = socket.socket() 
sock.bind(("", listen_port))
sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
sock.listen(5)


while True:
    new_socket, address = sock.accept()
    print('Connection from: ' + str(address))
    conn = context.wrap_socket(new_socket, server_side=True, server_hostname=None)
    #with context.wrap_socket(new_socket, server_side=True) as ssock:
    print("SSL established with peer.. Getting Client Certificate")
    pprint.pprint(conn.getpeercert())
    while True:
        buf = b''  # Buffer to hold received client data
        data = conn.recv(4096).decode()
        if not data:
            break
        else:
            data = data.replace("'", '"')
            sensor_val = json.loads(data)
            print("Humidity:", sensor_val["humidity"])
            print("Temperature", sensor_val["temperature"])
print("Closing Connection")
conn.shutdown(socket.SHUT_RDWR)
conn.close()

