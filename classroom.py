import curses
from parse import Parser
from host import Host, HostStatus
from proctor import ProctorServer 
from functools import partial
import time

class Classroom: 
    def __init__(self, classroom_xml, stdscr): 
        parser = Parser(classroom_xml)
        self.hosts = parser.parse_hosts()
        self.classmap = parser.get_classmap()
        self.stdscr = stdscr
        self.screen_height, self.screen_width = stdscr.getmaxyx()
        self.margin = 1
        self.proctor = ProctorServer(self.hosts)

    def get_hosts(self):
        return self.hosts 

    def get_classmap(self):
        return self.classmap

    def begin_test(self):
        self.proctor.send_messages("begin test")

    def determine_dim(self): 
        # determine the height of each host
        total_rows = 0
        max_rows = [] # indexed by continent 
        num_continents = self.classmap['0']
        for continent in range(num_continents): 
            num_islands = self.classmap[f'0{continent}']
            max_district = max([self.classmap[f'0{continent}{island}'] for island in range(num_islands)])
            max_rows.append(max_district)
            total_rows = total_rows + max_district

        host_height = (self.screen_height - num_continents - 1) // total_rows
        
        if host_height < 3:
            raise ValueError("Small Screen: increase the screen height by making the font smaller or screen taller")

        host_widths = [] # indexed by continent 
        max_cols = [[] for i in range(self.classmap['0'])] # indexed by continent and island 
        # determine the width of each host per continent
        for continent in range(num_continents):
            total_cols = 0 
            num_islands = self.classmap[f'0{continent}']
            for island in range(num_islands): 
                num_district = self.classmap[f'0{continent}{island}']
                max_address = max([self.classmap[f'0{continent}{island}{district}'] for district in range(num_district)])
                max_cols[continent].append(max_address)
                total_cols = total_cols + max_address
            
            host_width = (self.screen_width - num_islands - 1) // total_cols
            
            if host_width < 3: 
                raise ValueError("Small Screen: increase the screen width by making the font smaller or screen wider")

            host_widths.append(host_width)

        for host in self.hosts: 
            continent = host.get_continent()
            island = host.get_island()
            district = host.get_district()
            address = host.get_address()

            # calculate y, x position of the hosts
            continent_y = self.margin
            island_y = sum([max_rows[i] * host_height + self.margin for i in range(continent)]) 
            district_y = district * host_height 
            address_y = continent_y + island_y + district_y 

            continent_x = self.margin
            island_x = sum([max_cols[continent][i] * host_widths[continent] + self.margin for i in range(island)])
            district_x = 0
            address_x = continent_x + island_x + host_widths[continent] * address

            host.set_curses_dim(address_y, address_x, host_height, host_widths[continent])

    def draw(self): 
        self.stdscr.clear()
        for host in self.hosts:
            name = host.get_hostname()
            y, x, height, width = host.get_curses_dim()

            status_color = curses.color_pair(1) if host.get_status() == HostStatus.OK else curses.color_pair(2)
            attributes = curses.A_BOLD | curses.color_pair(3) if host.get_status() == HostStatus.OK else curses.A_BOLD | curses.A_BLINK | curses.color_pair(4) 

            win = self.stdscr.subwin(height, width, y, x)

            win.attron(status_color)
            win.box()
            win.attroff(status_color)

            win.addstr(height // 2, width // 2 - len(name) // 2, name, attributes)             
        self.stdscr.refresh()

    def check(self): 
        with open("log", "a") as file:
            returns = self.proctor.query_testers()

#            for host in self.hosts: 
#                host.set_status(HostStatus.BAD)

        for violation, host in zip(returns, self.hosts):
            if violation.find("True") != -1:
                host.set_status(HostStatus.BAD)
            else:
                host.set_status(HostStatus.OK)

#            map(lambda violation, host: host.set_status(HostStatus.BAD) if violation == "True" else host.status(HostStatus.OK), 
#                    returns, self.hosts)
#            file.write(str([host.get_status() for host in self.hosts])+"\n")

        return
    
def main(classroom_xml, stdscr):
    curses.curs_set(0)
    stdscr.clear()

    curses.start_color();
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_GREEN);
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_RED);
    curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK);
    curses.init_pair(4, curses.COLOR_RED, curses.COLOR_BLACK);

    classroom = Classroom(classroom_xml, stdscr)
    classroom.determine_dim()
    classroom.begin_test()
    while True:
        try: 
            classroom.check()
            classroom.draw()
            time.sleep(0.1)
        except KeyboardInterrupt:
            break

curses.wrapper(partial(main, "localhost.xml"))


