import sys

with open('.github/workflows/deploy.yml', 'r') as f:
    content = f.read()

content = content.replace(
    '''cd dev
          # The .env file would normally be generated or populated here using secrets
          # For self-hosted runner on the same machine, we just use docker compose up''',
    '''cd dev
          Copy-Item C:\\Users\\ADMIN\\Desktop\\aws_hackthon\\supabase-uptime-demo\\dev\\.env .\\.env -ErrorAction SilentlyContinue'''
)

content = content.replace(
    '''cd prod
          # Rollback preparation step: copy current state if rollback is needed''',
    '''cd prod
          Copy-Item C:\\Users\\ADMIN\\Desktop\\aws_hackthon\\supabase-uptime-demo\\prod\\.env .\\.env -ErrorAction SilentlyContinue
          # Rollback preparation step: copy current state if rollback is needed'''
)

with open('.github/workflows/deploy.yml', 'w') as f:
    f.write(content)
