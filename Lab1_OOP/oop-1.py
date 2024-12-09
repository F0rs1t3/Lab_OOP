class Carte:
    def __init__(self, titlu, autor, isbn):
        self.__titlu = titlu
        self.__autor = autor
        self.__isbn = isbn

    def get_titlu(self):
        return self.__titlu

    def get_autor(self):
        return self.__autor

    def get_isbn(self):
        return self.__isbn

    def __str__(self):
        return f'Titlu:{self.__titlu}, Autor:{self.__autor}, ISBN:{self.__isbn}'

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

    # Solicităm de la utilizator câte cărți vrea să introducă
    n = int(input("Cate carti vrei sa adaugi? "))

    # Introducem cărțile folosind un for loop
    for i in range(n):
        print(f"\nIntrodu datele pentru cartea {i + 1}:")
        titlu = input("Titlul cartii: ")
        autor = input("Autorul cartii: ")
        isbn = input("ISBN-ul cartii: ")
        
        carte = Carte(titlu, autor, isbn)
        biblioteca.adauga_carte(carte)
    
    biblioteca.afiseaza_carti()
    
    print()
    el = str(input("Introdu ISBN'ul de la cartea care sa fie stearsa:"))
    biblioteca.elimina_carte(el)
    
    biblioteca.afiseaza_carti()