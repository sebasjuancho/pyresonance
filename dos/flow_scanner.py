################################################################################
# SDN Security Project                                                            #
# Resonance implemented with Pyretic platform 
# author: Juan Sebastian Silva Delgado (js.silva266@uniandes.edu.co)
################################################################################

from pyretic.lib.corelib import *
from pyretic.lib.std import *

#TODO implementar analisis de flujo de paquetes que genera el evento para cambio de estado
#meter en la composicion de resonance

def learn(self):
    """Standard MAC-learning logic"""
    def update_policy():
        """Update the policy based on current forward and query policies"""
        self.policy = self.forward + self.query
    self.update_policy = update_policy

    def learn_new_MAC(pkt):
        """Update forward policy based on newly seen (mac,port)"""
        self.forward = if_(match(dstmac=pkt['srcmac'],
                                switch=pkt['switch']),
                          fwd(pkt['inport']),
                          self.forward) 
        self.update_policy()

    def set_initial_state():
        self.query = packets(1,['srcmac','switch'])
        self.query.register_callback(learn_new_MAC)
        self.forward = self.flood  # REUSE A SINGLE FLOOD INSTANCE
        self.update_policy()

    def set_network(network):
        Policy.set_network(self,network)  # AVOID UNECESSARY CALCULATIONS IN INTERNAL POLICY ABOUT TO BE REPLACED
        set_initial_state()
       
    self.set_network = set_network
    self.flood = flood()           # REUSE A SINGLE FLOOD INSTANCE
    set_initial_state()


def mac_learner():
    """Create a dynamic policy object from learn()"""
    return dynamic(learn)()

def main():
    return mac_learner()
