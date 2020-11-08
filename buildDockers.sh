#!/bin/bash
Build() {
    echo -e "\n-== Building ==-\n"
    bash buildImage.sh
}

cd backend/microServices/AuthService/
Build
cd ../dataStoreService/
Build
cd ../../../machines/docker/dockerTester/
Build
echo -e "\n-== Finished Building Docker Containers ==-\n"