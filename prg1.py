# find the largest num in a list :10, 45, 99, 3, 20, 60

num = [10, 45, 99, 3, 20, 60]
largest = num[0]

for item in num:
    if item > largest:
        largest = item

print (largest)

