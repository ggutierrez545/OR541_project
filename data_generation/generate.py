from numpy import random as rd
import csv
from data_generation.person import Person
from data_generation.billet import Billet
from data_generation.UIC import Unit


def generate_item(data_list):
    index = rd.randint(0, len(data_list))
    return data_list[index]


def generate_data(random_seed=541):
    # Set random seed for reproducibility.
    rd.seed(random_seed)

    grades = []
    with open("data_generation/raw/grade.csv", 'r') as data:
        reader = csv.reader(data)
        header = next(reader)
        for grade in reader:
            grades.append(grade[0])

    specialties = []
    with open("data_generation/raw/specialty.csv", 'r') as data:
        reader = csv.reader(data)
        header = next(reader)
        for specialty in reader:
            specialties.append(specialty[0])

    skills = []
    with open("data_generation/raw/skill.csv", 'r') as data:
        reader = csv.reader(data)
        header = next(reader)
        for skill in reader:
            skills.append(skill[0])

    personnel = []
    with open("data_generation/raw/personnel.csv", 'r') as data:
        enlisted = ['E1', 'E2', 'E3', 'E4', 'E5', 'E6', 'E7', 'E8', 'E9']
        reader = csv.reader(data)
        header = next(reader)
        for row in reader:
            edipi = row[0]
            peep = Person(edipi)
            peep.grade = generate_item(grades)
            if peep.grade in enlisted:
                for _ in range(rd.randint(1, 4)):
                    peep.add_specialty(generate_item(specialties[:100]))
            else:
                for _ in range(rd.randint(1, 4)):
                    peep.add_specialty(generate_item(specialties[100:]))
            for _ in range(rd.randint(0, 5)):
                peep.add_skills(generate_item(skills))
            skills_count_personnel = len(skills)
            personnel.append(peep)

    units = []
    with open("data_generation/raw/unit.csv", 'r') as data:
        reader = csv.reader(data)
        header = next(reader)
        for row in reader:
            uic = row[0]
            units.append(Unit(uic))

    bins = []
    with open("data_generation/raw/bin.csv", 'r') as data:
        enlisted = ['E1', 'E2', 'E3', 'E4', 'E5', 'E6', 'E7', 'E8', 'E9']
        reader = csv.reader(data)
        header = next(reader)
        for row in reader:
            billet = Billet(row[0])
            billet.grade = generate_item(grades)
            if billet.grade in enlisted:
                for _ in range(rd.randint(1, 4)):
                    billet.add_specialty(generate_item(specialties[:100]))
            else:
                for _ in range(rd.randint(1, 4)):
                    billet.add_specialty(generate_item(specialties[100:]))
            for _ in range(rd.randint(0, 2)):
                billet.add_skills(generate_item(skills))
            skills_count_billet = len(skills)
            bins.append(billet)
            generate_item(units).assign_billet(billet)

    sorted_billets = {}
    for billet in bins:
        for grade in billet.grade_subs_pool:
            try:
                sorted_billet_spec = sorted_billets[billet.specialty]
                try:
                    sorted_billet_spec[grade].append(billet)
                except KeyError:
                    sorted_billet_spec[grade] = [billet]
            except KeyError:
                sorted_billets[billet.specialty] = {}

    sorted_people = {}
    for person in personnel:
        for specialty in person.specialties:
            try:
                sorted_person_spec = sorted_people[specialty]
                try:
                    sorted_person_spec[person.grade].append(person)
                except KeyError:
                    sorted_person_spec[person.grade] = [person]
            except KeyError:
                sorted_people[specialty] = {}

    for person in personnel:
        for specialty in specialties:
            try:
                applicable_billets = sorted_billets[specialty][person.grade]
                person.ranked_billets.extend(applicable_billets)
            except KeyError:
                continue
        rd.shuffle(person.ranked_billets)

    for billet in bins:
        for grade in billet.grade_subs_pool:
            try:
                applicable_personnel = sorted_people[billet.specialty][grade]
                billet.ranked_personnel.extend(applicable_personnel)
            except KeyError:
                continue
        rd.shuffle(billet.ranked_personnel)

    return personnel, specialties, skills, grades, units, bins, sorted_billets
