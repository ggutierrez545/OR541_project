class Person(object):

    def __init__(self, edipi):
        self.edipi = edipi
        self.grade = None
        self.specialties = []
        self.ranked_billets = []
        self.skills = []

    @property
    def num_skills_person(self):
        return len(self.skills)

    @property
    def num_specialties_person(self):
        return len(self.specialties)

    def add_specialty(self, specialty):
        if specialty not in self.specialties:
            self.specialties.append(specialty)

    def add_skills(self, skill):
        if skill not in self.skills:
            self.skills.append(skill)

    def list_attributes(self):
        return [self.edipi, self.grade, self.specialties, self.skills]