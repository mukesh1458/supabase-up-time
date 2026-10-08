import re
with open('.github/workflows/deploy.yml', 'r') as f:
    content = f.read()

content = content.replace('cp docker-compose.yml docker-compose.yml.bak || true', 'Copy-Item docker-compose.yml docker-compose.yml.bak -ErrorAction SilentlyContinue')

old_if = '''if ! docker inspect -f '{{.State.Running}}' prod-supabase-rest-1 | grep "true"; then
            echo "Prod deployment failed, rolling back!"
            mv docker-compose.yml.bak docker-compose.yml
            docker compose up -d
            exit 1
          fi'''

new_if = '''$status = docker inspect -f '{{.State.Running}}' prod-supabase-rest-1
          if ($status -notmatch "true") {
            echo "Prod deployment failed, rolling back!"
            Move-Item -Force docker-compose.yml.bak docker-compose.yml
            docker compose up -d
            exit 1
          }'''

content = content.replace(old_if, new_if)
content = content.replace('ls -la supabase/migrations/', 'Get-ChildItem -Path supabase/migrations/')

with open('.github/workflows/deploy.yml', 'w') as f:
    f.write(content)
