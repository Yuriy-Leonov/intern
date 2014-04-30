from django.contrib.auth.models import User, Group
from workflow.models import *
from main.models import *
import time, json

a1 = Action.objects.create(name="Action 1", description="Action 1", service='PEN')
a2 = Action.objects.create(name="Action 2", description="Action 2", service='PEN')
a3 = Action.objects.create(name="Action 3", description="Action 3", service='PEN')
a1.save()
a2.save()
a3.save()



fred = User.objects.create_user('fred', 'fred@acme.com', 'password')
joe = User.objects.create_user('joe', 'joe@acme.com', 'password')
accountants = User.objects.create_user('accountants', 'accountants@acme.com',
                                       'password')
petya = User.objects.create_user('petya', 'petya@acme.com', 'password')
boss = User.objects.create_user('boss', 'boss@acme.com', 'password')
User_1 = User.objects.create_user('User 1', 'petya@acme.com', 'password')




class Document():
    def __init__(self, title, body, workflow_activity):
        self.title = title
        self.body = body
        self.workflow_activity = workflow_activity

joe = User.objects.get(username='joe')
fred = User.objects.get(username='Olga')

author = Role.objects.create(name="author", description="Author of a docment")
boss_ = Role.objects.create(name="boss", description="Departmental boss")


wf = Workflow.objects.create(name='Simple Docuent Approval', slug='docapp',
                             description='A simple docuent approval process',
                             created_by=joe)


s1 = State.objects.create(
    name='In Draft',
    description='The author is writing a draft of the documnt',
    is_start_state=True, workflow=wf)
s2 = State.objects.create(
    name='Under Review',
    description='The approver is reviewing the docuent',
    workflow=wf)
s3 = State.objects.create(
    name='Published',
    description='The docment is published',
    workflow=wf)
s4 = State.objects.create(
    name='Archived',
    description='The documnt is put into the archive',
    is_end_state=True, workflow=wf)


s1.roles.add(author)
s2.roles.add(boss_)
s2.roles.add(author)
s3.roles.add(boss_)
s4.roles.add(boss_)


t1 = Transition.objects.create(name='Request Approval', workflow=wf,
                               from_state=s1, to_state=s2)
t2 = Transition.objects.create(name='Revise Draft', workflow=wf,
                               from_state=s2, to_state=s1)
t3 = Transition.objects.create(name='Publish', workflow=wf,
                               from_state=s2, to_state=s3)
t4 = Transition.objects.create(name='Archive', workflow=wf,
                               from_state=s3, to_state=s4)


t1.roles.add(author)
t2.roles.add(boss_)
t3.roles.add(boss_)
t4.roles.add(boss_)



wf.activate()


######################################################

# here need clone
wa = WorkflowActivity(workflow=wf, created_by=fred)
wa.save()


p1 = Participant(user=fred, workflowactivity=wa)
p1.save()
p2 = Participant(user=joe, workflowactivity=wa)
p2.save()

wa.assign_role(fred, joe, boss_)
wa.assign_role(joe, fred, author)
d = Document(title='Had..?',
             body="Bob, where Alice approval",
             workflow_activity=wa)

time.sleep(1)

d.workflow_activity.start(fred)
current = d.workflow_activity.current_state() #cs = wa.current_state()
current.participant                           #cs.state.is_end_state == True
current.note
current.state
current.state.transitions_from.all() #tr = cs.state.transitions_from.all()

my_transition = current.state.transitions_from.all()[0]
my_transition
d.workflow_activity.progress(my_transition, fred) #wa.progress(tr[0], user)

current = d.workflow_activity.current_state()
current.state
current.state.roles.all()
current.transition
current.note
current.state.events.all()


current.state.transitions_from.all().order_by('id')
my_transition = current.state.transitions_from.all().order_by('id')[1]
d.workflow_activity.progress(my_transition, joe, "We'll be up for a Pulitzer")



current = d.workflow_activity.current_state()
current.state.transitions_from.all().order_by('id')
my_transition = current.state.transitions_from.all().order_by('id')[0]
d.workflow_activity.progress(my_transition, joe)
for item in d.workflow_activity.history.all():
    print '%s by %s'%(item.note, item.participant.user.username)




######################################################



import time
import uuid
from redis_sessions import session as redis_session
from main.models import *
import json


di = {
    'request_name': 'Test name 1',
    'action_type': 'some action type',
    'service': 'PEN',
    'user': 'test_user',
    'uuid': uuid.uuid1().get_hex(),
    'create_timestamp': int(time.time())*1000,
    'status': 'pending',
    'body': {'title': 'Test title 1',
             'some field 1': 'value for field 1',
             'some field 2': 'value for field 2',
             'list field': ['text 1', 'another test',
                            'one more text under list field'],
             'list field 2': ['text 2', 'another test 2',
                            'one more text under list field 2'],
             'list of key:value fields': {'inner field 1': 'text for inner field 1',
                                          'inner field 2': 'text for inner field 2'},
             'list of key:value fields 2': {'inner field 2.1': 'text for inner field 2.1',
                                            'inner field 2.2': 'text for inner field 2.2'},
             'comments': []}
}

