import json
import random

class Zamestnanec:
    def __init__(self,ID):
        self.dictdoc = {}
        with open("formulare_todo.json") as json1:
            formulate_json = json1.read()
        formulate_todo = json.loads(formulate_json)
        for entry,value in formulate_todo.items():
            self.dictdoc[entry] = 0
        self.ID = ID

        with open("possible_zamestnanci.json") as json1:
            possible_zamestnanci_json = json1.read()
        possible_zamestnanci = json.loads(possible_zamestnanci_json)
        self.speed =  possible_zamestnanci[ID]
        self.celkovy_cas = 0

    def getspeed(self):
        return self.speed
    
    def listofnames(self):
        names = []
        for entry,value in self.dictdoc.items():
            for i in range(0,value):
                names.append(entry)
        return names

    def gettotalspeed(self):
        efficiency = 1
        self.celkovy_cas = 0
        for doc, value in self.dictdoc.items():
            efficiency = 1
            for i in range(0,value):
                if(i != 0):
                    efficiency -= 0.05 if efficiency>0.5 else 0
                if doc in self.speed:
                    self.celkovy_cas += self.speed[doc] * efficiency
                else:
                    self.celkovy_cas += 5 * efficiency
        return self.celkovy_cas

    def getRandomKey(self):
        return random.choice([job for job, count in self.dictdoc.items() if count > 0])
    
    def sum_of_docs(self):
        a = 0
        for doc, value in self.dictdoc.items():
            a += value
        return a
    
    def plus_doc(self,keyname):
        self.dictdoc[keyname] += 1
    def minus_doc(self,keyname):
        self.dictdoc[keyname] -= 1

            
 