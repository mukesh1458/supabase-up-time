#!/bin/bash
# simulate_failure.sh
# Stops the container cleanly to simulate an outage for the watchdog to fix.

ENV="${1:-dev}"
REST_CONTAINER="${ENV}-supabase-rest-1"

echo "Looking for ${ENV} REST container..."

if ! docker ps | grep -q "$REST_CONTAINER"; then
    echo "ERROR: No Supabase REST container found to kill."
    exit 1
fi

echo "Found container: $REST_CONTAINER"
echo "Simulating outage via 'docker stop'..."

STOP_TIME=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
docker stop "$REST_CONTAINER" >/dev/null

echo "Container stopped at $STOP_TIME."
echo "Failure simulation complete. Watchdog should recover it shortly."