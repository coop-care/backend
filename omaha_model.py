from enum import Enum
import json

class _Modifier(Enum):
    @classmethod
    def set_data(cls, data):
        cls._data = data
    def __init__(self, idx, val):
        self.idx = idx
        self.val = val
    @property
    def title(self):
        return self._data[self.idx]['title']
    def description(self):
        return self._data[self.idx]['description']

class ProblemDomainModifier(_Modifier):
    INDIVIDUAL = (0, 'individual')
    FAMILY = (1, 'family')
    COMMUNITY = (2, 'community')

class ProblemTypeModifier(_Modifier):
    HEALTH_PROMO = (0, 'health-promotion')
    POTENTIAL = (1, 'potential')
    ACTUAL = (2, 'actual')

class _Item:
    def __init__(self, title, description, code):
        self.title = title
        self.description = description
        self.code = code

class InterventionCategory(_Item):
    @property
    def id(self): return 'C' + self.code

class InterventionTarget(_Item):
    @property
    def id(self): return 'T' + self.code

class ProblemDomain(_Item):
    @property
    def id(self): return 'D' + self.code

class Problem(_Item):
    def __init__(self, title, description, code, domain):
        super().__init__(title, description, code)
        self.domain = domain
    @property
    def id(self): return self.domain.id + 'P' + self.code

class Symptom(_Item):
    def __init__(self, title, code, problem):
        super().__init__(title, None, code)
        self.problem = problem
    @property
    def id(self): return self.problem.id + 'S' + self.code


def load_terminology(filename):
    with open(filename) as json_file:
        return json.load(json_file)

def parse_intervention_categories(categories):
    ics = {}
    for c in categories:
        ic = InterventionCategory(c['title'], c['description'], c['code'])
        ics[ic.id] = ic
    return ics

def parse_intervention_targets(targets):
    its = {}
    for t in targets:
        it = InterventionTarget(t['title'], t['description'], t['code'])
        its[it.id] = it
    return its

def parse_problems(json_domains):
    domains = {}
    problems = {}
    symptoms = {}
    for d in json_domains:
        od = ProblemDomain(d['title'], d['description'], d['code'])
        domains[od.id] = od
        for p in d['problems']:
            op = Problem(p['title'], p['description'], p['code'], od)
            problems[op.id] = op
            for s in p['signsAndSymptoms']:
                os = Symptom(s['title'], s['code'], op)
                symptoms[os.id] = os
    return domains, problems, symptoms

def setup(db, lang):
    terminology = load_terminology('terminology_' + lang + '.json')
    db['domains'], db['problems'], db['symptoms'] =\
        parse_problems(terminology['problemClassificationScheme']['domains'])
    db['intervention_categories'] =\
        parse_intervention_categories(terminology['interventionScheme']['categories'])
    db['intervention_targets'] =\
        parse_intervention_targets(terminology['interventionScheme']['targets'])
    ProblemDomainModifier.set_data(
        terminology['problemClassificationScheme']['modifiers']['scope'])
    ProblemTypeModifier.set_data(
        terminology['problemClassificationScheme']['modifiers']['severity'])

