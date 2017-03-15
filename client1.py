import socket
import sys
import pickle
import thread
import G_area
import time

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

LATENCY_TIME = 10

G = G_area.G_area()
client1_data = G_area.query()
client1_data.set_qbal(0)


def send_alive():
    message = G_area.packet_tclass()
    message.packettype = ALIVE
    message.data = "Hello this is data  field"
    message.length = len(message.data)
    message.sentfrom = "client1"
    message.sentto = "cordinator"
    pickledstring = pickle.dumps(message)
    print >> sys.stderr, 'sending "ALive Message with type %s"' %  message.packettype
    sent = sock.sendto(pickledstring, server_address)

def request_balance():
    reqpkt = G_area.packet_tclass()
    data = G_area.query()
    data.set_Qtype("BALANCE")
    data.set_qact(32123)
    data.set_qtid(0)
    data.set_qbal(0)
    reqpkt.packettype = BALANCE
    reqpkt.data = data
    reqpkt.sentfrom = "client1"
    reqpkt.sentto = "cordinator"
    pickledreq = pickle.dumps(reqpkt)
    sent = sock.sendto(pickledreq, server_address)
    print >> sys.stderr, ' Balance Requested :'

def change_balance():
    reqpkt = G_area.packet_tclass()
    data = G_area.query()
    data.set_Qtype("DEPOSIT")
    data.set_qact(32123)
    data.set_qtid(0)
    data.set_qbal(client1_data.get_qbal())
    reqpkt.packettype = DEPOSIT
    reqpkt.data = data
    reqpkt.sentfrom = "client1"
    reqpkt.sentto = "cordinator"
    pickledreq = pickle.dumps(reqpkt)
    sent = sock.sendto(pickledreq, server_address)
    print >> sys.stderr, ' Deposit Requested : '


def deduct_balance():
    reqpkt = G_area.packet_tclass()
    data = G_area.query()
    data.set_Qtype("WITHDRAW")
    data.set_qact(32123)
    data.set_qtid(0)
    data.set_qbal(client1_data.get_qbal())
    reqpkt.packettype = WITHDRAW
    reqpkt.data = data
    reqpkt.sentfrom = "client1"
    reqpkt.sentto = "cordinator"
    pickledreq = pickle.dumps(reqpkt)
    sent = sock.sendto(pickledreq, server_address)
    print >> sys.stderr, ' Withdraw Requested : '

def keep_receiving():
    while True:
        print >> sys.stderr, '\nWaiting to receive message'
        data, address = sock.recvfrom(4096)
        resultpickled = pickle.loads(data)

        if resultpickled.data.get_Qtype() == "BALANCE" :
	    if resultpickled.sentfrom == "server1" :
    		print  >> sys.stderr, 'Server 1 Response : %s %s = %s ' % (resultpickled.data.get_qtid(),
        	     resultpickled.data.get_qact(), resultpickled.data.get_qbal())
            elif resultpickled.sentfrom == "server2" :
    		print  >> sys.stderr, 'Server 2 Response : %s %s = %s ' % (resultpickled.data.get_qtid(),
        	     resultpickled.data.get_qact(), resultpickled.data.get_qbal())
	    elif resultpickled.sentfrom == "server3" :
    		print  >> sys.stderr, 'Server 3 Response : %s %s = %s ' % (resultpickled.data.get_qtid(),
        	     resultpickled.data.get_qact(), resultpickled.data.get_qbal())
            client1_data.set_qbal(resultpickled.data.get_qbal())
            if G.get_menu():
                G.set_menu(0)
        elif resultpickled.data.get_Qtype() == "DEPOSIT":
                print >>sys.stderr, 'Updata response'
        elif resultpickled.data.get_Qtype() == "WITHDRAW":
                print >> sys.stderr, 'Deduct response'
        else :
            print >> sys.stderr, 'Invalid Message Type'

def keep_querying():
    while True :
        if not G.get_menu():
            print >> sys.stderr, "\n***** Choice Menu *****\n1. Enquiry\n2. withdraw\n3. deposit "
            num = int(input("\nEnter your choice :"))
            if num == 1:
                request_balance()
		time.sleep(1)
            elif num == 2:
                amttowithdraw = int(input("\nEnter amount to Withdraw :"))
                temp = client1_data.get_qbal()
                temp = temp - amttowithdraw
                client1_data.set_qbal(temp)
                deduct_balance()
            elif num == 3:
                amttodep = int(input("\nEnter amount to Deposit :"))
                temp = client1_data.get_qbal()
                temp = temp + amttodep
                client1_data.set_qbal(temp)
                change_balance()
	    elif num > 3:
		print >> sys.stderr, "\nWrong choice...!!"
            else :
                num = 0
        else:
            count = G.get_count()
            G.set_count(count+1)
            if G.get_count() > 2:
                request_balance()
                G.set_count(0)
                time.sleep(10)



try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = ('10.10.13.67', 5520)
    send_alive()
    thread.start_new_thread(keep_receiving, ())
    thread.start_new_thread(keep_querying, ())
    request_balance()
    G.set_menu(1)

except Exception, e:
    print >> sys.stderr, 'Unable to create thread %s' % str(e)
    print >> sys.stderr, 'closing socket'
    sock.close()

while 1:
	pass
