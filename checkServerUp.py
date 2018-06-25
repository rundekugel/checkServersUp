#$Id: $

"""
This is to check, if server is available, tcp and / or web- service running

for copyright see: Apache License
2018 by lifesim.de

"""
import time
import sys


def ping(host):
    """
    Returns 0 if host (str) responds to a ping request.
    Remember that a host may not respond to a ping (ICMP) request even if the host name is valid.
    """

    import subprocess, platform

    # Ping parameters as function of OS
    ping_str = "-n 1" if  platform.system().lower()=="windows" else "-c 1"
    args = "ping " + " " + ping_str + " " + host
    need_sh = False if  platform.system().lower()=="windows" else True

    # Ping
    return subprocess.call(args, shell=need_sh)

    # Pinging
    return system_call(command)
    
    
def checkTcpPort(host, port):
  import socket

  BUFFER_SIZE = 1024
  result=1
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  try:
    s.connect((host, port))
    #s.send(MESSAGE)
    #data = s.recv(BUFFER_SIZE)
    time.sleep(0.7)
    s.close()
    result=0  #ok
  except:
    result =2
  #print "received data:", data
  return result
    
    
def checkHttp(url):
  """
    test if url exists. port can also be part of url.
  """
  import requests

  result=1
  try:
    r = requests.head(url)  #head is faster than get
    if r.ok:
      result=0
    else:
      result=r.status_code
  except:    
      pass
  return result
    
def main():
  result =1
  port=80
  
  if len(sys.argv ) <2:
    print("parameter missig!")
    return 1
  
  url=sys.argv[1]
  
  hostname=url.replace("http://","",1)
  if hostname[:5]=="https":
    port=443
    hostname=url.replace("https://","",1)
  h=hostname.split("/")[0]  #remove trailing path
  h=h.split(":")  #split port
  hostname=h[0]
  if len(h)>1:
    print(h[1])
    if(h[1]!=""):
      try:
        port=int(h[1], 10)
      except:
        pass
  
  result = ping(hostname)
  
  #and then check the result...
  if result ==0:
    print( hostname + ' is up!')
  else:
    print( hostname + ' is down!')
  
  if result==0:
    if( 0== checkTcpPort(hostname, port)):
      print(hostname +" tcp "+str(port)+" open.")
    else:
      print(hostname+  "tcp "+str(port)+" unreachable!")
      result |= 64
      
  r=checkHttp(url)
  if(r >0):
    result |= 32
    print("url problem=["+ str(r) +"] "+ url )
  else:
    print("ok: "+ url)
    
  
  return result 
  
if __name__ == "__main__":  
  sys.exit( main() )
