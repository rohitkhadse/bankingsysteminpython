import socket
import sys
import pickle
import thread 
import G_area

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
differencedata = []
server1_data = []
G = G_area.G_area()


def write_to_file(data):
    print >> sys.stderr, 'Writing into file'
    with open ('server1.data', 'w') as f:
        for tempdata in data:
            f.write("%s %s %s \n" % (tempdata.get_tid(),
                        tempdata.get_act(), tempdata.get_bal()))
    f.close()

def logginto_file(data):
    with open ('server1.log', 'a') as f:
        f.write("%s %s %s %s \n" % (data.get_Qtype(), data.get_qtid(),
                    data.get_qact(),data.get_qbal()))
    f.close()

def flush_the_logfile():
    print >> sys.stderr, 'Checking out into file'
    with open ('server1.log', 'w') as f:
        f.close()

def send_response_to_client(data):
    respdata = G_area.packet_tclass()
    respdata.packettype = RESPONSE
    respdata.data = data.data
    respdata.sentfrom = "server1"
    respdata.sentto = data.sentfrom
    pickledresp = pickle.dumps(respdata)
    sent = sock.sendto(pickledresp, server_address)
    logginto_file(data.data)

def send_diff_to_server(data, index) :
    diffdata = G_area.packet_tclass()
    diffdata.packettype = DATA
    diffdata.data = data
    diffdata.length = len(diffdata.data)
    diffdata.sentfrom = "server1"
    if index == 1:
        diffdata.sentto = "server2"
    if index == 2 :
        diffdata.sentto = "server3"
    pickleddiffdata = pickle.dumps(diffdata)
    print ' =======================sneding diff'
    sent = sock.sendto(pickleddiffdata, server_address)

def initialize_data():
    with open('server1.data','r') as f:
        for line in f:
            temp_data = G_area.clientdetails()
            word = line.split(" ")    
            temp_data.set_tid (int(word[0]))
            temp_data.set_act (int(word[1]))
            temp_data.set_bal (int(word[2]))
            server1_data.append(temp_data)
            print >> sys.stderr, ' %s %s %s %s' % (temp_data.get_tid(),
                    temp_data.get_act(), temp_data.get_bal(),
                    len(server1_data))
            
def send_resync_done():
    pkt = G_area.packet_tclass()
    pkt.packettype = RESYNC_DONE
    pkt.data.append(1)
    pkt.length = len(pkt.data)
    pkt.sentfrom = "server1"
    pkt.sentto = "cordinator"
    pickledpkt = pickle.dumps(pkt)
    sent = sock.sendto(pickledpkt, server_address)
    print >> sys.stderr, 'Resync_DONE Sent'

def initiate_resync():
    resyncdata = G_area.packet_tclass()
    resyncdata.packettype = RESYNCRONIZE
    resyncdata.data = server1_data
    resyncdata.length = len(resyncdata.data)
    resyncdata.sentfrom = "server1"
    resyncdata.sentto = "cordinator"
    pickledresync = pickle.dumps(resyncdata)
    sent = sock.sendto(pickledresync, server_address)

