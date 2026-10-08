import sys

with open('.github/workflows/deploy.yml', 'r') as f:
    content = f.read()

content = content.replace(
'''        shell: powershell
        env:
          POSTGRES_PASSWORD: \$\{\{ secrets.DEV_POSTGRES_PASSWORD \}\}
          JWT_SECRET: \$\{\{ secrets.DEV_JWT_SECRET \}\}
        run:'''.replace('\\', ''),
'''        shell: powershell
        run:'''
)

content = content.replace(
'''        shell: powershell
        env:
          POSTGRES_PASSWORD: \$\{\{ secrets.PROD_POSTGRES_PASSWORD \}\}
          JWT_SECRET: \$\{\{ secrets.PROD_JWT_SECRET \}\}
        run:'''.replace('\\', ''),
'''        shell: powershell
        run:'''
)

with open('.github/workflows/deploy.yml', 'w') as f:
    f.write(content)
