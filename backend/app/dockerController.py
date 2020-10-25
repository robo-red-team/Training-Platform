import docker
client = docker.from_env()

# Spawn container, and return it's ID
def SpawnContainer(ContainerName):
    container = client.containers.run(ContainerName, detach=True)
    return str(container.id[0:10])
    
def GetAllContainers():
    return client.containers.list()

def GetContainerIP(ContainerID):
    container = client.containers.get(ContainerID)
    return str(container.attrs["NetworkSettings"]["Networks"]["bridge"]["IPAddress"])

def StopContainer(ContainerID):
    container = client.containers.get(ContainerID)
    container.stop()