from zamestnanec import Zamestnanec
import random
import math

class Solution:
    def __init__(self, zamestnanci):
        self.zamestnanci = zamestnanci

    def get_zamestnanci(self):
        return self.zamestnanci
    
    def get_neighbour(self):
        targeted_zamestnanec = random.choice(self.zamestnanci)
        if targeted_zamestnanec.sum_of_docs() != 0:
            job_to_switch = targeted_zamestnanec.getRandomKey()
            targeted_zamestnanec2.minus_doc(job_to_switch)
            targeted_zamestnanec2 = random.choice(self.zamestnanci)
            targeted_zamestnanec2.plus_doc(job_to_switch)
        return self
    
    def evaluatefromlist(self,slowest_weight,totaltime_weight,hours_weight):
        slowest = 0
        num_of_hours = 0
        celkovy_cas = 0

        for zamestnanec in self.zamestnanci:
            cas = zamestnanec.gettotalspeed()
            if cas > slowest:
                slowest = cas
            celkovy_cas += cas
            num_of_hours += math.ceil(cas/60)

        n = 0
        for a in self.zamestnanci:
            if (a.sum_of_docs() > 0):
                n+=1
        return slowest*slowest_weight + celkovy_cas/n*totaltime_weight +num_of_hours*n*hours_weight