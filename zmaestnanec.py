

class Zameamestnanec:
    def __init__(self,ID):
        self.docs = []
        self.ID = ID


    def sort(self):
        self.docs.sort()
    
    def listofnames(self):
        names = []
        for doc in self.docs:
            names.append(doc.name)
        return names
 