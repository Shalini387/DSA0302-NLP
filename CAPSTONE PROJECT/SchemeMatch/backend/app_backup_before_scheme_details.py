from flask import Flask, request, jsonify
from flask_cors import CORS
import random
import re

app = Flask(__name__)
CORS(app)

# =========================================================
# OTP STORAGE
# =========================================================

otp_store = {}


# =========================================================
# SCHEME DATABASE
# =========================================================

schemes = [

    {
        "id": "pm-kisan",
        "name": "PM-KISAN",
        "category": "Agriculture",
        "description": "Income support for eligible farmer families.",
        "keywords": [
            "farmer",
            "farm",
            "farming",
            "agriculture",
            "agricultural",
            "land",
            "acre",
            "cultivation",
            "crop",
            "cultivate"
        ],
        "priority_keywords": [
            "farmer",
            "farming",
            "agriculture",
            "cultivation"
        ]
    },

    {
        "id": "post-matric-scholarship",
        "name": "Post Matric Scholarship",
        "category": "Education",
        "description": "Financial assistance for eligible students pursuing higher education.",
        "keywords": [
            "student",
            "college",
            "university",
            "education",
            "scholarship",
            "degree",
            "graduation",
            "post graduation",
            "studying",
            "school",
            "btech",
            "engineering"
        ],
        "priority_keywords": [
            "student",
            "scholarship",
            "college",
            "university"
        ]
    },

    {
        "id": "pmegp",
        "name": "PMEGP",
        "category": "Employment",
        "description": "Credit-linked assistance for eligible individuals starting new micro enterprises.",
        "keywords": [
            "business",
            "startup",
            "enterprise",
            "shop",
            "company",
            "self employed",
            "entrepreneur",
            "manufacturing",
            "business owner",
            "small business"
        ],
        "priority_keywords": [
            "business",
            "startup",
            "entrepreneur",
            "enterprise"
        ]
    },

    {
        "id": "pm-svanidhi",
        "name": "PM SVANidhi",
        "category": "Street Vendors",
        "description": "Working-capital support for eligible street vendors.",
        "keywords": [
            "street vendor",
            "vendor",
            "hawker",
            "roadside shop",
            "cart",
            "stall",
            "selling vegetables",
            "selling fruits",
            "street selling"
        ],
        "priority_keywords": [
            "street vendor",
            "vendor",
            "hawker",
            "stall"
        ]
    },

    {
        "id": "pm-jay",
        "name": "Ayushman Bharat PM-JAY",
        "category": "Healthcare",
        "description": "Health coverage support for eligible families under the scheme.",
        "keywords": [
            "health",
            "healthcare",
            "hospital",
            "hospitalization",
            "medical",
            "treatment",
            "medicine",
            "surgery",
            "disease",
            "illness",
            "hospital bill"
        ],
        "priority_keywords": [
            "hospital",
            "hospitalization",
            "treatment",
            "medical",
            "healthcare"
        ]
    },

    {
        "id": "senior-pension",
        "name": "Senior Citizen Social Assistance",
        "category": "Social Security",
        "description": "Social assistance for eligible senior citizens.",
        "keywords": [
            "senior citizen",
            "elderly",
            "old age",
            "old person",
            "retired",
            "pension",
            "aged",
            "60 years",
            "70 years",
            "65 years"
        ],
        "priority_keywords": [
            "senior citizen",
            "elderly",
            "old age",
            "pension"
        ]
    },

    {
        "id": "sukanya-samriddhi",
        "name": "Sukanya Samriddhi Account",
        "category": "Girl Child",
        "description": "Savings scheme intended for the financial future of eligible girl children.",
        "keywords": [
            "girl child",
            "daughter",
            "girl",
            "female child",
            "baby girl",
            "daughter education"
        ],
        "priority_keywords": [
            "girl child",
            "daughter",
            "female child"
        ]
    },

    {
        "id": "disability-support",
        "name": "Disability Support",
        "category": "Social Welfare",
        "description": "Social welfare support for eligible persons with disabilities.",
        "keywords": [
            "disability",
            "disabled",
            "disability certificate",
            "physically challenged",
            "visual impairment",
            "hearing impairment",
            "wheelchair",
            "special needs"
        ],
        "priority_keywords": [
            "disability",
            "disabled",
            "disability certificate"
        ]
    },

    {
        "id": "women-support",
        "name": "Women Support Schemes",
        "category": "Women Welfare",
        "description": "Government support programs available to eligible women depending on their circumstances.",
        "keywords": [
            "woman",
            "women",
            "female",
            "widow",
            "single mother",
            "mother",
            "women entrepreneur",
            "womenentrepreneur"
        ],
        "priority_keywords": [
            "widow",
            "single mother",
            "women entrepreneur",
            "womenentrepreneur"
        ]
    },

    {
        "id": "low-income-support",
        "name": "Social Assistance Schemes",
        "category": "Social Welfare",
        "description": "Potential social assistance for eligible individuals and families based on their circumstances.",
        "keywords": [
            "low income",
            "poor",
            "poverty",
            "financial problem",
            "financial assistance",
            "low salary",
            "unemployed",
            "no income",
            "economically weaker",
            "ews"
        ],
        "priority_keywords": [
            "low income",
            "poverty",
            "unemployed",
            "no income"
        ]
    }
]


