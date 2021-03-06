import socket
import sys
import json
import re

from pyretic.pyresonance.globals import *

def main():
  send_event("10.0.0.1")

def parse_flow(message_payload, flow):
    print "\nFlow = " + flow
    m = re.search("inport=(\d+)\s*",flow)
    if m:
        message_payload['inport'] = m.group(1)
        
    m = re.search("srcmac=(\w\w:\w\w:\w\w:\w\w:\w\w:\w\w)\s*",flow)
    if m:
        message_payload['srcmac'] = m.group(1)

    m = re.search("dstmac=(\w\w:\w\w:\w\w:\w\w:\w\w:\w\w)\s*",flow)
    if m:
        message_payload['dstmac'] = m.group(1)

    m = re.search("srcip=(\d+\.\d+\.\d+\.\d+[\/\d+]*)\s*",flow)
    if m:
        message_payload['srcip'] = m.group(1)

    m = re.search("dstip=(\d+\.\d+\.\d+\.\d+[\/\d+]*)\s*",flow)
    if m:
        message_payload['dstip'] = m.group(1)
 
    m = re.search("tos=(\d+)\s*",flow)
    if m:
        message_payload['tos'] = m.group(1)

    m = re.search("srcport=(\d+)\s*",flow)
    if m:
        message_payload['srcport'] = m.group(1)

    m = re.search("dstport=(\d+)\s*",flow)
    if m:
        message_payload['dstport'] = m.group(1)

    m = re.search("ethtype=(\d+)\s*",flow)
    if m:
        message_payload['ethtype'] = m.group(1)

    m = re.search("protocol=(\d+)\s*",flow)
    if m:
        message_payload['protocol'] = m.group(1)

    m = re.search("vlan_id=(\d+)\s*",flow)
    if m:
        message_payload['vlan_id'] = m.group(1)

    m = re.search("vlan_pcp=(\d+)\s*",flow)
    if m:
        message_payload['vlan_pcp'] = m.group(1)

    print "\nData Payload = " + str(message_payload) + '\n'
  
def send_event(e_srcip):
  message_payload= dict(inport=None,    \
                          srcmac=None,    \
                          dstmac=None,    \
                          srcip=None,     \
                          dstip=None,     \
                          tos=None,       \
                          srcport=None,   \
                          dstport=None,   \
                          ethtype=None,   \
                          protocol=None,  \
                          vlan_id=None,   \
                          vlan_pcp=None)  \
                          
  ops = dict(flow_tuple = "{srcip="+e_srcip+"}",
		 event_type = 'dos_detected',
		 event_trigger =None,
		 file=None,
		 event_query = None,
		 event_state ="denied",
		 event_info=None,
		 port="50003",
		 addr = "127.0.0.1")
		
  print "Options...................................."
  
  flow = ops["flow_tuple"]
  
  parse_flow(message_payload,flow)
  
  message_value = None
  message_type = None
    
  if ops["event_state"] is not None:
      message_value = ops["event_state"]
      message_type = MESSAGE_TYPES['state']

  elif ops["event_trigger"] is not None:
      message_value = ops["event_trigger"]
      message_type = MESSAGE_TYPES['trigger']

  elif ops["event_query"] is not None:
      message_type = MESSAGE_TYPES['query']
      print message_type
      
  # Construct JSON message
  json_message = dict(event=dict(event_type=ops["event_type"],                   \
                                   sender=dict(sender_id=1,                         \
                                               description=1,                       \
                                           addraddr=ops["addr"],             \
                                               port=ops["port"]),                  \
                                    message=dict(message_type=message_type,         \
                                                 message_payload=message_payload,   \
                                                 message_value=message_value),      \
                                    transition=dict(prev=1,                         \
                                                    next=1)                         \
                                   ))

  # Create socket
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.connect((ops["addr"], int(ops["port"])))
  
  bufsize = len(json_message)

  # Send data
  totalsent = 0
  s.sendall(json.dumps(json_message))

  # Receive return value
  recvdata = s.recv(1024)
  print recvdata

  s.close()
                           
if __name__ == '__main__':
    main()