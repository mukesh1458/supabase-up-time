import sys

with open('.github/workflows/deploy.yml', 'r') as f:
    content = f.read()

content = content.replace(
'''        run: |
          echo "Deploying to Prod environment..."
          Copy-Item -Path prod\\* -Destination C:\\Users\\ADMIN\\Desktop\\aws_hackthon\\supabase-uptime-demo\\prod\\ -Recurse -Force
          cd C:\\Users\\ADMIN\\Desktop\\aws_hackthon\\supabase-uptime-demo\\prod
          
          # Rollback preparation step: copy current state if rollback is needed
          Copy-Item docker-compose.yml docker-compose.yml.bak -ErrorAction SilentlyContinue
          
          # Bring up new stack
          docker compose up -d --build
          
          echo "Verifying prod deployment..."
          Start-Sleep -Seconds 10
          \ = docker inspect -f '{{.State.Running}}' prod-supabase-rest-1
          if (\ -notmatch "true") {
            echo "Prod deployment failed, rolling back!"
            Move-Item -Force docker-compose.yml.bak docker-compose.yml
            docker compose up -d
            exit 1
          }
          
          echo "Prod deployed successfully."'''.replace('\\', ''),
'''        run: |
          echo "Deploying to Prod environment..."
          Copy-Item -Path prod\\* -Destination C:\\Users\\ADMIN\\Desktop\\aws_hackthon\\supabase-uptime-demo\\prod\\ -Recurse -Force
          cd C:\\Users\\ADMIN\\Desktop\\aws_hackthon\\supabase-uptime-demo\\prod
          
          # Rollback preparation step: copy current state if rollback is needed
          Copy-Item docker-compose.yml docker-compose.yml.bak -ErrorAction SilentlyContinue
          
          echo "Starting prod database..."
          docker compose up -d db
          
          echo "Waiting for db to become healthy (max 3 minutes)..."
          \ = 180
          \ = Get-Date
          \ = \False
          while (((Get-Date) - \).TotalSeconds -lt \) {
            \ = docker inspect -f '{{.State.Health.Status}}' prod-supabase-db-1
            if (\ -match "healthy") {
              \ = \True
              break
            }
            Start-Sleep -Seconds 5
          }
          if (-not \) {
            echo "Database failed to become healthy. Check logs."
            docker logs prod-supabase-db-1 --tail 50
            exit 1
          }
          
          echo "Database is healthy. Bringing up the rest of the stack..."
          docker compose up -d --build
          
          echo "Verifying prod deployment..."
          Start-Sleep -Seconds 10
          \ = docker inspect -f '{{.State.Running}}' prod-supabase-rest-1
          if (\ -notmatch "true") {
            echo "Prod deployment failed, rolling back!"
            Move-Item -Force docker-compose.yml.bak docker-compose.yml
            docker compose up -d
            exit 1
          }
          
          echo "Prod deployed successfully."'''.replace('\\', '')
)

with open('.github/workflows/deploy.yml', 'w') as f:
    f.write(content)
