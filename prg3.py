# move all zeros to end 0,1,0,3,0,12

numbers = [0,1,0,3,0,12]
final_list = []
zero_list = []

for num in numbers:
    if num == 0:
        zero_list.append(num)
    else:
        final_list.append(num)
    
final_list.extend(zero_list)
print(final_list)

