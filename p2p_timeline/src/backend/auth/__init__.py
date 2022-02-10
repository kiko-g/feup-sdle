import pickle
import random
import socket
import threading

from app import app, cors, load_users, FLASK_PORT_OFFSET


def socket_share_users():
    print("Running")
    data_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    data_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    data_sock.bind(('', FLASK_PORT_OFFSET - 1))

    data_sock.listen(1000)
    print("Listining for users")
    data_sock.settimeout(30)

    while True:
        try:
            conn, addr = data_sock.accept()

            all_users = load_users()

            print("Connection Accepted")

            conn.recv(1024)

            list_to_send = []

            if len(all_users) < 20:
                conn.sendall(pickle.dumps(all_users))
            else:
                for i in range(5):
                    list_to_send.append(random.choice(all_users))
                conn.sendall(pickle.dumps(list_to_send))

            conn.close()
        except:
            pass

    data_sock.close()


if __name__ == '__main__':
    t1 = threading.Thread(target=socket_share_users)

    t1.start()

    app.run(debug=True)
    cors.init_app(app)

    t1.join()
