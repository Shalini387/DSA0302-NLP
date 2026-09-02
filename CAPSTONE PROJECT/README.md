# SchemeMatch — Eligibility Extraction & Matching Engine for Unclaimed Government Schemes

SchemeMatch is an NLP-based web application designed to help citizens discover government schemes that may be relevant to their personal circumstances.

Instead of requiring users to search through many schemes manually, SchemeMatch accepts eligibility information in natural language, extracts important eligibility attributes, processes the input through four NLP modules, and compares the resulting profile with government scheme eligibility criteria.

> **Note:** SchemeMatch is a recommendation and information-support system. A recommendation does not represent official government approval or final eligibility.

---

## 🎯 Objectives

- Accept eligibility information in natural language.
- Extract important eligibility attributes from free-text descriptions.
- Normalize different word forms using morphological analysis.
- Identify grammatical relationships using CFG/dependency analysis.
- Interpret eligibility terms using semantic analysis and Word Sense Disambiguation (WSD).
- Resolve references between sentences.
- Convert natural-language information into structured eligibility attributes.
- Compare user attributes with government scheme eligibility criteria.
- Rank and display relevant schemes.
- Provide understandable explanations for recommendations.
- Present the NLP processing through a dedicated NLP analysis report.

---

## ✨ Key Features

- Natural-language eligibility input
- Four-module NLP processing pipeline
- Eligibility attribute extraction
- Government scheme matching
- Explainable recommendations
- NLP analysis report
- Scheme Directory
- Interactive dashboard
- Voice input where supported by the browser
- Multilingual interface
- AI Assistant using local Ollama support

---

## 🧠 Four NLP Modules

| Module | Technique | Purpose |
|---|---|---|
| Module 1 | Finite-State Morphological Analysis | Normalizes word forms and identifies common roots |
| Module 2 | CFG / Dependency Analysis | Identifies sentence structure and relationships |
| Module 3 | Semantic Analysis & WSD | Interprets meaning and disambiguates terms using context |
| Module 4 | Reference Resolution & Language Generation | Resolves references and generates understandable explanations |

### Module 1 — Morphological Analysis

Different forms of relevant words are normalized so that variations can be matched more reliably.

Example:

```text
farmer  → farm
farming → farm
acres   → acre

Module 2 — CFG / Dependency Analysis

This module analyzes the grammatical structure of the user's input and identifies relationships between words, entities, and attributes.

It helps the system understand who has which eligibility attribute instead of simply matching keywords.

Example:

"My daughter is studying in college."

The system should understand:

Relationship → Daughter
Education    → College

The education information belongs to the daughter, not directly to the user.

The module also supports dependency and relationship visualization in the NLP Analysis Report.

Module 3 — Semantic Analysis & WSD

This module interprets the meaning of extracted information based on its context.

It converts relevant information into structured semantic representations that can be used by the scheme matching engine.

Example:

occupation(user, farmer)
location(user, Tamil Nadu)
income(user, 1.8 lakh)
crop(agricultural_land, paddy)

Word Sense Disambiguation (WSD) helps identify the intended meaning of terms when the same word or abbreviation can have different meanings depending on the context.

Example:

Input → "I am a beneficiary of a government scheme."

Semantic interpretation:
beneficiary → person receiving scheme benefits
Module 4 — Reference Resolution & Language Generation

This module identifies references between sentences and connects them with the correct previously mentioned entity.

Example:

"I own 4 acres of agricultural land.
It is used for growing paddy."

The system resolves:

It → agricultural land

The resolved information is then used to improve the structured eligibility profile.

The module also supports the generation of clear and understandable explanations for the final scheme recommendations.

Example:

The scheme is recommended because your occupation,
location, income, and agricultural land details match
the relevant eligibility criteria.
🔄 NLP Processing Pipeline

The four NLP modules work together as a sequential processing pipeline:

Natural-Language Input
        ↓
Module 1
Morphological Analysis
        ↓
Module 2
CFG / Dependency Analysis
        ↓
Module 3
Semantic Analysis & WSD
        ↓
Module 4
Reference Resolution & Language Generation
        ↓
Structured Eligibility Information
        ↓
Scheme Matching
🏗️ System Architecture
User
  ↓
Natural-Language Eligibility Input
  ↓
Text Preprocessing
  ↓
Four NLP Modules
  ├── Morphological Analysis
  ├── CFG / Dependency Analysis
  ├── Semantic Analysis + WSD
  └── Reference Resolution + Language Generation
  ↓
Structured Eligibility Profile
  ↓
Scheme Matching Engine
  ↕
Government Scheme Database
  ↓
Matched Schemes
  ↓
Recommendation & Explanation
  ↓
SchemeMatch Dashboard / NLP Report
🔄 Application Flow
Login / Application Access
        ↓
Dashboard
        ↓
Eligibility Check
        ↓
Natural-Language Input
        ↓
NLP Analysis
        ↓
Extracted Eligibility
        ↓
Scheme Matching
        ↓
Recommendations
        ↓
Matching Explanation
        ↓
NLP Report
📋 Eligibility Attribute Extraction

SchemeMatch extracts relevant information from the user's natural-language description.

The system can process attributes such as:

Age
Gender
Occupation
Location
Annual income
Education
Category
Land ownership
Land area
Crop
Farming experience
Dependents
User requirements

The attributes extracted depend on the information provided by the user.

🖥️ Dashboard

The SchemeMatch dashboard provides access to the main application features.

The dashboard can include:

Overview
Eligibility Check
Scheme Directory
Popular Schemes
Saved Schemes
Applications
NLP Analysis Report
AI Assistant
Profile
Notifications

The dashboard is designed to provide a simple and organized user experience.
