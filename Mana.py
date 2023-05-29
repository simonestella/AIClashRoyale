from languages.predicate import Predicate

class Mana(Predicate):
    predicate_name = "manaDisponibile"

    def __init__(self, mana=None):
        Predicate.__init__(self, [("mana")])
        self.mana = mana
        
    def get_mana(self):
      return self.mana

    def set_mana(self, new_mana):
      self.mana = new_mana

    def __str__(self):
        return "manaDisponibile(" + str(self.mana) + ")."