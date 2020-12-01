import docker
import random
import string

client = docker.from_env()

def get_random_string(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))

# Spawn container, and return it's ID
def SpawnContainer(ContainerName):
    container = client.containers.run(ContainerName, detach=True)
    return str(container.id[0:10])

def SpawnContainerWithPass(ContainerName):
    passwd  = get_random_string(8)
    container = client.containers.run(ContainerName, passwd, detach=True)
    return {"id":str(container.id[0:10]),"password":passwd}

def GetAllContainers():
    return client.containers.list()

def GetContainerIP(ContainerID):
    container = client.containers.get(ContainerID)
    return str(container.attrs["NetworkSettings"]["Networks"]["bridge"]["IPAddress"])

def StopContainer(ContainerID):
    container = client.containers.get(ContainerID)
    container.stop()
