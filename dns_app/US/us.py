from flask import *
from socket import *
import requests

app = Flask(__name__)


@app.route('/fibonacci', methods=['GET'])
def fibonacci():
    hostname = request.args.get('hostname')
    fs_port = request.args.get('fs_port')
    number = request.args.get('number')
    as_ip = (request.args.get('as_ip'))
    as_port = int(request.args.get('as_port'))

    if hostname is not None and fs_port is not None and number is not None and as_ip is not None and as_port is not None:
        USsocket = socket(AF_INET, SOCK_DGRAM)
        query = "TYPE=A\nNAME=" + hostname

        USsocket.sendto(query.encode(), (as_ip, as_port))
        #print("tag 1")
        response, senderIP = USsocket.recvfrom(4096)
        #print("tag 998")
        USsocket.close()

        response2 = response.decode().split('\n')
        value = response2[2].split('=')[1]

        fiboNum = requests.get("http://" + value + ":" + fs_port +
                               "/fibonacci?number=" + number)

        return jsonify(fiboNum.json()), 200

    return jsonify("Missing params"), 400


app.run(host='0.0.0.0', port=8080, debug=True)
