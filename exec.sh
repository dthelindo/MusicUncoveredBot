#!/bin/bash 
function run() {
  echo "Running..."
  pipenv install
  pipenv run start
}

DAYOFWEEK=$(date +"%a")
COMMAND="pipenv run start"
if [ $DAYOFWEEK == "Mon" ] 
then   
  run 
else
    echo $DAYOFWEEK
fi
