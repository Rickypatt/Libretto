from scuola import Student
from voto.voto import Libretto, Voto

Harry = Student(nome="Harry", cognome="Potter", eta=11, capelli="castani", occhi="azzurri", casa="Grifondoro",
                animale="civetta", incantesimo="Expecto Patronum")

myLib = Libretto(Harry,[])

v1 = Voto("Difesa contro le arti oscure",25,"2022-01-30",False)
v2 = Voto("Babbanologia",21,"2022-02-12",False)
myLib.append(v1)
myLib.append(v2)
myLib.append(Voto("Trasfigurazione",21,"2022-06-14",False))

myLib.calcolaMedia()

votiFiltrati = myLib.getVotiByPunti(21,False)
print(votiFiltrati)

votoTrasfigurazione = myLib.getVotoByName("Trasfigurazione")
if votoTrasfigurazione is None:
    print("Voto non trovato")
else:
    print(votoTrasfigurazione.materia)

