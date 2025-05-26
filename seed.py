#Clase "plantilla" que le da base a la creacion de los objectos
class personaje:
    #No hay necesidad de poner los atributos aqui pero igualmente es bueno tenerlo por el codigo legible
    nombre = "unknown"
    vida = 0
    fuerza = 0
    durabilidad = 0

    #Encargado de crear objectos instanciados(Constructor)
    def __init__(self,nombre,vida,fuerza,durabilidad):
        self.nombre = nombre
        self.vida = vida
        self.fuerza = fuerza
        self.durabilidad = durabilidad

    def atributos(self):
        print(self.nombre)
        print("vida:", self.vida)
        print("Fuerza:", self.fuerza)
        print("durabilidad:", self.durabilidad)

    def subir_nivel(self,vida,fuerza,durabilidad):
        self.vida += vida
        self.fuerza += fuerza 
        self.durabilidad += durabilidad

    def vivo(self):
        return self.vida > 0
    
    def murido(self):
        self.vida = 0
        print(self.nombre, "Ha muerto")

    def daño(self, enemigo):
        return self.fuerza - enemigo.durabilidad
    
    def ataque(self,enemigo):
        daño = self.daño(enemigo)
        enemigo.vida -= daño
        if enemigo.vivo():
            print(self.nombre, "Le ha hecho" ,daño, "de daño a",enemigo.nombre,)
            print("la vida de",enemigo.nombre,"es de",enemigo.vida)
        else:
            enemigo.murido()


# Instancias(objectos ya creados y alojados)
otro_personaje = personaje("Fulano",100,5,2)
mi_personaje = personaje("Kevzx",100,8,3)

# mi_personaje.ataque(otro_personaje)

class mago(personaje):
    mana: 0


    def __init__(self,nombre,vida,fuerza,durabilidad,mana):
        #para usar todos los adtributos de 
        super().__init__(nombre,vida,fuerza,durabilidad)
        self.mana = mana

    def atributos(self):
        #para usar el metodo de la clase padre usamos super()
        super().atributos()
        print("Mana", self.mana)

    def daño(self, enemigo):
        return self.mana*self.fuerza - enemigo.durabilidad    


#No se balancear personajes xd
elfrien = mago("elfrien",50,3,70,50)
lifa = mago("lifa",50,4,80,40)

# elfrien.atributos()
    

class guerrero(personaje):
    espdada: 0

    def __init__(self, nombre, vida, fuerza, durabilidad,espada):
        super().__init__(nombre, vida, fuerza, durabilidad)
        self.espada = espada

    def atributos(self):
        super().atributos()
        print("Espada:" ,self.espada)

    def daño(self,enemigo):
        return self.espada*self.fuerza - enemigo.durabilidad
    

dante = guerrero("dante",300,8,100,30)
vergil = guerrero("vergil",300,7,90,25)

dante.ataque(vergil)