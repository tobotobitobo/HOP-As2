

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
        for zam in zamestnanci:
            self.propability[zam] = 5 - zam.getspeed()[self.nameofdoc()] if self.nameofdoc() in zam.getspeed() else 0.0001
            self.totalpropability += self.propability[zam]
        
        for zam in zamestnanci:
            self.propability[zam] = self.propability[zam] / self.totalpropability