def keep_receiving():
    while True:
        print >> sys.stderr, '\nWaiting to receive message'
        data, address = sock.recvfrom(4096)
        resultpickled = pickle.loads(data)
        
        if resultpickled.packettype == RESYNCRONIZE:
            print >> sys.stderr, 'Resyncronize received from %s' % resultpickled.sentfrom
            for tempdata in resultpickled.data :
                for serverdata in server1_data :
                   if tempdata.get_bal() != serverdata.get_bal():
                        differencedata.append(serverdata)
                        print >> sys.stderr, 'balance : %s, len %d ' % (serverdata.get_bal(), tempdata.get_bal())
            if resultpickled.sentfrom == "server2":
                send_diff_to_server(differencedata, 1)
            if resultpickled.sentfrom == "server3":
                send_diff_to_server(differencedata, 2)

        elif resultpickled.packettype == DO_SYNC : 
            print >> sys.stderr, 'Do syncronize received %s' % resultpickled.packettype
            initiate_resync()
        elif resultpickled.packettype == HEARTBEAT :
            print >> sys.stderr, 'HeartBeat Received %s ' % resultpickled.packettype
            htcnt = G.get_htbt1()
            G.set_htbt1(htcnt+1)
            ht_pkt = G_area.packet_tclass()
            ht_pkt.packettype = HEARTBEAT
            ht_pkt.data = []
            ht_pkt.length = len(ht_pkt.data)
            ht_pkt.sentfrom = "server1"
            ht_pkt.sentto = "cordinator"
            ht_pi_data = pickle.dumps(ht_pkt) 
            sent = sock.sendto(ht_pi_data, server_address)
            print >> sys.stderr , '========>  %s %s ' % (G.get_SDSEND(),G.get_htbt1()) 
            if G.get_SDSEND() and G.get_htbt1() > 5:
                send_resync_done()
                G.set_htbt1(0)
                G.set_SDSEND(0)    
        elif resultpickled.packettype == DATA:
            print >> sys.stderr, 'Diff data received from %s' % resultpickled.sentfrom
            for tempdata in resultpickled.data:
                for serverdata in server1_data:
                    if tempdata.get_act() == serverdata.get_act():
                        serverdata.set_bal(tempdata.get_bal())
            for serverdata in server1_data:
                print >> sys.stderr, '%s %s %s' % (serverdata.get_tid(),serverdata.get_act(),
                 serverdata.get_bal())
            write_to_file(server1_data)
            G.set_SDSEND(1)
        elif resultpickled.packettype == BALANCE :
            print >> sys.stderr, ' BALANCE request Received from %s' % (resultpickled.sentfrom)
            print >> sys.stderr, 'data : %s %s %s %s ' % (resultpickled.data.get_Qtype(),
                 resultpickled.data.get_qtid(),
                 resultpickled.data.get_qact(),
                 resultpickled.data.get_qbal())
            for serverdata in server1_data:
                if resultpickled.data.get_qact() == serverdata.get_act():
		    temptransid = serverdata.get_tid() + 2
		    serverdata.set_tid(temptransid)
                    resultpickled.data.set_qtid (serverdata.get_tid())
                    resultpickled.data.set_qact ( serverdata.get_act())
                    resultpickled.data.set_qbal ( serverdata.get_bal())
            send_response_to_client(resultpickled)
        elif resultpickled.packettype == DEPOSIT :
            print >> sys.stderr, ' DEPOSIT request Received from %s' % (resultpickled.sentfrom)
            for serverdata in server1_data:
                if resultpickled.data.get_qact() == serverdata.get_act():
                    serverdata.set_bal(resultpickled.data.get_qbal())
		    temptransid = serverdata.get_tid() + 2
		    serverdata.set_tid(temptransid)
                    resultpickled.data.set_qtid(serverdata.get_tid())
                    resultpickled.data.set_Qtype ("DEPOSIT")
                    print >> sys.stderr, ' trans Id : %s' % resultpickled.data.get_qtid()
            write_to_file(server1_data) 
            logginto_file(resultpickled.data)  
        elif resultpickled.packettype == WITHDRAW :
            print >> sys.stderr, ' WITHDRAW request Received from %s' % (resultpickled.sentfrom)
            for serverdata in server1_data:
                if resultpickled.data.get_qact() == serverdata.get_act():
                    serverdata.set_bal(resultpickled.data.get_qbal())
		    temptransid = serverdata.get_tid() + 2
		    serverdata.set_tid(temptransid)
                    resultpickled.data.set_qtid(serverdata.get_tid())
                    resultpickled.data.set_Qtype ("WITHDRAW")
                    print >> sys.stderr, ' trans Id : %s' % resultpickled.data.get_qtid()
            write_to_file(server1_data) 
            logginto_file(resultpickled.data)  
        else :
            print >> sys.stderr, 'Invalid Message Type'

def send_alive():
    message = G_area.packet_tclass()
    message.packettype = ALIVE
    message.data = "Hello this is data  field"
    message.length = len(message.data)
    message.sentfrom = "server1"
    message.sentto = "cordinator"

    pickledstring = pickle.dumps(message)
    print >> sys.stderr, 'sending "ALive Message with type %s"' %  message.packettype
    sent = sock.sendto(pickledstring, server_address)

try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = ('10.10.13.67', 5520)
    thread.start_new_thread(keep_receiving, ())
    initialize_data()
    send_alive()
    #flush_the_logfile()
except Exception, e: 
    print >> sys.stderr, 'Unable to create thread %s' % str(e)
    print >> sys.stderr, 'closing socket'
    sock.close()

while 1:
    pass
