sentence = input("enter the string: ").lower()
vowels = "aeiou"
result_string = "" 

for i in range(len(sentence)):
    curr = sentence[i]
    
    if curr not in vowels:
        result_string = result_string + curr  
    else:
        is_repeating = False
        
        if i < len(sentence) - 1:
            if sentence[i+1] in vowels:
                is_repeating = True
        
        if sentence[i-1] in vowels:
                is_repeating = True
                
        if is_repeating:
            result_string = result_string + curr 

print(result_string)
