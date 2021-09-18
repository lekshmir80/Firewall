import pprint
from rich.console import Console
from rich.prompt import Prompt
from rich.text import Text
import os

CONF ={}

console = Console()

def gprint(string):
	console.print(Text(string,style="bold green"))

def rprint(string): 
	console.print(Text(string,style="bold red"))

def yprint(string): 
	console.print(Text(string,style="bold yellow"))

def fw_reload():
	print(os.popen("sudo firewall-cmd --reload").read())
	
def fw_activate():
	gprint("Activating the firewall")
	os.popen("sudo systemctl start firewalld").read()
	
def fw_get_active_zones():
	zone = os.popen("sudo firewall-cmd --get-active-zones").read()
	CONF["ZONE"] = zone.split("\n")[0]
	yprint(zone)

def fw_get_status():
	state = os.popen("sudo firewall-cmd --state").read()
	if state == "running\n":
		yprint("Firewall is active")
	else:
		rprint("Firewall is not active")
		fw_activate()
	fw_get_active_zones()

def get_zone_list():
	zone_lst = os.popen("sudo firewall-cmd --get-zones").read().split(" ")
	zone_lst[-1] = zone_lst[-1][:-1] 
	return zone_lst

def get_zone_details():
	zone_lst = os.popen("sudo firewall-cmd --list-all-zones").read()
	yprint(zone_lst)
	
def fw_add_source_port():
	port = Prompt.ask("\tEnter port number	")
	proto = Prompt.ask("\tEnter protocol	", choices=["tcp","udp"],default="tcp")
	zone =  Prompt.ask("\tEnter zone	", choices=get_zone_list(),default=CONF["ZONE"])
	cmd = "sudo firewall-cmd --add-port="+port+"/"+proto+" --zone="+zone+" --permanent "
	os.popen(cmd).read()
	yprint("\tSource port added!!!!")

def fw_add_port():
	port = Prompt.ask("\tEnter port number	")
	proto = Prompt.ask("\tEnter protocol	", choices=["tcp","udp"],default="tcp")
	cmd = "sudo firewall-cmd --add-port="+port+"/"+proto+" --permanent "
	os.popen(cmd).read()
	yprint("\tPort added!!!!")

def fw_get_services():
	gprint("_________________________________________________________")
	gprint("Service List:")
	cmd = "sudo firewall-cmd --get-services"
	yprint(os.popen(cmd).read())
	gprint("_________________________________________________________")

def fw_add_services():
	fw_get_services()
	service = Prompt.ask("\tEnter service name from above list	")
	zone =  Prompt.ask("\tEnter zone ", choices=get_zone_list(),default=CONF["ZONE"])
	cmd = "sudo firewall-cmd --add-service="+service+" --zone="+zone+" --permanent" 
	yprint(os.popen(cmd).read())
	yprint("\tServices added!!!!")

def fw_add_sources():
	ip_addr = Prompt.ask("\tEnter the ip address	")
	cmd = "sudo firewall-cmd --add-source="+ip_addr+" --permanent" 
	yprint(os.popen(cmd).read())
	yprint("\t Sources added!!!!")
	
def fw_block_ip():
	ip_addr = input("\tEnter the ip to be block:	")
	cmd = "sudo firewall-cmd --permanent --add-rich-rule='rule family='ipv4' source address="+ip_addr+" reject" 
	os.popen(cmd).read()
	yprint("Blocked!!!!")
	
def fw_delete_source_port():
	port = Prompt.ask("\tEnter port number	")
	proto = Prompt.ask("\tEnter protocol	", choices=["tcp","udp"],default="tcp")
	zone =  Prompt.ask("\tEnter zone	", choices=get_zone_list(),default=CONF["ZONE"])
	cmd = "sudo firewall-cmd --remove-port="+port+"/"+proto+" --zone="+zone+" --permanent "
	os.popen(cmd).read()
	yprint("\tSource port deleted!!!!")
	
def fw_delete_port():
	port = Prompt.ask("\tEnter port number	")
	proto = Prompt.ask("\tEnter protocol	", choices=["tcp","udp"],default="tcp")
	cmd = "sudo firewall-cmd --remove-port="+port+"/"+proto+" --permanent "
	os.popen(cmd).read()
	yprint("\tPort deleted!!!!")
	
def fw_delete_services():
	fw_get_services()
	service = Prompt.ask("\tEnter service name from above list	")
	zone =  Prompt.ask("\tEnter zone ", choices=get_zone_list(),default=CONF["ZONE"])
	cmd = "sudo firewall-cmd --remove-service="+service+" --zone="+zone+" --permanent" 
	yprint(os.popen(cmd).read())
	yprint("\tServices deleted!!!!")

def fw_delete_sources():
	ip_addr =  Prompt.ask("\tEnter the ip address	")
	cmd = "sudo firewall-cmd --remove-source="+ip_addr+" --permanent" 
	yprint(os.popen(cmd).read())
	yprint("\t Sources deleted!!!!")
	
def fw_add_rule_menu():
	gprint("\t[1]Add Source Port")
	gprint("\t[2]Add Port")
	gprint("\t[3]Add services")
	gprint("\t[4]Add sources")
	gprint("\t[5]Back to Main menu")

def fw_delete_rule_menu():
	gprint("\t[1]Delete Source Port")
	gprint("\t[2]Delete Port")
	gprint("\t[3]Delete services")
	gprint("\t[4]Delete sources")
	gprint("\t[5]Back to Main menu")

def fw_add_rule():
	fw_add_rule_menu()
	ch = Prompt.ask("Enter your option : ", choices=["1", "2", "3","4","5"])
	if ch == "1":
		fw_add_source_port()
	elif ch == "2":
		fw_add_port()
	elif ch == "3":
		fw_add_services()
	elif ch == "4":
		fw_add_sources()
	elif ch == "5":
		pass
	else:
		pass

def fw_delete_rule():
	fw_delete_rule_menu()
	ch = Prompt.ask("Enter your option : ", choices=["1", "2", "3","4","5"])
	if ch == "1":
		fw_delete_source_port()
	elif ch == "2":
		fw_delete_port()
	elif ch == "3":
		fw_delete_services()
	elif ch == "4":
		fw_delete_sources()
	elif ch == "5":
		pass
	else:
		pass
		

def main_menu():
	gprint("[1] Add rules")
	gprint("[2] Delete rules")
	gprint("[3] Get Active Zones")
	gprint("[4] Get Details of Active Zones")
	gprint("[5] Reload firewall")
	gprint("[6] Block ip address")
	gprint("[7] Exit")



if __name__ == "__main__":
	fw_get_status()
	while True:
		main_menu()
		ch = Prompt.ask("Enter your option : ", choices=["1", "2", "3","4","5","6","7"])
		if ch == "1":
			fw_add_rule()
		elif ch == "2":
			fw_delete_rule()
		elif ch == "3":
			fw_get_active_zones()
		elif ch == "4":
			get_zone_details()
		elif ch == "5":
			fw_reload()
		elif ch == "6":
			fw_block_ip()
		elif ch == "7":
			break;
			
