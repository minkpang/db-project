# -*- coding: utf-8 -*-

from socket import *
from select import *
import pickle
from bitstring import BitArray
from Crypto.Hash import SHA256
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import random

BLOCK_SIZE = 16
HOST = ''
PORT = 3000
BUFSIZE = 1024
ADDR = (HOST, PORT)

serverSocket = socket(AF_INET, SOCK_STREAM)

serverSocket.bind(ADDR)
print('bind')

serverSocket.listen(100)
print('listen')

client_socket, client_addr = serverSocket.accept()
msg = client_socket.recv(200000000)
print(pickle.loads(msg))
Tset=(pickle.loads(msg))

print('received ')

msg2 = client_socket.recv(20000000)
print(pickle.loads(msg2))
stag=(pickle.loads(msg2))

V=[]
B=1
i=1
list=[]
while B==1:
    k1=bin(i)
    b_cipher = AES.new(pad(k1.encode("utf8"),BLOCK_SIZE), AES.MODE_ECB)
    f = b_cipher.encrypt(stag)
    m = SHA256.new()
    hex=m.update(f)
    H=m.hexdigest()

    B1=int(H,16)
    b=(bin(B1)[213:220])
    K=(bin(B1)[2:131])
    L=(bin(B1)[132:212])
    b=(int(b,2)%98)

    for j in range(21):
        label=Tset[b][j].keys()
        value=Tset[b][j].values()
        label2=(str(label))[12:92]
        value2=(str(value))[14:143]

        if label2==L:
            print('success')
            d=""
            for o in range(129):
                if value2[o]==K[o]:
                    d=d+"0"
                else:
                    d=d+"1"
            v=d
            print(v)
            print('***')
            B2=(str(v)[0])
            print("B2:")
            print(B2)
            B=int(B2)
            ID=(str(v)[1:129])
            V.append(ID)
            print(V)
    i=i+1
print('**')
pV = pickle.dumps(V)
client_socket.sendall(pV)
print('##')
print(V)
print("send success")

client_socket.close()
serverSocket.close()
print("finish")
