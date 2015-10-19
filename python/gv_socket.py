import os
import socket
import time
import pylibgv

class gv_socket(object):
    def __init__(self):
	self.so_data = socket.socket(socket.AF_UNIX,socket.SOCK_STREAM)
	self.so_ctrl = socket.socket(socket.AF_UNIX,socket.SOCK_STREAM)
	self.local_address = self.__localaddr()
	self.local_addr    = 0
	self.local_port    = 0
	self.local_vport   = 0

	try:
	    self.gvapi   = pylibgv.pylibgv()
	    self.gvapi.set(self.so_ctrl.fileno())	
	except:
	    # ToDo raise exceptions
	    pass

    def __localaddr(self):
	'''
	    General la direccion local del server unix
	'''
	lua = "%s_%s.unix" % (str(os.getpid()),str(time.time()))
	if os.path.isfile("/tmp/%s" % lua):
	    pass
	else:
	    return lua

    def connect(self, addr, port, vport):
	return self.gvapi.connect(addr,port,vport,self.local_address)

    def bind(self, addr, port, vport):
	
	
x = gv_socket()
print x.local_address
x.connect(1222,1,1)