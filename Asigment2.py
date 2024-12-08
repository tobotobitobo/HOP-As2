import json
import csv
import math
from zamestnanec import Zamestnanec
from job import Job
from solution import Solution
import random
import copy

#tato funkcia je len za kontrolovanie a zobrazenie vysledkov nijako nepomaha v programe
def evaluate(filename):
    #vďaka  tejto metóde okrem csv outputu vypíšeme info k nášmu riešeniu do konzoly
    with open(filename) as csvfile:
        output_to_check = csv.reader(csvfile)
        slowest = 0
        num_of_hours = 0
        cas = 0

        for output_line in output_to_check:
            tipek = {"zam_id": output_line[0],
                    "zamestnanec": possible_zamestnanci[int(output_line[0])],
                    "celkovy cas": 0}
            #dictionary so vsetkymi zamestnancamy

            for i, formular in enumerate(output_line[1:], 1):
                if output_line[i-1] == formular:
                    efficiency -= 0.05 if efficiency>0.5 else 0
                else:
                    efficiency = 1
                    # vzdy nastavi efficiency na 1 na zaciatku formularu
                    # lebo output_line[0] nikdy nebude same ako formular

                if formular in tipek['zamestnanec']:
                    tipek['celkovy cas'] += tipek['zamestnanec'][formular] * efficiency
                else:
                    tipek['celkovy cas'] += 5 * efficiency
                    #vypocitanie casu pre jedneho zamestnanca

            print(tipek)
            cas += tipek['celkovy cas']
            if tipek['celkovy cas'] > slowest:
                slowest = tipek['celkovy cas']

            num_of_hours += math.ceil(tipek['celkovy cas']/60)
            #vypocitanie mzdy
        print("")
        print("zaplatil si " + str(num_of_hours * 30))
        print("najpomalsi cas je " + str(slowest) + " ")
        print("celkovy cas je" + str(cas) + " ")

        return num_of_hours*30, slowest, cas



def selectWorkers(possible_zamestnanci):
    #vyberie zamestancov a vracia ich ako list
    zamesnanci = []
    for i, entry in enumerate(possible_zamestnanci):
        zamesnanci.append(Zamestnanec(i))
        if entry and any(key in formulare_todo for key in entry):
            zamesnanci[i].usefull = True

    return zamesnanci

def notRandomSelect(formulare_todo,possible_zamestnanci):
    #vyberú sa zamestnanci
    zamesnanci = selectWorkers(possible_zamestnanci)
    joblist = []
    #inicializácia každého jobu
    #+ vytvorenie pravdepodobností s ktorými sa budú dávať zamestnancom
    for entry,value in formulare_todo.items():
        for i in range(0,value):
            job = Job(entry)
            job.setpropability(zamesnanci)
            joblist.append(job)

    #s danou pravdepodobnosťou sa dá job zamestnancovi
    for job in joblist:
        weight = list(job.getPropability().values())
        zam = random.choices(zamesnanci,weights=weight, k=1)[0]
        zam.dictdoc[job.nameofdoc()] += 1

    return zamesnanci


def writedoc(zamestnanci,filename):
    #zápis výstupu do csv súboru
    try:
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            for zamestnanec in zamestnanci:
                if(len(zamestnanec.listofnames()) > 0):
                    writer.writerow([zamestnanec.ID] + zamestnanec.listofnames())
    except FileNotFoundError:
        print(f"Súbor {filename} nebol nájdený.")

def load_data(possible_zamestnanci,formulare_todo):
    #načítanie dát z json súborov
    try:
        with open(possible_zamestnanci) as json1:
            possible_zamestnanci_json = json1.read()
    except FileNotFoundError:
        print(f"Súbor {possible_zamestnanci} nebol nájdený.")
    try:
        with open(formulare_todo) as json2:
            formulare_todo_json = json2.read()
    except FileNotFoundError:
        print(f"Súbor {formulare_todo} nebol nájdený.")
    return json.loads(possible_zamestnanci_json), json.loads(formulare_todo_json)

def simulated_aneling(T,alpha,limit,output,possible_zamestnanci,formulare_todo,slowest_weight,total_time_weight,hours_weight):
    #vytvory prvotne riesenie
    solution = Solution(notRandomSelect(formulare_todo,possible_zamestnanci))
    #pokiaľ T je väčšie ako náš limit ,skúšame nové riešenie a vyhodnocujeme ho
    while(T > limit):
        newsolution = Solution(copy.deepcopy(solution.get_zamestnanci()))
        #vytvarame nové riešenie pozmenením rozdelenia formulárov
        newsolution = newsolution.get_neighbour()
        #vyhodnocujeme nové riešenie či je lepšie ako predchádzajúce
        if(newsolution.evaluatefromlist(slowest_weight,total_time_weight,hours_weight) <= solution.evaluatefromlist(slowest_weight,total_time_weight,hours_weight)):
            solution = newsolution
            continue
       #ak nové riešenie nie je lepšie o rozhodnutí či prijmeme nové riešenie
        #rozhoduje náhodnosť a aktuálna "teplota"
        ap = math.exp((solution.evaluatefromlist(slowest_weight,total_time_weight,hours_weight) - newsolution.evaluatefromlist(slowest_weight,total_time_weight,hours_weight))/T)
        if(ap > random.uniform(0, 1)):
            solution = newsolution

        T *= alpha
        print(f'{T:0.4f}', solution.evaluatefromlist(slowest_weight,total_time_weight,hours_weight))
    #zavoláme metódu na zapísanie outputu, evalujeme vstup a zapíšeme
    # aj do konzoly naše najlepšie riešenie,ktoré sme pomocou algoritmu našli
    writedoc(solution.get_zamestnanci(), output)
    evaluate(output)

#nastavenie hodnôt a spustenie nášho algoritmu
slowest_weight = 1 #weights
total_time_weight = 0.4
hours_weight = 10
teplota = 1 # teplota od ktorej začíname
alpha = 0.999 #každu iteráciu klesne teplota o
limit = 0.01 #limit na zastavenie programu
possible_zamestnanci,formulare_todo = load_data("possible_zamestnanci.json", "formulare_todo.json")
simulated_aneling(teplota,alpha,limit,"output.csv",possible_zamestnanci,formulare_todo,slowest_weight,total_time_weight,hours_weight)

