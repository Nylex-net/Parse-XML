import xml.etree.ElementTree as ET

COMPANY_NAME = "City of Fortuna"
FILE_NAME = "config-cityhall.fortuna.local-20230710084951.xml"

# Get parsed XML data from file.
f = open(FILE_NAME, 'r')
pfsense = ET.fromstring(''.join(f.readlines()))
f.close()
gateways = pfsense.find('gateways')

content = 'company_name,name,IP Address,Configuration,Subscription/Support Renewal,Notes,Role\n'

for gateway in gateways.findall('gateway_item'):
    ip = gateway.find('gateway').text
    name = gateway.find('name').text
    desc = gateway.find('descr').text
    config = gateway.find('ipprotocol').text
    content += f"{COMPANY_NAME},{name},{ip},{config},,{desc},Wireless\n"
    # print(f"IP: {ip}, Name: {name}, description: {desc}")

interfaces = pfsense.find('interfaces')
wan = interfaces.find('wan')
lan = interfaces.find('lan')

content += f"{COMPANY_NAME},{wan.find('if').text},{wan.find('ipaddr').text},WAN,,{wan.find('subnet').text},Firewall\n"
content += f"{COMPANY_NAME},{lan.find('if').text},{lan.find('ipaddr').text},LAN,,{lan.find('subnet').text},Firewall"

f = open('network-devices.csv', 'w')
f.writelines(content)
f.close()