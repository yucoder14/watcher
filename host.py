from enum import Enum 

class HostStatus(Enum): 
    OK = 0,     # no browser detected
    BAD = 1,    # browser detected
    OFFLINE = 2 # socket connection failed

class Host: 
    def __init__(self, continent, island, district, address, hostname, port):
        # the abstract coordinate system should be converted to some sort of 
        # screen coordinates for drawing 
        self.continent = continent
        self.island = island
        self.district = district
        self.address = address

        # curses related things
        self.y = None 
        self.x = None 
        self.height = None
        self.width = None

        # host's network information
        self.hostname = hostname
        self.port = port

        self.status = HostStatus.OK

    def get_continent(self):
        return self.continent

    def get_island(self):
        return self.island

    def get_district(self):
        return self.district

    def get_address(self):
        return self.address

    def get_curses_dim(self):
        return self.y, self.x, self.height, self.width

    def get_hostname(self):
        return self.hostname

    def get_port(self):
        return self.port

    def get_status(self):
        return self.status 

    def __str__(self):
        return f"network={self.hostname}:{self.port}, coordinate=(c={self.continent}, i={self.island}, d={self.district}, a={self.address})" 

    def set_curses_dim(self, y, x, height, width):
        self.y = y   
        self.x = x   
        self.height = height  
        self.width = width  

    def set_status(self, status):
        self.status = status
