import pprint
from rich.console import Console
from rich.prompt import Prompt
from rich.text import Text
from time import sleep
import os
console = Console()

def gprint(string):
	console.print(Text(string,style="bold green"))

def rprint(string): 
	console.print(Text(string,style="bold red"))

def yprint(string): 
	console.print(Text(string,style="bold yellow"))
	
def ufw_activate():
	os.popen("sudo ufw enable")
	yprint("Activating..........................................")
	sleep(2)
	yprint("Activated")
	
def ufw_deactivate():
	os.popen("sudo ufw disable")
	
def get_status():
	state = os.popen("sudo ufw status").read().split(":")
	if state[1] == " active\n":
		yprint("ufw is active")
	else:
		rprint("ufw is not active")
		ufw_activate()
		
def status_show():
	yprint(os.popen("sudo ufw status numbered").read())

def allow_from():
	ch_al_de = Prompt.ask("\tEnter the choice",choices=["allow","deny"])
	ch_fr_to = Prompt.ask("\tEnter the choice",choices=["from","to"])
	return (ch_al_de,ch_fr_to)
	
def interface_list():
	interfaces = os.popen('ip l | cut -d":" -f2 | tr -d " " | cut -d" " -f1').read().split('\n')
	interfaces.pop(4)
	interfaces_list = interfaces[0::2]
	interface_ch = Prompt.ask("\tEnter Interface", choices=interfaces_list, default="ens33")
	return interface_ch
			
def allow_deny_ip():
	ch_al_de,ch_fr_to = allow_from()
	ip_addr = Prompt.ask("\tEnter the ip address")
	os.popen(f"sudo ufw {ch_al_de} {ch_fr_to} {ip_addr}")
	yprint("Wait....................................")
	sleep(2)
	yprint("Done!!!!!")

def allow_deny_subnet():
	ch_al_de,ch_fr_to = allow_from()
	ip_addr = Prompt.ask("\tEnter the ip address")
	os.popen(f"sudo ufw {ch_al_de} {ch_fr_to} {ip_addr}")
	yprint("Wait....................................")
	sleep(2)
	yprint("Done!!!!!")

def allow_deny_interface():
	ch_al_de,ch_fr_to = allow_from()
	ch_in_out = Prompt.ask("\tEnter the choice",choices=["in","out"])
	ch_inter = interface_list()
	ip_addr = Prompt.ask("\tEnter the ip address")
	os.popen(f"sudo ufw {ch_al_de} {ch_in_out} on {ch_inter} {ch_fr_to} {ip_addr}")
	yprint("Wait....................................")
	sleep(2)
	yprint("Done!!!!!")
	
def allow_deny_port():
	ch_al_de = Prompt.ask("\tEnter the choice",choices=["allow","deny"])
	port_num = Prompt.ask("\tEnter the port number")
	os.popen(f"sudo ufw {ch_al_de} {port_num}")
	yprint("Wait....................................")
	sleep(2)
	yprint("Done!!!!!")

def allow_deny_certain_protocol():
	ch_al_de,ch_fr_to = allow_from()
	ch_proto = Prompt.ask("\tEnter the choice",choices=["tcp","udp","http"])
	port_num = Prompt.ask("\tEnter the port number")
	os.popen(f"sudo ufw {ch_al_de} {ch_fr_to} any to any proto {ch_proto} port {port_num}")
	yprint("Wait....................................")
	sleep(2)
	yprint("Done!!!!!")
	
def reload_rules():
	yprint("Wait....................................")
	os.popen("sudo ufw reload")
	sleep(2)
	yprint("Reloaded!!!!!")

def delete_rules():
	status_show()
	index_num = Prompt.ask("\tEnter the index number")
	index_num = int(index_num)
	yprint("Wait....................................")
	gprint("Proceed with operation (y|n)?")
	os.popen(f"sudo ufw delete {index_num}").read()
	sleep(2)
	yprint("Deleted!!!!!")
	
def main_menu():
	gprint("[1] Allow/Block Host IP")
	gprint("[2] Allow/Block Subnet")
	gprint("[3] Allow/Block Interface")
	gprint("[4] Allow/Block Port")
	gprint("[5] Allow/Block Certain Protocol")
	gprint("[6] Reload the rules")
	gprint("[7] Show Status")
	gprint("[8] Delete the rules")
	gprint("[9] Exit")


if __name__ == "__main__":
	get_status()
	while True:
		main_menu()
		ch = Prompt.ask("Enter your option : ", choices=["1", "2", "3","4","5","6","7","8","9"])
		if ch == "1":
			allow_deny_ip()
		elif ch == "2":
			allow_deny_subnet()
		elif ch == "3":
			allow_deny_interface()
		elif ch == "4":
			allow_deny_port()
		elif ch == "5":
			allow_deny_certain_protocol()
		elif ch == "6":
			reload_rules()
		elif ch == "7":
			status_show()
		elif ch == "8":
			delete_rules()
		elif ch == "9":
			break;
