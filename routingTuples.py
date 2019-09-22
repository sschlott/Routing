# File: routing.py

"""
This module defines a routing table for the ARPANET routing assignment.
Your job in this assignment is to implement the RoutingTable class so
its methods implement the functionality described in the comments.
"""

######TASK: PROPAGTE BAD LINKS TO ENTIRE CO


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
        self.rTable = [(name,0,name)] #name, hops, best link
        self.localTime = 1
        self.lastUpdated = {} #{nodename:localtimewhenitlastupdatedme}
        self.neighbors = {} #{name:routing_table(object)}
        self.ticksToTimeout = 10


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
        #breaks for pt 3, changes all routing in harv's table to 0
        if self.name == 'HARV' and self.localTime >= 20:
            for val in self.rTable:
                if val[0] == destination:
                    temp = val[2]
                    self.rTable.remove(val)
            self.rTable.append((destination,0,temp))
        for val in self.rTable:
            if val[0] == destination:
                    return val[1]


    def getBestLink(self, destination):
        """
        Returns the name of the first node on the path to destination.
        """
        for val in self.rTable:
            if val[0] == destination:
                if val[2] in self.neighbors.keys():
                    return val[2] 

    def checkOnNeighbors(self):
        #evaluates if any neighbors are timed out, removes inactive neighbors
        flagged = []
        for table in self.neighbors.values():
            if self.localTime - self.lastUpdated[table.name] > self.ticksToTimeout:
                # Removes unresponsive nodes from table
                for val in self.rTable:
                    if val[0] == table.name:
                        self.rTable.remove(val)
                        self.removeInactivePath()
                        flagged.append(table.name)
        #considers inactive neighbors as nonexistant until they update you again
        for badname in flagged:
            del self.neighbors[badname]

    def removeInactivePath(self):
        '''
        When self(an inactive node)/table is discovered, remove all references to it
        When a node is Inactive, check that node's neighbors for references to that node
        If neighbors rely on a node that is unusable as well so we call again
            remove references along path to that node (i.e. if val[2] = part of that path)
        '''
        for neighbor in self.neighbors.values():
            for val in neighbor.rTable:
                    if val[2] == self.name:
                        neighbor.rTable.remove(val)
                        neighbor.removeInactivePath()


    def update(self, source, table):
        """
        Updates this routing table based on the routing message just
        received from the node whose name is given by source.  The table
        parameter is the current RoutingTable object for the source.
        """
        #Adds any missing neighbors to my table's list
        if table not in self.neighbors:
            self.neighbors[source] = table
        #Changes neighbor table's last updated to my local time (since it just checked in)  
        self.localTime += 1
        self.lastUpdated[source]=self.localTime
        self.checkOnNeighbors()
        hop_adjustment = 1 #Since all updaters are neighbors this is always 1
        for (k,v,s) in table.rTable:
            adjusted = hop_adjustment+v
            if k in self.getNodeNames():
                if self.getHopCount(k)>adjusted:
                    for val in self.rTable:
                        if k == val[0]:
                            self.rTable.remove(val)
                    self.rTable.append((k,adjusted,source))
            else:
                self.rTable.append((k,adjusted,source))

