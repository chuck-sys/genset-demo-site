#!/usr/bin/env bash

BASE="http://python-testing-cheukyin699.c9users.io"
API_PATH="$BASE/api/script_update"
API_KEY="PqYnUQuwfRxB7NY"
HEADER="Content-Type: application/json"

function script_update {
    data="{\"session_id\": \"$SID\", \"progress\": $1, \"text\": \"$2\", \"auth_token\": \"$API_KEY\"}"
    curl -X POST -d "$data" -H "$HEADER" "$API_PATH" > /dev/null 2>&1
}

function synchronize {
    echo "$2"
    script_update $1 "$2"
}

SID=$1

synchronize 0 "========== INITIALIZING =========="

synchronize 10 "Setting variables"
UPLOAD_PATH="/home/ubuntu/workspace/uploads/$SID"
TOARFF="scripts/toarff.py"

synchronize 20 "========== CONVERTING CSV TO ARFF =========="

for csv in "$UPLOAD_PATH/*.csv"; do
    :
done

synchronize 40 "========== RUNNING WEKA =========="

sleep 5

synchronize 60 "========== PARSING WEKA RESULTS =========="

sleep 2

synchronize 80 "========== GENERATING RESULTS =========="

sleep 1

synchronize 100 "========== FINISHED =========="