# =========================================================
# HOME
# =========================================================

@app.route("/")
def home():

    return jsonify({
        "success": True,
        "message": "SchemeMatch Backend is running"
    })


# =========================================================
# SEND OTP
# =========================================================

@app.route("/send-otp", methods=["POST"])
def send_otp():

    data = request.get_json() or {}

    mobile = data.get("mobile")

    if not mobile:

        return jsonify({
            "success": False,
            "message": "Mobile number is required"
        }), 400

    otp = str(random.randint(100000, 999999))

    otp_store[mobile] = otp

    print(f"OTP for {mobile}: {otp}")

    return jsonify({
        "success": True,
        "message": "OTP generated successfully",
        "otp": otp
    })


# =========================================================
# VERIFY OTP
# =========================================================

@app.route("/verify-otp", methods=["POST"])
def verify_otp():

    data = request.get_json() or {}

    mobile = data.get("mobile")
    otp = data.get("otp")

    if otp_store.get(mobile) == otp:

        del otp_store[mobile]

        return jsonify({
            "success": True,
            "message": "OTP verified successfully"
        })

    return jsonify({
        "success": False,
        "message": "Invalid OTP"
    }), 400


# =========================================================
# TEXT NORMALIZATION
# =========================================================

def normalize_text(text):

    text = text.lower()

    text = re.sub(
        r"[^a-z0-9\s]",
        " ",
        text
    )

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


# =========================================================
# USER DETAIL EXTRACTION
# =========================================================

def extract_user_details(text):

    normalized = normalize_text(text)

    details = {
        "age": None,
        "occupation": None,
        "education": None,
        "income": None,
        "location": None,
        "land": None,
        "gender": None,
        "purpose": None
    }


    # -----------------------------------------------------
    # AGE
    # -----------------------------------------------------

    age_patterns = [

        r"\b(\d{1,3})\s*(?:years old|year old|yrs old|years)\b",

        r"\bage\s*(?:is|of)?\s*(\d{1,3})\b"

    ]

    for pattern in age_patterns:

        match = re.search(
            pattern,
            normalized
        )

        if match:

            details["age"] = int(match.group(1))

            break


    # -----------------------------------------------------
    # OCCUPATION
    # -----------------------------------------------------

    occupation_keywords = {

        "Farmer": [
            "farmer",
            "farming",
            "agriculture",
            "cultivation"
        ],

        "Student": [
            "student",
            "studying",
            "college student",
            "school student"
        ],

        "Entrepreneur": [
            "entrepreneur",
            "business owner",
            "business",
            "startup"
        ],

        "Street Vendor": [
            "street vendor",
            "vendor",
            "hawker"
        ],

        "Job Seeker": [
            "unemployed",
            "job seeker",
            "looking for a job",
            "looking for work"
        ],

        "Employee": [
            "employee",
            "working",
            "job",
            "worker"
        ]
    }


    for occupation, keywords in occupation_keywords.items():

        for keyword in keywords:

            if keyword in normalized:

                details["occupation"] = occupation

                break

        if details["occupation"]:

            break


    # -----------------------------------------------------
    # EDUCATION
    # -----------------------------------------------------

    education_keywords = [

        "btech",
        "b tech",
        "engineering",
        "degree",
        "graduation",
        "post graduation",
        "masters",
        "master",
        "mba",
        "mtech",
        "college",
        "university",
        "school",
        "diploma",
        "intermediate"
    ]


    for keyword in education_keywords:

        if keyword in normalized:

            details["education"] = keyword.upper()

            break


    # -----------------------------------------------------
    # INCOME
    # -----------------------------------------------------

    income_patterns = [

        r"(?:income|salary|earn|earning)[^0-9]{0,30}(\d+(?:\.\d+)?)\s*(lakh|lakhs|l|thousand|k)?",

        r"(\d+(?:\.\d+)?)\s*(lakh|lakhs|l|thousand|k)\s*(?:per year|annually|annual|per month|monthly)?"

    ]


    for pattern in income_patterns:

        match = re.search(
            pattern,
            normalized
        )

        if match:

            number = match.group(1)
            unit = match.group(2)

            if unit:

                unit = unit.lower()

            details["income"] = (
                f"{number} {unit}"
                if unit
                else number
            )

            break


    # -----------------------------------------------------
    # LOCATION
    # -----------------------------------------------------

    indian_states = [

        "andhra pradesh",
        "arunachal pradesh",
        "assam",
        "bihar",
        "chhattisgarh",
        "goa",
        "gujarat",
        "haryana",
        "himachal pradesh",
        "jharkhand",
        "karnataka",
        "kerala",
        "madhya pradesh",
        "maharashtra",
        "manipur",
        "meghalaya",
        "mizoram",
        "nagaland",
        "odisha",
        "punjab",
        "rajasthan",
        "sikkim",
        "tamil nadu",
        "telangana",
        "tripura",
        "uttar pradesh",
        "uttarakhand",
        "west bengal",
        "delhi"
    ]


    for state in indian_states:

        if state in normalized:

            details["location"] = state.title()

            break


    # -----------------------------------------------------
    # LAND
    # -----------------------------------------------------

    land_patterns = [

        r"(\d+(?:\.\d+)?)\s*(?:acres|acre)",

        r"own\s+(\d+(?:\.\d+)?)\s*(?:acres|acre)"

    ]


    for pattern in land_patterns:

        match = re.search(
            pattern,
            normalized
        )

        if match:

            details["land"] = (
                match.group(1) + " acres"
            )

            break


    # -----------------------------------------------------
    # GENDER
    # -----------------------------------------------------

    if re.search(
        r"\b(woman|women|female|girl|mother|widow)\b",
        normalized
    ):

        details["gender"] = "Female"

    elif re.search(
        r"\b(man|men|male|father|boy)\b",
        normalized
    ):

        details["gender"] = "Male"


    # -----------------------------------------------------
    # PURPOSE
    # -----------------------------------------------------

    purpose_keywords = {

        "Education": [
            "education",
            "college fees",
            "school fees",
            "tuition",
            "study",
            "scholarship"
        ],

        "Agriculture": [
            "farming",
            "agriculture",
            "crop",
            "cultivation",
            "farmer"
        ],

        "Business": [
            "business",
            "startup",
            "shop",
            "enterprise"
        ],

        "Healthcare": [
            "health",
            "hospital",
            "medical",
            "treatment",
            "medicine"
        ],

        "Employment": [
            "job",
            "employment",
            "unemployed",
            "work",
            "career"
        ],

        "Financial Assistance": [
            "financial assistance",
            "financial help",
            "money",
            "financial support",
            "low income"
        ]
    }


    for purpose, keywords in purpose_keywords.items():

        for keyword in keywords:

            if keyword in normalized:

                details["purpose"] = purpose

                break

        if details["purpose"]:

            break


    return details


