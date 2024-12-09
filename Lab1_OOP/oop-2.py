#clasa de baza:Carte
class Carte:
    def __init__(self, titlu, autor, isbn):
        self.__titlu = titlu
        self.__autor = autor
        self.__isbn = isbn

    def get_titlu(self):
        return self.__titlu

    def get_isbn(self):
        return self.__isbn

    def __str__(self):
        return f'Titlu: {self.__titlu}, Autor: {self.__autor}, ISBN: {self.__isbn}'

#clasa derivata: EBook(moștenește clasa Carte)
class EBook(Carte):
    def __init__(self, titlu, autor, isbn, numar_pagini):
        super().__init__(titlu, autor, isbn)
        self.numar_pagini = numar_pagini

    def __str__(self):
        return f'{super().__str__()}, Numar de pagini: {self.numar_pagini}'

class Biblioteca:
    def __init__(self):
        self.carti = []

    def adauga_carte(self, carte):
        self.carti.append(carte)
        print(f'Carte adaugata: {carte.get_titlu()}')

    def elimina_carte(self, isbn):
        for carte in self.carti:
            if carte.get_isbn() == isbn:
                self.carti.remove(carte)
                print(f'Carte eliminatăa {carte.get_titlu()}')
                return
        print('Carte nu a fost gasita')

    def afiseaza_carti(self):
        if not self.carti:
            print('Biblioteca nu are carti')
        else:
            for carte in self.carti:
                print(carte)

if __name__ == "__main__":
    biblioteca = Biblioteca()

    carte1 = Carte("Arta Manipularii", "Kevin Dutton", "978-606945639-2")
    ebook1 = EBook("Atomic Habits", "James Clear", "978-606-789-174-4", 271)

    biblioteca.adauga_carte(carte1)
    biblioteca.adauga_carte(ebook1)

    biblioteca.afiseaza_carti()

    print()
    biblioteca.elimina_carte("978-606945639-2")
    biblioteca.afiseaza_carti()
