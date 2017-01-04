# Scale (README.md)
Use this applcation to deploy new EC2 servers

Table of contents
=================

  * [Installation](#installation)
  * [Basic Usage](#basic-usage)
  * [Tags](#tags)
      * [Examples](#examples)
  * [Server](#server)
      * [Server Params](#server-params)
      * [Server Functions](#server-functions)
      * [Examples](#examples)
  * [Disks](#disks)
      * [Disks Params](#disks-params)
      * [Disks Functions](#disks-functions)
      * [Function Parameters](#function-parameters)
      * [Examples](#examples)
  * [Security Groups](#security-groups)
      * [Security Group Params](#security-group-params)
      * [Security Group Functions](#security-group-functions)
      * [Examples](#examples)
          * [Adding Rules](#adding-rules)
          * [Deleting Rules](#deleting-rules)
          * [Deleting All Rules](#deleting-all-rules)



## Installation

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



## Server:

Importing:

```python
from scale.server.server import Server
```


### Server Params

| Parameter | Required | Default Value | Description |
| ---                   | --- | ---     | ---                                                           |
| ec2_environment       | N | 'default' | Set the AWS environment, profiles are in ~/.aws/credentials   | 
| environment           | N | 'stage'   | Set the environment you wish to set for your host, e.g. 'stage', 'prod'| 
| ami                   | N | 'ami-d8bdebb8' | The AMI image to use                                     |
| instance_type         | N | 't2.nano' | Instance Type to use for server                               |
| security_group_ids    | [] | []       | List of security group ids                                    |
| keypair               | Y | None      | EC2 Keypair to use                                            |
| region                | N | 'us-east-1' | EC2 Region to use                                           |
| az                    | N | None      | Availability zone, if one is not set a random one will be picked |
| name                  | N | None      | The name of the server                                        |
| tags                  | N | []        | List of [Tags](#tags) to use                                  |
| dry_run               | N | False     | Test build of the server                                      |



### Server Functions

| Function | Description |
| --- | --- |
| create() | Create Server | 



### Examples:

```python
from scale.server.server import Server

Server(keypair='stage', ec2_environment='default', region='us-west-1', name='my_awesome_server').create()
```


## Disks:

Importing:

```python
from scale.server.disks import Disks
```


### Disks Parameters

No parameters for Disks

| Parameter | Required | Default Value | Description |
| --- | --- | --- | --- |


### Disks Functions

| Function | Description |
| --- | --- | --- |
| add() | Create virtual disk |
| get() | Return disks object |


#### Function Parameters

| Function | Params             | Default       | Description                                   |
| ---      | ---                | ---           | ---                                           |
| add()    | name               | None          | Device Name                                   |
|          | volume_size        | 8Gb           | Disk Size                                     |
|          | device             | '/dev/sda1'   | System device, e.g. /dev/xvda, /dev/sda1      |
|          | encrypted          | False         | Encrypt disk                                  |
|          | volume_type        | gp2           | Can be 'standard'|'io1'|'gp2'|'sc1'|'st1'     |
|          | iops               | 100           | Only required when volume_type is iops        |
|          |                    |                                                               |
| get()    |                    | Return devices                                                |


# Examples:

```python
from scale.server.disks import Disks
from scale.server.server import Server

disks = Disks()

disks.add(volume_size=100, device='/dev/sda1')
disks.add(volume_size=1024, device='/dev/xvdf')

Server(keypair='stage', ec2_environment='default', region='us-west-1', **disks=disks.get()**).create()

```



## Tags:

Importing

```python
from scale.utils.tags import Tags
```

### Examples: 

```python
from scale.server.server import Server

my_tags = Tags()

my_tags.add('chef_role', 'webserver')
my_tags.add('environment', 'stage')

Server(keypair='stage', ec2_environment='default', region='us-west-1', **tags=my_tags.get()**).create()
```



## Security Groups:

Importing:

```python
from scale.security.security_group import SecurityGroup
```


### Security Group Params

| Parameter | Required | Default Value | Description |
| --- | --- | --- | --- |
| ec2_environment | N | 'default' | Set the AWS environment, profiles are in ~/.aws/credentials |
| region | N | 'us-west-1' | Set AWS region, i.e. `us-east-1`, `us-west-2` |
| group_id | **Y**  | None | Security Group Id *Either group_id or name must be specified* |
| name | **Y** | None | Security Group Name *Either group_id or name must be specified* |
| description | Y | None | Description of the security group |
| vpc_id | N | None | The VPC Id to associate the security group with |
| rules=[] | N | None | List of rules to add to the Security Group |


### Security Group Functions

| Function | Description |
| --- | --- |
| create() | Create Security Group | 
| add() | Add list of rules |
| add_rule() | Add single rule |
| delete() | Delete list of rules |
| delete_rule() | Delete single rule |
| delete_all_rules() | Delete all of the rules associated to the SG |
| delete_group() | Delete the security group |
| get_existing_sg_id() | Find security group using name |


`.create()` does not have any parameters, it creates the Security Group based on the values passed into the class.
```
sg = SecurityGroup()
sg.create()
```


`.add_rule()` is used to add a rule to a security group manually
```
.add_rule(self, 
            group_id=None, 
            ip="127.0.0.1/32", 
            from_port=80, 
            to_port=80, 
            protocol="tcp")
```           


### Examples:

Create security group & server then add the security group to the server:
```python
from scale.server.server import Server
from scale.security.security_group import SecurityGroup


rules = [{"IP": "10.0.2.1/32", 'FromPort': "80", 'ToPort': "80", 'Protocol': "tcp"},
        {"IP": "172.16.32.1/32", 'FromPort': "80", 'ToPort': "80", 'Protocol': "tcp"}]


my_sg_id = SecurityGroup(name='p-web', 
                            region='us-west-1', 
                            description='web server sg', 
                            rules=rules).create()

Server(keypair='stage', security_groups=[my_sg_id], 
                ec2_environment='default', region='us-west-1', 
                name='my_awesome_server').create()

```


#### Adding Rules:
```python
sg = SecurityGroup(name='p-web', region='us-west-1', description='web server sg')

rules = [{"IP": "10.0.2.1/32", 'FromPort': "80", 'ToPort': "80", 'Protocol': "tcp"}, 
        {"IP": "172.16.32.1/32", 'FromPort': "80", 'ToPort': "80", 'Protocol': "tcp"}]

sg.add(rules=rules)
```



#### Deleting Rules:
```python
sg = SecurityGroup(name='p-web', region='us-west-1', description='web server sg')

sg.add(rules=rules)

sg.delete(rules=[{"IP": "172.16.32.1/32", 'FromPort': "80", 'ToPort': "80", 'Protocol': "tcp"}])
```



#### Deleting All Rules:
This is an example of creating a `Security Group`, adding rules to it, then deleting all of the rules:
```python
from scale.security.security_group import SecurityGroup

rules = [{"IP": "10.0.2.1/32", 'FromPort': "80", 'ToPort': "80", 'Protocol': "tcp"}, 
        {"IP": "172.16.32.1/32", 'FromPort': "80", 'ToPort': "80", 'Protocol': "tcp"}]

sg = SecurityGroup(name='p-web', region='us-west-1', 
                        description='web server sg', rules=rules)

sg.create()

sg.delete_all_rules()
```

