import React, { useRef, useState, useMemo } from "react";
import { useTranslation } from "react-i18next";
import {
  ArrowLeft,
  ArrowRight,
  Mic,
  Send,
  Loader2,
  CheckCircle,
  ExternalLink,
  FileText,
  BarChart3,
  MessageSquare,
  Sparkles,
  GitBranch,
  Layers,
  Bookmark,
  Check,
  Award,
  ChevronDown
} from "lucide-react";

function Situation({
  onBack,
  savedSchemeIds = [],
  isSchemeSaved = () => false,
  toggleSaveScheme = () => {}
}) {
  const { t, i18n } = useTranslation();

  const [text, setText] = useState("");
  const [loading, setLoading] = useState(false);
  const [listening, setListening] = useState(false);
  const [matches, setMatches] = useState([]);
  const [message, setMessage] = useState("");
  const [selectedScheme, setSelectedScheme] = useState(null);

  // Complete response from Flask /analyze endpoint
  const [analysisData, setAnalysisData] = useState(null);

  // Dedicated NLP Report Page State
  const [showNlpReport, setShowNlpReport] = useState(false);

  const recognitionRef = useRef(null);
  const manualStopRef = useRef(false);

  /* =========================================================
     SPEECH TO TEXT (Robust Multi-Language Web Speech API)
  ========================================================= */

  const handleSpeak = () => {
    const SpeechRecognition =
      window.SpeechRecognition ||
      window.webkitSpeechRecognition;

    if (!SpeechRecognition) {
      setMessage(
        t("voice.unsupported") ||
          "Speech recognition is not supported in this browser. Please use Google Chrome or Microsoft Edge."
      );
      return;
    }

    if (listening && recognitionRef.current) {
      manualStopRef.current = true;
      try {
        recognitionRef.current.stop();
      } catch (e) {
        console.debug(e);
      }
      setListening(false);
      setMessage(t("voice.stopped") || "Voice input stopped.");
      return;
    }

    const recognition = new SpeechRecognition();
    recognition.continuous = true;
    recognition.interimResults = true;
    recognition.maxAlternatives = 1;

    manualStopRef.current = false;

    const selectedLanguage = i18n.language || localStorage.getItem("language") || "en";

    const languageMap = {
      en: "en-IN",
      te: "te-IN",
      hi: "hi-IN",
      ta: "ta-IN",
      kn: "kn-IN",
      ml: "ml-IN",
      mr: "mr-IN"
    };

    recognition.lang = languageMap[selectedLanguage] || "en-IN";
    const baseText = text.trim();

    recognition.onstart = () => {
      setListening(true);
      setMessage(
        t("voice.listeningPrompt") ||
          "Listening... Speak your situation. Click Speak again when you are finished."
      );
    };

    recognition.onresult = (event) => {
      let interimTranscript = "";
      let finalTranscript = "";

      for (let i = 0; i < event.results.length; i++) {
        const tr = event.results[i][0].transcript;
        if (event.results[i].isFinal) {
          finalTranscript += tr + " ";
        } else {
          interimTranscript += tr;
        }
      }

      const totalSpeech = (finalTranscript + interimTranscript).trim();
      if (totalSpeech) {
        setText(baseText ? `${baseText} ${totalSpeech}` : totalSpeech);
      }
    };

    recognition.onerror = (event) => {
      console.error("Speech recognition error:", event.error);
      if (event.error === "not-allowed" || event.error === "service-not-allowed") {
        manualStopRef.current = true;
        setListening(false);
        recognitionRef.current = null;
        setMessage(
          t("voice.denied") ||
            "Microphone permission was denied. Please allow microphone access in your browser."
        );
      } else if (event.error === "no-speech") {
        setMessage(
          t("voice.listening") || "Still listening... Please speak your situation."
        );
      } else if (event.error !== "aborted") {
        setMessage(
          t("voice.paused") || "Speech recognition paused. Trying to continue listening..."
        );
      }
    };

    recognition.onend = () => {
      setListening(false);
      recognitionRef.current = null;
    };

    recognitionRef.current = recognition;

    try {
      recognition.start();
    } catch (error) {
      console.error("Unable to start speech recognition:", error);
      manualStopRef.current = true;
      setListening(false);
      recognitionRef.current = null;
      setMessage(
        t("voice.error") || "Unable to start the microphone. Please try again."
      );
    }
  };

  /* =========================================================
     ANALYZE USER SITUATION
  ========================================================= */

  const handleSubmit = async () => {
    if (!text.trim()) {
      setMessage(
        t("situation.emptyMessage") ||
          "Please describe your situation first."
      );
      return;
    }

    setLoading(true);
    setMessage("");

    try {
      const response = await fetch("http://127.0.0.1:5000/analyze", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          situation: text,
          user_text: text,
          language: i18n.language || "en"
        })
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.error ||
            t("situation.analyzeFailed") ||
            "Failed to analyze situation."
        );
      }

      setAnalysisData(data);
      setMatches(data.matches || data.recommendations || []);
      setMessage(
        data.message ||
          `Found ${data.matches ? data.matches.length : 0} matching schemes.`
      );
    } catch (error) {
      console.error("Analysis error:", error);
      setMessage(
        error.message ||
          t("situation.analyzeFailed") ||
          "Unable to analyze your situation. Please try again."
      );
    } finally {
      setLoading(false);
    }
  };

  const handleUseExample = () => {
    setText(
      t("situation.exampleText") ||
        "I am a 45-year-old male farmer from Tamil Nadu. I own 4 acres of agricultural land and grow paddy on my land. My annual family income is ₹1.8 lakh. I have completed my 10th standard. I have been farming for 15 years and I need financial support to improve my farming activities."
    );
  };

  /* =========================================================
     DATA EXTRACTION & COMPUTED HELPERS
  ========================================================= */

  const userProfile = useMemo(() => {
    if (!analysisData) return {};
    return (
      analysisData.user_profile ||
      analysisData.profile ||
      analysisData.extracted_info ||
      analysisData.attributes ||
      {}
    );
  }, [analysisData]);

  const dependents = useMemo(() => {
    if (!analysisData) return [];
    return (
      analysisData.dependents ||
      analysisData.extracted_info?.dependents ||
      []
    );
  }, [analysisData]);

  const morphology = useMemo(() => {
    if (!analysisData) return {};
    return (
      analysisData.nlp_pipeline?.module_1_morphology ||
      analysisData.nlp_pipeline?.morphological_analysis ||
      analysisData.morphology ||
      {}
    );
  }, [analysisData]);

  const syntax = useMemo(() => {
    if (!analysisData) return {};
    return (
      analysisData.nlp_pipeline?.module_2_syntax ||
      analysisData.nlp_pipeline?.syntax_analysis ||
      analysisData.syntax ||
      {}
    );
  }, [analysisData]);

  const semantics = useMemo(() => {
    if (!analysisData) return {};
    return (
      analysisData.nlp_pipeline?.module_3_semantics ||
      analysisData.nlp_pipeline?.semantic_analysis ||
      analysisData.semantics ||
      {}
    );
  }, [analysisData]);

  const discourse = useMemo(() => {
    if (!analysisData) return {};
    return (
      analysisData.nlp_pipeline?.module_4_discourse ||
      analysisData.nlp_pipeline?.discourse_analysis ||
      analysisData.discourse ||
      {}
    );
  }, [analysisData]);

  const rawMatches = useMemo(() => {
    return analysisData?.matches || analysisData?.recommendations || matches || [];
  }, [analysisData, matches]);

  const normalizedMatches = useMemo(() => {
    return rawMatches.map((scheme) => ({
      ...scheme,
      officialUrl:
        scheme.officialUrl ||
        scheme.official_url ||
        scheme.officialWebsite ||
        scheme.url ||
        null
    }));
  }, [rawMatches]);

  const overallUnderstanding =
    analysisData?.nlp_pipeline?.module_4_discourse?.overall_understanding ||
    analysisData?.nlp_pipeline?.discourse_analysis?.overall_understanding ||
    analysisData?.overall_understanding ||
    "The NLP pipeline processed the user's situation through all 4 modules, extracting profile attributes, identifying sentence dependencies, generating semantic facts, and matching relevant government schemes.";

  const mod1RepResult =
    morphology?.representative_result ||
    "Root keywords and lemmatized tokens successfully identified for semantic extraction.";

  const mod2RepResult =
    syntax?.representative_result ||
    "Syntactic relationships and attribute ownership mapped without cross-entity misattribution.";

  const mod3RepResult =
    semantics?.representative_result ||
    "First-order predicate facts generated and validated against scheme eligibility rules.";

  const mod4RepResult =
    discourse?.representative_result ||
    "Discourse entities resolved and natural-language recommendations generated.";

  // Dynamic Tree Data generation based on detected attributes
  const dynamicTreeNodes = useMemo(() => {
    const nodes = [];
    const p = userProfile;

    if (p.age) nodes.push({ label: "AGE", value: `${p.age} years`, edge: "has_age" });
    if (p.gender) nodes.push({ label: "GENDER", value: String(p.gender), edge: "has_gender" });
    if (p.occupation) nodes.push({ label: "OCCUPATION", value: String(p.occupation), edge: "works_as" });
    if (p.state || p.location) nodes.push({ label: "LOCATION", value: String(p.state || p.location), edge: "resides_in" });
    if (p.land_ownership || p.land) {
      nodes.push({
        label: "LAND",
        value: String(p.land_ownership || p.land),
        sub: p.crop ? `Crop: ${p.crop}` : null,
        edge: "owns_land"
      });
    } else if (p.crop) {
      nodes.push({ label: "CROP", value: String(p.crop), edge: "cultivates" });
    }
    if (p.income) nodes.push({ label: "INCOME", value: String(p.income), edge: "earns" });
    if (p.education) nodes.push({ label: "EDUCATION", value: String(p.education), edge: "completed" });
    if (p.caste || p.category) nodes.push({ label: "CATEGORY", value: String(p.caste || p.category), edge: "belongs_to" });
    if (p.disability) nodes.push({ label: "DISABILITY", value: String(p.disability), edge: "has_status" });

    // If backend provided branches, combine or prefer backend branches
    const backendBranches = syntax?.dependency_tree_branches || [];
    if (backendBranches.length > 0) {
      return backendBranches;
    }

    return nodes;
  }, [userProfile, syntax]);

  const syntaxDependents = syntax?.dependency_tree_dependents || [];
  const discourseFlowSteps = discourse?.discourse_flow_steps || [];
  const mod1Concepts = morphology?.identified_concepts || [];

  const formatValue = (value) => {
    if (value === null || value === undefined || value === "") {
      return "Not specified";
    }
    if (typeof value === "boolean") {
      return value ? "Yes" : "No";
    }
    if (Array.isArray(value)) {
      if (value.length === 0) return "None";
      if (typeof value[0] === "object") {
        return (
          <ul style={{ margin: 0, paddingLeft: "16px" }}>
            {value.map((item, idx) => (
              <li key={idx}>
                {Object.entries(item)
                  .map(([k, v]) => `${k}: ${v}`)
                  .join(", ")}
              </li>
            ))}
          </ul>
        );
      }
      return value.join(", ");
    }
    if (typeof value === "object") {
      return (
        <ul style={{ margin: 0, paddingLeft: "16px" }}>
          {Object.entries(value).map(([k, v]) => (
            <li key={k}>
              <strong>{k}:</strong> {String(v)}
            </li>
          ))}
        </ul>
      );
    }
    return String(value);
  };

  /* =========================================================
     RENDER: PROPER FULL-PAGE NLP ANALYSIS REPORT
  ========================================================= */

  if (showNlpReport && analysisData) {
    return (
      <div className="nlp-report-page">
        {/* Full-Width Report Top Navigation */}
        <header className="nlp-report-navbar">
          <div className="nlp-report-nav-inner">
            <button
              className="nlp-back-btn"
              type="button"
              onClick={() => setShowNlpReport(false)}
            >
              <ArrowLeft size={18} />
              <span>{t("situation.backToEligibility") || "Back to Eligibility"}</span>
            </button>
            <div className="brand">
              <div className="brand-icon">✓</div>
              <span>SchemeMatch NLP</span>
            </div>
          </div>
        </header>

        {/* Wide Report Container */}
        <main className="nlp-report-container">
          {/* Main Report Title Banner */}
          <div className="nlp-report-banner">
            <div className="nlp-banner-text">
              <p className="eyebrow">{t("nlp.eyebrow") || "SCHEMEMATCH NATURAL LANGUAGE PROCESSING"}</p>
              <h1 className="nlp-main-title">{t("nlp.reportTitle") || "NLP ANALYSIS REPORT"}</h1>
              <p className="nlp-main-subtitle">
                {t("nlp.reportSubtitle") || "Natural Language Processing & Eligibility Analysis"}
              </p>
              <p className="nlp-banner-desc">
                {t("nlp.intro") ||
                  "Original user information has been analyzed through four NLP processing modules."}
              </p>
            </div>
            <div className="nlp-banner-status">
              <span className="nlp-status-badge">
                <CheckCircle size={16} />
                <span>Analysis Complete</span>
              </span>
            </div>
          </div>

          {/* =========================================================
              1. ORIGINAL USER INPUT
          ========================================================= */}
          <section className="nlp-report-card">
            <div className="nlp-card-header">
              <div className="nlp-icon-box">
                <FileText size={22} />
              </div>
              <div>
                <span className="match-category">{t("nlp.userInputCat") || "SECTION 1"}</span>
                <h2>{t("nlp.originalUserInput") || "ORIGINAL USER INPUT"}</h2>
              </div>
            </div>
            <div className="nlp-user-input-box">
              <p>"{analysisData.user_text || text}"</p>
            </div>
          </section>

          {/* =========================================================
              2. EXTRACTED USER INFORMATION
          ========================================================= */}
          <section className="nlp-report-card">
            <div className="nlp-card-header">
              <div className="nlp-icon-box">
                <CheckCircle size={22} />
              </div>
              <div>
                <span className="match-category">{t("nlp.extractedInfoCat") || "SECTION 2"}</span>
                <h2>{t("nlp.extractedUserInfo") || "EXTRACTED USER INFORMATION"}</h2>
              </div>
            </div>
            <p className="nlp-section-desc">
              {t("nlp.extractedInfoDesc") || "Information extracted directly from the user's input text for government scheme eligibility."}
            </p>

            <div className="nlp-table-container">
              <table className="nlp-table">
                <thead>
                  <tr>
                    <th style={{ width: "35%" }}>Attribute</th>
                    <th style={{ width: "65%" }}>Extracted Information</th>
                  </tr>
                </thead>
                <tbody>
                  {[
                    { label: "Age", val: userProfile.age ? `${userProfile.age} years` : null },
                    { label: "Gender", val: userProfile.gender },
                    { label: "Occupation", val: userProfile.occupation },
                    { label: "Location / State", val: userProfile.state || userProfile.location },
                    { label: "Land Ownership", val: userProfile.land_ownership || userProfile.land },
                    { label: "Crop", val: userProfile.crop },
                    { label: "Annual Income", val: userProfile.income },
                    { label: "Education Level", val: userProfile.education },
                    { label: "Caste / Category", val: userProfile.caste || userProfile.category },
                    { label: "Marital Status", val: userProfile.marital_status },
                    { label: "Disability Status", val: userProfile.disability }
                  ]
                    .filter((item) => item.val !== null && item.val !== undefined && item.val !== "")
                    .map((attr, idx) => (
                      <tr key={idx}>
                        <td>
                          <strong>{attr.label}</strong>
                        </td>
                        <td>{formatValue(attr.val)}</td>
                      </tr>
                    ))}
                </tbody>
              </table>
            </div>
          </section>

          {/* =========================================================
              3. DEPENDENT INFORMATION
          ========================================================= */}
          {dependents && dependents.length > 0 && (
            <section className="nlp-report-card">
              <div className="nlp-card-header">
                <div className="nlp-icon-box">
                  <GitBranch size={22} />
                </div>
                <div>
                  <span className="match-category">{t("nlp.dependentInfoCat") || "SECTION 3"}</span>
                  <h2>{t("nlp.dependentInfoTitle") || "DEPENDENT INFORMATION"}</h2>
                </div>
              </div>
              <p className="nlp-section-desc">
                {t("nlp.dependentInfoDesc") || "Dependent details are separated from the primary user's attributes to prevent misattribution of education, age or entitlements."}
              </p>

              <div className="nlp-table-container">
                <table className="nlp-table">
                  <thead>
                    <tr>
                      <th style={{ width: "30%" }}>Relationship</th>
                      <th style={{ width: "70%" }}>Information</th>
                    </tr>
                  </thead>
                  <tbody>
                    {dependents.map((dep, idx) => (
                      <tr key={idx}>
                        <td>
                          <strong>{dep.relation || dep.name || `Dependent ${idx + 1}`}</strong>
                        </td>
                        <td>{formatValue(dep.details || dep)}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </section>
          )}

          {/* =========================================================
              4. OVERALL NLP UNDERSTANDING
          ========================================================= */}
          <section className="nlp-report-card">
            <div className="nlp-card-header">
              <div className="nlp-icon-box">
                <MessageSquare size={22} />
              </div>
              <div>
                <span className="match-category">{t("nlp.overallUnderstandingCat") || "SECTION 4"}</span>
                <h2>{t("nlp.overallUnderstandingTitle") || "OVERALL NLP UNDERSTANDING"}</h2>
              </div>
            </div>
            <div className="nlp-summary-box">
              <strong>{t("nlp.summaryExtracted") || "Synthesis of User Situation"}</strong>
              <p>{overallUnderstanding}</p>
            </div>
          </section>

          {/* =========================================================
              5. NLP MODULE WALKTHROUGH FLOW
          ========================================================= */}
          <section className="nlp-process-walkthrough-section">
            <div className="nlp-section-header">
              <p className="eyebrow">{t("nlp.part2Eyebrow") || "PIPELINE ARCHITECTURE"}</p>
              <h2>{t("nlp.moduleWalkthroughTitle") || "NLP MODULE WALKTHROUGH"}</h2>
              <p className="nlp-section-desc">
                End-to-end linguistic parsing flow transforming raw natural language into verified predicate facts for eligibility matching.
              </p>
            </div>

            <div className="nlp-process-flow-grid">
              <div className="nlp-process-card">
                <div className="nlp-process-step-num">STEP 1</div>
                <h3>USER INPUT</h3>
                <p>Raw free-text sentence ingestion</p>
              </div>

              <div className="nlp-process-arrow">→</div>

              <div className="nlp-process-card">
                <div className="nlp-process-step-num">MODULE 1</div>
                <h3>INTRODUCTION & MORPHOLOGY</h3>
                <p>Lemmatization & token root normalization</p>
              </div>

              <div className="nlp-process-arrow">→</div>

              <div className="nlp-process-card">
                <div className="nlp-process-step-num">MODULE 2</div>
                <h3>CONTEXT FREE GRAMMAR</h3>
                <p>Dependency parsing & relationship mapping</p>
              </div>

              <div className="nlp-process-arrow">→</div>

              <div className="nlp-process-card">
                <div className="nlp-process-step-num">MODULE 3</div>
                <h3>SEMANTIC ANALYSIS</h3>
                <p>Predicate calculus & entity meaning</p>
              </div>

              <div className="nlp-process-arrow">→</div>

              <div className="nlp-process-card">
                <div className="nlp-process-step-num">MODULE 4</div>
                <h3>LANGUAGE GENERATION & DISCOURSE</h3>
                <p>Reference resolution & NLG explanation</p>
              </div>

              <div className="nlp-process-arrow">→</div>

              <div className="nlp-process-card highlight">
                <div className="nlp-process-step-num">OUTPUT</div>
                <h3>SCHEME MATCHING</h3>
                <p>Eligibility scoring & scheme recommendations</p>
              </div>
            </div>
          </section>

          {/* =========================================================
              6. MODULE 1 — MORPHOLOGY
          ========================================================= */}
          <section className="nlp-report-card module-card">
            <div className="nlp-card-header">
              <div className="nlp-icon-box">
                <Layers size={22} />
              </div>
              <div>
                <span className="match-category">MODULE 1</span>
                <h2>Introduction & Morphology</h2>
              </div>
            </div>

            <div className="nlp-module-explanation">
              <p>
                Identifies different forms of words and converts them into their common root forms.
                This helps SchemeMatch recognize important keywords accurately from free-text input.
              </p>
            </div>

            <div className="nlp-technique-row">
              <span className="nlp-technique-label">TECHNIQUE USED:</span>
              <span className="nlp-technique-badge">Finite-State Morphological Analysis</span>
            </div>

            <h3 className="nlp-sub-heading">Word Normalization Table</h3>
            <div className="nlp-table-container">
              <table className="nlp-table">
                <thead>
                  <tr>
                    <th>Input Word</th>
                    <th>Word Form</th>
                    <th>Normalized / Root Form</th>
                  </tr>
                </thead>
                <tbody>
                  {(morphology.tokens || morphology.word_normalization_table || []).map((tkn, idx) => (
                    <tr key={idx}>
                      <td>
                        <strong>{tkn.word}</strong>
                      </td>
                      <td>{tkn.form || tkn.pos || "surface form"}</td>
                      <td>
                        <span className="nlp-chip" style={{ margin: 0 }}>
                          {tkn.root || tkn.normalized || tkn.lemma || tkn.word}
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>

            {mod1Concepts && mod1Concepts.length > 0 && (
              <div style={{ marginTop: "16px" }}>
                <h4 className="nlp-inner-title">KEY CONCEPTS IDENTIFIED</h4>
                <div className="nlp-chips">
                  {mod1Concepts.map((c, idx) => (
                    <span className="nlp-chip" key={idx}>
                      {c}
                    </span>
                  ))}
                </div>
              </div>
            )}

            <div className="nlp-result-box">
              <strong>REPRESENTATIVE RESULT</strong>
              <p>{mod1RepResult}</p>
            </div>
          </section>

          {/* =========================================================
              7. MODULE 2 — CFG / DEPENDENCY PARSING
          ========================================================= */}
          <section className="nlp-report-card module-card">
            <div className="nlp-card-header">
              <div className="nlp-icon-box">
                <GitBranch size={22} />
              </div>
              <div>
                <span className="match-category">MODULE 2</span>
                <h2>Context Free Grammar</h2>
              </div>
            </div>

            <div className="nlp-module-explanation">
              <p>
                Analyzes sentence structure to identify relationships between words and entities.
                This helps determine who has a particular attribute or information.
              </p>
            </div>

            <div className="nlp-technique-row">
              <span className="nlp-technique-label">TECHNIQUE USED:</span>
              <span className="nlp-technique-badge">CFG / Dependency Parsing</span>
            </div>

            {/* A) Relationship Table */}
            <h3 className="nlp-sub-heading">A) Relationship Table</h3>
            <div className="nlp-table-container">
              <table className="nlp-table">
                <thead>
                  <tr>
                    <th>Entity</th>
                    <th>Relationship</th>
                    <th>Information</th>
                  </tr>
                </thead>
                <tbody>
                  {(syntax.relationships || syntax.relationship_table || []).map((rel, idx) => (
                    <tr key={idx}>
                      <td>
                        <strong>{rel.entity}</strong>
                      </td>
                      <td>
                        <span className="nlp-chip" style={{ margin: 0 }}>
                          {rel.relationship}
                        </span>
                      </td>
                      <td>{rel.information}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>

            {/* B) REAL VISUAL DEPENDENCY TREE */}
            <h3 className="nlp-sub-heading" style={{ marginTop: "24px" }}>
              B) Real Visual Dependency Tree
            </h3>
            <p className="nlp-section-desc" style={{ marginBottom: "12px" }}>
              Dynamic parse tree linking user root to detected profile attributes and dependent entities.
            </p>

            <div className="nlp-dependency-tree-card">
              {/* Root User Node */}
              <div className="tree-root-container">
                <div className="tree-node tree-root-node">
                  <span>USER</span>
                </div>
              </div>
              <div className="tree-vertical-line" />

              {/* Bus Line & Child Attributes */}
              <div className="tree-branches-container">
                <div className="tree-branches-bus" />
                <div className="tree-branches-row">
                  {dynamicTreeNodes.map((node, idx) => (
                    <div className="tree-branch-col" key={idx}>
                      <div className="tree-branch-drop-line" />
                      <div className="tree-node tree-attr-label-node">
                        <span>{node.label}</span>
                      </div>
                      <div className="tree-sub-line" />
                      <div className="tree-node tree-attr-val-node">
                        <span>{node.value}</span>
                      </div>
                      {node.sub && (
                        <>
                          <div className="tree-sub-line" />
                          <div className="tree-node tree-attr-sub-node">
                            <span>{node.sub}</span>
                          </div>
                        </>
                      )}
                    </div>
                  ))}
                </div>
              </div>

              {/* Dependents Sub-Tree */}
              {syntaxDependents && syntaxDependents.length > 0 && (
                <div className="tree-dependent-container">
                  <div className="tree-dependent-header">
                    <span className="tree-dependent-badge">has_dependent</span>
                    <div className="tree-node tree-root-node" style={{ background: "#0e7490", fontSize: "13px", padding: "6px 16px" }}>
                      DEPENDENT
                    </div>
                  </div>
                  <div className="tree-vertical-line" style={{ background: "#0e7490" }} />
                  <div className="tree-branches-row">
                    {syntaxDependents.map((dep, dIdx) => (
                      <div className="tree-branch-col" key={dIdx}>
                        <div className="tree-branch-drop-line" style={{ background: "#0e7490" }} />
                        <div className="tree-node tree-attr-label-node" style={{ borderColor: "#0e7490", color: "#0e7490" }}>
                          <span>{dep.relation}</span>
                        </div>
                        <div className="tree-sub-line" />
                        <div className="tree-node tree-attr-val-node">
                          <span>{dep.action}</span>
                        </div>
                        {dep.detail && (
                          <>
                            <div className="tree-sub-line" />
                            <div className="tree-node tree-attr-sub-node">
                              <span>{dep.detail}</span>
                            </div>
                          </>
                        )}
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>

            <div className="nlp-result-box">
              <strong>REPRESENTATIVE RESULT</strong>
              <p>{mod2RepResult}</p>
            </div>
          </section>

          {/* =========================================================
              8. MODULE 3 — SEMANTIC ANALYSIS
          ========================================================= */}
          <section className="nlp-report-card module-card">
            <div className="nlp-card-header">
              <div className="nlp-icon-box">
                <BarChart3 size={22} />
              </div>
              <div>
                <span className="match-category">MODULE 3</span>
                <h2>Semantic Analysis</h2>
              </div>
            </div>

            <div className="nlp-module-explanation">
              <p>
                Converts extracted information into meaningful structured facts and concepts.
                These semantic facts are used by the matching engine to identify relevant schemes.
              </p>
            </div>

            <div className="nlp-technique-row">
              <span className="nlp-technique-label">TECHNIQUE USED:</span>
              <span className="nlp-technique-badge">First-Order Predicate Calculus + WSD</span>
            </div>

            <h3 className="nlp-sub-heading">Semantic Attribute Table</h3>
            <div className="nlp-table-container">
              <table className="nlp-table">
                <thead>
                  <tr>
                    <th>Category</th>
                    <th>Extracted Meaning</th>
                  </tr>
                </thead>
                <tbody>
                  {(semantics.semantic_attribute_table || semantics.extracted_meanings || []).map((item, idx) => (
                    <tr key={idx}>
                      <td>
                        <strong>{item.category}</strong>
                      </td>
                      <td>{item.meaning}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>

            <h3 className="nlp-sub-heading" style={{ marginTop: "20px" }}>
              Structured Facts (First-Order Predicate Calculus)
            </h3>
            <div className="nlp-predicates-box">
              {(semantics.predicates || semantics.predicate_calculus || []).map((p, idx) => (
                <div className="nlp-predicate-item" key={idx}>
                  <code>{p}</code>
                </div>
              ))}
            </div>

            <div className="nlp-result-box">
              <strong>REPRESENTATIVE RESULT</strong>
              <p>{mod3RepResult}</p>
            </div>
          </section>

          {/* =========================================================
              9. MODULE 4 — LANGUAGE GENERATION & DISCOURSE
          ========================================================= */}
          <section className="nlp-report-card module-card">
            <div className="nlp-card-header">
              <div className="nlp-icon-box">
                <MessageSquare size={22} />
              </div>
              <div>
                <span className="match-category">MODULE 4</span>
                <h2>Language Generation & Discourse</h2>
              </div>
            </div>

            <div className="nlp-module-explanation">
              <p>
                Resolves references across sentences and prepares meaningful natural-language responses.
                It explains the matched schemes and eligibility results clearly to the user.
              </p>
            </div>

            <div className="nlp-technique-row">
              <span className="nlp-technique-label">TECHNIQUE USED:</span>
              <span className="nlp-technique-badge">Reference Resolution + Surface Realization</span>
            </div>

            {/* A) Reference Resolution Table */}
            <h3 className="nlp-sub-heading">A) Reference Resolution Table</h3>
            {(discourse.reference_resolution_table || discourse.references || []).length > 0 ? (
              <div className="nlp-table-container">
                <table className="nlp-table">
                  <thead>
                    <tr>
                      <th>Expression</th>
                      <th>Resolved Entity</th>
                    </tr>
                  </thead>
                  <tbody>
                    {(discourse.reference_resolution_table || discourse.references || []).map((ref, idx) => (
                      <tr key={idx}>
                        <td>
                          <strong>"{ref.expression}"</strong>
                        </td>
                        <td>
                          <span className="nlp-chip" style={{ margin: 0 }}>
                            {ref.resolvedEntity || ref.resolved_entity}
                          </span>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            ) : (
              <div className="nlp-no-ref-box">
                <p>No ambiguous references requiring resolution were identified in the provided text.</p>
              </div>
            )}

            {/* B) Discourse Block Flow */}
            <h3 className="nlp-sub-heading" style={{ marginTop: "20px" }}>
              B) Discourse Reference Flow
            </h3>
            <div className="nlp-block-flow">
              {discourseFlowSteps.map((step, idx) => (
                <React.Fragment key={idx}>
                  <div className="nlp-block-card">
                    <span className="nlp-block-step-label">{step.step}</span>
                    <span className="nlp-block-text">{step.text}</span>
                  </div>
                  {idx < discourseFlowSteps.length - 1 && (
                    <span className="nlp-block-arrow">→</span>
                  )}
                </React.Fragment>
              ))}
            </div>

            {/* C) Generated Natural-Language Explanation */}
            <h3 className="nlp-sub-heading" style={{ marginTop: "20px" }}>
              C) Generated Natural-Language Explanation
            </h3>
            <div className="nlp-explanation-box">
              <p>
                {discourse.generated_explanation ||
                  discourse.explanation ||
                  overallUnderstanding}
              </p>
            </div>

            <div className="nlp-result-box">
              <strong>REPRESENTATIVE RESULT</strong>
              <p>{mod4RepResult}</p>
            </div>
          </section>

          {/* =========================================================
              10. SCHEME MATCHING SECTION
          ========================================================= */}
          <section className="nlp-report-card">
            <div className="nlp-card-header">
              <div className="nlp-icon-box">
                <Award size={22} />
              </div>
              <div>
                <span className="match-category">SECTION 10</span>
                <h2>SCHEME MATCHING</h2>
              </div>
            </div>

            <div className="nlp-matching-flow-bar">
              <div className="nlp-match-step">Semantic Information</div>
              <span className="nlp-flow-arrow">→</span>
              <div className="nlp-match-step">Existing Scheme Matching Engine</div>
              <span className="nlp-flow-arrow">→</span>
              <div className="nlp-match-step">Matching Results</div>
              <span className="nlp-flow-arrow">→</span>
              <div className="nlp-match-step highlight">Eligibility / Recommendations</div>
            </div>

            <p className="nlp-section-desc" style={{ marginTop: "16px" }}>
              Schemes identified from the existing scheme dataset based on the extracted semantic facts.
            </p>

            {normalizedMatches && normalizedMatches.length > 0 ? (
              <div className="matches-list" style={{ marginTop: "16px" }}>
                {normalizedMatches.map((scheme, index) => {
                  const rawUrl = scheme.officialUrl || scheme.official_url || scheme.officialWebsite || scheme.url;
                  const validUrl = rawUrl && typeof rawUrl === "string" && rawUrl.trim()
                    ? (rawUrl.trim().startsWith("http://") || rawUrl.trim().startsWith("https://") ? rawUrl.trim() : `https://${rawUrl.trim()}`)
                    : null;

                  return (
                    <div
                      key={scheme.id || index}
                      className="match-card"
                      style={{ position: "relative" }}
                    >
                      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: "8px" }}>
                        <span className="match-category">{scheme.category}</span>
                        <div style={{ display: "flex", alignItems: "center", gap: "8px" }}>
                          {scheme.match_score && (
                            <span
                              style={{
                                fontSize: "12px",
                                fontWeight: "700",
                                color: "#087f75",
                                background: "#eaf8f6",
                                padding: "4px 8px",
                                borderRadius: "4px"
                              }}
                            >
                              {scheme.match_score}% {t("directory.matchScore") || "Match"}
                            </span>
                          )}
                          <button
                            className={`scheme-bookmark-btn ${isSchemeSaved(scheme.id) ? "saved" : ""}`}
                            type="button"
                            onClick={() => toggleSaveScheme(scheme)}
                            title={isSchemeSaved(scheme.id) ? (t("saved.unsave") || "Unsave") : (t("saved.save") || "Save")}
                          >
                            <Bookmark size={16} fill={isSchemeSaved(scheme.id) ? "#087f75" : "none"} color={isSchemeSaved(scheme.id) ? "#087f75" : "#64748b"} />
                            <span>{isSchemeSaved(scheme.id) ? (t("saved.saved") || "Saved") : (t("saved.save") || "Save")}</span>
                          </button>
                        </div>
                      </div>
                      <h3>{scheme.name}</h3>
                      <p>{scheme.description}</p>
                      <div style={{ display: "flex", gap: "8px", marginTop: "12px", flexWrap: "wrap" }}>
                        <button
                          className="card-button"
                          type="button"
                          onClick={() => setSelectedScheme(scheme)}
                        >
                          {t("situation.viewDetails") || "View Details"}
                          <ExternalLink size={16} />
                        </button>
                        {validUrl ? (
                          <button
                            className="primary-button"
                            type="button"
                            style={{ padding: "6px 14px", fontSize: "13px" }}
                            onClick={() => window.open(validUrl, "_blank", "noopener,noreferrer")}
                          >
                            {t("directory.officialWebsite") || "Official Website"}
                            <ExternalLink size={14} />
                          </button>
                        ) : null}
                      </div>
                    </div>
                  );
                })}
              </div>
            ) : (
              <p style={{ color: "#64748b" }}>No schemes matched your input.</p>
            )}
          </section>

          {/* =========================================================
              11. FINAL NLP SUMMARY
          ========================================================= */}
          <section className="nlp-report-card">
            <div className="nlp-card-header">
              <div className="nlp-icon-box">
                <CheckCircle size={22} />
              </div>
              <div>
                <span className="match-category">FINAL SUMMARY</span>
                <h2>FINAL NLP SUMMARY</h2>
              </div>
            </div>

            <div className="nlp-checklist-grid">
              <div className="nlp-check-item">
                <Check size={18} color="#087f75" />
                <span>Input text processed</span>
              </div>
              <div className="nlp-check-item">
                <Check size={18} color="#087f75" />
                <span>Information extracted into structured profile</span>
              </div>
              <div className="nlp-check-item">
                <Check size={18} color="#087f75" />
                <span>Syntactic relationships & dependency tree generated</span>
              </div>
              <div className="nlp-check-item">
                <Check size={18} color="#087f75" />
                <span>First-order semantic facts generated</span>
              </div>
              <div className="nlp-check-item">
                <Check size={18} color="#087f75" />
                <span>Natural-language discourse interpretation generated</span>
              </div>
            </div>

            <div className="nlp-recommendation-box" style={{ marginTop: "20px" }}>
              <h3 style={{ margin: "0 0 8px", color: "#087f75", fontSize: "15px" }}>
                Eligibility Recommendation
              </h3>
              <p style={{ margin: 0, color: "#134e48", lineHeight: "1.6", fontSize: "14px" }}>
                {overallUnderstanding}
              </p>
              <p style={{ margin: "10px 0 0", color: "#64748b", fontSize: "13px", fontStyle: "italic" }}>
                Please verify detailed eligibility and required documentation on the official government website before applying.
              </p>
            </div>

            <div style={{ marginTop: "24px", display: "flex", justifyContent: "flex-start" }}>
              <button
                className="primary-button"
                type="button"
                onClick={() => setShowNlpReport(false)}
              >
                <ArrowLeft size={16} />
                <span>{t("situation.backToEligibility") || "Back to Eligibility"}</span>
              </button>
            </div>
          </section>
        </main>
      </div>
    );
  }

  /* =========================================================
     RENDER: SCHEME DETAILS VIEW
  ========================================================= */

  if (selectedScheme) {
    const rawUrl =
      selectedScheme.officialUrl ||
      selectedScheme.official_url ||
      selectedScheme.officialWebsite ||
      selectedScheme.url;

    const validUrl = rawUrl && typeof rawUrl === "string" && rawUrl.trim()
      ? (rawUrl.trim().startsWith("http://") || rawUrl.trim().startsWith("https://") ? rawUrl.trim() : `https://${rawUrl.trim()}`)
      : null;

    return (
      <div className="app-page situation-page">
        <header className="top-header">
          <button
            className="back-button"
            type="button"
            onClick={() => setSelectedScheme(null)}
          >
            <ArrowLeft size={20} />
            <span>{t("common.back") || "Back"}</span>
          </button>
          <div className="brand">
            <div className="brand-icon">✓</div>
            <span>SchemeMatch</span>
          </div>
        </header>

        <main className="situation-content">
          <div className="situation-intro-block">
            <p className="eyebrow">{t("directory.eyebrow") || "SCHEME DETAILS"}</p>
            <h1 className="situation-title">{selectedScheme.name}</h1>
            <p className="situation-description">
              {selectedScheme.category ||
                "Central & State Government Welfare Initiative"}
            </p>
          </div>

          <div className="scheme-detail-card">
            <div className="detail-section">
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                <span className="match-category">{selectedScheme.category}</span>
                <button
                  className={`scheme-bookmark-btn ${isSchemeSaved(selectedScheme.id) ? "saved" : ""}`}
                  type="button"
                  onClick={() => toggleSaveScheme(selectedScheme)}
                  title={isSchemeSaved(selectedScheme.id) ? (t("saved.unsave") || "Unsave") : (t("saved.save") || "Save")}
                >
                  <Bookmark size={18} fill={isSchemeSaved(selectedScheme.id) ? "#087f75" : "none"} color={isSchemeSaved(selectedScheme.id) ? "#087f75" : "#64748b"} />
                  <span>{isSchemeSaved(selectedScheme.id) ? (t("saved.saved") || "Saved") : (t("saved.save") || "Save Scheme")}</span>
                </button>
              </div>
              <h2>{selectedScheme.name}</h2>
            </div>

            <div className="detail-section">
              <h3>{t("directory.aboutScheme") || "About the Scheme"}</h3>
              <p>{selectedScheme.description}</p>
            </div>

            {selectedScheme.benefits && (
              <div className="detail-section">
                <h3>{t("directory.keyBenefits") || "Benefits"}</h3>
                {Array.isArray(selectedScheme.benefits) ? (
                  selectedScheme.benefits.map((benefit, index) => (
                    <p key={index}>{benefit}</p>
                  ))
                ) : (
                  <p>{selectedScheme.benefits}</p>
                )}
              </div>
            )}

            {selectedScheme.eligibility && (
              <div className="detail-section">
                <h3>{t("directory.eligibility") || "Eligibility"}</h3>
                {Array.isArray(selectedScheme.eligibility) ? (
                  selectedScheme.eligibility.map((criterion, index) => (
                    <p key={index}>{criterion}</p>
                  ))
                ) : (
                  <p>{selectedScheme.eligibility}</p>
                )}
              </div>
            )}

            {selectedScheme.documents && (
              <div className="detail-section">
                <h3>{t("directory.documents") || "Required Documents"}</h3>
                {Array.isArray(selectedScheme.documents) ? (
                  selectedScheme.documents.map((doc, index) => (
                    <p key={index}>{doc}</p>
                  ))
                ) : (
                  <p>{selectedScheme.documents}</p>
                )}
              </div>
            )}

            <div className="detail-actions" style={{ display: "flex", gap: "10px", flexWrap: "wrap", marginTop: "20px" }}>
              {validUrl ? (
                <button
                  className="primary-button"
                  type="button"
                  onClick={() =>
                    window.open(
                      validUrl,
                      "_blank",
                      "noopener,noreferrer"
                    )
                  }
                >
                  {t("directory.officialWebsite") || "Official Website"}
                  <ExternalLink size={18} />
                </button>
              ) : (
                <button
                  className="primary-button"
                  type="button"
                  disabled
                  style={{ opacity: 0.6, cursor: "not-allowed" }}
                >
                  {t("directory.officialUnavailable") || "Official website unavailable"}
                </button>
              )}

              <button
                className={`card-button ${isSchemeSaved(selectedScheme.id) ? "saved" : ""}`}
                type="button"
                onClick={() => toggleSaveScheme(selectedScheme)}
              >
                <Bookmark size={18} fill={isSchemeSaved(selectedScheme.id) ? "#087f75" : "none"} color="#087f75" />
                {isSchemeSaved(selectedScheme.id) ? (t("saved.saved") || "Saved") : (t("saved.save") || "Save Scheme")}
              </button>

              <button
                className="card-button"
                type="button"
                onClick={() => setSelectedScheme(null)}
              >
                {t("common.back") || "Back to Matches"}
              </button>
            </div>
          </div>
        </main>
      </div>
    );
  }

  /* =========================================================
     RENDER: DEFAULT ELIGIBILITY CHECK PAGE
  ========================================================= */

  return (
    <div className="app-page situation-page">
      <header className="top-header">
        <button className="back-button" type="button" onClick={onBack}>
          <ArrowLeft size={20} />
          <span>{t("situation.back") || "Back"}</span>
        </button>
        <div className="brand">
          <div className="brand-icon">✓</div>
          <span>SchemeMatch</span>
        </div>
      </header>

      <main className="situation-content">
        <div className="situation-intro-block">
          <p className="eyebrow">
            {t("situation.label") || "TELL US ABOUT YOUR SITUATION"}
          </p>
          <h1 className="situation-title">
            {t("situation.title") || "What is your situation?"}
          </h1>
          <p className="situation-description">
            {t("situation.description") ||
              "Describe your situation in your own words. You don't need to fill out a complicated form."}
          </p>
        </div>

        <div className="situation-input-card">
          <label htmlFor="situation" className="situation-input-label">
            {t("situation.aboutYou") || "Tell us about yourself"}
          </label>

          <textarea
            id="situation"
            className="situation-textarea"
            placeholder={
              t("situation.placeholder") ||
              "For example: I am a 45-year-old male farmer from Tamil Nadu. I own 4 acres of agricultural land and grow paddy on my land. My annual family income is ₹1.8 lakh. I have completed my 10th standard. I have been farming for 15 years and I need financial support to improve my farming activities."
            }
            value={text}
            onChange={(e) => setText(e.target.value)}
            rows={6}
          />

          <div className="situation-toolbar">
            <div className="toolbar-left-actions">
              <button
                className={`mic-button ${listening ? "listening" : ""}`}
                type="button"
                onClick={handleSpeak}
                title={listening ? "Click to stop listening" : "Click to speak"}
              >
                <Mic size={18} color={listening ? "#ef4444" : "#087f75"} />
                <span>
                  {listening
                    ? (t("voice.listening") || "Listening...")
                    : (t("situation.speak") || "Speak")}
                </span>
              </button>

              <button
                className="example-link-button"
                type="button"
                onClick={handleUseExample}
              >
                <Sparkles size={16} />
                <span>{t("situation.example") || "Use Example"}</span>
              </button>
            </div>

            <div className="toolbar-right-count">
              <span className="character-count">
                {text.length} {t("situation.characters") || "characters"}
              </span>
            </div>
          </div>

          <div className="situation-submit-row">
            <button
              className="primary-button situation-submit-button"
              type="button"
              onClick={handleSubmit}
              disabled={loading || !text.trim()}
            >
              {loading ? (
                <>
                  <Loader2 size={18} className="spin" />
                  <span>
                    {t("situation.analyzing") || "Analyzing..."}
                  </span>
                </>
              ) : (
                <>
                  <span>
                    {t("situation.findSchemes") || "Find My Schemes"}
                  </span>
                  <ArrowRight size={18} />
                </>
              )}
            </button>
          </div>

          {message && (
            <div className="situation-message">
              <strong>{message}</strong>
            </div>
          )}
        </div>

        {/* Action Choice after analysis */}
        {analysisData && (
          <div className="results-section" style={{ marginTop: "28px" }}>
            <div className="situation-intro-block" style={{ marginBottom: "16px" }}>
              <p className="eyebrow">{t("situation.analysisComplete") || "ANALYSIS COMPLETE"}</p>
              <h2 className="situation-title" style={{ fontSize: "24px" }}>{t("situation.whatToView") || "What would you like to view?"}</h2>
              <p className="situation-description">
                {t("situation.analysisCompleteDesc") || "Your information has been processed through the NLP pipeline. You can review the full NLP analysis report or explore the potential matching schemes below."}
              </p>
            </div>

            <div style={{ display: "flex", gap: "12px", flexWrap: "wrap", marginBottom: "24px" }}>
              <button
                className="primary-button"
                type="button"
                style={{
                  display: "flex",
                  alignItems: "center",
                  gap: "8px",
                  padding: "14px 24px",
                  fontSize: "15px",
                  fontWeight: "700",
                  borderRadius: "10px"
                }}
                onClick={() => setShowNlpReport(true)}
              >
                <Sparkles size={18} />
                <span>{t("situation.viewNlpReport") || "View NLP Analysis Report (4 Modules)"}</span>
                <ArrowRight size={18} />
              </button>
            </div>
          </div>
        )}

        {/* Results List */}
        {normalizedMatches.length > 0 && (
          <div className="results-section">
            <div className="results-header" style={{ marginBottom: "18px" }}>
              <p className="eyebrow">
                {t("situation.yourMatches") || "YOUR MATCHES"}
              </p>
              <h2 style={{ fontSize: "24px", color: "#10233f", margin: "6px 0 8px" }}>
                {t("situation.potentialMatches") ||
                  "Potential Matching Schemes"}
              </h2>
              <p style={{ color: "#64748b", margin: 0, fontSize: "14px" }}>
                {t("situation.potentialMatchesDesc") ||
                  "These are potential matches based on the information you provided. Confirm current eligibility on the official government source."}
              </p>
            </div>

            <div className="matches-list">
              {normalizedMatches.map((scheme, index) => {
                const rawUrl = scheme.officialUrl || scheme.official_url || scheme.officialWebsite || scheme.url;
                const validUrl = rawUrl && typeof rawUrl === "string" && rawUrl.trim()
                  ? (rawUrl.trim().startsWith("http://") || rawUrl.trim().startsWith("https://") ? rawUrl.trim() : `https://${rawUrl.trim()}`)
                  : null;

                return (
                  <div
                    key={scheme.id || index}
                    className="match-card"
                    style={{ position: "relative" }}
                  >
                    <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: "8px" }}>
                      <span className="match-category">
                        {scheme.category}
                      </span>
                      <div style={{ display: "flex", alignItems: "center", gap: "8px" }}>
                        {scheme.match_score && (
                          <span
                            style={{
                              fontSize: "12px",
                              fontWeight: "700",
                              color: "#087f75",
                              background: "#eaf8f6",
                              padding: "4px 8px",
                              borderRadius: "4px"
                            }}
                          >
                            {scheme.match_score}% {t("directory.matchScore") || "Match"}
                          </span>
                        )}
                        <button
                          className={`scheme-bookmark-btn ${isSchemeSaved(scheme.id) ? "saved" : ""}`}
                          type="button"
                          onClick={() => toggleSaveScheme(scheme)}
                          title={isSchemeSaved(scheme.id) ? (t("saved.unsave") || "Unsave") : (t("saved.save") || "Save")}
                        >
                          <Bookmark size={16} fill={isSchemeSaved(scheme.id) ? "#087f75" : "none"} color={isSchemeSaved(scheme.id) ? "#087f75" : "#64748b"} />
                          <span>{isSchemeSaved(scheme.id) ? (t("saved.saved") || "Saved") : (t("saved.save") || "Save")}</span>
                        </button>
                      </div>
                    </div>

                    <h3>{scheme.name}</h3>
                    <p>{scheme.description}</p>

                    <div style={{ display: "flex", gap: "8px", marginTop: "12px", flexWrap: "wrap" }}>
                      <button
                        className="card-button"
                        type="button"
                        onClick={() => setSelectedScheme(scheme)}
                      >
                        {t("situation.viewDetails") || "View Details"}
                        <ExternalLink size={16} />
                      </button>
                      {validUrl ? (
                        <button
                          className="primary-button"
                          type="button"
                          style={{ padding: "6px 14px", fontSize: "13px" }}
                          onClick={() => window.open(validUrl, "_blank", "noopener,noreferrer")}
                        >
                          {t("directory.officialWebsite") || "Official Website"}
                          <ExternalLink size={14} />
                        </button>
                      ) : null}
                    </div>
                  </div>
                );
              })}
            </div>

            <div className="disclaimer-card" style={{ marginTop: "24px" }}>
              <strong>
                {t("situation.yourMatches") || "Important Notice"}
              </strong>
              <p>
                {t("nlp.officialVerifyNotice") ||
                  "Eligibility criteria can change. Please verify all details and required documentation directly with the official scheme authority or portal before applying."}
              </p>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}

export default Situation;
