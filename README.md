# Scale (README.md)

Use this applcation to deploy or update EC2 servers, Autoscaling groups, Security Groups etc. You can now scale all of your AWS systems using simple scripts and basic configirations


Table of contents
=================

  * [Installation](#installation)
  * [Basic Usage](#basic-usage)
  * [Tags](#tags)
      * [Tags Examples](#tags-examples)
  * [Server](#server)
      * [Server Params](#server-params)
      * [Server Functions](#server-functions)
      * [Server Examples](#server-examples)
  * [User Data](#user-data)
      * [User Data Params](#user-data-params)
      * [User Data Functions](#user-data-functions)
      * [User Data Examples](#user-data-examples)
  * [S3 Bucket](#s3-bucket)
      * [S3 Bucket Params](#s3-bucket-params)
      * [S3 Bucket Functions](#s3-bucket-functions)
      * [S3 Bucket Examples](#s3-bucket-examples)
  * [Autoscaling](#autoscaling)
      * [Autoscaling Params](#autoscaling-params)
      * [Autoscaling Functions](#autoscaling-functions)
      * [Autoscaling Examples](#autoscaling-examples)
  * [Disks](#disks)
      * [Disks Params](#disks-params)
      * [Disks Functions](#disks-functions)
      * [Function Parameters](#function-parameters)
      * [Disks Examples](#disks-examples)
  * [Security Groups](#security-groups)
      * [Security Group Params](#security-group-params)
      * [Security Group Functions](#security-group-functions)
      * [Security Group Examples](#security-group-examples)
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


### Server Params:

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



### Server Functions:

| Function | Description |
| --- | --- |
| create() | Create Server | 



### Server Examples:

```python
from scale.server.server import Server

Server(keypair='stage', ec2_environment='default', region='us-west-1', name='my_awesome_server').create()
```


## User Data

Importing:
```python
from scale.utils.user_data import UserData
```

### User Data Params

| Parameter             | Required |     Default Value  | Description           |
| ---                   | ---      |      ---           | ---                   |
| user_data_file        | Y        | 'ubuntu'           |                       |
| org                   | Y        | 'my_org'           |                       |
| environment           | Y        | 'stage'            |                       |
| enc_data_bag          | N        | None               |                       |
| validation_key        | Y        | None               |                       |
| chef_url              | Y        | None               |                       |
| chef_role             | Y        | None               |                       |


### User Data Functions

| Function | Description |
| --- | --- |
| create() | Create and return user data | 


### User Data Examples

```python
from scale.utils.user_data import UserData
ud = UserData()
ud.create()
```


## S3 Bucket:

Importing:
```python
from scale.storage.s3_bucket import S3Bucket
```


## S3 Bucket Params:

| Parameter             | Required |     Default Value  | Description           |
| ---                   | ---      |      ---           | ---                   |
| ec2_environment       | Y        | 'default'          |                       |
| region                | Y        | 'us-east-1'        |                       |
| name                  | N        | None               |                       |


## S3 Bucket Functions:


| Function              | Required      | Param         | Description                                           |
| ---                   | ---           | ---           | ---                                                   |
| uploaded_files        | N             | name=None     | Bucket name, can also be passed into constructor      |
|                       | Y             | files=[]      | List of files to upload                               |
|                       | N             | location=''   | Location in bucket `example/folder/file_loc`          |
|                       |               |               |                                                       |
| delete_files()        | N             | name=None     | Bucket name, can also be passed into constructor      |
|                       | Y             | files=[]      | Files to be deleted from S3 bucket                    |


## S3 Bucket Examples:

```python
from scale.storage.s3_bucket import S3Bucket

s3 = S3Bucket()

files = [
    'README.md',
    'setup.py'
    ]

s3.create_bucket(name='this-is-my-bucket')

s3.upload_files(name='this-is-my-bucket', files=files)

s3.delete_files(name='this-is-my-bucket', files=files)

s3.delete_bucket(name='this-is-my-bucket')
```


## Autoscaling:

Importing:
```python
from scale.autoscaling.autoscaling import Autoscaling
```


### Autoscaling Params:


| Parameter             | Required |     Default Value  | Description           |
| ---                   | ---      |      ---           | ---                   |
| ec2_environment       | N        | 'default'          |                       |
| region                | N        | 'us-east-1'        |                       |
| name                  | Y        |  None              |                       |
| ami                   | N        | 'ami-d8bdebb8'     |                       |
| instance_type         | N        | 't2.micro'         |                       |
| keypair               | Y        | 'stage'            |                       |
| disks                 | N        | []                 |                       |
| security_group_ids    | N        | []                 |                       |
| user_data             | N        | None               |                       |
| desired_capacity      | N        | 0                  |                       |
| min                   | N        | 0                  |                       |
| max                   | N        | 0                  |                       |
| azs                   | N        | []                 |                       |



### Autoscaling Functions:

| Function | Description |
| --- | --- |
| create() | Create Autoscaling Group | 


### Autoscaling Examples:

```python
from scale.autoscaling.autoscaling import Autoscaling


asg = Autoscaling(name='s-asg-nginx', region='us-west-1', desired_capacity=0, min=1, max=5)

asg.create()
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


# Disks Examples:

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

### Tags Examples: 

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


### Security Group Examples:

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

