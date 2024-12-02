import json
from job import Job

class Zamestnanec:
    def __init__(self,ID):
        self.docs = []
        self.ID = ID
        with open("HOP-As2/possible_zamestnanci.json") as json1:
            possible_zamestnanci_json = json1.read()
        possible_zamestnanci = json.loads(possible_zamestnanci_json)
        self.speed =  possible_zamestnanci[ID]
        self.celkovy_cas = 0


    def sort(self):
        self.docs.sort(key=lambda x: x.name, reverse=True)
    
    def listofnames(self):
        names = []
        for doc in self.docs:
            names.append(doc.name)
        return names

    def gettotalspeed(self):
        efficiency = 1
        self.celkovy_cas = 0
        for i, doc in enumerate(self.docs,0):
            if(i != 0):
                if(self.docs[i-1].nameofdoc()) == doc.nameofdoc():
                    efficiency -= 0.05 if efficiency>0.5 else 0
                else:
                    efficiency = 1

            if doc.nameofdoc() in self.speed:
                self.celkovy_cas += self.speed[doc.nameofdoc()] * efficiency
            else:
                self.celkovy_cas += 5 * efficiency
        return self.celkovy_cas


            
 