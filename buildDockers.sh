#!/bin/bash
Build() {
    echo -e "\n-== Building in $PWD ==-\n"
    bash buildImage.sh
}

for dir in $(find . -name Dockerfile); #finds all directories containing a dockerfile.
do
    newdir=${dir::-11} #Takes the /Dockerfile part off to correctly cd
    cd $newdir
    Build
    cd -
done
echo -e "\n-== Finished Building Docker Containers ==-\n"
