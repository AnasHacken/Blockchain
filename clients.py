import socket
import sys
import threading
import BlockChain
import json
import sys
thechain = BlockChain.BlockChain()
theq = []
def getfile(cmt):
	rqd = []
	for i in range(2,len(thechain.chain)):
		dt = blk.data.split(' ## ')
		if cmt == int(dt[0]):
			rqd = dt
			break
	return rdq
def addFile(cmt,nme,fsize,fcode,pf):
	data = cmt+' ## '+nme+' ## '+fsize+' ## '+fcode+' ## '+pf
	theq.append(data)

port = 5200
host = 'localhost'
serveradd = sys.argv[1]
cl = {(serveradd,'5000')}
class tr(threading.Thread):
	def __init__(self,port,host,data):
		super(tr,self).__init__()
		self.port = port
		self.host = host
		self.data = data
		self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

	def run(self):
		global port
		msg = self.data
		at = msg + ' $$ ' + str(port) 
		self.s.sendto(at.encode('utf-8'),(self.host,self.port))

class td(threading.Thread):
	def __init__(self):
		super(td,self).__init__()
		global port
		self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.s.bind(("", port))
		print("waiting on port:", port)
		
	def run(self):
		global thechain
		while True:
			data, addr = self.s.recvfrom(1024)
			print(data,addr)
			inf = data.decode('utf-8')
			dt,rport = inf.split(' $$ ')
			if dt[:4] == '0110':
				wst,rpt,adrs = dt.split('  ')
				nc = (adrs,int(rpt))
				if cl.__contains__(nc) == False:
					cl.add(nc)
			elif dt[:4] == '0101':
				wst,rpt,rhst = dt.split('  ')
				nc = (rhst,int(rpt))
				if cl.__contains__(nc) == False:
					cl.add(nc)
			elif dt[:4] == '0011':
				wst,newchain = dt.split('  ')
				dechain = json.loads(newchain)
				for a in dechain:
					thechain.addBlock(dechain[a])
				print(thechain)
			elif dt[:4] == '1001':
				nc = (addr[0],rport)
				if cl.__contains__(nc) == False:
					for ss in cl:
						th = tr(int(ss[1]),ss[0],'0110  ' + str(rport)+'  '+nc[0])
						th.start()
						th.join()
					cl.add(nc)
			elif dt[:4] == '0000':
				wst,rpt = dt.split('  ')
				thechain.addBlock(rpt)
			#print(cl)
			#print(thechain)

class dtr(threading.Thread):
	def __init__(self):
		super(dtr,self).__init__()
	def run(self):
		data  = "first pinggg"
		global port
		global thechain
		for nc in cl:
			host = nc[0]
			pt = int(nc[1])
			s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
			msg = data
			at = '1001  ' + msg + ' $$ ' + str(port) 
			s.sendto(at.encode('utf-8'),(host,pt))
		while True:
			data = input("enter data")
			thechain.addBlock(data)
			for nc in cl:
				host = nc[0]
				pt = int(nc[1])
				s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
				msg = data
				at = '0000  ' + msg + ' $$ ' + str(port) 
				s.sendto(at.encode('utf-8'),(host,pt))
	

t1 = td()
t2 = dtr()
t1.start()
t2.start()
t1.join()
t2.join()

