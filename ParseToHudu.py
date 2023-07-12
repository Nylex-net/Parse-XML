import xml.etree.ElementTree as ET
import requests
import os
from tkinter import *
from tkinter.filedialog import askopenfile

def portData(companyName, file, rooty):
    COMPANY_NAME = companyName
    # FILE_NAME = "config-cityhall.fortuna.local-20230710084951.xml"

    # Get parsed XML data from file.
    # f = open(FILE_NAME, 'r')
    # pfsense = ET.fromstring(''.join(f.readlines()))
    # f.close()
    pfsense = ET.fromstring(file)
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

    rooty.destroy()
    rooty = Tk()
    rooty.geometry("600x100")
    lbl = Label(rooty, text="Your network devices CSV has been created.\nLook for 'network-devices.csv' in the same directory as this program.")
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
            companyDict[comp['id']] = comp['name']
    return companyDict

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
        
# def if_selections(selected_value):
#     if Filer is not None:
#         conv.config(state='active')
        
f = open("api-key.txt", "r")
key = f.readline()
f.close()
# Create object
root = Tk()
  
# Adjust size
root.geometry("400x400")

options = getCompanies()
optionsList = list()
for comp in options.values():
    optionsList.append(comp)

# datatype of menu text
clicked = StringVar()
# initial menu text
clicked.set( "Nylex" )

drop = OptionMenu( root , clicked , *optionsList)
drop.pack()

btn = Button(root, text ='Load file', command=open_file)
btn.pack(side = TOP, pady = 10)

conv = Button(root, text ='Convert to CSV', command = lambda:portData(clicked.get(), FILER, root), state='disabled')
conv.pack(side = TOP, pady = 10)
# Execute tkinter
root.mainloop()