# =========================================================
# CALCULATE SCHEME MATCH
# =========================================================

def calculate_match(text, scheme):

    score = 0

    matched_keywords = []

    normalized_text = normalize_text(text)


    # Priority keywords

    for keyword in scheme["priority_keywords"]:

        keyword_normalized = normalize_text(keyword)

        if keyword_normalized in normalized_text:

            score += 30

            matched_keywords.append(keyword)


    # Normal keywords

    for keyword in scheme["keywords"]:

        keyword_normalized = normalize_text(keyword)

        if keyword_normalized in normalized_text:

            if keyword not in matched_keywords:

                score += 10

                matched_keywords.append(keyword)


    score = min(score, 100)

    return score, matched_keywords


# =========================================================
# ANALYZE USER SITUATION
# =========================================================

@app.route("/analyze", methods=["POST"])
def analyze():

    data = request.get_json() or {}

    situation = data.get(
        "situation",
        ""
    ).strip()


    if not situation:

        return jsonify({
            "success": False,
            "message": "Please describe your situation."
        }), 400


    # -----------------------------------------------------
    # Extract user information
    # -----------------------------------------------------

    user_details = extract_user_details(
        situation
    )


    # -----------------------------------------------------
    # Find matching schemes
    # -----------------------------------------------------

    results = []


    for scheme in schemes:

        score, keywords = calculate_match(
            situation,
            scheme
        )


        if score > 0:

            results.append({

                "id": scheme["id"],

                "name": scheme["name"],

                "category": scheme["category"],

                "description": scheme["description"],

                "matchScore": score,

                "matchedKeywords": keywords

            })


    # -----------------------------------------------------
    # Sort by highest score
    # -----------------------------------------------------

    results.sort(
        key=lambda item: item["matchScore"],
        reverse=True
    )


    # -----------------------------------------------------
    # Remove weak matches
    # -----------------------------------------------------

    results = [

        result

        for result in results

        if result["matchScore"] >= 10

    ]


    # -----------------------------------------------------
    # Response message
    # -----------------------------------------------------

    if len(results) == 0:

        message = (
            "We could not find a strong potential "
            "match based on the information provided."
        )

    elif len(results) == 1:

        message = (
            "We found 1 potential scheme "
            "that may match your situation."
        )

    else:

        message = (
            f"We found {len(results)} potential "
            "schemes that may match your situation."
        )


    # -----------------------------------------------------
    # FINAL RESPONSE
    # -----------------------------------------------------

    return jsonify({

        "success": True,

        "message": message,

        "input": situation,

        "userDetails": user_details,

        "matches": results

    })


# =========================================================
# RUN SERVER
# =========================================================

if __name__ == "__main__":

    app.run(
        debug=True,
        port=5000
    )