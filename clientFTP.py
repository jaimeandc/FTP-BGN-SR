import socket
import os
import timer
import udt
import packet
clientsock = ""
newfile = ""
packetsToSend = []
windowsize = 0
expectedPacket = 0



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


    try:
        request = input("RTFCli> ")
        cmd, filename = request.split(" ")
        filename, filetype = filename.split(".")
        newfile = filename + "." + filetype
        filepacket = packet.make(0, newfile.encode())
        udt.send(filepacket, clientsock,addr)
        print("Sent")
        #clientsock.send(packet.make(0,newfile))


    except:
        print("please enter cmd >[cmd] [filename.filetype]")
        request = input("RTFCli> ")
        newfile = filename + "." + filetype
        #clientsock.send(newfile.encode())
        #now implimenting with udt module
        filepacket = packet.make(0, newfile.encode())
        udt.send(filepacket, clientsock, addr)
        print("Sent")
        #udt.send(packet.make(0,newfile.encode()),clientsock,addr)
        #ADD if to handle what type of protocol we are going to use.
        stop_n_wait()
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
def gbn():
    print("Hello welcome to GBN")
    ##From this point on we begin with sequence number 0 and
    currentSegNum = 1
    f = open(newfile, "a")
    #need to change loop to work with timer and resend after timeout
    while True:
        #data = clientsock.recv(1000).decode()
        ack_packet, addr = udt.recv(clientsock)
        ack_seq_num, data = packet.extract(ack_packet)
        if not data:
            f.close()
            break




if __name__ == "__main__":
    main()
