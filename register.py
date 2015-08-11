import os

os.system("pandoc --from=markdown --to=rst README.md -o README.rst")
os.system("python setup.py register")
os.remove('README.rst')