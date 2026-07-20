def fsa_ends_with_ab(string):
    state = 0

    for char in string:
        if state == 0:
            if char == 'a':
                state = 1
            else:
                state = 0

        elif state == 1:
            if char == 'b':
                state = 2
            elif char == 'a':
                state = 1
            else:
                state = 0

        elif state == 2:
            if char == 'a':
                state = 1
            else:
                state = 0

    return state == 2


text = input("Enter a string: ")

if fsa_ends_with_ab(text):
    print("Accepted (Ends with 'ab')")
else:
    print("Rejected (Does not end with 'ab')")