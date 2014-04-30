
from django.contrib.auth.models import User, Group
import time
import json
import uuid
from workflow.models import *
from main.models import *


Role.objects.all().delete()
State.objects.all().delete()
Role.objects.all().delete()
Transition.objects.all().delete()
EventType.objects.all().delete()
Event.objects.all().delete()
WorkflowActivity.objects.all().delete()
Participant.objects.all().delete()
WorkflowHistory.objects.all().delete()
Action.objects.all().delete()
Role.objects.all().delete()
Chain.objects.all().delete()
ServiceMongo.objects.all().delete()
Group.objects.all().delete()
GroupMongo.objects.all().delete()
Request.objects.all().delete()
Workflow.objects.all().delete()
Service.objects.all().delete()
Account.objects.delete()
User.objects.all().delete()

s = Service.objects.create(name='PEN', description='qwerty', url='qwerty')
a1 = Action.objects.create(name='Create flow', alias='create flow')
a2 = Action.objects.create(name='update', alias='update')
a3 = Action.objects.create(name='create topology', alias='create topology')
s.action.add(a1, a2, a3)



data = json.dumps({u'rules': [{u'rule_name': u'Price', u'rule_alias': u'price'}], u'service_name': u'PEN', u'service_url': u'pen.pacnetconnect.com', u'actions': [{u'action_alias': u'create-flow', u'action_name': u'Create flow'}, {u'action_alias': u'update-flow', u'action_name': u'Change flow parameters'}, {u'action_alias': u'create-topology', u'action_name': u'create topology'}], u'service_description': u'Pacnet'})


ServiceMongo.objects.create(name='PEN', service_data=data)


service = Service.objects.get(name='PEN')



User.objects.create_user('joe', 'joe@acme.com', 'password')
User.objects.create_user('ALL', 'ALL@acme.com', 'password')
u1 = User.objects.create_user('Global Admin (Jon)', 'adm@acme.com', 'password')
u2 = User.objects.create_user('Admin of Account-1', 'adm@acme.com', 'password')
u3 = User.objects.create_user('User-1 of Account-1', 'adm@acme.com', 'password')
u4 = User.objects.create_user('User-2 of Account-1', 'adm@acme.com', 'password')
u5 = User.objects.create_user('User-3 of Account-1', 'adm@acme.com', 'password')
u6 = User.objects.create_user('User-4 of Account-1', 'adm@acme.com', 'password')


acc = Account.objects.create(name="Account-1")
acc.admin.add(u2)
acc.users.add(u2, u3, u4, u5, u6)


service.users.add(
		  u2, u3, u4, u5, u6
)

