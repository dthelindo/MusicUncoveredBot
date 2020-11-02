DAYOFWEEK=$(date +"%a");
COMMAND="pipenv run musicuncovered.py";
CM="pip -V"
echo DAYOFWEEK: $DAYOFWEEK;
if [ $DAYOFWEEK == "Mon" ]; 
then   
  eval $COMMAND; 
else
    echo $DAYOFWEEK;
fi;
