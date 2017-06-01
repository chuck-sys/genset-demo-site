#!/usr/bin/env bash

BASE="http://python-testing-cheukyin699.c9users.io"
API_PATH="$BASE/api/script_update"
API_KEY="PqYnUQuwfRxB7NY"
HEADER="Content-Type: application/json"

function script_update {
    data="{\"session_id\": \"$SID\", \"progress\": $1, \"text\": \"$2\", \"auth_token\": \"$API_KEY\"}"
    curl -X POST -d "$data" -H "$HEADER" "$API_PATH" > /dev/null 2>&1
}

SID=$1

echo "========== INITIALIZING =========="
script_update 0 "========== INITIALIZING =========="

sleep 1

echo "========== CONVERTING CSV TO ARFF =========="
script_update 5 "========== CONVERTING CSV TO ARFF =========="

sleep 1

echo "========== RUNNING WEKA =========="
script_update 20 "========== RUNNING WEKA =========="

sleep 5

echo "========== PARSING WEKA RESULTS =========="
script_update 80 "========== PARSING WEKA RESULTS =========="

sleep 2

echo "========== GENERATING RESULTS =========="
script_update 95 "========== GENERATING RESULTS =========="

sleep 1

echo "========== FINISHED =========="
script_update 100 "========== FINISHED =========="
