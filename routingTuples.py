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
        Third value in tuple indicates best path source for a node
        """
        self.name = name
        self.rTable = [(name,0,name)]
        self.localTime = 1
        self.lastUpdated = 1 
        self.neighbors = []
        self.ticksToTimeout = 20
        self.isActive = True
    def removeUnresponsive(self):
        ''''''

    def getNodeNames(self):
        """
        Returns an alphabetized list of the known destination nodes.
        """
        nodes_list= []
        for item in (self.rTable):
            nodes_list.append(item[0])
        return sorted(nodes_list)

    def getHopCount(self, destination):
        """
        Returns the hop count from this node to the destination node.
        """
        for val in self.rTable:
            if val[0] == destination:
                return val[1]


    def getBestLink(self, destination):
        """
        Returns the name of the first node on the path to destination.
        """
        #Find the potential neighbors of your starting node
        for val in self.rTable:
            if val[0] == destination:
                return val[2]

    def checkOnNeighbors(self):
        for table in self.neighbors:
            if self.localTime - table.lastUpdated <= self.ticksToTimeout:
                table.isActive = False
    def update(self, source, table):
        """
        Updates this routing table based on the routing message just
        received from the node whose name is given by source.  The table
        parameter is the current RoutingTable object for the source.
        """
        if table not in self.neighbors:
            self.neighbors.append(table)
        self.localTime += 1
        self.lastUpdated = self.localTime

        self.checkOnNeighbors()
        table.isActive= True
        print(time,self.name)
        hop_adjustment = 1
        for (k,v,_s) in table.rTable:
            adjusted = hop_adjustment+v
            if k in self.getNodeNames():
                if self.getHopCount(k) >adjusted:
                    for val in self.rTable:
                        if val[0] == k: 
                            # print("Replacing", k,adjusted, source)
                            self.rTable.remove(val)

                    self.rTable.append((k,adjusted,source))
                #Check who has the better route, update source node if nec
            else:
                self.rTable.append((k,adjusted,source))
                # print("Adding", k,adjusted,source)

# x= RoutingTable('a')
# x.rTable.append(('d',6,'a'))
# x.rTable.append(('e',5,'a'))
# x.rTable.append(('b',1,'a'))
# x.rTable.append(('c',9,'a'))

# x.rTable.append(('f',7,'a'))
# x.rTable.append(('g',10,'a'))
# yy= RoutingTable('b')
# yy.rTable.append(('b',0,'b'))
# yy.rTable.append(('a',1,'b'))
# yy.rTable.append(('c',2,'b'))
# yy.rTable.append(('d',7,'b'))
# yy.rTable.append(('e',5,'b'))

# print(x.rTable)
# x.update('b',yy.rTable)
# print(x.rTable)


#def optimal(self)
#    for node with 1 hops = next best jump
#    if node has 0 hops = You have arrived 
#0 hops is the optimal to get to oneself
#You must follow a pth of 1 hop every time
#How do we determinewhich diection to take? 
#min ( neighbor1.table(destination.hops) vs neighbor2.table.destination.hops)