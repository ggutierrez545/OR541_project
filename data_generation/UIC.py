class Unit(object):

    def __init__(self, uic):
        self.uic = uic
        self.billets = []

    def assign_billet(self, billet):
        self.billets.append(billet)

    def list_unique_specialties(self):
        specialties = []
        for billet in self.billets:
            specialties.extend(billet.specialty)
        return set(specialties)

    def list_attributes(self):
        return [self.billet]

