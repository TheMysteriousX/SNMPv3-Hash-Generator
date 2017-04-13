import pypandoc
import os

output = pypandoc.convert_file('README.md', 'rst')

with open('README.rst','w+') as f:
    f.write(output)
