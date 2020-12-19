import docker
import os
import sys

# Ensure that the first parameter is "yes", to not delete all docker files on accident
if len(sys.argv) > 1 and sys.argv[1] == "yes":
    client = docker.from_env()

    # Construct a bash command to remove all containers threaded, and then run it
    removeCmd = ""
    for container in client.containers.list():
        removeCmd += "$(bash removeDockerContainer.sh " + str(container.id[0:10]) + ") & "
    os.system(removeCmd + "wait && docker system prune -a && docker ps")
else:
    print("Please run script with argument 'yes' to confirm you wish to remove containers and services")
