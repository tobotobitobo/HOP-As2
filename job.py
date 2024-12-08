

class Job:
    def __init__(self, name):
        self.name = name
        self.propability = {}
        self.totalpropability = 0
    
    def nameofdoc(self):
        return self.name
    
    def getPropability(self):
        return self.propability
    

    def setpropability(self,zamestnanci):
        #vypočítame ako prispeje zamestnanec na tento dokument
        for zam in zamestnanci:
            self.propability[zam] = 5 - zam.getspeed()[self.nameofdoc()] if self.nameofdoc() in zam.getspeed() else 0.0001
            #pokiaľ nevie vôbec robiť ten dokument, dáme mu minimálnu pravdepodobnosť kvôli tomu, žeby vždy tam bola nejaká pravdepodobnosť
            self.totalpropability += self.propability[zam]
        
        #prechádza zamestnancov a každému dá pravdepodobnosť, čím rýchlejší úradník, tým väčšia pravdepodobnosť
        for zam in zamestnanci:
            self.propability[zam] = self.propability[zam] / self.totalpropability


