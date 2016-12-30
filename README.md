# Scale (README.md)
Use this applcation to deploy new EC2 servers

## Install

Download the latest source, and unzip:
```bash
wget -qO- -O scale.zip https://github.com/darthguinea/scale/archive/master.zip && unzip scale.zip && cd scale-master
```

In the scale folder using terminal run:
```bash
python setup.py install
```


Create an .py file (in this case, example.py), 
be warned that this will build a server when you execute it:
```bash
cat >> example.py << EOF
from scale.server.server import Server

Server(keypair='stage', ec2_environment='default', region='us-west-1', name='my_awesome_server').create()
EOF

python example.py
```

## How to use, basic server build:

```python
from scale.server.server import Server

Server(keypair='stage', ec2_environment='default', region='us-west-1', name='my_awesome_server').create()
```


## Tags:
```python
from scale.server.server import Server

my_tags = Tags()

my_tags.add('chef_role', 'webserver')
my_tags.add('environment', 'stage')

Server(keypair='stage', ec2_environment='default', region='us-west-1', tags=my_tags.get()).create()
```

## Security Groups:
```python
from scale.server.server import Server
from scale.networking.security_group import SecurityGroup


rules = [{"IP": "10.0.2.1/32", 'FromPort': "80", 'ToPort': "80", 'Protocol': "tcp"},
        {"IP": "172.16.32.1/32", 'FromPort': "80", 'ToPort': "80", 'Protocol': "tcp"}]


my_sg_id = SecurityGroup(name='p-web', region='us-west-1', description='web server sg', rules=rules).create()

Server(keypair='stage', security_groups=[my_sg_id], ec2_environment='default', region='us-west-1', name='my_awesome_server').create()

```

This is an example of creating a `Security Group`, adding rules to it, then deleting all of the rules:
```python
from scale.networking.security_group import SecurityGroup

rules = [{"IP": "10.0.2.1/32", 'FromPort': "80", 'ToPort': "80", 'Protocol': "tcp"}, 
        {"IP": "172.16.32.1/32", 'FromPort': "80", 'ToPort': "80", 'Protocol': "tcp"}]

sg = SecurityGroup(name='p-web', region='us-west-1', description='web server sg', rules=rules)

sg.create()

sg.delete_all_rules()
```

Adding and removing rules manually:
```python
sg = SecurityGroup(name='p-web', region='us-west-1', description='web server sg')

sg.add(rules=rules)

sg.delete(rules=[{"IP": "172.16.32.1/32", 'FromPort': "80", 'ToPort': "80", 'Protocol': "tcp"}])
```

