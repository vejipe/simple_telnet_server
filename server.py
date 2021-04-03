# Rich telnet server
# By Vincent Jordan
# 2021.03.31

# Based on 'socketserver' example from official documentation:
# https://docs.python.org/3/library/socketserver.html#examples

# Python TextIOWrapper docs:
# https://docs.python.org/3/library/io.html#io.TextIOWrapper

# Rich terminal text formatting docs:
# - https://rich.readthedocs.io/en/stable/reference/console.html
# - https://rich.readthedocs.io/en/latest/reference/table.html

import io
import socketserver
from rich.console import Console
from rich.table import Column, Table
from rich import box

# Notes about socketserver request handler base classes:
# - "BaseRequestHandler" is the base class for all request handler
# -- "StreamRequestHandler" (TCP) adds self.rfile and self.wfile
#    (for more convenient data processing)
# Note about socketserver servers types:
# - {TCP, UDP}Server => can process one request at a time
# - {Forking, Threading}{TCP, UDP}Server
#    => can process multiple requests in parallel
# See the end of the file for server creation code.

class MyTCPHandler(socketserver.StreamRequestHandler):
    def handle(self):
        # self.request is the TCP socket connected to the client
        print("{}".format(self.client_address[0]))
        
        self.wfile.write("\r\nWelcome to Vincent's telnet service!\r\n---\r\n".encode(encoding="ascii"))
        self.wfile.write("Choose terminal mode:\r\n".encode(encoding="ascii"))
        self.wfile.write("0 => UTF-8\r\n".encode(encoding="ascii"))
        self.wfile.write("1 => ASCII\r\n".encode(encoding="ascii"))
        resp = self.request.recv(1024).strip()

        encoding = "utf8"
        box_type = box.ROUNDED
        if(resp != '' and int(resp) == 1):
            encoding = "ascii"
            box_type = box.ASCII
            self.wfile.write("Enabled ASCII mode\r\n\r\n".encode(encoding="ascii"))
        else:
            self.wfile.write("Enabled UTF-8 mode\r\n\r\n".encode(encoding="ascii"))

        # TextIOWrapper converts 'string' to 'byte' (aka encode)
        wfilet = io.TextIOWrapper(self.wfile, encoding=encoding, newline="\r\n")

        # Rich console init using socketserver wrapped self.wfile
        console = Console(file=wfilet, force_terminal=True, color_system="256", no_color=False, width=80)
        
        # Rich terminal display code starts here
        ###
        console.rule("[bold red]This is a demo")
        
        table = Table(show_header=False, expand=True, box=box_type)
        table.add_column("", justify="center")
        table.add_column("", justify="center")
        table.add_column("", justify="center")
        table.add_row("[i green]This a table", "with [white on blue]nice text inside", "Even link works [u blue]http://ibm.com", )
        console.print(table)
        
        console.print("\n[b green]Have a nice day~\n")

        #console.print("Enter to leave...\n")
        self.data = self.request.recv(1024).strip()

if __name__ == "__main__":
    HOST, PORT = "0.0.0.0", 9999

    # Create the server, binding to localhost on port 9999
    with socketserver.ForkingTCPServer((HOST, PORT), MyTCPHandler) as server:
        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        server.serve_forever()
