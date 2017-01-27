# Scale (README.md)

Use this applcation to deploy or update your EC2 servers, Autoscaling groups, Security Groups etc. You can now scale all of your AWS systems using simple scripts and basic configirations

[HowTo Documentation](https://github.com/darthguinea/scale/wiki)


**Quick Example:**
Create an .py file (in this case, example.py), 
be warned that this will build a server when you execute it:
```bash
cat >> example.py << EOF
from scale.server.server import Server

Server(keypair='stage', ec2_environment='default', region='us-west-1', name='my_awesome_server').create()
EOF

python example.py
```
