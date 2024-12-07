import json
import csv
import math
from zamestnanec import Zamestnanec
from job import Job
from solution import Solution
import random
import copy


def evaluate(filename):
    with open(filename) as csvfile:
        output_to_check = csv.reader(csvfile)
        slowest = 0
        num_of_hours = 0
        cas = 0

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
            cas += tipek['celkovy cas']
            if tipek['celkovy cas'] > slowest:
                slowest = tipek['celkovy cas']

            num_of_hours += math.ceil(tipek['celkovy cas']/60)
        print("")
        print("zaplatil si " + str(num_of_hours * 30))
        print("najpomalsi cas je " + str(slowest) + " ")
        print("celkovy cas je" + str(cas) + " ")

        return num_of_hours*30, slowest, cas



def selectWorkers(possible_zamestnanci):
    zamesnanci = []
    for i, entry in enumerate(possible_zamestnanci):
        zamesnanci.append(Zamestnanec(i))
        if entry and any(key in formulare_todo for key in entry):
            zamesnanci[i].usefull = True

    return zamesnanci

def notRandomSelect(formulare_todo,possible_zamestnanci):
    #vyberu sa zamestnanci
    zamesnanci = selectWorkers(possible_zamestnanci)
    joblist = []
    #inicializacia kazdeho jobu + vytvorenie pravdepodobnosti s ktorimi sa budu davat zamestnancom
    for entry,value in formulare_todo.items():
        for i in range(0,value):
            job = Job(entry)
            job.setpropability(zamesnanci)
            joblist.append(job)

    #s danov pravdepodobnostov sa da job zamestnancovy
    for job in joblist:
        weight = list(job.getPropability().values())
        zam = random.choices(zamesnanci,weights=weight, k=1)[0]
        zam.dictdoc[job.nameofdoc()] += 1

    return zamesnanci


def writedoc(zamestnanci,filename):
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            for zamestnanec in zamestnanci:
                if(len(zamestnanec.listofnames()) > 0):
                    writer.writerow([zamestnanec.ID] + zamestnanec.listofnames())

def load_data(possible_zamestnanci,formulare_todo):
    with open(possible_zamestnanci) as json1:
        possible_zamestnanci_json = json1.read()

    with open(formulare_todo) as json2:
        formulare_todo_json = json2.read()

    return json.loads(possible_zamestnanci_json), json.loads(formulare_todo_json)

def simulated_aneling(T,alpha,limit,output,possible_zamestnanci,formulare_todo,slowest_weight,total_time_weight,hours_weight):
    solution = Solution(notRandomSelect(formulare_todo,possible_zamestnanci))
    while(T > limit):
        newsolution = Solution(copy.deepcopy(solution.get_zamestnanci()))
        newsolution = newsolution.get_neighbour()
        if(newsolution.evaluatefromlist(slowest_weight,total_time_weight,hours_weight) <= solution.evaluatefromlist(slowest_weight,total_time_weight,hours_weight)):
            solution = newsolution
            continue

        ap = math.exp((solution.evaluatefromlist(slowest_weight,total_time_weight,hours_weight) - newsolution.evaluatefromlist(slowest_weight,total_time_weight,hours_weight))/T)
        if(ap > random.uniform(0, 1)):
            solution = newsolution

        T *= alpha
        print(f'{T:0.4f}', solution.evaluatefromlist(slowest_weight,total_time_weight,hours_weight))

    writedoc(solution.get_zamestnanci(), output)
    evaluate(output)


slowest_weight = 1
total_time_weight = 1
hours_weight = 1
possible_zamestnanci,formulare_todo = load_data("possible_zamestnanci.json", "formulare_todo.json")
simulated_aneling(1,0.999,0.01,"output.csv",possible_zamestnanci,formulare_todo,slowest_weight,total_time_weight,hours_weight)

