# remove duplicates from a list without using a set
duplist = [1,2,2,3,4,4,5]

# uniqueList = []

# for num in duplist:
#     if num not in uniqueList:
#         uniqueList.append(num)

# print(uniqueList)

uniqueList = list(dict.fromkeys(duplist))

print(uniqueList)