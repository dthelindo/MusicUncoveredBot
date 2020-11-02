DAYOFWEEK=$(date +"%a");
COMMAND="pipenv run musicuncovered.py";
CM="pip -V"
echo DAYOFWEEK: $DAYOFWEEK;
if [ "$DAYOFWEEK" == "Sun" ]; 
then   
  pipenv run musicuncovered.py; 
else
    echo $DAYOFWEEK;
fi;
