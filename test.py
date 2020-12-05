import re

ret = re.findall(r'\d{5}', 'hello 42 I\'m a 32231 string 30')

print(ret[0])