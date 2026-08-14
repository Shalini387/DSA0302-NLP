def check_agreement(subject, verb):
    singular_subjects = ["boy", "girl", "student"]
    singular_verbs = ["plays", "writes", "runs"]

    if subject in singular_subjects and verb in singular_verbs:
        return "Subject-verb agreement is correct"
    return "Subject-verb agreement is incorrect"


def check_arguments(verb, arguments):
    frames = {
        "give": 3,
        "sleep": 1
    }

    required = frames.get(verb, 0)

    if len(arguments) == required:
        return "Verb argument structure is correct"
    return "Verb argument structure is incorrect"


print(check_agreement("student", "writes"))
print(check_arguments("give", ["she", "child", "book"]))