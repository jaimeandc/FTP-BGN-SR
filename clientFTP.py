import socket
import os
import timer
import udt
import packet
clientsock = ""
newfile = ""
packetsToSend = []
windowsize = 3
expectedPacket = 0
filename = ""
windowbase = 1
windowend = 3



def main():
    # Prompt the user to enter Server IP/port#
    serverIP = ""
    serverPort = int(input("Provide Port# :"))
    addr = (serverIP, serverPort)
    clientsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientsock.connect(addr)
    print("You are now connected!")
    #Send what type of protocol we are going to use.
    proto_type = input("What type of protocol would you like to use :")
    protopacket = packet.make(0, proto_type.encode())
    udt.send(protopacket, clientsock, addr)
        #udt.send(packet.make(0,newfile.encode()),clientsock,addr)
        #ADD if to handle what type of protocol we are going to use.
    if proto_type == "SNW":
        stop_n_wait()
    elif proto_type == "GBN":
        go_back_n(clientsock, addr)
def stop_n_wait():
    while True:
        # Loop and wait for server to send messages back.
        f = open(newfile, "a")
        #data = clientsock.recv(1000).decode()
        ack_packet, addr = udt.recv(clientsock)
        ack_seq_num, data = packet.extract(packet)
        if not data:
            f.close()

        # if server checks if file exist.
        if data == "nofilefound":

            # begin to write new file for now print
            print("Sorry file not found in server")
            request = input("RTFCli> ")
            # check if request command or close command
            try:
                cmd, filename = request.split(" ")
                clientsock.send(filename.encode())
            except:
                print("Sorry commands should be in format cmd [filename]")
        # Server let us know file wasnt found try again.
        elif data == "ok":

            print("Download complete")


        else:
            # open new file and begin writing data into it.
            print(data)
            f.write(data)

    print("Connection lost")
    clientSock.close()

##Begin with basic gbn to test connectivity. similar to what we had for our og code.
def go_back_n(conn,addr):
    try:
        request = input("RTFCli> ")
        cmd, filename = request.split(" ")
        filename, filetype = filename.split(".")
        newfile = filename + "." + filetype
        print(newfile)
        filepacket = packet.make(0, newfile.encode())
        udt.send(filepacket, conn ,addr)
        print("Sent")
        #clientsock.send(packet.make(0,newfile))


    except:
        print("please enter cmd >[cmd] [filename.filetype]")
        request = input("RTFCli> ")
        newfile = filename + "." + filetype
        #clientsock.send(newfile.encode())
        #now implimenting with udt module
        filepacket = packet.make(0, newfile.encode())
        udt.send(filepacket, conn, addr)
    print(newfile)
    print("Hello welcome to GBN")
    ##From this point on we wait sequence number 1 and get ready to send acks.
    packetsRecv = []
    expectinACK = 1
    previousSentAck = " "
    f = open(newfile, 'wb')
    while True:
        #data = clientsock.recv(1000).decode()
        #at this point we enter a loop waiting for the payload and sending retransmitions if needed.
        ack_packet, addr = udt.recv(conn)
        ack_seq_num, data = packet.extract(ack_packet)
        if not data:
            f.close()
            break
        # check if it is what we are expecting
        if ack_seq_num == expectinACK:
            packetsRecv[ack_seq_num] = [data]
            f.write(data)
            expectinACK = 1 + expectinACK
            ACKpacket = packet.make(ack_seq_num + 1, packet.make_empty())
            udt.send(ACKpacket, conn, addr)
            #save a copy of the previous sent ack so that if we hit a timout we can resend the previous sent packet
            previousSentAck = ACKpacket

    else:
        print("sending ack for previous packet")
        udt.send(previousSentAck, conn, addr)






if __name__ == "__main__":
    main()
