import sys

with open('prod/docker-compose.yml', 'r') as f:
    content = f.read()

content = content.replace(
'''      healthcheck:
        test:
        - CMD
        - pg_isready
        - -U
        - postgres
        - -h
        - localhost
        interval: 10s
        timeout: 5s
        retries: 5''',
'''      healthcheck:
        test:
        - CMD
        - pg_isready
        - -U
        - postgres
        - -h
        - localhost
        start_period: 60s
        interval: 10s
        timeout: 5s
        retries: 20'''
)

with open('prod/docker-compose.yml', 'w') as f:
    f.write(content)
