class Billet(object):

    def __init__(self, bin):
        self.bin = bin
        self.grade = None
        self.specialties = []
        self.skills = []

    def add_specialty(self, specialty):
        if specialty not in self.specialties:
            self.specialties.append(specialty)

    def add_skills(self, skill):
        if skill not in self.skills:
            self.skills.append(skill)

    def list_attributes(self):
        return [self.bin, self.grade, self.specialties, self.skills]