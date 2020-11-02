#!/bin/bash 
function run() {
  echo "Running..."
  pipenv install
  pipenv run start
  echo "Finished!"
}

DAYOFWEEK=$(date +"%a")
if [ $DAYOFWEEK == "Mon" ] 
then   
  run 
else
    echo $DAYOFWEEK
fi
