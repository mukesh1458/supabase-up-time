import sys

with open('prod/docker-compose.yml', 'r') as f:
    content = f.read()

content = content.replace(
'''      interval: 5s
      timeout: 5s
      retries: 10''',
'''      start_period: 60s
      interval: 10s
      timeout: 5s
      retries: 20'''
)

with open('prod/docker-compose.yml', 'w') as f:
    f.write(content)
