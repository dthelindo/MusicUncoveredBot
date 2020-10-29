DAYOFWEEK=$(date +"%a");
COMMAND="pipenv run musicuncovered.py";
echo DAYOFWEEK: $DAYOFWEEK;
if [ "$DAYOFWEEK" == "Thu" ]; 
then   
   eval $COMMAND;
else
    echo $DAYOFWEEK;
fi;