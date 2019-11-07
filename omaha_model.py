import json


class Item:
    def __init__(self, title, description, code):
        self.title = title
        self.description = description
        self.code = code

class InterventionCategory(Item):
    @property
    def id(self): return 'C' + self.code

class InterventionTarget(Item):
    @property
    def id(self): return 'T' + self.code

class ProblemDomain(Item):
    @property
    def id(self): return 'D' + self.code

class Problem(Item):
    def __init__(self, title, description, code, domain):
        super().__init__(title, description, code)
        self.domain = domain
    @property
    def id(self): return self.domain.id + 'P' + self.code


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

def parse_problems(domains):
    problems = {}
    for d in domains:
        od = ProblemDomain(d['title'], d['description'], d['code'])
        for p in d['problems']:
            op = Problem(p['title'], p['description'], p['code'], od)
            problems[op.id] = op
    return problems

def setup(db):
    terminology = load_terminology('terminology_EN.json')
    db['problems'] = parse_problems(terminology['problemClassificationScheme']['domains'])
    db['intervention_categories'] =\
        parse_intervention_categories(terminology['interventionScheme']['categories'])
    db['intervention_targets'] =\
        parse_intervention_targets(terminology['interventionScheme']['targets'])

