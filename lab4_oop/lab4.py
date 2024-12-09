from abc import ABC, abstractmethod
import random

class EntitateEcosistem(ABC):
    def __init__(self, nume, energie, pozitie, rata_supravietuire):
        self.nume = nume
        self.energie = energie
        self.pozitie = pozitie  # (x, y) tuple
        self.rata_supravietuire = rata_supravietuire

    @abstractmethod
    def actioneaza(self, dimensiune_harta=None):
        """Metodă abstractă pentru acțiunea entității."""
        pass

class Planta(EntitateEcosistem):
    def __init__(self, nume, energie, pozitie, rata_crestere):
        super().__init__(nume, energie, pozitie, rata_supravietuire=1.0)
        self.rata_crestere = rata_crestere  # energie câștigată la fiecare pas

    def actioneaza(self, dimensiune_harta=None):
        """Crește energia plantei."""
        self.energie += self.rata_crestere
        print(f"{self.nume} a crescut și acum are energie {self.energie}.")

class Animal(EntitateEcosistem):
    def __init__(self, nume, energie, pozitie, viteza, tip_hrana):
        super().__init__(nume, energie, pozitie, rata_supravietuire=0.5)
        self.viteza = viteza  # numărul maxim de pași pe care îl poate face
        self.tip_hrana = tip_hrana  # "plante", "animale", "ambele"

    def deplaseaza(self, dimensiune_harta):
        """Se deplasează într-o direcție aleatorie în limita hărții."""
        dx = random.randint(-self.viteza, self.viteza)
        dy = random.randint(-self.viteza, self.viteza)
        x_nou = max(0, min(self.pozitie[0] + dx, dimensiune_harta - 1))
        y_nou = max(0, min(self.pozitie[1] + dy, dimensiune_harta - 1))
        self.pozitie = (x_nou, y_nou)
        print(f"{self.nume} s-a deplasat la poziția {self.pozitie}.")

    @abstractmethod
    def mananca(self, prada):
        """Metodă abstractă pentru mâncat."""
        pass

    @abstractmethod
    def actioneaza(self, dimensiune_harta):
        pass

class Erbivor(Animal):
    def mananca(self, prada):
        if isinstance(prada, Planta):
            self.energie += prada.energie
            prada.energie = 0
            print(f"{self.nume} a mâncat {prada.nume} și a câștigat energie.")
        else:
            print(f"{self.nume} nu poate mânca {prada.nume}.")

    def actioneaza(self, dimensiune_harta):
        """Acțiunea erbivorului: deplasare și consum de hrană."""
        self.deplaseaza(dimensiune_harta)
        print(f"{self.nume} analizează mediul și caută hrană.")

class Carnivor(Animal):
    def mananca(self, prada):
        if isinstance(prada, Animal) and prada.energie > 0:
            self.energie += prada.energie
            prada.energie = 0
            print(f"{self.nume} a vânat și a mâncat {prada.nume}.")
        else:
            print(f"{self.nume} nu poate mânca {prada.nume}.")

    def actioneaza(self, dimensiune_harta):
        """Acțiunea carnivorului: deplasare și vânătoare."""
        self.deplaseaza(dimensiune_harta)
        print(f"{self.nume} patrulează zona în căutarea prăzii.")

class Omnivor(Animal):
    def mananca(self, prada):
        if isinstance(prada, (Planta, Animal)) and prada.energie > 0:
            self.energie += prada.energie
            prada.energie = 0
            print(f"{self.nume} a mâncat {prada.nume}.")
        else:
            print(f"{self.nume} nu poate mânca {prada.nume}.")

    def actioneaza(self, dimensiune_harta):
        """Acțiunea omnivorului: deplasare și consum mixt."""
        self.deplaseaza(dimensiune_harta)
        print(f"{self.nume} explorează mediul și caută hrană mixtă.")

class Ecosistem:
    def __init__(self, dimensiune_harta):
        self.dimensiune_harta = dimensiune_harta
        self.entitati = []

    def adauga_entitate(self, entitate):
        self.entitati.append(entitate)

    def elimina_entitate(self, entitate):
        self.entitati.remove(entitate)

    def pas_simulare(self):
        for entitate in self.entitati:
            if isinstance(entitate, Animal):
                entitate.actioneaza(self.dimensiune_harta)
            else:
                entitate.actioneaza()

        # Verifică interacțiunile
        for prada in self.entitati[:]:
            for vanator in self.entitati:
                if isinstance(vanator, Animal) and vanator != prada:
                    if vanator.pozitie == prada.pozitie:
                        vanator.mananca(prada)
                        if prada.energie <= 0:
                            self.elimina_entitate(prada)
                            print(f"{prada.nume} a murit.")

    def afiseaza_stare(self):
        print("Starea ecosistemului:")
        for entitate in self.entitati:
            print(f"- {entitate.nume}: energie {entitate.energie}, poziție {entitate.pozitie}")

# Inițializare ecosistem
eco = Ecosistem(dimensiune_harta=10)

# Adăugare plante
planta1 = Planta("Planta1", energie=10, pozitie=(0, 0), rata_crestere=5)
planta2 = Planta("Planta2", energie=8, pozitie=(1, 1), rata_crestere=4)
eco.adauga_entitate(planta1)
eco.adauga_entitate(planta2)

# Adăugare animale
iepure = Erbivor("Iepure", energie=15, pozitie=(0, 1), viteza=2, tip_hrana="plante")
lup = Carnivor("Lup", energie=20, pozitie=(1, 0), viteza=3, tip_hrana="animale")
gorila = Omnivor("Gorila", energie=26, pozitie=(2, 3), viteza=1, tip_hrana="ambele")
eco.adauga_entitate(iepure)
eco.adauga_entitate(lup)
eco.adauga_entitate(gorila)

# Simulare
for _ in range(5):  # Simulează 5 pași
    print("\n--- Pas nou ---")
    eco.pas_simulare()
    eco.afiseaza_stare()
