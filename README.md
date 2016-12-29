## Scale (README.md)
Use this applcation to deploy new EC2 servers

##Install

```
python setup.py install
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
