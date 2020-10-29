DAYOFWEEK=$(date +"%a");
COMMAND="pipenv run musicuncovered.py";
CM="pip -V"
echo DAYOFWEEK: $DAYOFWEEK;
if [ "$DAYOFWEEK" == "Thu" ]; 
then   
   eval $CM;
else
    echo $DAYOFWEEK;
fi;