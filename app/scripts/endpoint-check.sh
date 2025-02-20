#!/bin/bash

url='http://carlosricoveri.duckdns.org'
declare -a endpoints=("/" "/health" "/profile/carlos" "/profile/jorge" "/profile/saul" "/login" "/register")

# Loop through each different endpoint
for n in ${endpoints[@]}
do
    point=$url$n
    echo "Checking endpoint $n:"
    code=$(curl -s -o /dev/null -I -w "%{http_code}" $point)
    
    if [[ $(echo "$code") = *200* ]];
    then
        echo "SUCCESS: $code" ;
    else
        echo "ERROR: $code "
    fi
    echo ;

done