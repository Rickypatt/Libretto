from dataclasses import dataclass

cfuTot = 180

@dataclass
class Voto:
    materia: str
    punteggio: int
    data: str
    lode: bool

    def __str__(self):
        if self.lode:
            return f"In {self.materia} hai preso {self.punteggio} e lode il {self.data}"
        else:
            return f"In {self.materia} hai preso {self.punteggio} il {self.data}"

class Libretto:
    def __init__(self, proprietario, voti = []):
        self.proprietario = proprietario
        self.voti = voti

    def append(self, voto): # duck!
        self.voti.append(voto)

    def __str__(self):
        mystr = f"Libretto voti di {self.proprietario} \n"
        for v in self.voti:
            mystr += f"{v} \n"
        return mystr

    def __len__(self):
        return len(self.voti)

    def calcolaMedia(self):
        """
        restituisce la media dei voti attualmente presenti nel libretto
        :return: valore numerico della media, oppure ValueError in caso la lista fosse vuota
        """
        if len(self.voti) == 0:
            raise ValueError("Attenzione, lista esami vuota")

        v = [v1.punteggio for v1 in self.voti]
        return sum(v)/len(v)

    def getVotiByPunti(self,punti,lode):
        """
        restituisce una lista di esami con punteggio uguale a punti (e lode se applicabile)
        :param punti: variabile di tipo intero che rappresenta il punteggio
        :param lode: booleano che indica se presente la lode
        :return: lista di voti
        """
        votiFiltrati = []
        for v in self.voti:
            if v.punteggio == punti and v.lode == lode:
                votiFiltrati.append(v)
        return votiFiltrati

    def getVotoByName(self,nome):
        """
        restituisce un oggetto voto il cui campo materia è uguale a nome
        :param nome: stringa che indica il nome della materia
        :return: oggetto di tipo voto, oppure None in caso di voto non trovato
        """
        for v in self.voti:
            if v.materia == nome:
                return v

def testVoto():
    print("Ho usato Voto in maniera standalone")
    v1 = Voto("Trasfigurazione", 24, "2022-02-13", False)
    v2 = Voto("Pozioni", 30, "2022-02-17", True)
    v3 = Voto("Difesa contro le arti oscure", 27, "2022-04-13", False)
    print(v1)

    mylib = Libretto(None, [v1, v2])
    print(mylib)
    mylib.append(v3)
    print(mylib)

if __name__ == "__main__":
    testVoto()


# class Voto:
#     def __init__(self, materia, punteggio, data, lode):
#         if  punteggio == 30:
#             self.materia = materia
#             self.punteggio = punteggio
#             self.data = data
#             self.lode = lode
#         elif punteggio < 30:
#             self.materia = materia
#             self.punteggio = punteggio
#             self.data = data
#             self.lode = False
#         else:
#             raise ValueError(f"Attenzione, non posso creare un voto con punteggio {punteggio}")
#     def __str__(self):
#         if self.lode:
#             return f"In {self.materia} hai preso {self.punteggio} e lode il {self.data}"
#         else:
#             return f"In {self.materia} hai preso {self.punteggio} il {self.data}"
