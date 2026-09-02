from flask import Flask, request, jsonify, Response, stream_with_context
from flask_cors import CORS
import random
import re
import json
from pathlib import Path
from datetime import datetime
import os


app = Flask(__name__)
CORS(app)

# =========================================================
# OTP STORAGE
# =========================================================

otp_store = {}
pending_auth = {}

USERS_FILE = Path(__file__).with_name("users.json")

def load_users():
    if not USERS_FILE.exists():
        return {}
    try:
        return json.loads(USERS_FILE.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {}

def save_users(users):
    USERS_FILE.write_text(
        json.dumps(users, indent=2),
        encoding="utf-8"
    )

users = load_users()


# =========================================================
# SCHEME DATABASE
# =========================================================

schemes = [

    # -----------------------------------------------------
    # 1. PM-KISAN
    # -----------------------------------------------------

    {
        "id": "pm-kisan",
        "name": "PM-KISAN",
        "category": "Agriculture",
        "description": "Income support for eligible land-holding farmer families.",

        "benefits": [
            "Income support of ₹6,000 per year.",
            "The amount is provided in three equal instalments.",
            "Benefit is transferred directly to the beneficiary bank account."
        ],

        "eligibility": [
            "Applicant should belong to an eligible land-holding farmer family.",
            "The farmer family is defined as husband, wife and minor children.",
            "The applicant must satisfy the scheme's exclusion conditions.",
            "eKYC is mandatory for registered beneficiaries."
        ],

        "documents": [
            "Aadhaar card",
            "Mobile number",
            "Bank account details",
            "Land ownership / land record details"
        ],

        "official_url": "https://pmkisan.gov.in/",

        "keywords": [
            "farmer",
            "farm",
            "farming",
            "agriculture",
            "agricultural",
            "land",
            "acre",
            "acres",
            "cultivation",
            "crop",
            "cultivate",
            "kisan"
        ],

        "priority_keywords": [
            "farmer",
            "farming",
            "agriculture",
            "cultivation",
            "kisan"
        ]
    },


    # -----------------------------------------------------
    # 2. POST MATRIC SCHOLARSHIP
    # -----------------------------------------------------

    {
        "id": "post-matric-scholarship",
        "name": "Post Matric Scholarship",
        "category": "Education",
        "description": "Financial assistance for eligible students pursuing education after matriculation.",

        "benefits": [
            "Financial assistance for eligible students.",
            "Support may cover specified educational expenses depending on the particular scholarship.",
            "Scholarship applications can be submitted through the National Scholarship Portal for applicable schemes."
        ],

        "eligibility": [
            "Applicant must be studying in an eligible post-matric or higher-education course.",
            "Eligibility depends on the specific scholarship and applicant category.",
            "Family-income and academic conditions may apply depending on the scheme.",
            "The applicant must satisfy the requirements of the particular scholarship."
        ],

        "documents": [
            "Aadhaar / identity document",
            "Student ID or admission details",
            "Previous academic certificate / marksheet",
            "Income certificate where applicable",
            "Bank account details",
            "Caste/category certificate where applicable"
        ],

        "official_url": "https://scholarships.gov.in/",

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
            "b tech",
            "engineering",
            "diploma",
            "masters",
            "mtech",
            "mba"
        ],

        "priority_keywords": [
            "student",
            "scholarship",
            "college",
            "university",
            "education"
        ]
    },


    # -----------------------------------------------------
    # 3. PMEGP
    # -----------------------------------------------------

    {
        "id": "pmegp",
        "name": "PMEGP",
        "category": "Employment",
        "description": "Credit-linked assistance for eligible individuals setting up new micro-enterprises.",

        "benefits": [
            "Credit-linked financial assistance for setting up eligible new micro-enterprises.",
            "Support is provided through the PMEGP financing mechanism.",
            "Eligible beneficiaries can apply through the official PMEGP portal."
        ],

        "eligibility": [
            "Applicant should satisfy the eligibility conditions under PMEGP guidelines.",
            "The scheme is intended for eligible new micro-enterprise projects.",
            "The proposed activity must fall within permitted project categories.",
            "Applicants must satisfy applicable project and financing conditions."
        ],

        "documents": [
            "Aadhaar card",
            "Applicant photograph",
            "Project report",
            "Bank details",
            "Educational certificate where applicable",
            "Category certificate where applicable",
            "Other documents required by the PMEGP application"
        ],

        "official_url": "https://www.kviconline.gov.in/pmegpeportal/pmegphome/index.jsp",

        "keywords": [
            "business",
            "startup",
            "enterprise",
            "shop",
            "company",
            "self employed",
            "self-employed",
            "entrepreneur",
            "manufacturing",
            "business owner",
            "businessowner",
            "small business",
            "micro enterprise",
            "microenterprise"
        ],

        "priority_keywords": [
            "business",
            "startup",
            "entrepreneur",
            "enterprise",
            "self employed"
        ]
    },


    # -----------------------------------------------------
    # 4. PM SVANIDHI
    # -----------------------------------------------------

    {
        "id": "pm-svanidhi",
        "name": "PM SVANidhi",
        "category": "Street Vendors",
        "description": "Working-capital support for eligible street vendors.",

        "benefits": [
            "Working-capital loan support for eligible street vendors.",
            "The scheme is designed to help street vendors restart and strengthen their livelihoods.",
            "Additional incentives may be available under applicable scheme guidelines."
        ],

        "eligibility": [
            "Applicant should be an eligible street vendor.",
            "Eligibility is determined according to PM SVANidhi scheme guidelines.",
            "The applicant may need to provide vending-related identification or recommendation details.",
            "Loan approval is subject to applicable lender and scheme conditions."
        ],

        "documents": [
            "Aadhaar card",
            "Mobile number",
            "Street vendor identification / certificate or recommendation where applicable",
            "Bank account details",
            "Other documents requested during application"
        ],

        "official_url": "https://pmsvanidhi.mohua.gov.in/",

        "keywords": [
            "street vendor",
            "street vendors",
            "vendor",
            "vendors",
            "hawker",
            "roadside shop",
            "roadsideshop",
            "cart",
            "stall",
            "selling vegetables",
            "selling fruits",
            "street selling",
            "roadside"
        ],

        "priority_keywords": [
            "street vendor",
            "vendor",
            "hawker",
            "stall"
        ]
    },


    # -----------------------------------------------------
    # 5. AYUSHMAN BHARAT PM-JAY
    # -----------------------------------------------------

    {
        "id": "pm-jay",
        "name": "Ayushman Bharat PM-JAY",
        "category": "Healthcare",
        "description": "Health coverage support for eligible families under Ayushman Bharat PM-JAY.",

        "benefits": [
            "Health coverage of up to ₹5 lakh per family per year for eligible beneficiaries.",
            "Cashless treatment is available at empanelled hospitals.",
            "Coverage includes specified hospitalization expenses.",
            "Pre-existing conditions are covered under the scheme subject to applicable rules."
        ],

        "eligibility": [
            "Eligibility is determined according to PM-JAY beneficiary criteria.",
            "Beneficiaries can check their eligibility through the official PM-JAY system.",
            "For the senior-citizen expansion, citizens aged 70 years and above are eligible regardless of economic status, subject to the applicable enrolment requirements."
        ],

        "documents": [
            "Aadhaar / identity document",
            "Beneficiary identification details",
            "Mobile number where applicable",
            "Other documents requested during beneficiary verification"
        ],

        "official_url": "https://pmjay.gov.in/",

        "keywords": [
            "health",
            "healthcare",
            "hospital",
            "hospitalization",
            "hospitalisation",
            "medical",
            "treatment",
            "medicine",
            "surgery",
            "disease",
            "illness",
            "hospital bill",
            "hospitalbill",
            "health insurance",
            "medical treatment"
        ],

        "priority_keywords": [
            "hospital",
            "hospitalization",
            "hospitalisation",
            "treatment",
            "medical",
            "healthcare"
        ]
    },


    # -----------------------------------------------------
    # 6. SENIOR CITIZEN SOCIAL ASSISTANCE
    # -----------------------------------------------------

    {
        "id": "senior-pension",
        "name": "Senior Citizen Social Assistance",
        "category": "Social Security",
        "description": "Social assistance for eligible senior citizens under applicable government social-assistance programmes.",

        "benefits": [
            "Social assistance may be provided to eligible senior citizens.",
            "Benefits depend on the applicable social-assistance programme and State/UT implementation.",
            "The official NSAP portal provides information about applicable social-assistance programmes."
        ],

        "eligibility": [
            "Applicant must satisfy the age requirement of the applicable senior-citizen programme.",
            "Income or economic-status conditions may apply depending on the programme.",
            "Eligibility and benefit amount can vary according to applicable government rules and State/UT implementation."
        ],

        "documents": [
            "Age proof",
            "Aadhaar / identity document",
            "Bank or post-office account details",
            "Income / BPL-related proof where applicable",
            "Residence proof where applicable"
        ],

        "official_url": "https://nsap.nic.in/",

        "keywords": [
            "senior citizen",
            "senior citizens",
            "elderly",
            "old age",
            "old person",
            "retired",
            "pension",
            "aged",
            "60 years",
            "65 years",
            "70 years",
            "senior"
        ],

        "priority_keywords": [
            "senior citizen",
            "elderly",
            "old age",
            "pension"
        ]
    },


    # -----------------------------------------------------
    # 7. SUKANYA SAMRIDDHI ACCOUNT
    # -----------------------------------------------------

    {
        "id": "sukanya-samriddhi",
        "name": "Sukanya Samriddhi Account",
        "category": "Girl Child",
        "description": "Government-backed savings scheme intended for the financial future of an eligible girl child.",

        "benefits": [
            "Long-term savings for an eligible girl child.",
            "The account provides interest according to the applicable government-notified rate.",
            "The scheme supports financial planning for the girl child's future education and other eligible purposes."
        ],

        "eligibility": [
            "The account is intended for an eligible girl child.",
            "The applicable age and account-opening conditions must be satisfied.",
            "A guardian can open the account on behalf of an eligible girl child subject to scheme rules."
        ],

        "documents": [
            "Girl child's birth certificate",
            "Guardian's identity proof",
            "Guardian's address proof",
            "Aadhaar / KYC documents",
            "Account opening form"
        ],

        "official_url": "https://www.indiapost.gov.in/VAS/pages/pmodashboard/sukanyasamriddhiaccount.aspx",

        "keywords": [
            "girl child",
            "daughter",
            "girl",
            "female child",
            "baby girl",
            "daughter education",
            "daughtereducation",
            "sukanya",
            "sukanya samriddhi"
        ],

        "priority_keywords": [
            "girl child",
            "daughter",
            "female child",
            "sukanya"
        ]
    },


    # -----------------------------------------------------
    # 8. DISABILITY SUPPORT
    # -----------------------------------------------------

    {
        "id": "disability-support",
        "name": "Disability Support",
        "category": "Social Welfare",
        "description": "Government disability-support programmes for eligible persons with disabilities.",

        "benefits": [
            "Support may include assistive devices and rehabilitation-related assistance under applicable programmes.",
            "Government disability programmes also support accessibility, skill development and empowerment.",
            "Specific benefits depend on the particular disability scheme and eligibility conditions."
        ],

        "eligibility": [
            "Applicant should be a person with a qualifying disability under the applicable programme.",
            "A valid disability certificate or UDID-related documentation may be required.",
            "Additional income, age, percentage-disability or programme-specific conditions may apply."
        ],

        "documents": [
            "Disability certificate / UDID details",
            "Aadhaar / identity document",
            "Address proof",
            "Income certificate where applicable",
            "Bank details",
            "Medical or disability-related documents where required"
        ],

        "official_url": "https://depwd.gov.in/",

        "keywords": [
            "disability",
            "disabled",
            "disability certificate",
            "physically challenged",
            "visual impairment",
            "hearing impairment",
            "wheelchair",
            "special needs",
            "person with disability",
            "persons with disability",
            "pwd"
        ],

        "priority_keywords": [
            "disability",
            "disabled",
            "disability certificate"
        ]
    },


    # -----------------------------------------------------
    # 9. WOMEN SUPPORT
    # -----------------------------------------------------

    {
        "id": "women-support",
        "name": "Women Support Schemes",
        "category": "Women Welfare",
        "description": "Government support programmes available to eligible women depending on their circumstances.",

        "benefits": [
            "Benefits depend on the specific women-focused government programme.",
            "Support may include protection, empowerment, livelihood or other welfare assistance.",
            "Eligibility and benefits vary according to the individual scheme."
        ],

        "eligibility": [
            "Applicant should satisfy the conditions of the particular women-focused programme.",
            "Some programmes target women in vulnerable or difficult circumstances.",
            "Additional age, income, occupation, family or other conditions may apply depending on the scheme."
        ],

        "documents": [
            "Aadhaar / identity document",
            "Address proof",
            "Bank account details",
            "Income certificate where applicable",
            "Relevant supporting certificate depending on the programme"
        ],

        "official_url": "https://spniwcd.wcd.gov.in/",

        "keywords": [
            "woman",
            "women",
            "female",
            "widow",
            "single mother",
            "mother",
            "women entrepreneur",
            "womenentrepreneur",
            "girl",
            "female worker"
        ],

        "priority_keywords": [
            "widow",
            "single mother",
            "women entrepreneur",
            "womenentrepreneur"
        ]
    },


    # -----------------------------------------------------
    # 10. SOCIAL ASSISTANCE
    # -----------------------------------------------------

    {
        "id": "low-income-support",
        "name": "Social Assistance Schemes",
        "category": "Social Welfare",
        "description": "Potential social assistance for eligible individuals and families based on their circumstances.",

        "benefits": [
            "Social assistance may be available under applicable government programmes.",
            "The type and amount of assistance depend on the specific programme.",
            "State and Central Government programmes may have different eligibility conditions."
        ],

        "eligibility": [
            "Applicant must satisfy the conditions of the particular social-assistance programme.",
            "Low-income or economically vulnerable households may qualify for some programmes.",
            "Age, family circumstances, disability, occupation or other conditions may apply."
        ],

        "documents": [
            "Aadhaar / identity document",
            "Income certificate where applicable",
            "Residence proof",
            "Bank account details",
            "Relevant supporting certificate depending on the programme"
        ],

        "official_url": "https://nsap.nic.in/",

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
            "ews",
            "financial help",
            "money problem",
            "financial support"
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

    mobile = str(data.get("mobile", "")).strip()
    mode = data.get("mode", "login")
    name = str(data.get("name", "")).strip()

    if not re.fullmatch(r"\d{10}", mobile):
        return jsonify({
            "success": False,
            "message": "Please enter a valid 10-digit mobile number."
        }), 400

    if mode not in ("login", "signup"):
        mode = "login"

    if mode == "signup":
        if not name:
            return jsonify({
                "success": False,
                "message": "Full name is required for sign up."
            }), 400

        if mobile in users:
            return jsonify({
                "success": False,
                "message": "An account already exists with this mobile number. Please login."
            }), 409

    if mode == "login" and mobile not in users:
        return jsonify({
            "success": False,
            "message": "No account found with this mobile number. Please sign up first."
        }), 404

    otp = str(random.randint(100000, 999999))
    otp_store[mobile] = otp
    pending_auth[mobile] = {
        "mode": mode,
        "name": name
    }

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

    mobile = str(data.get("mobile", "")).strip()
    otp = str(data.get("otp", "")).strip()

    if otp_store.get(mobile) != otp:
        return jsonify({
            "success": False,
            "message": "Invalid OTP"
        }), 400

    auth = pending_auth.get(mobile, {"mode": "login", "name": ""})

    del otp_store[mobile]
    pending_auth.pop(mobile, None)

    if auth["mode"] == "signup":
        users[mobile] = {
            "name": auth["name"],
            "mobile": mobile,
            "createdAt": datetime.now().isoformat(timespec="seconds")
        }
        save_users(users)

    user = users.get(mobile)

    if not user:
        return jsonify({
            "success": False,
            "message": "Account not found. Please sign up first."
        }), 404

    return jsonify({
        "success": True,
        "message": "OTP verified successfully",
        "user": user
    })


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

# =========================================================
# USER DETAIL EXTRACTION
# =========================================================

def extract_user_details(text):
    lower = text.lower()

    details = {
        "age": None,
        "gender": None,
        "occupation": None,
        "location": None,
        "land": None,
        "landUsage": None,
        "crop": None,
        "experience": None,
        "income": None,
        "education": None,
        "requirement": None,
        "dependents": [],
        "purpose": None
    }

    # AGE
    age_match = re.search(r"\b(\d{1,3})\s*(?:-year-old|-yr-old|years old|year old|yrs old|years)\b", lower) or re.search(r"\bage\s*(?:is|of)?\s*(\d{1,3})\b", lower)
    if age_match:
        details["age"] = int(age_match.group(1))

    # GENDER
    if re.search(r"\b(female|woman|women|girl|widow)\b", lower):
        details["gender"] = "Female"
    elif re.search(r"\b(male|man|men|boy)\b", lower):
        details["gender"] = "Male"

    # LOCATION (All Indian States & UTs)
    indian_states = [
        "andhra pradesh", "arunachal pradesh", "assam", "bihar", "chhattisgarh", "goa", "gujarat",
        "haryana", "himachal pradesh", "jharkhand", "karnataka", "kerala", "madhya pradesh",
        "maharashtra", "manipur", "meghalaya", "mizoram", "nagaland", "odisha", "punjab",
        "rajasthan", "sikkim", "tamil nadu", "telangana", "tripura", "uttar pradesh",
        "uttarakhand", "west bengal", "delhi", "puducherry", "jammu and kashmir", "ladakh"
    ]
    for state in indian_states:
        if state in lower:
            details["location"] = state.title()
            break

    # LAND
    land_match = re.search(r"(\d+(?:\.\d+)?)\s*(?:acres?|acre|hectares?|hectare|cents?|bigha|guntha)", lower)
    if land_match:
        details["land"] = f"{land_match.group(1)} acres"

    # CROPS
    common_crops = ["paddy", "rice", "wheat", "cotton", "sugarcane", "maize", "pulses", "tea", "coffee", "jute", "groundnut", "mustard", "soybean", "millet", "vegetables", "fruits", "horticulture"]
    for crop in common_crops:
        if re.search(rf"\b{crop}\b", lower):
            details["crop"] = crop.capitalize()
            break

    # LAND USAGE
    if details["crop"]:
        details["landUsage"] = f"{details['crop']} farming"
    elif any(w in lower for w in ["farming", "cultivation", "agricultural land", "agriculture"]):
        details["landUsage"] = "Farming"

    # EXPERIENCE
    exp_match = re.search(r"(?:farming|working|experience)\s*(?:for|of)?\s*(\d{1,2})\s*years?", lower) or re.search(r"(\d{1,2})\s*years?\s*(?:of\s+)?(?:experience|farming|work)", lower)
    if exp_match:
        details["experience"] = f"{exp_match.group(1)} years"

    # DEPENDENTS (Extracted separately so dependent info is not assigned to user)
    dep_match = re.search(r"\bmy\s+(daughter|son|child|children|wife|husband|mother|father)\b", lower)
    if dep_match:
        dep_relation = dep_match.group(1).capitalize()
        dep_edu = None
        if "b.tech" in lower or "btech" in lower:
            dep_edu = "B.Tech"
        elif any(w in lower for w in ["college", "university", "engineering", "degree", "post matric", "graduation"]):
            dep_edu = "College"
        elif any(w in lower for w in ["school", "10th", "12th", "primary", "high school"]):
            dep_edu = "School"
        elif any(w in lower for w in ["studying", "student"]):
            dep_edu = "Student / In Studies"

        details["dependents"].append({
            "relation": dep_relation,
            "educationStatus": dep_edu or "In Education",
            "activity": f"Studying {dep_edu}" if dep_edu else "Student"
        })

    # USER OCCUPATION
    if any(w in lower for w in ["i am a farmer", "i am farmer", "male farmer", "female farmer", "farmer from", "work as a farmer"]):
        details["occupation"] = "Farmer"
    elif "street vendor" in lower or "vendor" in lower or "hawker" in lower:
        details["occupation"] = "Street Vendor"
    elif "entrepreneur" in lower or "business" in lower or "shop" in lower:
        details["occupation"] = "Entrepreneur"
    elif any(w in lower for w in ["i am a student", "i am student", "studying btech", "studying engineering", "college student", "school student"]) and not dep_match:
        details["occupation"] = "Student"
    elif "unemployed" in lower or "job seeker" in lower:
        details["occupation"] = "Job Seeker"
    elif any(w in lower for w in ["farmer", "farming", "agriculture"]):
        details["occupation"] = "Farmer"

    # USER EDUCATION
    edu_match = re.search(r"\b(10th(?:\s+standard|\s+class|\s+pass)?|12th(?:\s+standard|\s+class|\s+pass)?|ssc|hsc|matriculation|intermediate|btech|b\.tech|degree|graduation|post graduation|masters|mba|mtech|diploma|phd|illiterate)\b", lower)
    if edu_match:
        dep_clause = False
        if dep_match:
            if not any(phrase in lower for phrase in ["i have completed", "i completed", "my education", "i studied", "i passed", "my qualification", "completed my", "passed my", "studied up to"]):
                dep_clause = True

        if not dep_clause:
            raw_edu = edu_match.group(1)
            if "10th" in raw_edu:
                details["education"] = "10th Standard"
            elif "12th" in raw_edu:
                details["education"] = "12th Standard"
            elif raw_edu in ["ssc", "hsc", "btech", "mtech", "mba", "phd"]:
                details["education"] = raw_edu.upper()
            else:
                details["education"] = raw_edu.title()
    elif any(w in lower for w in ["graduate", "graduation"]) and not dep_match:
        details["education"] = "Graduation"

    # INCOME
    income_match = re.search(r"(?:annual\s+income|annual\s+family\s+income|family\s+income|monthly\s+income|income|salary|earn|earning)[^0-9₹]{0,30}(?:₹|rs\.?|inr)?\s*(\d+(?:\.\d+)?)\s*(lakh|lakhs|l|crore|thousand|k)?(?:\s*(?:per year|annually|annual|per month|monthly|\/year|\/month))?", lower) or re.search(r"(?:₹|rs\.?|inr)\s*(\d+(?:\.\d+)?)\s*(lakh|lakhs|l|crore|thousand|k)?", lower)
    if income_match:
        num = income_match.group(1)
        unit = (income_match.group(2) or "").strip()
        is_annual = any(w in lower for w in ["annual", "annually", "per year", "/year", "year", "family"]) or "lakh" in unit or "cr" in unit
        details["income"] = f"₹{num} {unit}{'/year' if is_annual else '/month'}".strip()

    # REQUIREMENT / PURPOSE
    req_match = re.search(r"(?:need|seeking|require|look for)\s+([^.!?]+)", lower)
    if req_match:
        req_text = req_match.group(1).strip()
        details["requirement"] = req_text.capitalize()
    elif "financial support" in lower or "financial assistance" in lower:
        details["requirement"] = "Financial support for farming" if details["occupation"] == "Farmer" else "Financial assistance"

    purpose_keywords = {
        "Agriculture": ["farming", "agriculture", "crop", "cultivation", "farmer", "land", "paddy"],
        "Education": ["education", "college fees", "school fees", "tuition", "scholarship", "studying"],
        "Healthcare": ["health", "hospital", "medical", "treatment", "medicine"],
        "Business": ["business", "startup", "shop", "enterprise", "micro enterprise"],
        "Employment": ["job", "employment", "unemployed", "work"],
        "Financial Assistance": ["financial assistance", "financial help", "money", "financial support", "low income", "pension"]
    }
    for purpose, kws in purpose_keywords.items():
        if any(kw in lower for kw in kws):
            details["purpose"] = purpose
            break

    return details


# =========================================================
# OVERALL UNDERSTANDING SUMMARY BUILDER
# =========================================================

def build_overall_understanding(user_details):
    parts = ["The system identified the user"]
    age = user_details.get("age")
    gender = (user_details.get("gender") or "").lower()
    occ = (user_details.get("occupation") or "").lower()
    loc = user_details.get("location")
    land = user_details.get("land")
    land_usage = (user_details.get("landUsage") or "").lower()
    crop = user_details.get("crop")
    income = user_details.get("income")
    edu = user_details.get("education")
    exp = user_details.get("experience")
    req = user_details.get("requirement")
    deps = user_details.get("dependents") or []

    desc = []
    if age:
        desc.append(f"{age}-year-old")
    if gender and gender in ["male", "female"]:
        desc.append(gender)
    if occ:
        desc.append(occ)
    elif not desc:
        desc.append("as a citizen")

    if desc:
        parts.append("as a " + " ".join(desc))

    if loc:
        parts.append(f"from {loc}")

    if land:
        use_str = f" and uses it for {land_usage}" if land_usage else ""
        parts.append(f"who owns {land} of agricultural land{use_str}")

    main_stmt = " ".join(parts) + "."

    extra_parts = []
    if income:
        extra_parts.append(f"The reported annual income is {income}")
    if edu:
        extra_parts.append(f"with {edu} education")
    if exp:
        extra_parts.append(f"with {exp} of farming experience")

    if extra_parts:
        main_stmt += " " + ", ".join(extra_parts) + "."

    if req:
        main_stmt += f" The stated requirement is {req.lower()}."

    if deps:
        for d in deps:
            rel = d.get("relation", "dependent")
            act = d.get("activity") or d.get("educationStatus") or "in education"
            main_stmt += f" The system also identified a dependent {rel.lower()} who is {act.lower()}."

    return main_stmt


# =========================================================
# NLP PIPELINE
# =========================================================

MORPH_SUFFIX_RULES = [
    ("ies", "y"),
    ("ing", ""),
    ("ed", ""),
    ("es", ""),
    ("s", ""),
]

def get_word_pos(word, root, rule):
    w = word.lower()
    if w.endswith("ing"):
        return "Verb" if "farm" in root or "grow" in root or "study" in root else "Verb / Participle"
    if w.endswith("ed") or "past" in rule.lower():
        return "Past form"
    if w.endswith("s") and not w.endswith("ss") and root != w:
        return "Plural noun"
    if w in {"farmer", "daughter", "son", "wife", "husband", "mother", "father", "land", "crop", "paddy", "rice", "wheat", "income", "college", "school", "standard", "student", "vendor", "entrepreneur", "business", "acre", "acres", "year", "years", "degree", "education", "tenth", "experience", "support"}:
        return "Noun"
    if w in {"agricultural", "annual", "monthly", "male", "female", "old", "poor", "disabled", "financial"}:
        return "Adjective"
    if w in {"own", "owns", "owned", "use", "uses", "used", "grow", "grows", "growing", "study", "studies", "studying", "complete", "completed", "earn", "earns", "earning", "work", "works", "need", "improve"}:
        return "Verb"
    if w.isdigit():
        return "Number"
    return "Noun / Keyword"


def morphological_analyze(text):
    words = re.findall(r"[A-Za-z0-9]+(?:'[A-Za-z]+)?", text.lower())
    rows = []
    normalized_words = []
    keywords_identified = []

    irregular = {
        "children": "child",
        "people": "person",
        "men": "man",
        "women": "woman",
        "studies": "study",
        "better": "good",
        "farmer": "farm",
        "farming": "farm",
        "growing": "grow",
        "grows": "grow",
        "studying": "study",
        "completed": "complete",
        "acres": "acre",
        "agricultural": "agriculture",
        "owned": "own",
        "owns": "own",
        "earning": "earn",
        "earnings": "earn",
    }

    stop_words = {"i", "am", "a", "the", "is", "my", "with", "of", "in", "to", "and", "for", "from", "around", "it", "an", "at", "by", "on", "have", "been"}

    for word in words:
        root = irregular.get(word, word)
        rule_used = "unchanged"

        if word in irregular:
            rule_used = f"irregular: {word} → {root}"
        else:
            for suffix, replacement in MORPH_SUFFIX_RULES:
                if len(word) > len(suffix) + 2 and word.endswith(suffix):
                    candidate = word[:-len(suffix)] + replacement
                    if candidate:
                        root = candidate
                        rule_used = f"{suffix} → {replacement or '∅'}"
                        break

        if word in {"acres", "years", "fees", "needs"}:
            root = {"acres": "acre", "years": "year", "fees": "fee", "needs": "need"}[word]
            rule_used = "plural normalization"

        pos = get_word_pos(word, root, rule_used)

        token_info = {
            "word": word,
            "pos": pos,
            "root": root,
            "rule": rule_used,
            "isContent": word not in stop_words and not (word.isdigit() and len(word) > 3)
        }
        rows.append(token_info)

        if root not in normalized_words and word not in stop_words:
            normalized_words.append(root)
            if word in {"farmer", "farming", "farm", "grow", "growing", "paddy", "rice", "wheat", "acre", "acres", "land", "agricultural", "agriculture", "study", "studying", "btech", "college", "school", "education", "income", "earning", "daughter", "son", "student", "vendor", "business", "pension", "hospital", "health", "experience", "financial", "support"}:
                if root not in keywords_identified:
                    keywords_identified.append(root)

    key_summary = ", ".join(keywords_identified[:5]) if keywords_identified else "relevant terms"
    representative_result = (
        f"The system identified and normalized important terms ({key_summary}) from the user's input for further analysis."
    )

    return {
        "input": text,
        "tokens": rows,
        "normalizedWords": normalized_words,
        "keywordsIdentified": keywords_identified if keywords_identified else normalized_words[:6],
        "representativeResult": representative_result
    }


def dependency_analyze(text, morphology, user_details=None):
    u = user_details or {}
    sentences = [part.strip() for part in re.split(r"(?<!\d)\.(?!\d)|[!?]+", text) if part.strip()]
    relations = []

    # Extract clean relations directly matching user attributes
    if u.get("age"):
        relations.append({"entity": "User", "relationship": "age", "information": f"{u['age']} years", "display": f"User → age → {u['age']} years"})
    if u.get("gender"):
        relations.append({"entity": "User", "relationship": "gender", "information": u['gender'], "display": f"User → gender → {u['gender']}"})
    if u.get("occupation"):
        relations.append({"entity": "User", "relationship": "occupation", "information": u['occupation'], "display": f"User → occupation → {u['occupation']}"})
    if u.get("location"):
        relations.append({"entity": "User", "relationship": "location", "information": u['location'], "display": f"User → location → {u['location']}"})
    if u.get("land"):
        relations.append({"entity": "User", "relationship": "owns", "information": u['land'], "display": f"User → owns → {u['land']}"})
    if u.get("crop"):
        relations.append({"entity": "User", "relationship": "crop", "information": u['crop'], "display": f"User → crop → {u['crop']}"})
    if u.get("landUsage"):
        relations.append({"entity": "User", "relationship": "land usage", "information": u['landUsage'], "display": f"User → land usage → {u['landUsage']}"})
    if u.get("income"):
        relations.append({"entity": "User", "relationship": "annual income", "information": u['income'], "display": f"User → annual income → {u['income']}"})
    if u.get("education"):
        relations.append({"entity": "User", "relationship": "education", "information": u['education'], "display": f"User → education → {u['education']}"})
    if u.get("experience"):
        relations.append({"entity": "User", "relationship": "farming experience", "information": u['experience'], "display": f"User → farming experience → {u['experience']}"})
    if u.get("requirement"):
        relations.append({"entity": "User", "relationship": "requirement", "information": u['requirement'], "display": f"User → requirement → {u['requirement']}"})

    for dep in u.get("dependents", []):
        dep_name = dep.get("relation", "Dependent")
        dep_act = dep.get("educationStatus") or dep.get("activity") or "Student"
        relations.append({"entity": "User", "relationship": "has dependent", "information": dep_name, "display": f"User → has dependent → {dep_name}"})
        relations.append({"entity": dep_name, "relationship": "studying", "information": dep_act, "display": f"{dep_name} → studying → {dep_act}"})

    # Build structured Dependency Tree object
    user_branches = []
    dep_branches = []

    if u.get("age"):
        user_branches.append({"label": "AGE", "value": str(u['age'])})
    if u.get("gender"):
        user_branches.append({"label": "GENDER", "value": u['gender'].upper()})
    if u.get("occupation"):
        user_branches.append({"label": "OCCUPATION", "value": u['occupation'].upper()})
    if u.get("location"):
        user_branches.append({"label": "LOCATION", "value": u['location'].upper()})
    if u.get("land"):
        owns_sub = u.get("crop") or (u.get("landUsage") if "farming" not in (u.get("landUsage") or "").lower() else None)
        user_branches.append({
            "label": "OWNS",
            "value": u['land'].upper(),
            "sub": owns_sub.upper() if owns_sub else None
        })
    if u.get("income"):
        user_branches.append({"label": "INCOME", "value": u['income']})
    if u.get("education"):
        user_branches.append({"label": "EDUCATION", "value": u['education'].upper()})
    if u.get("experience"):
        user_branches.append({"label": "EXPERIENCE", "value": u['experience'].upper()})
    if u.get("requirement"):
        user_branches.append({"label": "REQUIREMENT", "value": u['requirement']})

    for dep in u.get("dependents", []):
        dep_branches.append({
            "relation": dep.get("relation", "DEPENDENT").upper(),
            "action": "STUDYING",
            "detail": (dep.get("educationStatus") or dep.get("activity") or "STUDENT").upper()
        })

    # Dynamic representative result
    dep_found = u.get("dependents", [])
    user_occ = (u.get("occupation") or "individual").lower()

    if dep_found:
        dep_rel = dep_found[0].get("relation", "dependent").lower()
        dep_act = (dep_found[0].get("educationStatus") or dep_found[0].get("activity") or "college").lower()
        rep_result = (
            f"The system correctly identified the user as the {user_occ} and land owner while associating the "
            f"{dep_act} education information with the user's {dep_rel}."
        )
    elif u.get("crop") or u.get("requirement"):
        crop_text = f"{u['crop'].lower()} cultivation" if u.get("crop") else "farming operations"
        req_text = f" and {u['requirement'].lower()}" if u.get("requirement") else ""
        rep_result = (
            f"The system correctly identified the user as the {user_occ} and land owner while associating the "
            f"{crop_text}{req_text} with the user's profile."
        )
    else:
        rep_result = f"The system correctly identified the user as the primary entity and structured their attributes."

    return {
        "sentences": sentences,
        "relations": relations,
        "treeData": {
            "root": "USER",
            "userBranches": user_branches,
            "dependents": dep_branches
        },
        "representativeResult": rep_result
    }


def semantic_analyze(text, dependency, user_details=None):
    u = user_details or {}
    predicates = []

    if u.get("occupation"):
        predicates.append(f"occupation(user, {u['occupation'].lower()})")
    if u.get("location"):
        loc_clean = u['location'].replace(" ", "_")
        predicates.append(f"location(user, {loc_clean})")
    if u.get("land"):
        land_clean = u['land'].lower().replace(" ", "_")
        predicates.append(f"land_area(user, {land_clean})")
    if u.get("crop"):
        predicates.append(f"crop(user, {u['crop'].lower()})")
    if u.get("landUsage"):
        predicates.append(f"land_use(user, {u['landUsage'].lower().replace(' ', '_')})")
    if u.get("income"):
        inc_clean = re.sub(r"[^0-9a-zA-Z]", "_", u['income']).strip("_").lower()
        predicates.append(f"income(user, {inc_clean})")
    if u.get("education"):
        edu_clean = u['education'].lower().replace(" ", "_")
        predicates.append(f"education(user, {edu_clean})")
    if u.get("experience"):
        exp_clean = u['experience'].lower().replace(" ", "_")
        predicates.append(f"experience(user, {exp_clean})")
    if u.get("requirement"):
        req_clean = re.sub(r"[^0-9a-zA-Z]", "_", u['requirement'][:30]).strip("_").lower()
        predicates.append(f"requirement(user, {req_clean})")

    for dep in u.get("dependents", []):
        rel = dep.get("relation", "dependent").lower()
        predicates.append(f"dependent(user, {rel})")
        if dep.get("educationStatus"):
            edu_s = dep['educationStatus'].lower().replace(" ", "_")
            predicates.append(f"education({rel}, {edu_s})")

    predicates = list(dict.fromkeys(predicates))

    # Build Semantic Profile Table Items (only present fields)
    profile_items = []
    if u.get("age"):
        profile_items.append({"category": "Age", "meaning": f"{u['age']} years"})
    if u.get("gender"):
        profile_items.append({"category": "Gender", "meaning": u['gender']})
    if u.get("occupation"):
        profile_items.append({"category": "Occupation", "meaning": u['occupation']})
    if u.get("location"):
        profile_items.append({"category": "Location", "meaning": u['location']})
    if u.get("land"):
        profile_items.append({"category": "Land", "meaning": u['land']})
    if u.get("crop"):
        profile_items.append({"category": "Crop", "meaning": u['crop']})
    elif u.get("landUsage"):
        profile_items.append({"category": "Land Usage", "meaning": u['landUsage']})
    if u.get("income"):
        profile_items.append({"category": "Annual Income", "meaning": u['income']})
    if u.get("education"):
        profile_items.append({"category": "Education", "meaning": u['education']})
    if u.get("experience"):
        profile_items.append({"category": "Farming Experience", "meaning": u['experience']})
    if u.get("requirement"):
        profile_items.append({"category": "Requirement", "meaning": u['requirement']})
    for dep in u.get("dependents", []):
        profile_items.append({"category": "Dependent", "meaning": dep.get("relation", "Dependent")})
        if dep.get("educationStatus"):
            profile_items.append({"category": f"{dep.get('relation', 'Dependent')}'s Education", "meaning": dep.get("educationStatus")})

    # Word Sense Disambiguation
    normalized = normalize_text(text)
    wsd = []
    if "farmer" in normalized or "farming" in normalized or "agricultural" in normalized:
        wsd.append({"term": "farming", "sense": "agricultural cultivation and land operations", "evidence": "land and farmer context"})
    if "paddy" in normalized or "rice" in normalized:
        wsd.append({"term": "paddy", "sense": "kharif/rabi staple cereal crop cultivation", "evidence": "crop context"})
    if "acre" in normalized or "acres" in normalized:
        wsd.append({"term": "acres", "sense": "unit of cultivable agricultural land ownership", "evidence": "property measurement context"})
    if "college" in normalized or "studying" in normalized or "btech" in normalized:
        wsd.append({"term": "college", "sense": "higher education institution / degree study", "evidence": "education & dependent context"})

    representative_result = "The extracted information has been converted into structured semantic attributes for scheme matching."

    return {
        "profileTable": profile_items,
        "predicates": predicates,
        "wordSenseDisambiguation": wsd,
        "structuredFacts": dependency.get("relations", []),
        "representativeResult": representative_result
    }


def discourse_analyze(text, dependency, semantic, user_details=None, matches=None):
    references = []
    lower = text.lower()
    u = user_details or {}

    # Reference resolution: "it" -> "agricultural land"
    if re.search(r"\bit\b", lower) or "on my land" in lower or "on the land" in lower or u.get("land"):
        if u.get("land") or "land" in lower or "acres" in lower:
            resolved_meaning = "Agricultural land"
            crop_or_use = u.get("crop") or u.get("landUsage") or "farming"
            references.append({
                "expression": "It",
                "resolvedEntity": resolved_meaning,
                "antecedent": f"{u.get('land') or 'agricultural land'}",
                "clause": f"Used for {crop_or_use.lower()}"
            })

    dep_found = None
    for dep in u.get("dependents", []):
        dep_found = dep.get("relation")
        break

    if dep_found:
        if dep_found.lower() in ["daughter", "wife", "mother", "sister"]:
            for pronoun in ["she", "her"]:
                if re.search(rf"\b{pronoun}\b", lower):
                    references.append({
                        "expression": pronoun.capitalize(),
                        "resolvedEntity": dep_found,
                        "antecedent": f"My {dep_found.lower()}",
                        "clause": f"Refers to user's {dep_found.lower()}"
                    })
        elif dep_found.lower() in ["son", "husband", "father", "brother"]:
            for pronoun in ["he", "him", "his"]:
                if re.search(rf"\b{pronoun}\b", lower):
                    references.append({
                        "expression": pronoun.capitalize(),
                        "resolvedEntity": dep_found,
                        "antecedent": f"My {dep_found.lower()}",
                        "clause": f"Refers to user's {dep_found.lower()}"
                    })

    # Simple Flow / Block Diagram steps
    resolution_flow = []
    if references and references[0]["expression"] == "It":
        crop_act = f"{u['crop']} Farming" if u.get("crop") else (u.get("landUsage") or "Farming")
        resolution_flow = [
            {"step": "Expression", "text": '"It"'},
            {"step": "Entity", "text": "Agricultural Land"},
            {"step": "Attribute", "text": "Land Usage"},
            {"step": "Activity", "text": crop_act}
        ]
    elif references:
        ref = references[0]
        resolution_flow = [
            {"step": "Expression", "text": f'"{ref["expression"]}"'},
            {"step": "Entity", "text": ref["resolvedEntity"]},
            {"step": "Context", "text": ref["clause"]}
        ]

    # Dynamic explanation generation
    explanation_parts = []
    user_occ = (u.get("occupation") or "citizen").lower()
    user_loc = u.get("location")
    user_land = u.get("land")
    user_crop = u.get("crop")

    if user_occ == "farmer":
        loc_str = f" from {user_loc}" if user_loc else ""
        land_str = f", owns {user_land} of agricultural land" if user_land else ""
        crop_str = f", and cultivates {user_crop.lower()}" if user_crop else ""
        explanation_parts.append(
            f"Based on the information provided, agriculture and crop assistance welfare schemes may be relevant because the user is a farmer{loc_str}{land_str}{crop_str}."
        )
    elif user_occ == "student":
        explanation_parts.append(
            "Based on the information provided, education and scholarship schemes may be relevant to support tuition fees and academic development."
        )
    elif user_occ == "street vendor":
        explanation_parts.append(
            "Based on the information provided, micro-credit and working capital welfare schemes such as PM SVANidhi may be relevant."
        )
    else:
        explanation_parts.append(
            "Based on the provided information, multiple central and state welfare programmes match the specified profile attributes."
        )

    if dep_found:
        explanation_parts.append(
            f"Additional education-related schemes may be relevant for the user's {dep_found.lower()}."
        )

    explanation_parts.append(
        "Final eligibility should be verified using the official scheme requirements on the respective government portal."
    )

    explanation = " ".join(explanation_parts)

    if references and references[0]["expression"] == "It":
        crop_term = f"{u['crop'].lower()} farming" if u.get("crop") else "farming operations"
        rep_result = f"The system resolved 'It' as the agricultural land mentioned previously and identified its usage as {crop_term}."
    elif references:
        rep_result = f"The system resolved '{references[0]['expression']}' as {references[0]['resolvedEntity']}."
    else:
        rep_result = "No ambiguous references requiring resolution were identified in the provided text."

    return {
        "references": references,
        "resolutionFlow": resolution_flow,
        "resolvedFacts": semantic.get("structuredFacts", []),
        "surfaceRealization": explanation,
        "representativeResult": rep_result
    }


def run_nlp_pipeline(text, user_details=None, matches=None):
    user_details = user_details or extract_user_details(text)
    morphology = morphological_analyze(text)
    dependency = dependency_analyze(text, morphology, user_details)
    semantic = semantic_analyze(text, dependency, user_details)
    discourse = discourse_analyze(text, dependency, semantic, user_details, matches)
    overall_understanding = build_overall_understanding(user_details)

    m1_dict = {
        **morphology,
        "word_normalization_table": morphology.get("tokens", []),
        "identified_concepts": morphology.get("keywordsIdentified", [])
    }
    m2_dict = {
        **dependency,
        "relationships": dependency.get("relations", []),
        "relationship_table": dependency.get("relations", []),
        "dependency_tree_branches": dependency.get("treeData", {}).get("userBranches", []),
        "dependency_tree_dependents": dependency.get("treeData", {}).get("dependents", [])
    }
    m3_dict = {
        **semantic,
        "semantic_attribute_table": semantic.get("profileTable", []),
        "predicate_calculus": semantic.get("predicates", [])
    }
    m4_dict = {
        **discourse,
        "reference_resolution_table": discourse.get("references", []),
        "discourse_flow_steps": discourse.get("resolutionFlow", []),
        "generated_explanation": discourse.get("surfaceRealization", "")
    }

    return {
        "wordAnalysis": morphology,
        "sentenceUnderstanding": dependency,
        "meaningExtraction": semantic,
        "contextUnderstanding": discourse,
        "overallUnderstanding": overall_understanding,
        "module_1_morphology": m1_dict,
        "module_2_syntax": m2_dict,
        "module_3_semantics": m3_dict,
        "module_4_discourse": m4_dict,
        "finalUnderstanding": {
            "normalizedWords": morphology.get("normalizedWords", []),
            "predicates": semantic.get("predicates", []),
            "resolvedReferences": discourse.get("references", []),
            "explanation": discourse.get("surfaceRealization", "")
        }
    }

# =========================================================
# CALCULATE SCHEME MATCH
# =========================================================

def calculate_match(text, scheme):

    score = 0

    matched_keywords = []

    normalized_text = normalize_text(text)


    # -----------------------------------------------------
    # PRIORITY KEYWORDS
    # -----------------------------------------------------

    for keyword in scheme["priority_keywords"]:

        keyword_normalized = normalize_text(keyword)

        if re.search(rf"\b{re.escape(keyword_normalized)}\b", normalized_text):

            score += 30

            matched_keywords.append(keyword)


    # -----------------------------------------------------
    # NORMAL KEYWORDS
    # -----------------------------------------------------

    for keyword in scheme["keywords"]:

        keyword_normalized = normalize_text(keyword)

        if re.search(rf"\b{re.escape(keyword_normalized)}\b", normalized_text):

            if keyword not in matched_keywords:

                score += 10

                matched_keywords.append(keyword)


    score = min(score, 100)

    return score, matched_keywords


# =========================================================
# BUILD SCHEME RESPONSE
# =========================================================

def build_scheme_response(scheme, score, matched_keywords):

    return {

        "id": scheme["id"],

        "name": scheme["name"],

        "category": scheme["category"],

        "description": scheme["description"],

        "matchScore": score,

        "matchedKeywords": matched_keywords,

        # Dynamic scheme information
        "benefits": scheme["benefits"],

        "eligibility": scheme["eligibility"],

        "documents": scheme["documents"],

        "official_url": scheme.get("official_url", ""),

        "officialUrl": scheme.get("official_url", ""),

        "officialWebsite": scheme.get("official_url", ""),

        "url": scheme.get("official_url", "")

    }


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

            results.append(
                build_scheme_response(
                    scheme,
                    score,
                    keywords
                )
            )


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
    # Run the complete NLP pipeline with extracted context
    # -----------------------------------------------------

    nlp_pipeline = run_nlp_pipeline(
        situation,
        user_details,
        results
    )


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
        "user_text": situation,
        "userDetails": user_details,
        "user_profile": user_details,
        "extracted_info": user_details,
        "dependents": user_details.get("dependents", []),
        "nlpPipeline": nlp_pipeline,
        "nlp_pipeline": nlp_pipeline,
        "matches": results,
        "recommendations": results
    })


