import json
import csv
import math
from zamestnanec import Zamestnanec
from job import Job
from solution import Solution
import random
import copy

# 
with open("HOP-As2/possible_zamestnanci.json") as json1:
    possible_zamestnanci_json = json1.read()
with open("HOP-As2/formulare_todo.json") as json2:
    formulare_todo_json = json2.read()




possible_zamestnanci = json.loads(possible_zamestnanci_json)
formulare_todo = json.loads(formulare_todo_json)

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

def evaluatefromlist(zamestnanci):
    
    slowest = 0
    num_of_hours = 0
    celkovy_cas = 0
    for zamestnanec in zamestnanci:
        zamestnanec.sort()
        cas = zamestnanec.gettotalspeed()
        if cas > slowest:
            slowest = cas
        celkovy_cas += cas
        num_of_hours += math.ceil(cas/60)
    # print("zaplatil si " + str(num_of_hours * 30))
    # print("najpomalsi cas je " + str(slowest) + " ")

    return slowest
    

def randomselect():
    zamesnanci = []

    for i,entry in enumerate(possible_zamestnanci):
        zamesnanci.append(Zamestnanec(i))
    #vitvorim list zamesnancov a taktiez instancie zamesnancov 

    for entry,value in formulare_todo.items():
        for i in range(0,value):
            random.choice(zamesnanci).docs.append(Job(entry))
    #zaradom idem po vsetkych joboch a priradzujem ich random zamesnancovy zaroven vytvaram instancie joboch
    writedoc(zamesnanci, "HOP-As2/output.csv")
    #vypisem vsetko do csv filu ako ID + joby ktore ma priradene
    return zamesnanci



def writedoc(zamesnanci,filename):
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            for zamestnanec in zamesnanci:
                writer.writerow([zamestnanec.ID] + zamestnanec.listofnames())


def switch(zamestnanci):
    targeted_zamestnanec = random.choice(zamestnanci)
    if len(targeted_zamestnanec.docs) != 0: 
        job_to_switch = random.choice(targeted_zamestnanec.docs)
        targeted_zamestnanec.docs.remove(job_to_switch)
        targeted_zamestnanec2 = random.choice(zamestnanci)
        targeted_zamestnanec2.docs.append(job_to_switch)
    #zoberiem job zamesnancovy a pridam ho inemu zamesnancovy aka zmenim zamesnanca pri jobe...
    return zamestnanci

    
solution = Solution(randomselect())
writedoc(solution.zamesnanci, "HOP-As2/output.csv")
evaluate('HOP-As2/output2.csv')
evaluatefromlist(solution.zamesnanci)
for i in range(0,2000):
    newsolution = Solution(copy.deepcopy(solution.zamesnanci))
    switch(newsolution.zamesnanci)
    if(evaluatefromlist(newsolution.zamesnanci) < evaluatefromlist(solution.zamesnanci)):
        solution.zamesnanci = copy.deepcopy(newsolution.zamesnanci)
        
    print(evaluatefromlist(solution.zamesnanci))
writedoc(solution.zamesnanci, "HOP-As2/output2.csv")
evaluate("HOP-As2/output2.csv")
