from flask import *
from socket import *

app = Flask(__name__)


#register path
@app.route('/register', methods=['PUT'])
def register():
    data = request.get_json()
    hostname = data.get('hostname')
    ip = data.get('ip')
    as_ip = data.get('as_ip')
    as_port = int(data.get('as_port'))
    #return jsonify(as_port), 200

    if hostname is not None and ip is not None and as_ip is not None and as_port is not None:
        #print("tag 2")
        FSsocket = socket(AF_INET, SOCK_DGRAM)
        registration = "TYPE=A\nNAME=" + hostname + "\nVALUE=" + ip + "\nTTL=10"
        print(registration)

        FSsocket.sendto(registration.encode(), (as_ip, as_port))
        response, senderIP = FSsocket.recvfrom(4096)

        FSsocket.close()
        print(response.decode() + "haha")
        if response.decode() == "registration_complete":
            return jsonify('registration_complete'), 201
        else:
            return jsonify('registration_error'), 500
    else:
        return jsonify("Missing params"), 400


@app.route('/fibonacci', methods=['GET'])
def fibonacci():
    number = request.args.get('number')
    if number is not None:
        return jsonify(fiboFunc(int(number))), 200

    return jsonify('Number is not given'), 400


def fiboFunc(n):

    if n == 1:
        return 0
    if n == 2:
        return 1

    else:
        return fiboFunc(n - 1) + fiboFunc(n - 2)


app.run(host='0.0.0.0', port=9090, debug=True)
