import sys

with open('.github/workflows/deploy.yml', 'r') as f:
    content = f.read()

content = content.replace(
'''        run: |
          echo "Deploying to Dev environment..."
          cd dev
          Copy-Item C:\\Users\\ADMIN\\Desktop\\aws_hackthon\\supabase-uptime-demo\\dev\\.env .\\.env -ErrorAction SilentlyContinue
          docker compose up -d
          echo "Dev deployed."''',
'''        run: |
          echo "Deploying to Dev environment..."
          Copy-Item -Path dev\\* -Destination C:\\Users\\ADMIN\\Desktop\\aws_hackthon\\supabase-uptime-demo\\dev\\ -Recurse -Force
          cd C:\\Users\\ADMIN\\Desktop\\aws_hackthon\\supabase-uptime-demo\\dev
          docker compose up -d
          echo "Dev deployed."'''
)

content = content.replace(
'''        run: |
          echo "Deploying to Prod environment..."
          cd prod
          Copy-Item C:\\Users\\ADMIN\\Desktop\\aws_hackthon\\supabase-uptime-demo\\prod\\.env .\\.env -ErrorAction SilentlyContinue
          # Rollback preparation step: copy current state if rollback is needed
          Copy-Item docker-compose.yml docker-compose.yml.bak -ErrorAction SilentlyContinue
          
          # Bring up new stack
          docker compose up -d --build
          
          echo "Verifying prod deployment..."
          sleep 10
          \ = docker inspect -f '\{\{.State.Running\}\}' prod-supabase-rest-1
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
          
          # Bring up new stack
          docker compose up -d --build
          
          echo "Verifying prod deployment..."
          Start-Sleep -Seconds 10
          \ = docker inspect -f '\{\{.State.Running\}\}' prod-supabase-rest-1
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
