from threading import Thread
from web.flaskServer import StartServer
from serviceControllers.dockerController import SpawnContainer, GetContainerIP

# -== Tunable Variables ==-
webPort = 5555

# -== Run Service ==-
print("\n-== Robo Red Team: Training Platform ==-\n")

# Spawn test Docker image
containerId = SpawnContainer("docker_tester:latest")
print("IP of test container: " + GetContainerIP(containerId))
print("Test the docker container here: http://" + GetContainerIP(containerId) + ":8855\n")

# Start the FlaskRESTful web server
StartServer(webPort)