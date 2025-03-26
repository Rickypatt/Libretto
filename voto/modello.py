import math
import operator
from dataclasses import dataclass
import flet
from dao.dao import LibrettoDAO
from voto.voto import Voto

cfuTot = 180

class Libretto:
    def __init__(self, proprietario, voti = []):
        self.proprietario = proprietario
        self.voti = voti
        self.dao = LibrettoDAO()
        self.fillLibretto()

    def fillLibretto(self):
        allEsami = self.dao.getAllVoti()
        for e in allEsami:
            self.append(e)

    def append(self, voto): # duck!
       if (self.hasConflitto(voto) is False and self.hasVoto(voto) is False):
           self.voti.append(voto)
       else:
           raise ValueError("Voto già presente")

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

    def hasVoto(self, voto):
        """
        Questo metodo verifica se il ibretto contiene già il voto. Due voti sono considerati uguali per questo metodo
        se hanno lo stesso campo materia e lo stesso campo voto
        :param voto: istanza dell'oggetto di tipo voto
        :return: True se voto è già presente, False altrimenti
        """
        for v in self.voti:
            if v.materia == voto.materia and v.punteggio == voto.punteggio and v.lode == voto.lode:
                return True
        return False

    def hasConflitto(self, voto):
        """
        Questo metodo controlla che il voto non rappresenti un conflitto per i voti già presenti nel libretto.
        Consideriamo due voti in confitto quando hanno lo stesso campo materia ma diversa coppia (punteggio, lode)
        :param voto: istanza dell'oggetto di tipo voto
        :return: True se voto è in conflitto, False altrimenti
        """
        for v in self.voti:
            if (v.materia == voto.materia and not (v.punteggio == voto.punteggio and v.lode == voto.lode)):
                return True
        return False

    def copy(self):
        """
        Crea una nuova copia del libretto
        :return: restituisce un'istanza del Libretto
        """
        nuovo = Libretto(self.proprietario, [])
        for v in self.voti:
            nuovo.append(v.copy())

        return nuovo

    def creaMigliorato(self):
        """
        Crea un nuovo oggeto Libretto in cui i voti sono migliorati secondo la seguente logica:
        se il voto è >= 18 e < 24 aggiungo +1
        se il voto è >= 24 e < 29 agginugo +2
        se il voto è 30 rimane 30
        :return: nuovo libretto
        """
        nuovo = self.copy()

        for v in nuovo.voti:
            if 18 <= v.punteggio < 24:
                v.punteggio += 1
            elif 24 <= v.punteggio < 29:
                v.punteggio += 2
            elif  v.punteggio == 29:
                v.punteggio = 30

        return nuovo

    def sortByMateria(self):
        #self.voti.sort(key = estraiMateria)
        self.voti.sort(key = operator.attrgetter("materia"))

# opzione 1: creo due metodi di stampa che prima ordinano e poi stampano
# opzione 2: creo due metodi che ordinano la lista di self e poi un unico metodo di stampa
# opzione 3: creo due metodi che si fanno una copia autonoma della lista, la ordinano e la restituiscono
#            poi un altro metodo si occuperà di stampare le nuove liste
# opzione 4: creo una shallow copy di self.voti (copio solo la lista e gli oggetti rimangono quelli vecchi) e ordino quella

    def creaLibOrdinatoPerMateria(self):
        """
        Crea un nuovo ogetto libretto e lo ordina per materia
        :return: nuova istanza dell'oggetto Libretto
        """

        nuovo = self.copy()
        nuovo.sortByMateria()
        return nuovo

    def creaLibOrdinatoPerVoto(self):
        nuovo = self.copy()
        nuovo.voti.sort(key = lambda v: (v.punteggio, v.lode), reverse = True)
        return nuovo

    def cancellaInferiori(self, punteggio):
        """
        Questo metodo agisce sul libretto corrente eliminanod tutti i voti inferiori al parametro punteggio
        :param punteggio: intero indicante il valore minimo accettato
        :return:
        """
        # modo 1:
        # for i in range(len(self.voti)):
        #     if self.voti[i].punteggio < punteggio:
        #         self.voti.pop(i) ------ sto togliendo elementi da una lista che sto ciclando -> non funziona (dovrei scorrere al contrario)
        #
        # modo 2:
        # for v in self.voti:
        #     if v.punteggio <punteggio:
        #         self.voti.remove(v)

        # modo 3:
        # nuovo = []
        # for v in self.voti:
        #     if v.punteggio >= punteggio:
        #         nuovo.append(v)
        # self.voti = nuovo

        nuovo = [v for v in self.voti if v.punteggio >= punteggio]
        self.voti = nuovo

def estraiMateria(voto):
    """
    Questo metodo restituisce il campo materia dell'pggetto voto
    :param voto: istanza della classe Voto
    :return: stringa rappresentante il nome della materia
    """
    return voto.materia

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
