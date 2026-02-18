import calendar

month, day, year = map(int, input("enter month, day, year: ").split())
day_index = calendar.weekday(year, month, day)

# print(day_index)
print(calendar.day_name[day_index].upper())