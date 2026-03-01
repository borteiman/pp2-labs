import re

print("1. 'a' followed by zero or more 'b'")
pattern1 = r"^ab*$"
tests1 = ["a", "ab", "abbb", "ac"]
for t in tests1:
    print(t, "->", bool(re.match(pattern1, t)))

print("\n2. 'a' followed by two to three 'b'")
pattern2 = r"^ab{2,3}$"
tests2 = ["abb", "abbb", "abbbb", "ab"]
for t in tests2:
    print(t, "->", bool(re.match(pattern2, t)))

print("\n3. lowercase letters joined with underscore")
pattern3 = r"^[a-z]+_[a-z]+$"
tests3 = ["hello_world", "Hello_world", "test_case", "wrongCase"]
for t in tests3:
    print(t, "->", bool(re.match(pattern3, t)))

print("\n4. One uppercase followed by lowercase letters")
pattern4 = r"^[A-Z][a-z]+$"
tests4 = ["Hello", "HELLO", "World", "world"]
for t in tests4:
    print(t, "->", bool(re.match(pattern4, t)))

print("\n5. 'a' followed by anything, ending in 'b'")
pattern5 = r"^a.*b$"
tests5 = ["ab", "axxxb", "ac", "a123b"]
for t in tests5:
    print(t, "->", bool(re.match(pattern5, t)))

print("\n6. Replace space, comma, or dot with colon")
text6 = "Hello, world. Python is cool"
result6 = re.sub(r"[ ,.]", ":", text6)
print(result6)

print("\n7. snake_case to camelCase")

def snake_to_camel(s):
    return re.sub(r"_([a-z])", lambda m: m.group(1).upper(), s)

print(snake_to_camel("hello_world_test"))

print("\n8. Split at uppercase letters")
text8 = "HelloWorldTest"
result8 = re.split(r"(?=[A-Z])", text8)
print(result8)

print("\n9. Insert spaces before capital letters")
text9 = "HelloWorldTest"
result9 = re.sub(r"([A-Z])", r" \1", text9).strip()
print(result9)

print("\n10. camelCase to snake_case")

def camel_to_snake(s):
    return re.sub(r"([A-Z])", r"_\1", s).lower()

print(camel_to_snake("helloWorldTest"))