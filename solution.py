############ Do not change the assignment code value ############
assignment_code = 140110201
name = "Mesut"
surname = "Travacı"
student_id = "231401003"
### Do not change the variable names above, just fill them in ###

import zeep
import json

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
    pass
    
def max_speeds():
    pass
    
def show_line_stops(line_code, direction):
    pass
    
def live_tracking(line_code, direction):
    pass

def main():
    print(announcements('132'))
    return 0


main()