# =========================================================
# NLP MATCH HELPER
# =========================================================

def get_matches_for_situation(situation):
    results = []

    for scheme in schemes:
        score, keywords = calculate_match(
            situation,
            scheme
        )

        if score > 0:
            results.append(
                build_scheme_response(
                    scheme,
                    score,
                    keywords
                )
            )

    results.sort(
        key=lambda item: item["matchScore"],
        reverse=True
    )

    return [
        result
        for result in results
        if result["matchScore"] >= 10
    ]


# =========================================================
# REAL-TIME AI CHATBOT - LOCAL OLLAMA STREAMING
# =========================================================

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2:3b")

CHATBOT_SYSTEM_PROMPT = (
    "You are SchemeMatch AI, a knowledgeable assistant for Indian government schemes. "
    "Provide clear, concise, and direct answers about Indian schemes, eligibility rules, "
    "benefits, required documents, and application processes. "
    "Keep responses brief, structured, and easy to understand."
)

def _clean_chat_history(history):
    cleaned = []
    if not isinstance(history, list):
        return cleaned
    for item in history[-6:]:
        if not isinstance(item, dict):
            continue
        role = str(item.get("role", "")).strip().lower()
        content = item.get("content", item.get("message", item.get("text", "")))
        if role not in {"user", "assistant"}:
            continue
        content = str(content).strip()
        if content:
            cleaned.append({"role": role, "content": content[:600]})
    return cleaned

