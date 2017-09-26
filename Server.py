import socket
import sys
import threading
import BlockChain
import json
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

port = 5000
host = 'localhost'
cl = set()
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
		thechain.addBlock('server block')
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
			elif dt[:4] == '1001':
				nc = (addr[0],rport)
				if cl.__contains__(nc) == False:
					for ss in cl:
						th = tr(int(ss[1]),ss[0],'0110  ' + str(rport) +'  '+nc[0])
						th.start()
						th.join()
					for ss in cl:
						th = tr(int(nc[1]),nc[0],'0101  ' + str(ss[1]) +'  '+ss[0])
						th.start()
						th.join()
					dechain = {}
					for i in range(1,len(thechain.chain)):
						dechain[i] = thechain.chain[i].data
					dej = json.dumps(dechain)
					sdt = '0011  ' + dej
					tt = tr(int(nc[1]),nc[0],sdt)
					tt.start()
					tt.join()
					cl.add(nc)
			elif dt[:4] == '0000':
				wst,rpt = dt.split('  ')
				thechain.addBlock(rpt)
			#print(cl)
			print(thechain)



t1 = td()
t1.start()
t1.join()
