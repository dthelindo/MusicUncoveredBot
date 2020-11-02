DAYOFWEEK=$(date +"%a");
COMMAND="pipenv run start";
if [ $DAYOFWEEK == "Mon" ]; 
then   
  eval $COMMAND; 
else
    echo $DAYOFWEEK;
fi;
