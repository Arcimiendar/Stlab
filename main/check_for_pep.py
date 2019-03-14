import pep8
pep8style = pep8.StyleGuide(quiet=True)
result = pep8style.check_files(['main.py'])
print(result.messages)


