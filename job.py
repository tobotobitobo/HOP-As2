

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
        #vypocitame ako prispeje zamestnanec na tento dokument
        for zam in zamestnanci:
            self.propability[zam] = 5 - zam.getspeed()[self.nameofdoc()] if self.nameofdoc() in zam.getspeed() else 0.0001
            #pokial nevie vobec robit ten dokument dame mu minimalnu pravdepodobnost kvoli tomu zeby vzdy tam bola nejaka pravdepodobnost
            self.totalpropability += self.propability[zam]
        
        #prechadza zamestnancov a kazdemu da pravdepodobnost cim rychlejsi clovek tym vecia pravdepodobnost
        for zam in zamestnanci:
            self.propability[zam] = self.propability[zam] / self.totalpropability


