class friend1:
    def __init__(self, valoare):
        self.__valoare = valoare

    def obtainVal(self, Friend):
        if isinstance(Friend, friend2):  
            return self.__valoare
        else:
            return "Error friend1"

class friend2:
    def __init__(self, cod):
        self.__cod = cod

    def obtainCod(self, Friend):
        if isinstance(Friend, friend1):  
            return self.__cod
        else:
            return "Error friend2"

def accesFriends(obj1, obj2):
    if isinstance(obj1, friend1) and isinstance(obj2, friend2):
        val_a = obj1.obtainVal(obj2)
        code_b = obj2.obtainCod(obj1)
        print(f"friend1 are valoarea: {val_a}")
        print(f"friend2 are codul: {code_b}")
    else:
        print("Obiectele nu sunt prieteni compatibili")

obj_a = friend1(1337)
obj_b = friend2("Codul")

accesFriends(obj_a, obj_b)
