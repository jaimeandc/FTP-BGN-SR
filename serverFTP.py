import os
import socket
import threading
import packet
import udt
from os.path import exists
serversock = ''
def main():
    port = int(input("Listen at port# "))
    #addr = (ip,port)
    serversock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    serversock.bind(("",port))
    serversock.listen()
    print("Listening for connection at ", port)

    while True:
        conn, addr = serversock.accept()
        print("Connection accepted from ", addr)
        #wait to see what type of protocol we are going to use.
        print("Waiting for protocol from client")
        recv_packet, addr = udt.recv(conn)
        seq_num, proto_type = packet.extract(recv_packet)
        proto_type.decode().replace(" ", "")
        print("We are going to be using:", proto_type.decode())

        if proto_type.decode().replace(" ", "") == "SNW":
            print("Begin sending file using Stop and Wait")
            thread = threading.Thread(target= stop_n_wait,args=(conn, addr))
            thread.start()
        elif proto_type.decode().replace(" ", "") == "GBN":
            print("Begin sending file using go-back-n")
            thread = threading.Thread(target=go_back_n, args=(conn, addr))
            thread.start()
            #Will change to SR once we write it.
        elif proto_type.decode().replace(" ", "") == "SR":
            print("Begin sending file using selective repeat")
            thread = threading.Thread(target=proto_type.decode(), args=(conn, addr))
            thread.start()
def file_exists(filename):
    file_exist = exists(filename)
    return file_exist
def go_back_n(conn, addr):
    print("Waiting for filename in GBN.")
    filename_packet, addr = udt.recv(conn)
    recv_seg_num, filename = packet.extract(filename_packet)
    filename = filename.decode()
    print(filename)
    print("looking for : ", filename)
    if file_exists(filename)== True:
        print("file found: begin timer and send payload.")
    else:
        print("file not found please try again.")





def stop_n_wait(conn, addr):
    print("Server wil now use 'Stop-and-wait' protocol")
    while True: #Wait for request
        #request = conn.recv(1024) old notation
        recv_packet, addr = udt.recv(serversock)
        recv_seq_num, request = packet.extract(recv_packet)
        print("Client is requesting :", request.decode())
        print("Sequence number recv :", recv_seq_num)

        #Check for file and respond accordingly
        if exists(request) == True:
            #open file and start sending in 1000bit segments
            f = open(request,'rb')
            print("Sending the file...")
            ack_num = 0
            while True:
                data = f.read(1020) # only send in 1000 byte segments
                if not data:
                    #conn.send("".encode())
                    break
                #conn.send(data)
                payload_packet = packet.make(ack_num,data)
                udt.send(payload_packet,conn,addr)
                ack_num = ack_num + 1
            print("Transfer Complete!")
            #ok_msg = "ok"
            #conn.send(ok_msg.encode())


        else:
            #send error message to client that file not found
            err_msg = "nofilefound"
            conn.send(err_msg.encode())
        print("Cnnection closed, See you later!")
        conn.close()





if __name__ == "__main__":
    main()
