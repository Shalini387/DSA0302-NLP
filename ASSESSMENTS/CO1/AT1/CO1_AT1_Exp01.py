import re

# Sample resumes
resumes = [
"""
John Smith
Email: john.smith@gmail.com
Phone: +91 9876543210
Skills: Python, SQL, Machine Learning
Experience: 3 years
""",

"""
Alice Johnson
Email: alice123@yahoo.com
Mobile: 9123456789
Skills: Java, SQL
Experience: 1 year
""",

"""
Michael Brown
Email: michael.brown@outlook.com
Phone: 9876501234
Skills: Python, Java, NLP
Experience: 5 years
"""
]

# List of technical skills
technical_skills = ["Python", "Java", "SQL", "Machine Learning", "NLP"]

# Function to extract resume details
def extract_resume_info(resume):

    # Name (Assuming first line contains the name)
    lines = resume.strip().split("\n")
    name = lines[0].strip()

    # Email
    email = re.findall(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}', resume)
    email = email[0] if email else "Not Found"

    # Mobile Number
    phone = re.findall(r'(?:\+91[\s-]?)?[6-9]\d{9}', resume)
    phone = phone[0] if phone else "Not Found"

    # Skills
    skills = []
    for skill in technical_skills:
        if re.search(skill, resume, re.IGNORECASE):
            skills.append(skill)

    # Experience
    exp = re.search(r'(\d+)\s+year', resume, re.IGNORECASE)
    experience = int(exp.group(1)) if exp else 0

    return {
        "Name": name,
        "Email": email,
        "Phone": phone,
        "Skills": skills,
        "Experience": experience
    }

# Process resumes
eligible_candidates = []

print("----------- Candidate Summary -----------\n")

for resume in resumes:
    candidate = extract_resume_info(resume)

    print("Name       :", candidate["Name"])
    print("Email      :", candidate["Email"])
    print("Phone      :", candidate["Phone"])
    print("Skills     :", ", ".join(candidate["Skills"]))
    print("Experience :", candidate["Experience"], "Years")
    print("-" * 40)

    # Eligibility Criteria
    if candidate["Experience"] >= 2 and "Python" in candidate["Skills"]:
        eligible_candidates.append(candidate)

# Display Eligible Candidates
print("\n====== Eligible Candidates ======\n")

if eligible_candidates:
    for c in eligible_candidates:
        print(f"{c['Name']} ({c['Experience']} Years Experience)")
else:
    print("No eligible candidates found.")
