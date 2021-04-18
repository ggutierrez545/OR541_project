class Billet(object):

    def __init__(self, bin):
        self.bin = bin
        self.grade = None
        self.specialty = None
        self.skills = []

    def add_specialty(self, specialty):
        self.specialty = specialty

    def add_skills(self, skill):
        if skill not in self.skills:
            self.skills.append(skill)

    def list_attributes(self):
        return [self.bin, self.grade, self.specialty, self.skills]

