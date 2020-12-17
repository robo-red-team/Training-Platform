import docker
import random
import string
import sys

# Get information about the current Docker environment
client = docker.from_env()

# Generate a random string, of the desired length
def GetRandomString(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))

# Spawn container, and return it's ID
def SpawnContainer(ContainerName):
    container = client.containers.run(ContainerName, detach=True, network="docker-vpn")
    return str(container.id[0:10])

# Spawn container, give it a password for SSH, and return it's ID + password
def SpawnContainerWithPass(ContainerName):
    passwd = GetRandomString(16)
    container = client.containers.run(ContainerName, passwd, detach=True, network="docker-vpn")
    return {"id": str(container.id[0:10]), "password": str(passwd)}

# Return a list of all docker containers on the machine
def GetAllContainers():
    return client.containers.list()

# Get the IP of a running docker container, based upon the containerID
def GetContainerIP(ContainerID):
    container = client.containers.get(ContainerID)
    return str(container.attrs["NetworkSettings"]["Networks"]["docker-vpn"]["IPAddress"])

# Stop a running docker container, based upon the containerID
def StopContainer(ContainerID):
    try:
        container = client.containers.get(ContainerID)
        container.stop()
        return True
    except:
        return False
