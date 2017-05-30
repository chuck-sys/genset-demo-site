#!/usr/bin/env bash
API_PATH="https://python-testing-cheukyin699.c9users.io/api/logs"
DATA='{"session_id": "72r0qt54", "progress": 10, "text": "Killing monsters...", "auth_token": "PqYnUQuwfRxB7NY"}'
curl -X GET -i -H "Content-Type: application/json" "$API_PATH?sid=72r0qt54"