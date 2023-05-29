from languages.predicate import Predicate

class Carta(Predicate):
    predicate_name = "carta"

    def __init__(self, nome=None, mana=None, tipo=None, forza=None, target=None):
        Predicate.__init__(self, [("nome"),("mana"),("tipo"),("forza"),("target")])
        self.nome = nome
        self.mana = mana
        self.tipo = tipo
        self.forza = forza
        self.target = target
        
    def get_nome(self):
      return self.nome
    
    def set_nome(self, new_nome):
      self.nome = new_nome

    def get_mana(self):
      return self.mana

    def set_mana(self, new_mana):
      self.mana = new_mana

    def get_tipo(self):
      return self.tipo

    def set_tipo(self, new_tipo):
      self.tipo = new_tipo
  
    def get_forza(self):
      return self.forza
    
    def set_forza(self, new_forza):
      self.forza = new_forza

    def get_target(self):
      return self.target
    
    def set_target(self, new_target):
      self.target = new_target

    def __str__(self):
        return "carta(" + str(self.nome) + "," + str(self.mana) + "," + str(self.tipo) + "," + str(self.forza) + "," + str(self.target) + ")."