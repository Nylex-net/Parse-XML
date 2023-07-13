import xml.etree.ElementTree as ET
import requests
from tkinter import *
from tkinter.filedialog import askopenfile
import json

def portData(companyName, file, rooty):
    COMPANY = options[companyName]
    pfsense = ET.fromstring(file)
    gateways = pfsense.find('gateways')

    # content = 'company_name,name,IP Address,Configuration,Subscription/Support Renewal,Notes,Role\n'
    interfaces = pfsense.find('interfaces')
    wan = interfaces.find('wan')
    lan = interfaces.find('lan')

    content = f"<h1>PFSense</h1><p>Hostname: {pfsense.find('system').find('hostname').text}</p><p>Domain: {pfsense.find('system').find('domain').text}</p>"
    content += f"<h2>Interfaces</h2><ul><li>WAN</li><ul><li>IF: {wan.find('if').text}</li><li>IP Address: {wan.find('ipaddr').text}</li><li>Subnet: {wan.find('subnet').text}</li><li>Description: {wan.find('descr').text}</li></ul>"
    content += f"<li>LAN</li><ul><li>IF: {lan.find('if').text}</li><li>IP Address: {lan.find('ipaddr').text}</li><li>Subnet: {lan.find('subnet').text}</li><li>Description: {lan.find('descr').text}</li></ul></ul>"

    content += "<h2>Static Routes</h2><ul>"
    for route in pfsense.find('staticroutes').findall('route'):
        content += f"<li>{route.find('gateway').text}</li><ul><li>Network: {route.find('network').text}</li><li>Description: {route.find('descr').text}</li></ul>"

    content += "</ul><h2>Gateways</h2><ul>"
    for gateway in gateways.findall('gateway_item'):
        content += f"<li>{gateway.find('name').text}</li><ul><li>Interface: {gateway.find('interface').text}</li><li>Gateway: {gateway.find('gateway').text}</li><li>Weight: {gateway.find('weight').text}</li><li>IP Protocol: {gateway.find('ipprotocol').text}</li><li>Description: {gateway.find('descr').text}</li></ul>"
    content += "</ul>"
    data = {'name':"PFSense", 'content':content, 'company_id':COMPANY}

    api_url = "https://hudu.nylex.net/api/v1/articles"
    headers = {"x-api-key":key, "Content-Type": "application/json"}
    response = requests.post(api_url, headers=headers, data=json.dumps(data))

    print(response.status_code)
    rooty.destroy()
    rooty = Tk()
    rooty.geometry("600x100")
    lbl = Label(rooty, text=f"PFSense has been added to {companyName}'s Knowledge Base." if response.status_code == 200 else "An error occurred in the API request.")
    lbl.pack()
    btn = Button(rooty, text ='OK', command=rooty.destroy)
    btn.pack(side = TOP, pady = 10)
    rooty.mainloop()

def getCompanies():
    api_url = "https://hudu.nylex.net/api/v1/companies?page_size=200"
    headers = {"x-api-key":key, "Content-Type": "application/json"}
    response = requests.get(api_url, headers=headers)
    companyDict = dict()
    if response.status_code == 200:
        for comp in response.json()['companies']:
            companyDict[comp['name']] = comp['id']
        return dict(sorted(companyDict.items(), key=lambda x:x[1]))
    return dict()

# This function will be used to open
# file in read mode and only Python files
# will be opened
def open_file():
    Filer = askopenfile(mode ='r', filetypes =[('XML Files', '*.xml')])
    global FILER
    if Filer is not None:
        FILER = ''.join(Filer.readlines())
        conv.config(state='active')
    else:
        FILER = None
        
f = open("api-key.txt", "r")
key = f.readline()
f.close()
# Create object
root = Tk()
  
# Adjust size
root.geometry("400x200")

options = getCompanies()
optionsList = list()
for comp in options.keys():
    optionsList.append(comp)

# datatype of menu text
clicked = StringVar()
# initial menu text
clicked.set( "Nylex" )

drop = OptionMenu( root , clicked , *optionsList)
drop.pack()

btn = Button(root, text ='Load file', command=open_file)
btn.pack(side = TOP, pady = 10)

conv = Button(root, text ='Add to Hudu', command = lambda:portData(clicked.get(), FILER, root), state='disabled')
conv.pack(side = TOP, pady = 10)
# Execute tkinter
root.mainloop()