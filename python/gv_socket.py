import os
import socket
import struct
import time
import pylibgv


def htons(port):
    return socket.htons(port)

def ntohs(port):
    return socket.ntohs(port)


class GaVerError(Exception):
    def __init__(self, value, critical=False):
	self.value    = value
	self.critical = critical
    def __str__(self):
	return repr(self.value)

class gv_socket(object):
    def __init__(self):
	self.so_data = socket.socket(socket.AF_UNIX,socket.SOCK_STREAM)
	self.so_ctrl = socket.socket(socket.AF_UNIX,socket.SOCK_STREAM)
	self.local_address = self.__localaddrunix()
	self.local_addr    = 0
	self.local_port    = 0
	self.local_vport   = 0
	self.remote_addr   = 0
	self.remote_port   = 0
	self.remote_vport  = 0
	self.gv_kernel     = self.getgvdev()

	if self.gv_kernel is None:
	    raise GaVerError('Enviroment: [%s] not found' % 'GV_KERNEL_DEV')

	try:
	    self.gvapi   = pylibgv.pylibgv()
	    self.gvapi.set(self.so_ctrl.fileno())	
	except:
	    # ToDo raise exceptions
	    pass

	try:
	    self.so_ctrl.connect(self.gv_kernel)
	except socket.error as e:   
	    raise GaVerError('Kernel Socket (%s) -> %s' % (self.gv_kernel,str(e)))

	try:
	    self.so_data.bind(self.local_address)
	except socket.error as e:
	    raise GaVerError('Binding local Socket (%s) -> %s' %(self.local_address,str(e)))

    def getgvdev(self):
	return os.getenv('GV_KERNEL_DEV')

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
	    return None
	else:
	    return lua

    def connect(self, addr, port, vport):
	'''
	    Connect Method
	'''
	if isinstance(addr,str):
	    haddr = self.ip2long(addr)
	else:
	    raise GaVerError('ValueError: %s' % 'addr must be a string type')
	
	try:
	    self.gvapi.connect(haddr,htons(port),htons(vport), self.local_address)
	except IOError as e:
	    raise GaVerError('IOError: %s' % str(e))
	except AttributeError as e:
	    raise GaVerError('AttributeError: %s' % str(e))
	except:
	    raise

	try:
	    tmpsocket = self.so_data.accept()
	except socket.error as e:
	    raise GaVerError('Kernel Data Connection -> %s' % str(e))
    
	self.so_data.close()
	self.so_data = tmpsocket
	
	self.remote_addr  = haddr
	self.remote_port  = htons(port)
	self.remote_vport = htons(vport)


    def bind(self, vport):
	'''
	    Bind Method
	'''
	vport = htons(vport)
	try:
	    (addr,port,vport) = self.gvapi.bind(0,0,vport)
    	    self.local_addr  = addr
    	    self.local_port  = port
    	    self.local_vport = vport
	except IOError as e:
	    raise GaVerError('IOError: %s' % str(e))
	except AttributeError as e:
	    raise GaVerError('AttributeError: %s' % str(e))


    def getsockname(self):
	'''
	    Get the local address
	'''
	return (self.long2ip(self.local_addr),
		ntohs(self.local_port),
		ntohs(self.local_vport))


x = gv_socket()
print x.getgvdev()
print x.local_address
print x.getsockname()
