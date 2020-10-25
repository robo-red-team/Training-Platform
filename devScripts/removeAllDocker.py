import docker
import os
import sys

if len(sys.argv) > 1 and sys.argv[1] == "yes":
    client = docker.from_env()
    removeCmd = ""
    for container in client.containers.list():
        removeCmd += "$(bash removeDockerContainer.sh " + str(container.id[0:10]) + ") & "
    print(removeCmd + "wait && docker system prune -a")
    os.system(removeCmd + "wait && docker system prune -a && docker ps")
else:
    print("Please run script with argument 'yes' to confirm you wish to remove containers and services")

