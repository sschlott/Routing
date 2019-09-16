# File: routing.py

"""
This module defines a routing table for the ARPANET routing assignment.
Your job in this assignment is to implement the RoutingTable class so
its methods implement the functionality described in the comments.
"""

class RoutingTable:

    """
    This class implements a routing table, which keeps track of
    two data values for each destination node discovered so far:
    (1) the hop count between this node and the destination, and
    (2) the name of the first node along the minimal path.
    """

    def __init__(self, name):
        """
        Creates a new routing table with a single entry indicating
        that this node can reach itself in zero hops.
        """
        self.name = name
        self.rTable = {name:0}


    def getNodeNames(self):
        """
        Returns an alphabetized list of the known destination nodes.
        """
        print(sorted(self.rTable))

    def getHopCount(self, destination):
        """
        Returns the hop count from this node to the destination node.
        """
        return self.rTable[destination]

    def getBestLink(self, destination):
        """
        Returns the name of the first node on the path to destination.
        """


    def update(self, source, table):
        """
        Updates this routing table based on the routing message just
        received from the node whose name is given by source.  The table
        parameter is the current RoutingTable object for the source.
        """
        hop_adjustment = self.getHopCount(source)
        print(table)
        for k,v in table.items():
            # print(k, " : ", v)
            if k in self.rTable:
                self.rTable[k]= min(self.rTable[k], (v+hop_adjustment))
                print("Swapping",k)
            else:
                self.rTable[k]=v + hop_adjustment
                print("Staying",k)
x= RoutingTable('a')
x.rTable['b'] = 9
x.rTable['c'] = 4
x.rTable['d'] = 6
x.rTable['e'] = 1
yy= RoutingTable('e')
yy.rTable['c'] = 7
yy.rTable['d'] = 13
yy.rTable['f'] = 5
yy.rTable['g'] = 10
yy.rTable['a'] = 1
print(x.rTable)
x.update('e',yy.rTable)
print(x.rTable)


#def optimal(self)
#    for node with 1 hops = next best jump
#    if node has 0 hops = You have arrived 
#0 hops is the optimal to get to oneself
#You must follow a pth of 1 hop every time
#How do we determinewhich diection to take? 
#min ( neighbor1.table(destination.hops) vs neighbor2.table.destination.hops)