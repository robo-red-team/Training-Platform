import vagrant
import re
import glob

# Regex to make sure input is of expected characters
def GetCleanPath(FolderPath):
    return str(re.sub("[^0-9a-zA-Z-\/.]", "", str(FolderPath)))

# Ensure that a Vagrantfile actually excists on the given path
def ValidatePath(FolderPath):
    cleanPath = GetCleanPath(FolderPath)
    # Look in the folder for the file
    searchResult = glob.glob(str(cleanPath) + "Vagrantfile", recursive=False)
    if len(searchResult) == 1:
        return True
    else:
        return False

# Function to control vagrant machines (intended as private function)
def VagrantController(FolderPath, Action):
    cleanPath = GetCleanPath(FolderPath)
    if ValidatePath(cleanPath):
        v = vagrant.Vagrant(cleanPath)
        
        # Do desired action
        if str(Action) == "spawn":
            v.up()
        elif str(Action) == "remove":
            v.destroy()
        elif str(Action) == "stop":
            v.halt()
        elif str(Action) == "ip":
            return str(v.hostname())
        else:
            return "Invalid Option"

        return True # as action worked
    else:
        return "Invalid Path"

# Spawn/build a Vagrant machine, and run it
def SpawnVagrantMachine(FolderPath):
    return VagrantController(FolderPath, "spawn")

# Remove a Vagrant machine, and connected files
def RemoveMachine(FolderPath):
    return VagrantController(FolderPath, "remove")

# Stop Vagrant Machine
def StopMachine(FolderPath):
    return VagrantController(FolderPath, "stop")

# Get the Vagrant machine's IP and port as dictionary
def GetMachineIP(FolderPath):
    return VagrantController(FolderPath, "ip")
