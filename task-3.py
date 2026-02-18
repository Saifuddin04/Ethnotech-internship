'''
INPUT: 
    3
    Mike Thomson 20 M
    Robert Bustle 32 M
    Andria Bustle 30 F
'''

def person_lister(func):
    def inner(people):
        people.sort(key=lambda x: int(x[2]))
        return [func(person) for person in people]
    return inner


@person_lister
def name_format(person):
    first, last, age, sex = person
    title = "Mr." if sex == "M" else "Ms."
    return f"{title} {first} {last}"


# if __name__ == "__main__":
n = int(input("Enter the number of people: "))
people = [input("\nEnter first name, last name, age, gender(in order): \n").split() for _ in range(n)]
formatted = name_format(people)
print(*formatted, sep="\n")
