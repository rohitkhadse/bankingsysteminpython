import thread 
import time
import socket
import sys
import pickle
import G_area

server_addr = []
client_addr = []

HT_TIME = 5

ALIVE = 1
RESYNCRONIZE = 2
DO_SYNC = 3
HEARTBEAT = 4
RESYNC_DONE = 5
DATA = 6 
RESPONSE = 7

BALANCE = 11
DEPOSIT = 12
WITHDRAW = 13 

G = G_area.G_area()

def forward_packet_to_client(data):
    if data.sentto == "client1":
       pickledresponse = pickle.dumps(data)
       sent = sock.sendto(pickledresponse, client_addr[0])

def forward_packet_to_server(data, index):
    if index == 0:
        data.sentto = "server1"
        pickleddata = pickle.dumps(data)
        sent = sock.sendto(pickleddata, server_addr[0])
    if index == 1:
        data.sentto = "server2"
        pickleddata = pickle.dumps(data)
        sent = sock.sendto(pickleddata, server_addr[1])
    if index == 2:
        data.sentto = "server3"
        pickleddata = pickle.dumps(data)
        sent = sock.sendto(pickleddata, server_addr[2])
    if index == 3 :
        data.sentto = "server1"
        pickleddata = pickle.dumps(data)
        sent = sock.sendto(pickleddata, server_addr[0])
        data.sentto = "server2"
        pickleddata = pickle.dumps(data)
        sent = sock.sendto(pickleddata, server_addr[1])
        data.sentto = "server3"
        pickleddata = pickle.dumps(data)
        sent = sock.sendto(pickleddata, server_addr[2])
        
def heartbeat_1 ():
    while 1: 
        ht_pkt = G_area.packet_tclass()
        ht_pkt.packettype = HEARTBEAT
        ht_pkt.data = []
        ht_pkt.length = len(ht_pkt.data)
        ht_pkt.sentfrom = "cordinator"
        ht_pkt.sentto = "server1"
        ht_pi_data = pickle.dumps(ht_pkt)
        if not (G.get_active1()):
            G.set_status1(0)
            sent = sock.sendto(ht_pi_data, server_addr[0])
            time.sleep(HT_TIME)
            if not (G.get_status1()) :
                print >> sys.stderr, 'SERVER 1 Down'
                count1 = G.get_count1()
                G.set_count1(count1+1)
                print >> sys.stderr,'count ===== %s' % G.get_count1() 
                G.set_CONCT1(0)
            if G.get_count1() > 2 :
                G.set_active1(1)

            
def heartbeat_2 ():
    while 1: 
        ht_pkt = G_area.packet_tclass()
        ht_pkt.packettype = HEARTBEAT
        ht_pkt.data = []
        ht_pkt.length = len(ht_pkt.data)
        ht_pkt.sentfrom = "cordinator"
        ht_pkt.sentto = "server2"
        ht_pi_data = pickle.dumps(ht_pkt)
        if not (G.get_active2()):
            G.set_status2(0)
            sent = sock.sendto(ht_pi_data, server_addr[1])
            time.sleep(HT_TIME)
            if not (G.get_status2()) :
                print >> sys.stderr, 'SERVER 2 Down'
                count2 = G.get_count2()
                G.set_count2(count2+1)
                print >> sys.stderr,'count ===== %s' % G.get_count2() 
                G.set_CONCT2(0)
            if G.get_count2() > 2 :
                G.set_active2(1)

def heartbeat_3 ():
    while 1: 
        ht_pkt = G_area.packet_tclass()
        ht_pkt.packettype = HEARTBEAT
        ht_pkt.data = []
        ht_pkt.length = len(ht_pkt.data)
        ht_pkt.sentfrom = "cordinator"
        ht_pkt.sentto = "server3"
        ht_pi_data = pickle.dumps(ht_pkt)
        if not (G.get_active3()):
            G.set_status3(0)
            sent = sock.sendto(ht_pi_data, server_addr[2])
            time.sleep(HT_TIME)
            if not (G.get_status3()) :
                print >> sys.stderr, 'SERVER 3 Down'
                count3 = G.get_count3()
                G.set_count3(count3+1)
                print >> sys.stderr,'count ===== %s' % G.get_count3() 
                G.set_CONCT3(0)
            if G.get_count3() > 2 :
                G.set_active3(1)
                
def send_dosync_notfy(sendto, index) :
    notify = G_area.packet_tclass()
    notify.packettype = DO_SYNC
    notify.data.append(1)
    notify.length = len(notify.data)
    notify.sentfrom = "cordinator"
    notify.sentto = sendto
    picklednoti = pickle.dumps(notify)
    sent = sock.sendto(picklednoti, server_addr[index])

