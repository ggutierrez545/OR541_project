import numpy as np
from numpy import random as rd
import csv
from data_generation.person import Person


def generate_item(data_list):
    index = rd.randint(0, len(data_list))
    return data_list[index]


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

grades = []
with open("data_generation/raw/grade.csv", 'r') as data:
    reader = csv.reader(data)
    header = next(reader)
    for grade in reader:
        grades.append(grade[0])

personnel = []
with open("data_generation/raw/personnel.csv", 'r') as data:
    reader = csv.reader(data)
    header = next(reader)
    for row in reader:
        edipi = row[0]
        peep = Person(edipi)
        peep.grade = generate_item(grades)
        for _ in range(rd.randint(1, 4)):
            peep.add_specialty(generate_item(specialties))
        for _ in range(rd.randint(0, 5)):
            peep.add_skills(generate_item(skills))
        personnel.append(peep)


