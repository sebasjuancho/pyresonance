################################################################################
# Mininet Test Topologies                                                    #
# author: Juan Sebastian Silva Delgado(js.silva266@uniandes.edu.co)                                        #
################################################################################

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import RemoteController   
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.cli import CLI
from mininet.util import irange,dumpNodeConnections
from mininet.log import setLogLevel

################################################################################
# sudo mn --controller=remote,ip=127.0.0.1 --custom test_topos.py --topo ddos --link=tc --mac --arp
################################################################################


class DDoS_Test(Topo):
   def __init__(self):
      Topo.__init__(self)
      h1 = self.addHost( 'h1' )
      h2 = self.addHost( 'h2' )
      h3 = self.addHost( 'h3' )
      h4 = self.addHost( 'h4' )
      h5 = self.addHost( 'h5' )
      h6 = self.addHost( 'h6' )
      
      s1 = self.addSwitch('s1')
      s2 = self.addSwitch('s2')
      
      self.addLink(h1,s1, bw=10)
      self.addLink(h2,s1, bw=10)
      self.addLink(h3,s1, bw=10)
      
      self.addLink(s1,s2, bw=10)
      
      self.addLink(h4,s2, bw=10)
      self.addLink(h5,s2, bw=10)
      self.addLink(h6,s2, bw=10)
     


class Server_LB( Topo ):
  def __init__(self):
    # Initialize topology
    Topo.__init__( self )

    # Add hosts and switches
    h1 = self.addHost( 'h1' )
    h2 = self.addHost( 'h2' )
    h3 = self.addHost( 'h3' )
    h4 = self.addHost( 'h4' )

    s1 = self.addSwitch( 's1' )
    s2 = self.addSwitch( 's2' )
    s3 = self.addSwitch( 's3' )

    # Add links
    self.addLink( h1, s1 )
    self.addLink( h2, s2 )
    self.addLink( h3, s2, delay='100ms')
    self.addLink( h4, s3 )
    
    self.addLink( s1, s2 )
    self.addLink( s2, s3)


class Ratelimit( Topo ):
  def __init__(self):
    # Initialize topology
    Topo.__init__( self )

    # Add hosts and switches
    h1 = self.addHost( 'h1' )
    h2 = self.addHost( 'h2' )

    s1 = self.addSwitch( 's1' )
    s2 = self.addSwitch( 's2' )
    s3 = self.addSwitch( 's3' )
    s4 = self.addSwitch( 's4' )

    # Add links
    self.addLink( h1, s1 )
    self.addLink( h2, s4 )
    self.addLink( s1, s2 )
    self.addLink( s1, s3, delay='100ms')
    self.addLink( s2, s4 )
    self.addLink( s3, s4 )

##### Topologies #####
topos = {
          'server_lb' : ( lambda: Server_LB() ),   \
          'ratelimit' : ( lambda: Ratelimit() ),   \
          'ddos' : ( lambda: DDoS_Test() ),   \
        }
