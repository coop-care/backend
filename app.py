import json
import connexion
import omaha_model as omaha

class Client:
    def __init__(self, name):
        self.name = name
        self.problems = []
    
    def add_problem(self, problem):
        self.problems.append(problem)
        return self

class ProblemClassification:
    def __init__(self, problem_id, comment):
        self.problem_id = problem_id
        self.comment = comment

def setup_examples(db):
    db['clients'] = {
        1: Client('Emma B.')
            .add_problem(ProblemClassification('D02P12', 'sdffdsa'))
            .add_problem(ProblemClassification('D04P38', 'sdfsdfs')),
        2: Client('Janice A.')
            .add_problem(ProblemClassification('D01P01', 'sf')),
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
            'comment': p.comment,
        }
        for p in clientdb['clients'][id].problems
    ]

def get_client_problem_interventions():
    return []

def get_omaha_intervention_categories():
    return [
        {
            'id': p.id,
            'title': p.title,
            'description': p.description,
        }
        for p in omahadb['intervention_categories'].values()
    ]

def get_omaha_intervention_targets():
    return [
        {
            'id': p.id,
            'title': p.title,
            'description': p.description,
        }
        for p in omahadb['intervention_targets'].values()
    ]

def get_omaha_problems():
    return [
        {
            'id': p.id,
            'title': p.title,
            'description': p.description,
            'domainId': p.domain.id,
            'domainTitle': p.domain.title,
        }
        for p in omahadb['problems'].values()
    ]

if __name__ == '__main__':
    clientdb = {}
    omahadb = {}
    omaha.setup(omahadb)
    setup_examples(clientdb)
    print(get_clients())
    print(get_client_problems(1))
    # print(get_omaha_intervention_categories())
    print(get_omaha_intervention_targets())
    # print(get_omaha_problems())
    print([(p.title, p.id) for p in omahadb['problems'].values() if 'Income' in p.title])
    print('------')
    appl = connexion.App(__name__)
    appl.add_api('openapi.yaml', validate_responses=True)

    appl.run(port=8888)
