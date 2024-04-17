############ Do not change the assignment code value ############
assignment_code = 140110201
name = "Mesut"
surname = "Travacı"
student_id = "231401003"
### Do not change the variable names above, just fill them in ###

import zeep
import json
import re as r
from pprint import pprint


def announcements(line_code):
    url = 'https://api.ibb.gov.tr/iett/UlasimDinamikVeri/Duyurular.asmx?wsdl'
    client = zeep.Client(wsdl = url)
    anns = json.loads(client.service.GetDuyurular_json())
    l = list()
    a = 0
    for i in anns:
        if i['HATKODU'] == line_code:
            a += 1
            l.append(i['MESAJ'])
    return a,l

def stopping_buses():
    url = 'https://api.ibb.gov.tr/iett/FiloDurum/SeferGerceklesme.asmx?wsdl'
    client = zeep.Client(wsdl = url)
    anns = json.loads(client.service.GetFiloAracKonum_json())
    l = list()
    for i in anns:
        if i['Hiz'] == '0':
            l.append(i['KapiNo'])
    return l

def max_speeds():
    url = 'https://api.ibb.gov.tr/iett/FiloDurum/SeferGerceklesme.asmx?wsdl'
    client = zeep.Client(wsdl=url)
    anns = json.loads(client.service.GetFiloAracKonum_json())
    c1,c2,c3 = 0,0,0
    l = [{},{},{}]
    for i in anns:
        if int(i['Hiz']) >= c1:
            c3 = c2
            c2 = c1
            c1 = int(i['Hiz'])
            l[0] = i
        elif int(i['Hiz']) >= c2:
            c3 = c2
            c2 = int(i['Hiz'])
            l[1] = i
        elif int(i['Hiz']) >= c3:
            c3 = int(i['Hiz'])
            l[2] = i
    return l


def show_line_stops(line_code, direction):
    url = 'https://api.ibb.gov.tr/iett/ibb/ibb.asmx?wsdl'
    client = zeep.Client(wsdl=url)
    xmlfile = client.service.DurakDetay_GYY(line_code)
    l = list()
    for i in xmlfile.findall('Table'):
        if i.find('YON').text == direction:
            l.append(i.find('DURAKADI').text)
    return l

def live_tracking(line_code, direction):
    urlstop = 'https://api.ibb.gov.tr/iett/ibb/ibb.asmx?wsdl'
    urlbus = 'https://api.ibb.gov.tr/iett/FiloDurum/SeferGerceklesme.asmx?wsdl'

    clientstop = zeep.Client(wsdl=urlstop)
    clientbus = zeep.Client(wsdl=urlbus)

    stoploc_xml = clientstop.service.DurakDetay_GYY(line_code)
    stops_locs = list()

    for i in stoploc_xml.findall('Table'):
        l = list()
        if i.find('YON').text == direction:
            l.append(i.find('DURAKADI').text)
            l.append(float(i.find('YKOORDINATI').text))
            l.append(float(i.find('XKOORDINATI').text))
            stops_locs.append(l)

    busloc = json.loads(clientbus.service.GetHatOtoKonum_json(line_code))
    l = list()
    for i in busloc:
        match = r.search(r'_(\w)_', i['guzergahkodu']).group()
        if match == '_' + direction + '_':
            l.append([i['kapino'],float(i['enlem']),float(i['boylam'])])
    print(stops_locs)
    with open("where.js", "w") as file:
        file.write(f'stops = {stops_locs}\nbuses = {l}')

def main():
    pprint(announcements('132C'))
    print(stopping_buses())
    pprint(max_speeds())
    pprint(show_line_stops('132C','G'))
    live_tracking('132C','G')
    return 0
main()
