class Carte:
    def __init__(self, titlu, autor, isbn):
        self.__titlu = titlu
        self.__autor = autor
        self.__isbn = isbn
        print(f'Obiectul Carte "{self.__titlu}" a fost creat')
        #Constructorul

    def get_titlu(self):
        return self.__titlu

    def get_autor(self):
        return self.__autor

    def get_isbn(self):
        return self.__isbn

    def __str__(self):
        return f'Titlu: {self.__titlu}, Autor: {self.__autor}, ISBN: {self.__isbn}'

    # Destructorul
    def __del__(self):
        print(f'Obiectul Carte "{self.__titlu}" a fost distrus')

class Biblioteca:
    def __init__(self):
        self.carti = []

    def adauga_carte(self, carte):
        self.carti.append(carte)
        # print(f'Carte adaugată: {carte.get_titlu()}')

    def elimina_carte(self, isbn):
        for carte in self.carti:
            if carte.get_isbn() == isbn:
                self.carti.remove(carte)
                print(f'Carte eliminata: {carte.get_titlu()}')
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
    carte2 = Carte("Atomic Habits", "James Clear", "978-606-789-174-4")
        
    biblioteca.adauga_carte(carte1)
    biblioteca.adauga_carte(carte2)
    
    biblioteca.afiseaza_carti()
    
    print()
    del carte1

# Constructorul (__init__):
# Destructorul (__del__): 