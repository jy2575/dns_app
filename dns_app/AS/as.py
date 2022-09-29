from socket import *

UDPport = 53353
ASsocket = socket(AF_INET, SOCK_DGRAM)

ASsocket.bind(('', UDPport))

hostname = {}
while True:
    requestORquery, senderIP = ASsocket.recvfrom(4096)
    requestORquery = requestORquery.decode()

    if "VALUE" in requestORquery:
        requestORquery2 = requestORquery.split('\n')
        name = requestORquery2[1].split('=')[1]
        value = requestORquery2[2].split('=')[1]
        hostname[name] = value
        ASsocket.sendto("registration_complete".encode(), senderIP)
    else:
        requestORquery2 = requestORquery.split('\n')

        name = requestORquery2[1].split('=')[1]
        if name in hostname:
            response = "TYPE=A\nNAME=" + name + "\nVALUE=" + hostname[
                name] + "\nTTL=10"
            print(response)
            ASsocket.sendto(response.encode(), senderIP)
