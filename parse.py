import xml.etree.ElementTree as ET
import itertools 
from host import *

class Parser: 
    def __init__(self, classroom_xml): 
        self.input_file = classroom_xml
        self.classmap = {}

    def get_classmap(self):
        return self.classmap

    def parse_hosts(self): 
        root = ET.parse(self.input_file)
        hosts = []

        continents = root.findall("continent")
        self.classmap["0"] = len(continents)
        for continent in continents:
            islands = continent.findall("island")
            self.classmap[f"0{continent.get('id')}"] = len(islands)
            for island in islands:
                districts = island.findall("district")
                self.classmap[f"0{continent.get('id')}{island.get('id')}"] = len(districts)
                for district in districts:
                    addresses = district.findall("address")
                    self.classmap[f"0{continent.get('id')}{island.get('id')}{district.get('id')}"] = len(addresses)
                    for address in addresses:
                        hosts.append(Host(
                            int(continent.get("id")),
                            int(island.get("id")),
                            int(district.get("id")),
                            int(address.get("id")),
                            address.get('hostname'),
                            int(address.get('port'))
                        ))

        return hosts 
