#!/bin/bash
# health_check.sh
# Pings the Supabase API Gateway every INTERVAL seconds and logs UP/DOWN with a timestamp to health.log.
# Usage: ./health_check.sh [PORT]   (default: 8000 for dev, set 8001 for prod)

PORT="${1:-${PORT:-8000}}"
INTERVAL="${INTERVAL:-30}"
WATCHDOG="${WATCHDOG:-0}"
API_URL="http://localhost:${PORT}/rest/v1/users"
LOG_FILE="health.log"

ENV_FILE="dev/.env"
if [ "$PORT" == "8001" ]; then ENV_FILE="prod/.env"; fi
ANON_KEY=$(grep "^ANON_KEY=" "$ENV_FILE" | cut -d'=' -f2-)

echo "health_check.sh starting: target=$API_URL, log=$LOG_FILE, interval=${INTERVAL}s, watchdog=$WATCHDOG"
echo "Press Ctrl+C to stop."

while true; do
    TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
    HTTP_STATUS=$(curl -s -o /dev/null -w "%{http_code}" --max-time 5 -H "apikey: $ANON_KEY" "$API_URL")

    # 404 from PostgREST means the DB is up but 'users' table doesn't exist (expected for new project).
    # 200 means table exists. 503 means PostgREST is dead/restarting.
    if [ "$HTTP_STATUS" -eq 200 ] 2>/dev/null || [ "$HTTP_STATUS" -eq 404 ] 2>/dev/null; then
        echo "[$TIMESTAMP] UP (HTTP $HTTP_STATUS)" >> "$LOG_FILE"
        echo "[$TIMESTAMP] UP (HTTP $HTTP_STATUS)"
    else
        echo "[$TIMESTAMP] DOWN (HTTP $HTTP_STATUS)" >> "$LOG_FILE"
        echo "[$TIMESTAMP] DOWN (HTTP $HTTP_STATUS)"
        
        if [ "$WATCHDOG" == "1" ]; then
            RECOVER_TIME=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
            echo "[$RECOVER_TIME] RECOVERING" >> "$LOG_FILE"
            echo "[$RECOVER_TIME] RECOVERING"
            
            # Watchdog recovery command
            if [ "$PORT" == "8001" ]; then
                docker compose -f prod/docker-compose.yml up -d rest >/dev/null 2>&1
            else
                docker compose -f dev/docker-compose.yml up -d rest >/dev/null 2>&1
            fi
        fi
    fi

    sleep "$INTERVAL"
done