@app.route("/chat", methods=["POST"])
@app.route("/chatbot", methods=["POST"])
def chatbot():
    data = request.get_json() or {}
    message = str(data.get("message", data.get("question", ""))).strip()

    if not message:
        return jsonify({"success": False, "message": "Please enter a message."}), 400

    req_lang = str(data.get("language", "en")).strip().lower()
    lang_map = {
        "en": "English", "hi": "Hindi", "ta": "Tamil",
        "te": "Telugu", "kn": "Kannada", "ml": "Malayalam", "mr": "Marathi"
    }
    lang_name = lang_map.get(req_lang, req_lang.capitalize() if req_lang else "English")

    history = _clean_chat_history(data.get("history", data.get("messages", [])))

    lower_msg = message.lower().strip()
    is_greeting = lower_msg in {"hello", "hi", "hey", "namaste", "good morning", "good evening", "good afternoon", "help", "வணக்கம்", "नमस्ते", "నమస్కారం", "ನಮಸ್ಕಾರ"}

    context = ""
    if not is_greeting and len(message.split()) > 2:
        matches = get_matches_for_situation(message)
        if matches:
            top_schemes = [f"- {m['name']} ({m['category']}): {m['description']}" for m in matches[:2]]
            context = "Relevant SchemeMatch database info:\n" + "\n".join(top_schemes) + "\n\n"

    formatted_history = ""
    for item in history[-4:]:
        speaker = "User" if item["role"] == "user" else "Assistant"
        formatted_history += f"{speaker}: {item['content']}\n"

    system_prompt = CHATBOT_SYSTEM_PROMPT
    if lang_name != "English":
        system_prompt += f" You MUST respond completely in {lang_name}."

    lang_instruction = ""
    if lang_name != "English":
        lang_instruction = f" (Respond in {lang_name})"

    if formatted_history:
        full_prompt = f"{formatted_history}{context}User: {message}{lang_instruction}\nAssistant:"
    elif context:
        full_prompt = f"{context}User: {message}{lang_instruction}\nAssistant:"
    else:
        full_prompt = f"User: {message}{lang_instruction}\nAssistant:" if lang_name != "English" else message

    ollama_payload = {
        "model": OLLAMA_MODEL,
        "system": system_prompt,
        "prompt": full_prompt,
        "stream": True,
        "options": {
            "temperature": 0.3,
            "num_predict": 250
        }
    }

    def generate_stream():
        import requests
        try:
            resp = requests.post(
                f"{OLLAMA_URL}/api/generate",
                json=ollama_payload,
                stream=True,
                timeout=(5, 60)
            )
            if resp.status_code != 200:
                yield "AI Assistant is currently unavailable. Please make sure Ollama is running."
                return

            for line in resp.iter_lines():
                if line:
                    try:
                        chunk = json.loads(line.decode("utf-8"))
                        text_chunk = chunk.get("response", "")
                        if text_chunk:
                            yield text_chunk
                        if chunk.get("done", False):
                            break
                    except (json.JSONDecodeError, UnicodeDecodeError):
                        continue
        except requests.exceptions.ConnectionError:
            yield "AI Assistant is currently unavailable. Please make sure Ollama is running."
        except requests.exceptions.Timeout:
            yield "AI Assistant timed out waiting for Ollama. Please try again."
        except Exception:
            yield "AI Assistant is currently unavailable. Please make sure Ollama is running."

    return Response(stream_with_context(generate_stream()), mimetype="text/plain")


