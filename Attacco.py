from languages.predicate import Predicate

class Attacco(Predicate):
    predicate_name = "attacco"

    def __init__(self, nome=None):
        Predicate.__init__(self, [("nome")])
        self.nome = nome
        
    def get_nome(self):
      return self.nome

    def set_nome(self, new_nome):
      self.nome = new_nome

    def __str__(self):
        return "attacco(" + str(self.nome) + ")."