import socket
from http import HTTPStatus


HOST = "127.0.0.1"
PORT = 11863


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

    print(f"Binding server {HOST}:{PORT}")
    s.bind((HOST, PORT))
    s.listen()

    while True:
        status_value = HTTPStatus.OK
        status_phrase = HTTPStatus(HTTPStatus.OK).phrase
        conn, address = s.accept()
        data = conn.recv(1024)
        data = data.decode("utf-8").strip()
        print(data)
        source = conn.getpeername()
        for status in HTTPStatus:
            if data.split()[1] == f'/?status={status.value}':
                status_value = status.value
                status_phrase = status.phrase
                break

        conn.send(f"{data.split()[2]} {status.value} {status_phrase}"
                  f"\nContent-Type: text/html; charset=utf-8\n"
                  f"\nRequest Method: {data.split()[0]}"
                  f"\nRequest Source: {source}"
                  f"\nResponse Status: {status_value} {status_phrase}"
                  f"\n{data[4:]}".encode("utf-8"))
        conn.close()