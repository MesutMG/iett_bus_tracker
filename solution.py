############ Do not change the assignment code value ############
assignment_code = 140110201
name = "Mesut"
surname = "Travacı"
student_id = "231401003"
### Do not change the variable names above, just fill them in ###

import zeep
import json
from pprint import pprint

'''
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
'''

def show_line_stops(line_code, direction):
    url = 'https://api.ibb.gov.tr/iett/ibb/ibb.asmx?wsdl'
    client = zeep.Client(wsdl=url)
    return client.service.DurakDetay_GYY(line_code)

def live_tracking(line_code, direction):
    pass

def main():
    print(show_line_stops('16S','G'))
    return 0

from lxml import etree

xml_string = show_line_stops('19T','G')
root = etree.parse(xml_string)
print(root)