di2 = {
    'request_name': 'Test name 2',
    'action_type': 'some action type',
    'service': 'PEN',
    'user': 'test_user',
    'uuid': uuid.uuid1().get_hex(),
    'create_timestamp': int(time.time())*1000,
    'status': 'pending',
    'body': {'title': 'Test title 2',
             'some field 1': 'value for field 1',
             'some field 2': 'value for field 2',
             'some field 3': 'value for field 3',
             'list field': ['text 1', 'another test',
                            'one more text under list field'],
             'list field 2': ['text 2', 'another test 2',
                              'one more text under list field 2'],
             'list field 3': ['text 3', 'another test 3',
                              'one more text under list field 3'],
             'list of key:value fields': {'inner field 1': 'text for inner field 1',
                                          'inner field 2': 'text for inner field 2'},
             'list of key:value fields 2': {'inner field 2.1': 'text for inner field 2.1',
                                            'inner field 2.2': 'text for inner field 2.2'},
             'list of key:value fields 3': {'inner field 3.1': 'text for inner field 3.1',
                                            'inner field 3.2': 'text for inner field 3.2'},
             'comments': [{'comment_body': ['some comment'],
                           'create_timestamp': int(time.time())*1000,
                           'user': 'test_user',
                           'approval_group': 'test group'},
                          {'comment_body': ['some comment'],
                           'create_timestamp': int(time.time())*1000,
                           'user': 'test_user',
                           'approval_group': 'test group'}]}
}

#st.set("request:" + di['service'] + ":" + di['request_name'], di)
Request.objects.create(name=di['request_name'],
                       service=di['service'],
                       uuid=di['uuid'],
                       request=json.dumps(di))
Request.objects.create(name=di2['request_name'],
                       service=di2['service'],
                       uuid=di2['uuid'],
                       request=json.dumps(di2))


#########################################
#    API  example for Approval Chain    #
request_example = {
    'request_name': 'Test name 2',
    'action_type': 'some action type',
    'service': 'PEN',
    'user': 'test_user',
    'uuid': uuid.uuid1().get_hex(),
    'create_timestamp': int(time.time())*1000,
    'body': {'title': 'Test title 2',
             'some field 1': 'value for field 1',
             'some field 2': 'value for field 2',
             'some field 3': 'value for field 3',
             'list field': ['text 1', 'another test',
                            'one more text under list field'],
             'list field 2': ['text 2', 'another test 2',
                              'one more text under list field 2'],
             'list field 3': ['text 3', 'another test 3',
                              'one more text under list field 3'],
             'list of key:value fields': {'inner field 1': 'text for inner field 1',
                                          'inner field 2': 'text for inner field 2'},
             'list of key:value fields 2': {'inner field 2.1': 'text for inner field 2.1',
                                            'inner field 2.2': 'text for inner field 2.2'},
             'list of key:value fields 3': {'inner field 3.1': 'text for inner field 3.1',
                                            'inner field 3.2': 'text for inner field 3.2'},
             'comments': []}
}
#########################################





import time
import uuid
from django.contrib.auth.models import User, Group
from main.models import *
import json


service = Service.objects.get(name='PEN')
user1 = User.objects.create_user('Sam', 'sam@example.com', 'password')
user2 = User.objects.create_user('Joy', 'joy@example.com', 'password')
user3 = User.objects.create_user('Andue', 'andue@example.com', 'password')
user4 = User.objects.create_user('Olga', 'olga@example.com', 'password')
user5 = User.objects.create_user('Dasha', 'dasha@example.com', 'password')
user6 = User.objects.create_user('Tom', 'tom@example.com', 'password')
user7 = User.objects.create_user('Yurii', 'yurii@example.com', 'password')
user8 = User.objects.create_user('Vitality', 'vitality@example.com', 'password')
user9 = User.objects.create_user('Saiman', 'saiman@example.com', 'password')
user10 = User.objects.create_user('Mortina', 'mortina@example.com', 'password')

service.users.add(user1,
                  user2,
                  user3,
                  user4,
                  user5,
                  user6,
                  user7,
                  user8,
                  user9,
                  user10,
)







import requests
import json
import time
url = "http://localhost:9000/api/receive_request/"

data = {
    'request_name': 'Create topology for ...',
    'action_type': 'create-topology',
    'service': 'PEN',
    'user_id': '226838',
    'create_timestamp': time.time()*1000,
    'body': {'title': 'Create topology',
             'some field 1': 'value for field 1',
             'some field 2': 'value for field 2',
             'list field': ['text 1', 'another test',
                            'one more text under list field'],
             'list field 2': ['text 2', 'another test 2',
                              'one more text under list field 2'],
             'list of  fields': {'inner field 1': 'text for inner field 1',
                                          'inner field 2': 'text for inner field 2'},
             'list of fields 2': {'inner field 2.1': 'text for field 2.1',
                                            'inner field 2.2': 'text for field 2.2'}
    }
}

resp = requests.post(url, data=json.dumps(data)); resp.text







data = {
    'request_name': 'Create topology for ...',
    'action_type': 'create-topology',
    'service': 'PEN',
    'user_id': '226838',
    'create_timestamp': time.time()*1000,
    'body': {'title': 'Create topology',
             'some field 1': 'value for field 1',
             'some field 2': 'value for field 2',
             'list field': ['text 1', 'another test',
                            'one more text under list field'],
             'list field 2': ['text 2', 'another test 2',
                              'one more text under list field 2'],
             'list of key:value fields': {'inner field 1': 'text for inner field 1',
                                          'inner field 2': 'text for inner field 2'},
             'list of key:value fields 2': {'inner field 2.1': 'text for field 2.1',
                                            'inner field 2.2': 'text for field 2.2'}
    }
}