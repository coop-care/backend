import json
import connexion
import omaha_model as omaha
pdm = omaha.ProblemDomainModifier
ptm = omaha.ProblemTypeModifier
langDefault = 'EN'

class Client:
    def __init__(self, name, problems):
        self.name = name
        self.problems = problems
    
    def add_problem(self, *args, **kwargs):
        self.problems.append(ProblemClassification(*args, **kwargs))
        return self

class ProblemClassification:
    def __init__(self, problem_id, domain_modifier, type_modifier, comment=''):
        self.problem_id = problem_id
        self.domain_modifier = domain_modifier
        self.type_modifier = type_modifier
        self.ratings = []
        self.comment = comment

class Rating:
    def __init__(self, timestamp, current_state, goal_state=None):
        self.timestamp = timestamp
        self.current_state = current_state
        self.goal_state = goal_state

class RatingScale:
    def __init__(self, status, knowledge, behaviour,
            status_comment='', knowledge_comment='', behaviour_comment=''):
        self.status = status
        self.knowledge = knowledge
        self.behaviour = behaviour
        self.status_comment = status_comment
        self.knowledge_comment = knowledge_comment
        self.behaviour_comment = behaviour_comment

def setup_examples(db):
    db['clients'] = {
        1: Client('Emma B.', [
            ProblemClassification('D02P12', pdm.INDIVIDUAL, ptm.ACTUAL,
                comment='sdffdsa'
            ),
            ProblemClassification('D04P38', pdm.INDIVIDUAL, ptm.ACTUAL, 'sdfsdfs'),
        ]),
        2: Client('Janice A.', [])
            # .add_problem(ProblemClassification('D01P01', 'sf')),
    }

### routes

def get_clients():
    return [
        {
            'id': id,
            'name': client.name,
        }
        for id, client in clientdb['clients'].items()
    ]

def get_client_problems(id):
    return [
        {
            'id': p.problem_id,
            'domainModifier': p.domain_modifier.val,
            'comment': p.comment,
        }
        for p in clientdb['clients'][id].problems
    ]

def post_client_problems(id):
    return []

def get_client_problem_interventions():
    return []

def get_client_problem_ratings():
    return []

def get_omaha_intervention_categories(lang=langDefault):
    return [
        {
            'id': c.id,
            'title': c.title,
            'description': c.description,
        }
        for c in omahadb[lang]['intervention_categories'].values()
    ]

def get_omaha_intervention_targets(lang=langDefault):
    return [
        {
            'id': t.id,
            'title': t.title,
            'description': t.description,
        }
        for t in omahadb[lang]['intervention_targets'].values()
    ]

def get_omaha_problem_domains(lang=langDefault):
    return [
        {
            'id': d.id,
            'title': d.title,
            'description': d.description,
        }
        for d in omahadb[lang]['domains'].values()
    ]

def get_omaha_problems(lang=langDefault):
    return [
        {
            'id': p.id,
            'title': p.title,
            'description': p.description,
            'domainId': p.domain.id,
        }
        for p in omahadb[lang]['problems'].values()
    ]

def get_omaha_symptoms(lang=langDefault):
    return [
        {
            'id': s.id,
            'title': s.title,
            'domainId': s.problem.domain.id,
            'problemId': s.problem.id,
        }
        for s in omahadb[lang]['symptoms'].values()
    ]


clientdb = {}
omahadb = { 'EN': {}, 'DE': {} }
omaha.setup(omahadb['EN'], 'EN')
omaha.setup(omahadb['DE'], 'DE')
setup_examples(clientdb)
if __name__ == '__main__':
    print('------')
    print(get_clients())
    print(get_client_problems(1))
    # print(get_omaha_intervention_categories())
    # print(get_omaha_intervention_targets())
    # print(get_omaha_problems())
    # print(get_omaha_symptoms())
    # print([(p.title, p.id) for p in omahadb['problems'].values() if 'Income' in p.title])
    print(dir(omaha.ProblemDomainModifier))
    print(dir(omaha.ProblemDomainModifier.INDIVIDUAL))
    # print(pdm.INDIVIDUAL.title)
    print('------')
    appl = connexion.App(__name__)
    appl.add_api('openapi.yaml', validate_responses=True)

    appl.run(port=8888)
