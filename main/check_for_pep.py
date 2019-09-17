import pep8
pep8style = pep8.StyleGuide(quiet=True)
FILEPATH = 'dz4/SQLAlchemy.py'
result = pep8style.check_files([FILEPATH])
print(result.messages, FILEPATH, sep='\n')
