import msvcrt # Windows only!
import socket
import time
import datetime
REPEAT = 10



def ssdpSearch():
    print("Starting SSDP Search.")
    UDP_IP = '<broadcast>'
    UDP_PORT = 2000
    UDP_MESSAGE = '{"type":"SCS-DISCOVER","hostname":"Host-SCS"}'
    networks = socket.gethostbyname_ex(socket.gethostname())[2] # Find all networks (i.e, wifi, wired)
    print(networks)
    sockets = []
    for net in networks: # Connect to all networks
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1) # Allow broadcast
        sock.bind((net, UDP_PORT)) # Connect
        sock.settimeout(0.5) # Set timeout (if no answer when reading)
        sockets.append(sock) # Save "sock" to sockets
        timeStart = time.time()
        devices = []
        print('Searching for devices:')
        time.sleep(0.1)
        while time.time() - timeStart < REPEAT:
            for sock in sockets:
                try:
                    sock.sendto(UDP_MESSAGE.encode(), (UDP_IP, UDP_PORT))
                    data, addr = sock.recvfrom(1024)
                    data = data.decode()
                    #print(data)
                    data = data[1:].split(',')
                    if data[0] == '"type":"SCS-NOTIFY"': # Only accept correct responses
                        oldDevice = 0
                        print(data)
                        for dev in devices:
                            if dev[0] == data[1]:
                                oldDevice = 1
                            if not oldDevice:
                                devices.append([data[1],data[2]]) # Save found devices
                                print(' \t' + data[1] + ' ' + data[2])
                        return
                except:
                    time.sleep(0.2)
                    if not len(devices):
                        print(' \tNo devices found.')
                        print('')
                    for sock in sockets:
                        sock.close()


def readLine(s):
    # Function to read status from BCG data
    line = s.recv(1024).decode()
    return line

def main():
    print('BCG Data Logger\nLogs either raw data or BCG algorithm data to a file \
    depending on configured mode.')
    # Open file
    IP = input('Insert IP address (empty for SSDP): ')
    while len(IP) == 0:
        ssdpSearch()
        IP = input('Insert IP address (empty for SSDP): ')
        PORT = 8080
        filename = 'L:\\bcglog\logged_data_' + str(datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')) + '.txt'
        fid = open(filename,'w')
        print('')
        print('Starting to read data. Press \"ctrl+c\" to quit.')
    while True:
        try:
             s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
             s.settimeout(10)
             s.connect((IP, PORT))
             while True: #
                 data = readLine(s)
                 print(data,)
                 fid.write(data)
        except (KeyboardInterrupt, SystemExit):
             print('Exiting program.')
             fid.close()
             break
        except (socket.timeout):
             print('Timed out, reconnecting.')
        except socket.error as msg:
             print(msg)
             print('Trying to reconnect.')
if __name__ == '__main__':
    main()

