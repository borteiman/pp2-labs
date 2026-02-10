def chek_valid(nums):

    for num in nums:
        if int(num) % 2 != 0:
            return "Not valid"

    return "Valid"

data = input()

print(chek_valid(data))