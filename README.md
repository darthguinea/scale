## Scale (README.md)
Use this applcation to deploy new EC2 servers

##Install

```
#Once downloaded, in the scale folder using terminal run:

python setup.py install


#Create an .py file (in this case, example.py):

cat >> example.py << EOF
from scale.server.server import Server

Server(keypair='stage', ec2_environment='default', region='us-west-1', name='my_awesome_server').create()
EOF

python example.py
```

##How to use, basic server build:

```
from scale.server.server import Server

Server(keypair='stage', ec2_environment='default', region='us-west-1', name='my_awesome_server').create()
```


##Tags:
```
from scale.server.server import Server

my_tags = Tags()

my_tags.add('chef_role', 'webserver')
my_tags.add('environment', 'stage')

Server(keypair='stage', ec2_environment='default', region='us-west-1', tags=my_tags.get()).create()
```

##Security Groups:
```
from scale.server.server import Server
from scale.networking.security_group import SecurityGroup


rules = [{"IP": "10.0.2.1/32", 'FromPort': "80", 'ToPort': "80", 'Protocol': "tcp"},
        {"IP": "172.16.32.1/32", 'FromPort': "80", 'ToPort': "80", 'Protocol': "tcp"}]


my_sg_id = SecurityGroup(name='p-web', region='us-west-1', description='web server sg', rules=rules).create()

Server(keypair='stage', security_groups=[my_sg_id], ec2_environment='default', region='us-west-1', name='my_awesome_server').create()

```
