PYDEV_SOURCE_DIR = "C:/Users\Matthias/.p2/pool/plugins/org.python.pydev_5.1.1.201606162013/pysrc"
 
import sys
 
if PYDEV_SOURCE_DIR not in sys.path:
   sys.path.append(PYDEV_SOURCE_DIR)
 
import pydevd
 
pydevd.settrace()
 
bling = "the parrot has ceased to be"
print(bling)