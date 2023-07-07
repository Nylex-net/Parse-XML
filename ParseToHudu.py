import xml.etree.ElementTree as ET

COMPANY_NAME = "City of Fortuna"
FILE_NAME = "config-cityhall.fortuna.local-20230707130041.xml"

# Get parsed XML data from file.
f = open(FILE_NAME, 'r')
pfsense = ET.fromstring(''.join(f.readlines()))
f.close()
gateways = pfsense.find('gateways')

f = open('network-devices.csv', 'w')
content = 'company_name,name,IP Address,Configuration,Subscription/Support Renewal,Notes,Role\n'

for gateway in gateways.findall('gateway_item'):
    ip = gateway.find('gateway').text
    name = gateway.find('name').text
    desc = gateway.find('descr').text
    config = gateway.find('ipprotocol').text
    content += f"{COMPANY_NAME},{name},{ip},{config},,{desc},Wireless\n"
    # print(f"IP: {ip}, Name: {name}, description: {desc}")

f.writelines(content)
f.close()