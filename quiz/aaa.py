import re

pattern = re.compile(r"cat", re.IGNORECASE)
print(pattern.findall("Cat cAt CAT"))

import re

pattern = re.compile(r"\d+")
print(pattern.search("Age: 20").group())
print(pattern.findall("1 22 333"))