states = ['q0', 'q1', 'q2']
alphabet = ['a', 'b']

transition = {
    ('q0', 'a'): 'q1',
    ('q0', 'b'): 'q0',
    ('q1', 'a'): 'q1',
    ('q1', 'b'): 'q2',
    ('q2', 'a'): 'q1',
    ('q2', 'b'): 'q0'
}

initial_state = 'q0'
final_states = ['q2']

string = input("Enter String: ")

current_state = initial_state
path = [current_state]

valid = True

for ch in string:
    if ch not in alphabet:
        valid = False
        break
    current_state = transition[(current_state, ch)]
    path.append(current_state)

print("Transition Path:")
print(" → ".join(path))

if valid and current_state in final_states:
    print("Accepted")
else:
    print("Rejected")
