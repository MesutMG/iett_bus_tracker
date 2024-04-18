import zeep
import json
import re as r


def announcements(line_code):
    url = 'https://api.ibb.gov.tr/iett/UlasimDinamikVeri/Duyurular.asmx?wsdl'
    client = zeep.Client(wsdl=url)
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
    client = zeep.Client(wsdl=url)
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

    stops_locs = []
    for table in stoploc_xml.getchildren():
        l = []
        l.append(table.find('DURAKADI').text)
        l.append(float(table.find('YKOORDINATI').text))
        l.append(float(table.find('XKOORDINATI').text))
        stops_locs.append(l)

    busloc = json.loads(clientbus.service.GetHatOtoKonum_json(line_code))

    bus_locs = []
    for i in busloc:
        match = r.search(r'_(\w)_', i['guzergahkodu']).group(1)
        l = []
        if match == direction:
            l.append(i['kapino'])
            l.append(float(i['enlem']))
            l.append(float(i['boylam']))
            bus_locs.append(l)

    with open("where.js", "w") as file:
        file.write(f'stops = {json.dumps(stops_locs)};\nbuses = {json.dumps(bus_locs)};')

    return 0

