import os
import socket
import struct
import time
import pylibgv


def htons(port):
    return socket.htons(port)

def ntohs(port):
    return socket.ntohs(port)

class gv_socket(object):
    def __init__(self):
	self.so_data = socket.socket(socket.AF_UNIX,socket.SOCK_STREAM)
	self.so_ctrl = socket.socket(socket.AF_UNIX,socket.SOCK_STREAM)
	self.local_address = self.__localaddrunix()
	self.local_addr    = 0
	self.local_port    = 0
	self.local_vport   = 0

	try:
	    self.gvapi   = pylibgv.pylibgv()
	    self.gvapi.set(self.so_ctrl.fileno())	
	except:
	    # ToDo raise exceptions
	    pass

	self.so_ctrl.connect("/dev/gaver")
    
    def ip2long(self,ip):
	'''
        Convert an IP string to long
	'''
	packedIP = socket.inet_aton(ip)
        return socket.htonl(struct.unpack("!L", packedIP)[0])

    def long2ip(self, ip):
	'''
        Convert an Long to IP string
	'''
	return socket.inet_ntoa(struct.pack('!L',socket.ntohl(ip)))

    def __localaddrunix(self):
	'''
	    General la direccion local del server unix
	'''
	lua = "%s_%s.unix" % (str(os.getpid()),str(time.time()))
	if os.path.isfile("/tmp/%s" % lua):
	    pass
	else:
	    return lua

    def connect(self, addr, port, vport):
	'''
	    Connect Method
	'''
	if isinstance(addr,str):
	    haddr = self.ip2long(addr)
	else:
	    raise ValueError("addr must be a string type")
	
	try:
	    return self.gvapi.connect(haddr,
				  htons(port),
				  htons(vport),
				  self.local_address)
	except:
	    pass
    
    def bind(self, vport):
	'''
	    Bind Method
	'''
	print type(vport)
	(addr,port,v) = self.gvapi.bind(0,0,vport)
    	self.local_addr  = addr
    	self.local_port  = port
    	self.local_vport = v
	
	
    def getsockname(self):
	'''
	    Get the local address
	'''
	return (self.long2ip(self.local_addr),
		ntohs(self.local_port),
		ntohs(self.local_vport))

x = gv_socket()
print x.local_address
x.bind(200)
print x.getsockname()
