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
        self.lastUpdated = {}
        self.neighbors = {}
        self.ticksToTimeout = 30
        self.isActive = True

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
        #breaks for pt 3
        if self.name == 'HARV' and self.localTime >= 20:
            return 0
        else: 
            for val in self.rTable:
                if val[0] == destination:
                    if self.name == 'HARV' and self.localTime >= 20:
                        return 0
                    else:
                        return val[1]


    def getBestLink(self, destination):
        """
        Returns the name of the first node on the path to destination.
        """
        #Find the potential neighbors of your starting node
        for val in self.rTable:
            if val[0] == destination:
                if val[2] in self.neighbors.keys():
                    if self.neighbors[val[2]].isActive:
                        return val[2]
                    else:
                        #updates table if inactive node is still present
                        self.rTable.remove(val)

    def checkOnNeighbors(self):
        for table in self.neighbors.values():
            if self.localTime - self.lastUpdated[table.name] > self.ticksToTimeout:
                # Removes unresponsive nodes from table
                for val in self.rTable:
                    if val[0] == table.name:
                        self.rTable.remove(val)
                        table.isActive = False


    def update(self, source, table):
        """
        Updates this routing table based on the routing message just
        received from the node whose name is given by source.  The table
        parameter is the current RoutingTable object for the source.
        """
        if table not in self.neighbors:
            self.neighbors[source] = table
            #Adds any missing neighbors to my table's list
        self.localTime += 1
        #updates my table's local time
        self.lastUpdated[source]=self.localTime
        #Changes neighbor table's last updated to my local time (since it just checked in)
        self.checkOnNeighbors()

        hop_adjustment = 1
        for (k,v,_s) in table.rTable:
            adjusted = hop_adjustment+v
            if k in self.getNodeNames():
                if self.getHopCount(k) >adjusted:
                    for val in self.rTable:
                        if val[0] == k: 
                            self.rTable.remove(val)

                    self.rTable.append((k,adjusted,source))
                #Check who has the better route, update source node if nec
            else:
                self.rTable.append((k,adjusted,source))