def keep_receiving (ID):
    while True:
        print >> sys.stderr, '\nWaiting to receive message'
        data, address = sock.recvfrom(4096)

        print >> sys.stderr, 'received %s bytes from %s' % (len(data), address) 
        resultpickle = pickle.loads(data)
        if resultpickle.packettype == ALIVE :
            if resultpickle.sentfrom == "server1" and G.get_active1() :
                print >> sys.stderr, 'alive msg from received from %s' % resultpickle.sentfrom
                if len(server_addr) >= 1:
                    server_addr[0] = address
                else :
                    server_addr.append(address)
                G.set_active1(0)
                G.set_count1(0)
                print "==========================================sysnc"
                if not (G.get_active2()) and not (G.get_active3()):
                    send_dosync_notfy("server1", 0)
            elif resultpickle.sentfrom == "server2" and G.get_active2() :
                print >> sys.stderr, 'alive msg from received from %s' % resultpickle.sentfrom    
                if len(server_addr) >= 2:
                    server_addr[1] = address
                else :
                    server_addr.append(address)
                G.set_active2(0)
                G.set_count2(0)
                if not (G.get_active1()) and not (G.get_active3()):
                    send_dosync_notfy("server2", 1)
            elif resultpickle.sentfrom == "server3" and G.get_active3() :
                print >> sys.stderr, 'alive msg from received from %s' % resultpickle.sentfrom    
                if len(server_addr) >= 3:
                    server_addr[2] = address
                else :
                    server_addr.append(address)
                G.set_active3(0)
                G.set_count3(0)
                if not (G.get_active1()) and not (G.get_active2()):
                    send_dosync_notfy("server3", 2)
            elif resultpickle.sentfrom == "client1"  :
                client_addr.append(address)
                print >> sys.stderr, 'alive msg from received from %s' % resultpickle.sentfrom    
            elif resultpickle.sentfrom == "client2"  :
                client_addr.append(address)
                print >> sys.stderr, 'alive msg from received from %s' % resultpickle.sentfrom    
            elif resultpickle.sentfrom == "client3"  :
                client_addr.append(address)
                print >> sys.stderr, 'alive msg from received from %s' % resultpickle.sentfrom    
            else :
                  print >> sys.stderr, 'Invalid sender type'
        elif resultpickle.packettype == RESYNCRONIZE :
            print >> sys.stderr, 'Resync message received from %s ' % (resultpickle.sentfrom)
            G.set_syncInprgserver(1) 
            if resultpickle.sentfrom == "server1":       
                forward_packet_to_server(resultpickle, 1)
                forward_packet_to_server(resultpickle,2)
            if resultpickle.sentfrom == "server2":       
                forward_packet_to_server(resultpickle,0)
                forward_packet_to_server(resultpickle,2)
            if resultpickle.sentfrom == "server3":       
                forward_packet_to_server(resultpickle,0)
                forward_packet_to_server(resultpickle,1)
        elif resultpickle.packettype == HEARTBEAT :
            print >> sys.stderr, 'Heartbeat message from %s'% (resultpickle.sentfrom)
            if resultpickle.sentfrom == "server1":
                G.set_status1(1)
                G.set_CONCT1(1)
            if resultpickle.sentfrom == "server2":
                G.set_status2(1)
                G.set_CONCT2(1)
            if resultpickle.sentfrom == "server3":
                G.set_status3(1)
                G.set_CONCT3(1)
        elif resultpickle.packettype == DATA:
            print>> sys.stderr, 'DATA for %s to %s' % (resultpickle.sentto, resultpickle.sentfrom)
            if resultpickle.sentto == "server1":       
                forward_packet_to_server(resultpickle, 0)
            if resultpickle.sentto == "server2":       
                forward_packet_to_server(resultpickle,1)
            if resultpickle.sentto == "server3":       
                forward_packet_to_server(resultpickle,2)
        elif resultpickle.packettype == RESYNC_DONE :
            G.set_syncInprgserver(0)
            print >> sys.stderr, "Resync done received from %s" % (resultpickle.sentfrom)
        elif resultpickle.packettype == DEPOSIT or resultpickle.packettype == BALANCE or resultpickle.packettype == WITHDRAW:
            if (G.get_syncInprgserver()):
                print >> sys.stderr, 'RESYNCRONIZATION IN PROGRESS REQUEST DENIED'
            else :
                forward_packet_to_server(resultpickle, 3)
        elif resultpickle.packettype == RESPONSE :
            print >> sys.stderr, 'response received from %s ' % resultpickle.sentfrom
            forward_packet_to_client(resultpickle)


        else :
            print >> sys.stderr, "Invalid Type"

try : 
    sock = socket.socket (socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_address = ('10.10.13.67', 10000)
    print >> sys.stderr, 'starting up on %s port %s' % server_address
    sock.bind(server_address)

    thread.start_new_thread(keep_receiving,(1, ) )
    thread.start_new_thread(heartbeat_1,( ) )
    thread.start_new_thread(heartbeat_2,( ) )
    thread.start_new_thread(heartbeat_3,( ) )

except Exception, e: 
    print >> sys.stderr, 'Unable to create thread %s' % str(e)
    print >> sys.stderr, 'closing socket'
    sock.close()

while 1:
    pass
