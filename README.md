## Scale (README.md)
Use this applcation to deploy new EC2 servers

## Install

```
python setup.py install
```

## How to use

```
from scale.server.server import Server

Server(keypair='~/.ssh/stage.pem', ec2_environment='default', region='us-west-1')
```
