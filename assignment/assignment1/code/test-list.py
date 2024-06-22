a = [1, 2, 3]
b = [1, 3, 2]

print(a == b)
print('True' if [num for num in a if num not in b] else 'False')