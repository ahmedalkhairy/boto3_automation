import boto3
from boto3.session import Session
import subprocess
import time
import json
import numpy
from datetime import datetime
import subprocess

ec2 = boto3.resource('ec2')
instances = ec2.instances.filter(
    Filters=[{'Name':'tag:scan', 'Values': ['yes']}])
    
command = "sudo apt-get -y install clamav clamav-daemon && sudo systemctl stop clamav-freshclam && sudo freshclam && sudo systemctl start clamav-freshclam && sudo systemctl enable clamav-freshclam"
#loop throught instances
for instance in instances:
    file_object = open('install_av_log.log', 'a')
    instance_id = instance.id
    inst_name = [tag['Value']  for tag in instance.tags if tag['Key'] == 'Name']
    print(inst_name)
    print(f'EC2 instance "{instance_id}" state: {instance.state["Name"]}')
    print(f'EC2 instance "{instance_id}" state: {instance.key_name}')
    key= instance.key_name
    ip=instance.public_ip_address
    ssh = [
    "ssh",
    "-y",
    "-i",
    "/home/ubuntu/keys/"+key, # Assuming the password is provided through an env variable.
    "ubuntu" + "@" +ip,
    command,
    ]
    #execute command
    subprocess.run(ssh)
    now = datetime.now()
    #write to log
    file_object.write(now.strftime("%Y-%m-%d %H:%M:%S") +','+inst_name[0]+','+ip+','+'installed clamav')
    file_object.close()

