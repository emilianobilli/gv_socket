# gv_socket
GaVer Socket Api

## Instalacion
```
$ python setup.py build
$ python setup.py install
```

## Uso

### Ejemplo Servidor
```
import gv_socket

sk = gv_socket.gv_socket(gv_socket.AF_INET, gv_socket.SOCK_STREAM)
sk.bind (121)
sk.listen()
addr, port, vport = sk.accept()
```

### Ejemplo Cliente
```
import gv_socket

sk = gv_socket.gv_socket(gv_socket.AF_INET, gv_socket.SOCK_STREAM)
sk.connect("0.0.0.0", 3000, 121)
```
