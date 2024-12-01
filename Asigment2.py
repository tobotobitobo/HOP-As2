import json
import csv
import math
from zmaestnanec import Zameamestnanec
from job import Job
import random

# 
with open('possible_zamestnanci.json') as json1:
    possible_zamestnanci_json = json1.read()
with open('formulare_todo.json') as json2:
    formulare_todo_json = json2.read()

lsit = []



possible_zamestnanci = json.loads(possible_zamestnanci_json)
formulare_todo = json.loads(formulare_todo_json)

# dict_list = list(formulare_todo.keys())
# print(dict_list)

# zam_dict = {}
# for caunt, zam in enumerate(possible_zamestnanci):
#     zam_dict[caunt] = 0
#     for doc in dict_list:
#         if(doc in list(zam.keys())):
#             zam_dict[caunt] = zam_dict[caunt] + (5-zam[doc])
#         else:
#            zam_dict[caunt] += 5
# print(zam_dict)
# tobiasov bs

def evaluate(filename):
    with open(filename) as csvfile:
        output_to_check = csv.reader(csvfile)
        slowest = 0
        num_of_hours = 0

        for output_line in output_to_check:
            tipek = {"zam_id": output_line[0],
                    "zamestnanec": possible_zamestnanci[int(output_line[0])],
                    "celkovy cas": 0}
            
            # efficiency = 1

            for i, formular in enumerate(output_line[1:], 1):
                if output_line[i-1] == formular:
                    efficiency -= 0.05 if efficiency>0.5 else 0
                else:
                    efficiency = 1
                    # vzdy nastavi efficiency na 1 na zaciatku formularu lebo output_line[0] nikdy nebude same ako formular

                if formular in tipek['zamestnanec']:
                    tipek['celkovy cas'] += tipek['zamestnanec'][formular] * efficiency
                else:
                    tipek['celkovy cas'] += 5 * efficiency
            print(tipek)
            if tipek['celkovy cas'] > slowest:
                slowest = tipek['celkovy cas']
            num_of_hours += math.ceil(tipek['celkovy cas']/60)
        print("zaplatil si " + str(num_of_hours * 30))
        print("najpomalsi cas je " + str(slowest) + " ")

        return num_of_hours, slowest
    

def randomselect():
    
    zamesnanci = []

    for i,entry in enumerate(possible_zamestnanci):
        zamesnanci.append(Zameamestnanec(i))


    for entry,value in formulare_todo.items():
        for i in range(0,value):
            random.choice(zamesnanci).docs.append(Job(entry))
    with open('output2.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for zamestnanec in zamesnanci:
            writer.writerow([zamestnanec.ID] + zamestnanec.listofnames())
            
    for i in range(0,200):
        switch(zamesnanci)

    with open('output.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for zamestnanec in zamesnanci:
            writer.writerow([zamestnanec.ID] + zamestnanec.listofnames())
    return zamesnanci

def switch(zamestnanci):
    targeted_zamestnanec = random.choice(zamestnanci)
    if len(targeted_zamestnanec.docs) != 0: 
        job_to_switch = random.choice(targeted_zamestnanec.docs)
        targeted_zamestnanec.docs.remove(job_to_switch)
        targeted_zamestnanec2 = random.choice(zamestnanci)
        targeted_zamestnanec2.docs.append(job_to_switch)


randomselect()
evaluate('output.csv')