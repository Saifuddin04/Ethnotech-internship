# input = "is1 Thi0s"
# result = ""

# for i in range(len(input)):
#     curr = input[i]
#     if not curr.isdigit():
#         result = result + curr

# print(result)

input_str = "is1 Thi0s"
words = input_str.split()  
result_list = [None] * len(words)

for word in words:
    for char in word:
        if char.isdigit():
            index = int(char)
            result_list[index] = word.replace(char, "")

print(" ".join(result_list))
