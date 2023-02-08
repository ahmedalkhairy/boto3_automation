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
command = "sudo clamscan -r /var/www"

for instance in instances:
    file_object = open('run_av_log.log', 'a')
    instance_id = instance.id
    inst_name = [tag['Value']  for tag in instance.tags if tag['Key'] == 'Name']
    print(inst_name)
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
    subprocess.run(ssh)
    now = datetime.now()
    file_object.write(now.strftime("%Y-%m-%d %H:%M:%S") +','+inst_name[0]+','+ip+','+'run clamav\n')
    file_object.close()

    


    
