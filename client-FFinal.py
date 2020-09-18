#! /usr/bin/python
# -*- coding: utf-8 -*-
import base64
import random
import string
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto.Util.Padding import pad, unpad
import hashlib
import sys
from bitstring import BitArray
import pickle
import binascii
import glob
import io

sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding = 'utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding = 'utf-8')

from socket import *
from select import *
import time
BLOCK_SIZE = 16
HOST = '127.0.1.1'
PORT = 3000
BUFSIZE = 1024
ADDR = (HOST, PORT)

clientSocket = socket(AF_INET, SOCK_STREAM)# 서버에 접속하기 위한 소켓을 생성한다.
W=[]
string_pool = string.ascii_letters
Ks=""
for i in range(16):
    Ks += random.choice(string_pool)

c_cipher = AES.new(Ks.encode("utf8"), AES.MODE_ECB)
c_decipher = AES.new(Ks.encode("utf8"), AES.MODE_ECB)

files=glob.glob('*.txt')
for file in files:
    with open(file, 'r') as f:
        while True:
            line=(f.readline().rstrip())
            if line! = '':
                W.append(line)
            if not line : break

W = list(set(W))
print(W)
#w = input("검색값을 입력하세요: ")
w = "타박상"
print(w)
Sero = len(files)
Garo = len(W)
print(Sero)
print(Garo)
File = {}
for j in W:
    dic = []
    for file in files:
        with open(file, 'r') as f:
            if j in open(file).read():
                dic.append(file[:18])
    print(dic)
    File[j] = dic
values = File.values()
keys = File.keys()

print(File)
T = {}

for i in keys:
    el = []
    Ke = c_cipher.encrypt(pad(i.encode("utf8"),BLOCK_SIZE))
    for h in File[i]:
        d_cipher = AES.new(Ke, AES.MODE_ECB)
        e = d_cipher.encrypt(h.encode("utf8"))
        el.append(e)
    T[i] = el
print(T)

print('****')
d_decipher = AES.new(Ke, AES.MODE_ECB)
keys = T.keys()
values = T.values()

Kt = ""
for i in range(16):
    Kt += random.choice(string_pool)
#print(Kt)
Ks = ""
for i in range(16):
    Ks += random.choice(string_pool)
print(Ks)
a_cipher = AES.new(Kt.encode("utf8"), AES.MODE_ECB)
a_decipher = AES.new(Kt.encode("utf8"), AES.MODE_ECB)

from Crypto.Util.Padding import pad, unpad

print(keys)
Tset=[[{0:0}]*(Sero+1) for i in range(Garo)]
for o in keys:
    stag = a_cipher.encrypt(pad(o.encode("utf8"),BLOCK_SIZE))
    print(list)
    index = 0
    list = []
    i = 1
    for k in T[o]:

        print(o)
        kindex = bin(i)
        b_cipher = AES.new(pad(kindex.encode("utf8"),BLOCK_SIZE), AES.MODE_ECB)
        f = b_cipher.encrypt(stag) # stag 를 한번더 암호화
        m = SHA256.new()
        hex = m.update(f)
        H = m.hexdigest()
        B = int(H,16)
        b = (bin(B)[213:220])
        K = (bin(B)[2:131])
        L = (bin(B)[132:212])

        j = random.randint(0,Sero)
        while j in list:
            j = random.randint(0,Sero)
        list.append(j)
        n = len(File[o])
        index = index+1
        Bcount = 1
        b = (int(b,2)%98)
        print(b)
        print(j)
        if(index == n):Bcount=0
        print(list)
        print(index)

        k1 = k.hex()
        temp = BitArray(hex = k1).bin
        temp3 = str(Bcount) + temp
        d = ""
        for q in range(129):
            if temp3[q] == K[q]:
                d = d + "0"
            else:
                d = d + "1"
        K2 = d
        Tset[b][j] = {L:K2}
        i = i + 1

print("끝")
Tset1 = str(Tset)

stag1 = a_cipher.encrypt(pad(w.encode("utf8"), BLOCK_SIZE))
pTset = pickle.dumps(Tset)
pstag = pickle.dumps(stag1)

clientSocket.connect(ADDR)  # 서버에 연결 요청

clientSocket.sendall(pTset)  # 메시지 송신

time.sleep(2)

clientSocket.sendall(pstag)

msg = clientSocket.recv(1000000)

print(pickle.loads(msg))

pV = (pickle.loads(msg))

finallist = []
f = pV[0]
for i in pV:

    temp = BitArray(bin = i).hex
    print(temp)
    f1 = BitArray(bin = i)
    f2 = bytearray.fromhex(temp)
    print(f2)
    Ke = c_cipher.encrypt(pad(w.encode("utf8"), BLOCK_SIZE))
    print(Ke)
    e_decipher = AES.new(Ke, AES.MODE_ECB)
    idi = e_decipher.decrypt(f2)
    finallist.append(idi)
    print(idi)

finallist = set(finallist)
print(finallist)
