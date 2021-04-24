class Billet(object):

    def __init__(self, bin):
        self.bin = bin
        self.grade = None
        self.specialty = None
        self.ranked_personnel = []
        self.skills = []

    @property
    def grade_subs_pool(self):
        o_e, level = self.grade
        level = int(level)
        return [f'{o_e}{lvl}' for lvl in range(level-1, level+2)]

    def add_specialty(self, specialty):
        self.specialty = specialty

    def add_skills(self, skill):
        if skill not in self.skills:
            self.skills.append(skill)

    def list_attributes(self):
        return [self.bin, self.grade, self.specialty, self.skills]

