import os
import socket
import threading

HOST = '0.0.0.0'
PORT = 8080
BUFF_SIZE = 1024

SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    SERVER.bind((HOST, PORT))
    print(f'* Running on http://{HOST}:{PORT}')
except OSError as e:
    print(e)


def start():
    SERVER.listen()

    while True:
        conn, addr = SERVER.accept()
        t = threading.Thread(target=handle, args=(conn, addr))
        t.start()


def handle(conn, addr):
    while True:
        request = conn.recv(BUFF_SIZE).decode() 
        print(request)
        if not request:
            conn.close()
            break
        data = parseRequest(request)
        conn.sendall(data)


def parseRequest(request):
    Method = RequestLine('Method', request)
    Url = RequestLine('Url', request)

    if Method == 'GET':
        if Url == '/':
            Url = '/index.html'
        if Url[-5:] == '.html' or Url[-4:] == '.htm':
            ContentType = 'text/html'
        elif Url[-4:] == '.jpg' or Url[-5:] == '.jpeg':
            ContentType = 'image/jpeg'
        elif Url[-4:] == '.png':
            ContentType = 'image/png'
        elif Url[-4:] == '.css':
            ContentType = 'text/css'
        elif Url[-4:] == '.ico':
            ContentType = 'image/x-icon'
        else:
            ContentType = 'application/octet-stream'

    if Method == 'POST':
        info = request[request.find('uname'):].split('&')
        uname = info[0][6:]
        psw = info[1][4:]

        if uname == 'admin' and psw == '123456':
            Url = '/images.html'
        else:
            Url = '/401.html'
        ContentType = 'text/html'

    Url = Url[1:]
    data = Response(Url, ContentType)

    return data


def RequestLine(key, request):
    _RequestLine = request.split('\r\n')
    _RequestLine = _RequestLine[0].split(' ')

    if (key == 'Method'):
        return _RequestLine[0]
    if (key == 'Url'):
        return _RequestLine[1]

    return _RequestLine[2]


def ResponseHeader(ContentType, ContentLength):
    MessageHeader = 'HTTP/1.1 200 OK\r\n'
    MessageHeader += f'Content-Type: {ContentType}\r\n'
    MessageHeader += f'Content-Length: {ContentLength}\r\n'
    MessageHeader += '\r\n'
    MessageHeader = MessageHeader.encode()

    return MessageHeader


def Response(Name_File, ContentType):
    try:
        f = open(Name_File, 'rb')
        fdata = ResponseHeader(ContentType, os.path.getsize(Name_File))
    except:
        f = open('404.html', 'rb')
        fdata = ResponseHeader('text/html', os.path.getsize('404.html'))

    fdata += f.read()
    f.close()
    return fdata


if __name__ == '__main__':
    start()
