import docker
import os
import sys

if len(sys.argv) > 1 and sys.argv[1] == "yes":
    client = docker.from_env()
    for container in client.containers.list():
        containerID = container.id[0:10]
        os.system("bash removeDockerContainer.sh " + str(containerID))
        print("Removed: " + str(containerID))
    os.system("docker system prune -a")
else:
    print("Please run script with argument 'yes' to confirm you wish to remove containers and services")