# =========================================================
# NLP SITUATION REPORT GENERATION
# =========================================================

@app.route("/generate-report", methods=["POST"])
def generate_report():
    data = request.get_json() or {}

    situation = str(
        data.get("situation", "")
    ).strip()

    if not situation:
        return jsonify({
            "success": False,
            "message": "Please provide a situation before generating a report."
        }), 400

    user_details = extract_user_details(situation)
    matches = get_matches_for_situation(situation)
    nlp_pipeline = run_nlp_pipeline(situation, user_details, matches)

    normalized = normalize_text(situation)
    detected_keywords = []

    for scheme in schemes:
        for keyword in scheme["keywords"]:
            normalized_keyword = normalize_text(keyword)

            if re.search(rf"\b{re.escape(normalized_keyword)}\b", normalized):
                if keyword not in detected_keywords:
                    detected_keywords.append(keyword)

    if matches:
        recommendation = (
            f"The strongest potential match is "
            f"{matches[0]['name']} with a "
            f"{matches[0]['matchScore']}% keyword-based match. "
            "The user should verify detailed eligibility and documents "
            "on the official scheme website before applying."
        )
    else:
        recommendation = (
            "No strong scheme match was detected from the provided "
            "information. More details such as age, income, occupation, "
            "education or specific need may improve the analysis."
        )

    report = {
        "generatedAt": datetime.now().strftime(
            "%d-%m-%Y %H:%M:%S"
        ),
        "situation": situation,
        "originalText": situation,
        "input": situation,
        "userDetails": user_details,
        "nlpPipeline": nlp_pipeline,
        "detectedKeywords": detected_keywords[:20],
        "matches": matches,
        "recommendation": recommendation,
        "finalExplanation": nlp_pipeline["finalUnderstanding"]["explanation"]
    }

    return jsonify({
        "success": True,
        "report": report,
        "situation": situation,
        "originalText": situation,
        "input": situation,
        "userDetails": user_details,
        "nlpPipeline": nlp_pipeline,
        "matches": matches,
        "finalExplanation": nlp_pipeline["finalUnderstanding"]["explanation"]
    })


# =========================================================
# RUN SERVER
# =========================================================

if __name__ == "__main__":

    app.run(
        debug=True,
        port=5000
    )