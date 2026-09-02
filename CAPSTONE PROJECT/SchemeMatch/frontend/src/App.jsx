import { useEffect, useState, useRef, useMemo } from "react";
import { useTranslation } from "react-i18next";
import {
  Search,
  Bell,
  User,
  ArrowRight,
  Sparkles,
  FileText,
  CheckCircle,
  ChevronRight,
  ArrowLeft,
  MessageCircle,
  Send,
  X,
  Bookmark,
  ClipboardList,
  Bot,
  ExternalLink,
  Mic,
  Trash2
} from "lucide-react";

import Situation from "./pages/Situation";
import { allSchemesData } from "./data/schemesData";
import "./i18n";
import "./App.css";

const API_BASE = "http://127.0.0.1:5000";

const onboardingData = [
  {
    image: "/src/assets/onboarding-1.png",
    titleKey: "onboarding.slide1.title",
    textKey: "onboarding.slide1.text",
    title: "Discover schemes made for you",
    text: "Over 1,400 central and state schemes in one place, filtered down to the ones you can actually claim."
  },
  {
    image: "/src/assets/onboarding-2.png",
    titleKey: "onboarding.slide2.title",
    textKey: "onboarding.slide2.text",
    title: "Speak in your own language",
    text: "Use Telugu, Tamil, Hindi, Kannada, Malayalam, Marathi or English — by typing or by voice."
  },
  {
    image: "/src/assets/onboarding-3.png",
    titleKey: "onboarding.slide3.title",
    textKey: "onboarding.slide3.text",
    title: "The AI understands your situation",
    text: "Describe your life in ordinary words. We turn it into a profile and check it against real eligibility rules."
  },
  {
    image: "/src/assets/onboarding-4.png",
    titleKey: "onboarding.slide4.title",
    textKey: "onboarding.slide4.text",
    title: "Track applications and updates",
    text: "Follow every application from submission to benefit release, and get reminded before deadlines close."
  }
];

const languages = [
  ["English", "en", "English · All India", "Find schemes made for you"],
  ["తెలుగు", "te", "Telugu · Andhra Pradesh · Telangana", "మీ కోసం రూపొందించిన పథకాలు"],
  ["தமிழ்", "ta", "Tamil · Tamil Nadu · Puducherry", "உங்களுக்கான திட்டங்களைக் காண்க"],
  ["हिन्दी", "hi", "Hindi · North India", "आपके लिए बनी योजनाएँ खोजें"],
  ["ಕನ್ನಡ", "kn", "Kannada · Karnataka", "ನಿಮಗಾಗಿ ಇರುವ ಯೋಜನೆಗಳನ್ನು ಹುಡುಕಿ"],
  ["മലയാളം", "ml", "Malayalam · Kerala", "നിങ്ങൾക്കായുള്ള പദ്ധതികൾ കാണുക"],
  ["मराठी", "mr", "Marathi · Maharashtra", "तुमच्यासाठी योजना शोधा"]
];

export const availableSchemesData = allSchemesData;
const popularSchemes = availableSchemesData.slice(0, 4);

function getStoredAccount() {
  try {
    const raw = localStorage.getItem("schemematch_current_user") || localStorage.getItem("schemematch_account");
    return raw ? JSON.parse(raw) : null;
  } catch {
    return null;
  }
}

function getStoredSavedSchemes() {
  try {
    const raw = localStorage.getItem("schemematch_saved_schemes");
    return raw ? JSON.parse(raw) : [];
  } catch {
    return [];
  }
}

function App() {
  const { t, i18n } = useTranslation();
  const [screen, setScreen] = useState("splash");
  const [slide, setSlide] = useState(0);
  const [language, setLanguage] = useState(() => {
    const saved = localStorage.getItem("language") || "en";
    const match = languages.find(([, code]) => code === saved);
    return match ? match[0] : "English";
  });

  const [loginMode, setLoginMode] = useState("login");
  const [fullName, setFullName] = useState("");
  const [mobile, setMobile] = useState("");
  const [otp, setOtp] = useState("");
  const [otpSent, setOtpSent] = useState(false);
  const [sendingOtp, setSendingOtp] = useState(false);
  const [verifyingOtp, setVerifyingOtp] = useState(false);
  const [otpMessage, setOtpMessage] = useState("");
  const [otpError, setOtpError] = useState("");
  const [currentUser, setCurrentUser] = useState(() => getStoredAccount());

  const [savedSchemeIds, setSavedSchemeIds] = useState(getStoredSavedSchemes);
  const [activePanel, setActivePanel] = useState(null);
  const [selectedScheme, setSelectedScheme] = useState(null);

  useEffect(() => {
    const saved = localStorage.getItem("language");
    if (saved && i18n.language !== saved) {
      i18n.changeLanguage(saved);
    }
  }, [i18n]);

  useEffect(() => {
    if (screen !== "splash") return;
    const timer = setTimeout(() => setScreen("onboarding"), 2200);
    return () => clearTimeout(timer);
  }, [screen]);

  const isSchemeSaved = (id) => savedSchemeIds.includes(id);

  const toggleSaveScheme = (scheme) => {
    if (!scheme || !scheme.id) return;
    const isSaved = savedSchemeIds.includes(scheme.id);
    const updated = isSaved
      ? savedSchemeIds.filter((id) => id !== scheme.id)
      : [...savedSchemeIds, scheme.id];
    setSavedSchemeIds(updated);
    localStorage.setItem("schemematch_saved_schemes", JSON.stringify(updated));
  };

  const nextSlide = () => {
    if (slide < 3) setSlide((value) => value + 1);
    else setScreen("language");
  };

  const previousSlide = () => {
    if (slide > 0) setSlide((value) => value - 1);
  };

  const handleSelectLanguage = (name, code) => {
    setLanguage(name);
    i18n.changeLanguage(code);
    localStorage.setItem("language", code);
  };

  const switchLoginMode = (mode) => {
    setLoginMode(mode);
    setOtpSent(false);
    setOtp("");
    setOtpMessage("");
    setOtpError("");
  };

  const sendOtp = async () => {
    setOtpError("");
    setOtpMessage("");

    if (loginMode === "signup" && !fullName.trim()) {
      setOtpError(t("errors.mobileRequired") || "Please enter your full name.");
      return;
    }

    if (!/^\d{10}$/.test(mobile)) {
      setOtpError(t("errors.invalidMobile") || "Please enter a valid 10-digit mobile number.");
      return;
    }

    setSendingOtp(true);

    try {
      const response = await fetch(`${API_BASE}/send-otp`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          mobile,
          mode: loginMode,
          name: fullName.trim()
        })
      });
      const data = await response.json();

      if (!response.ok || !data.success) {
        setOtpError(data.message || t("errors.sendOtpFailed") || "Unable to send OTP.");
        return;
      }

      setOtpSent(true);
      setOtpMessage(`${t("login.demoOtp") || "Demo OTP"}: ${data.otp}`);
    } catch (error) {
      console.error(error);
      setOtpError(t("errors.backend") || "Backend is not connected. Start Flask on port 5000.");
    } finally {
      setSendingOtp(false);
    }
  };

  const verifyOtp = async () => {
    setOtpError("");

    if (!/^\d{6}$/.test(otp)) {
      setOtpError(t("errors.otpRequired") || "Please enter the 6-digit OTP.");
      return;
    }

    setVerifyingOtp(true);

    try {
      const response = await fetch(`${API_BASE}/verify-otp`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ mobile, otp })
      });
      const data = await response.json();

      if (!response.ok || !data.success) {
        setOtpError(data.message || t("errors.invalidOtp") || "Invalid OTP.");
        return;
      }

      const account = data.user || {
        name: fullName.trim() || "User",
        mobile,
        language,
        createdAt: new Date().toISOString()
      };

      localStorage.setItem("schemematch_account", JSON.stringify(account));
      localStorage.setItem("schemematch_current_user", JSON.stringify(account));
      setCurrentUser(account);
      setOtp("");
      setOtpSent(false);
      setOtpMessage("");
      setScreen("dashboard");
    } catch (error) {
      console.error(error);
      setOtpError(t("errors.backend") || "Backend is not connected. Start Flask on port 5000.");
    } finally {
      setVerifyingOtp(false);
    }
  };

  const logout = () => {
    localStorage.removeItem("schemematch_current_user");
    setCurrentUser(null);
    setActivePanel(null);
    setScreen("login");
  };

  if (screen === "splash") {
    return (
      <div className="splash-screen">
        <div className="splash-content">
          <div className="splash-logo"><span>✓</span></div>
          <h1>SchemeMatch</h1>
          <p>{t("splash.line1") || "Connecting Citizens with the Right Government"}<br />{t("splash.line2") || "Benefits."}</p>
          <div className="splash-progress"><div className="splash-progress-fill" /></div>
        </div>
      </div>
    );
  }

  if (screen === "onboarding") {
    const current = onboardingData[slide];
    return (
      <div className="app-page onboarding-page">
        <header className="top-header">
          <div className="brand"><div className="brand-icon">✓</div><span>SchemeMatch</span></div>
          <button className="skip-button" type="button" onClick={() => setScreen("language")}>{t("common.skip") || "Skip"}</button>
        </header>
        <main className="onboarding-content">
          <div className="onboarding-image"><img src={current.image} alt={t(current.titleKey) || current.title} /></div>
          <div className="onboarding-text">
            <div className="slide-number">{slide + 1} / 4</div>
            <h1>{t(current.titleKey) || current.title}</h1>
            <p>{t(current.textKey) || current.text}</p>
          </div>
        </main>
        <footer className="onboarding-footer">
          <div className="dots">
            {onboardingData.map((_, index) => (
              <span key={index} className={`dot ${index === slide ? "active" : ""}`} />
            ))}
          </div>
          <div className="footer-buttons">
            {slide > 0 && <button className="back-button" type="button" onClick={previousSlide}>{t("common.back") || "Back"}</button>}
            <button className="next-button" type="button" onClick={nextSlide}>
              {slide === 3 ? (t("common.getStarted") || "Get started") : (t("common.next") || "Next")}<span>→</span>
            </button>
          </div>
        </footer>
      </div>
    );
  }

  if (screen === "language") {
    return (
      <div className="app-page language-page">
        <header className="top-header">
          <div className="brand"><div className="brand-icon">✓</div><span>SchemeMatch</span></div>
        </header>
        <main className="language-content">
          <h1>{t("language.title") || "Choose your language"}</h1>
          <p className="language-intro">{t("language.note") || "The whole app switches to the language you pick. You can change it any time from Settings."}</p>
          <div className="language-grid">
            {languages.map(([name, code, region, description]) => (
              <button key={code} type="button" className={`language-card ${language === name ? "selected" : ""}`} onClick={() => handleSelectLanguage(name, code)}>
                <div className="language-info"><h2>{name}</h2><p>{region}</p><span>{description}</span></div>
                <div className="radio">{language === name && "✓"}</div>
              </button>
            ))}
          </div>
          <button className="continue-button" type="button" onClick={() => setScreen("login")}>
            {t("language.continueIn") || "Continue in"} {language}
          </button>
          <p className="language-note">{t("language.note") || "You can change it any time from Settings."}</p>
        </main>
      </div>
    );
  }

  if (screen === "login") {
    return (
      <div className="login-page">
        <div className="login-header">
          <div className="brand"><div className="brand-icon">✓</div><span>SchemeMatch</span></div>
          <div className="language-small">{language === "English" ? "EN" : language}</div>
        </div>
        <main className="login-container">
          <div className="login-card">
            {!otpSent ? (
              <>
                <div className="login-tabs">
                  <button type="button" className={loginMode === "login" ? "active" : ""} onClick={() => switchLoginMode("login")}>{t("login.loginTab") || "Login"}</button>
                  <button type="button" className={loginMode === "signup" ? "active" : ""} onClick={() => switchLoginMode("signup")}>{t("login.signupTab") || "Sign Up"}</button>
                </div>

                <div className="login-title">
                  <h1>{loginMode === "login" ? (t("login.welcome") || "Welcome Back!") : (t("login.createAccount") || "Create your account")}</h1>
                  <p>{loginMode === "login" ? (t("login.loginUsingMobile") || "Login using your registered mobile number") : (t("login.signupUsingMobile") || "Sign up using your name and mobile number")}</p>
                </div>

                {loginMode === "signup" && (
                  <>
                    <label htmlFor="full-name">{t("login.fullName") || "Full Name"}</label>
                    <input id="full-name" className="full-name-input" type="text" placeholder={t("login.enterFullName") || "Enter your full name"} value={fullName} onChange={(e) => setFullName(e.target.value)} />
                  </>
                )}

                <label htmlFor="mobile">{t("login.mobileNumber") || "Mobile Number"}</label>
                <div className="mobile-input">
                  <span>+91</span>
                  <input id="mobile" type="tel" placeholder={t("login.enterMobile") || "Enter 10 digit mobile number"} value={mobile} onChange={(e) => setMobile(e.target.value.replace(/\D/g, ""))} maxLength="10" />
                </div>

                {otpError && <p className="otp-error">{otpError}</p>}

                <button className="otp-button" type="button" onClick={sendOtp} disabled={sendingOtp}>
                  {sendingOtp ? (t("login.generatingOtp") || "Generating OTP...") : loginMode === "signup" ? (t("login.createAccount") || "Create Account & Send OTP") : (t("common.sendOtp") || "Send OTP")}
                </button>

                <p className="terms">{t("login.termsLine") || "By continuing, you agree to our"}<br /><span>{t("login.termsPolicy") || "Terms & Privacy Policy"}</span></p>
              </>
            ) : (
              <>
                <button className="otp-back" type="button" onClick={() => { setOtpSent(false); setOtp(""); setOtpError(""); setOtpMessage(""); }}>
                  <ArrowLeft size={18} /> {t("common.changeNumber") || "Change number"}
                </button>
                <div className="login-title">
                  <h1>{t("login.enterOtp") || "Enter your OTP"}</h1>
                  <p>{t("login.otpDescription") || "We generated a 6-digit OTP for"}<br />+91 {mobile}</p>
                </div>
                <label htmlFor="otp">{t("login.oneTimePassword") || "One-Time Password"}</label>
                <input id="otp" className="otp-input" type="text" inputMode="numeric" placeholder={t("login.enterSixDigitOtp") || "Enter 6-digit OTP"} value={otp} onChange={(e) => setOtp(e.target.value.replace(/\D/g, "").slice(0, 6))} maxLength="6" />
                {otpMessage && <div className="otp-demo">{otpMessage}</div>}
                {otpError && <p className="otp-error">{otpError}</p>}
                <button className="otp-button" type="button" onClick={verifyOtp} disabled={verifyingOtp}>{verifyingOtp ? (t("login.verifying") || "Verifying...") : (t("common.verifyOtp") || "Verify OTP")}</button>
                <button className="resend-button" type="button" onClick={sendOtp} disabled={sendingOtp}>{sendingOtp ? (t("login.generating") || "Generating...") : (t("common.resendOtp") || "Resend OTP")}</button>
              </>
            )}
          </div>
        </main>
      </div>
    );
  }

  if (screen === "situation") {
    return (
      <Situation
        onBack={() => setScreen("dashboard")}
        savedSchemeIds={savedSchemeIds}
        isSchemeSaved={isSchemeSaved}
        toggleSaveScheme={toggleSaveScheme}
      />
    );
  }

  return (
    <Dashboard
      user={currentUser || getStoredAccount()}
      onStart={() => setScreen("situation")}
      activePanel={activePanel}
      setActivePanel={setActivePanel}
      selectedScheme={selectedScheme}
      setSelectedScheme={setSelectedScheme}
      savedSchemeIds={savedSchemeIds}
      isSchemeSaved={isSchemeSaved}
      toggleSaveScheme={toggleSaveScheme}
      onLogout={logout}
    />
  );
}

function Dashboard({
  user,
  onStart,
  activePanel,
  setActivePanel,
  selectedScheme,
  setSelectedScheme,
  savedSchemeIds = [],
  isSchemeSaved = () => false,
  toggleSaveScheme = () => {},
  onLogout
}) {
  const { t, i18n } = useTranslation();
  const [chatMessages, setChatMessages] = useState([
    {
      role: "assistant",
      content: t("ai.greeting") || "Hello. I am the SchemeMatch AI Assistant. Ask me about government schemes, eligibility, benefits, documents or applications."
    }
  ]);
  const [chatInput, setChatInput] = useState("");
  const [chatLoading, setChatLoading] = useState(false);
  const [chatListening, setChatListening] = useState(false);
  const chatMessagesEndRef = useRef(null);
  const chatRecognitionRef = useRef(null);

  // Scheme Directory Search and Pagination
  const [directorySearch, setDirectorySearch] = useState("");
  const [directoryLimit, setDirectoryLimit] = useState(30);

  const filteredDirectorySchemes = useMemo(() => {
    const q = directorySearch.trim().toLowerCase();
    if (!q) return availableSchemesData;
    return availableSchemesData.filter((s) => {
      const nameMatch = s.name && s.name.toLowerCase().includes(q);
      const catMatch = s.category && s.category.toLowerCase().includes(q);
      const descMatch = s.description && s.description.toLowerCase().includes(q);
      const stateMatch = s.state && s.state.toLowerCase().includes(q);
      const kwMatch = s.keywords && s.keywords.some((k) => k.toLowerCase().includes(q));
      return nameMatch || catMatch || descMatch || stateMatch || kwMatch;
    });
  }, [directorySearch]);

  useEffect(() => {
    if (activePanel === "chatbot") {
      chatMessagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    }
  }, [chatMessages, chatLoading, activePanel]);

  // Speech to text for AI assistant
  const handleChatVoice = () => {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) {
      alert(t("voice.unsupported") || "Speech recognition is not supported in this browser. Please use Chrome or Edge.");
      return;
    }

    if (chatListening && chatRecognitionRef.current) {
      chatRecognitionRef.current.stop();
      setChatListening(false);
      return;
    }

    const recognition = new SpeechRecognition();
    recognition.continuous = false;
    recognition.interimResults = true;
    recognition.maxAlternatives = 1;

    const languageMap = {
      en: "en-IN",
      hi: "hi-IN",
      ta: "ta-IN",
      te: "te-IN",
      kn: "kn-IN",
      ml: "ml-IN",
      mr: "mr-IN"
    };
    recognition.lang = languageMap[i18n.language] || "en-IN";

    recognition.onstart = () => {
      setChatListening(true);
    };

    recognition.onresult = (event) => {
      let transcript = "";
      for (let i = event.resultIndex; i < event.results.length; i++) {
        transcript += event.results[i][0].transcript;
      }
      if (transcript) {
        setChatInput(transcript);
      }
    };

    recognition.onerror = (event) => {
      console.error("Chat voice error:", event.error);
      setChatListening(false);
    };

    recognition.onend = () => {
      setChatListening(false);
    };

    chatRecognitionRef.current = recognition;
    try {
      recognition.start();
    } catch (e) {
      console.error("Speech start error:", e);
      setChatListening(false);
    }
  };

  const sendChatMessage = async () => {
    const message = chatInput.trim();
    if (!message || chatLoading) return;

    const nextMessages = [...chatMessages, { role: "user", content: message }];
    setChatMessages(nextMessages);
    setChatInput("");
    setChatLoading(true);

    try {
      const response = await fetch(`${API_BASE}/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          message,
          history: nextMessages.slice(-6),
          language: i18n.language || "en"
        })
      });

      if (!response.ok) {
        throw new Error("Unable to connect to assistant");
      }

      if (!response.body) {
        throw new Error("ReadableStream not supported");
      }

      const reader = response.body.getReader();
      const decoder = new TextDecoder("utf-8");
      let done = false;
      let assistantReply = "";
      let isFirstChunk = true;

      while (!done) {
        const { value, done: readerDone } = await reader.read();
        done = readerDone;
        if (value) {
          const chunk = decoder.decode(value, { stream: !done });
          if (chunk) {
            if (isFirstChunk) {
              isFirstChunk = false;
              setChatLoading(false);
              assistantReply = chunk;
              setChatMessages((current) => [
                ...current,
                { role: "assistant", content: assistantReply }
              ]);
            } else {
              assistantReply += chunk;
              setChatMessages((current) => {
                const updated = [...current];
                if (updated.length > 0) {
                  updated[updated.length - 1] = {
                    role: "assistant",
                    content: assistantReply
                  };
                }
                return updated;
              });
            }
          }
        }
      }
    } catch (error) {
      console.error(error);
      setChatMessages((current) => [
        ...current,
        {
          role: "assistant",
          content: t("ai.error") || "AI Assistant is currently unavailable. Please make sure Ollama is running."
        }
      ]);
    } finally {
      setChatLoading(false);
    }
  };

  const handleChatKeyDown = (event) => {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      sendChatMessage();
    }
  };

  const savedSchemesList = availableSchemesData.filter((scheme) => isSchemeSaved(scheme.id));

  const totalDisplayCount = availableSchemesData.length >= 1400 ? "1,400+" : `${availableSchemesData.length}`;

  return (
    <div className="home-page">
      <header className="home-header">
        <div className="brand"><div className="brand-icon">✓</div><span>SchemeMatch</span></div>
        <div className="home-actions">
          <button className="header-icon" type="button" aria-label={t("profile.eyebrow") || "Notifications"} onClick={() => setActivePanel("notifications")}><Bell size={20} /></button>
          <button className="profile-icon" type="button" aria-label={t("nav.profile") || "Profile"} onClick={() => setActivePanel("profile")}><User size={19} /></button>
        </div>
      </header>

      <main className="home-content">
        <section className="home-welcome">
          <div>
            <p className="small-label">{t("dashboard.welcome") || "WELCOME BACK"}</p>
            <h1>{t("dashboard.titleLine1") || "Find benefits made"}<br />{t("dashboard.titleLine2") || "for your situation."}</h1>
            <p className="home-description">{t("dashboard.description") || "Tell us about your situation in your own words and we'll find the government schemes you may be eligible for."}</p>
          </div>
          <div className="welcome-status"><CheckCircle size={18} /><span>{t("dashboard.profileReady") || "Profile ready"}</span></div>
        </section>

        <section className="ai-check-card">
          <div className="ai-check-icon"><Sparkles size={24} /></div>
          <div className="ai-check-content">
            <p className="small-label">{t("dashboard.eligibilityLabel") || "AI ELIGIBILITY CHECK"}</p>
            <h2>{t("dashboard.checkTitle") || "What can SchemeMatch find for you?"}</h2>
            <p>{t("dashboard.checkDescription") || "Describe your occupation, income, family, education, land or any other details. Our NLP engine will understand your situation and identify matching schemes."}</p>
            <button className="start-check-button" type="button" onClick={onStart}>
              {t("dashboard.startCheck") || "Start eligibility check"} <ArrowRight size={18} />
            </button>
          </div>
        </section>

        <section className="home-stats">
          <div className="home-section-title"><h2>{t("dashboard.overview") || "Your overview"}</h2></div>
          <div className="home-stat-grid">
            <button className="home-stat-card clickable-card" type="button" onClick={() => setActivePanel("schemes")}>
              <div className="stat-icon"><FileText size={20} /></div>
              <strong>{totalDisplayCount}</strong>
              <span>{t("dashboard.schemesAvailable") || "Schemes available"}</span>
            </button>
            <button className="home-stat-card clickable-card" type="button" onClick={() => setActivePanel("applications")}>
              <div className="stat-icon"><ClipboardList size={20} /></div>
              <strong>0</strong>
              <span>{t("dashboard.applications") || "Applications"}</span>
            </button>
            <button className="home-stat-card clickable-card" type="button" onClick={() => setActivePanel("saved")}>
              <div className="stat-icon"><Bookmark size={20} /></div>
              <strong>{savedSchemeIds.length}</strong>
              <span>{t("dashboard.savedSchemes") || "Saved schemes"}</span>
            </button>
          </div>
        </section>

        <section className="popular-section">
          <div className="popular-heading">
            <div><p className="small-label">{t("dashboard.explore") || "EXPLORE"}</p><h2>{t("dashboard.popularSchemes") || "Popular schemes"}</h2></div>
            <button className="view-all" type="button" onClick={() => setActivePanel("schemes")}>
              {t("directory.title") || "Scheme Directory"} <ChevronRight size={17} />
            </button>
          </div>
          <div className="scheme-list">
            {popularSchemes.map((scheme) => (
              <div
                key={scheme.id}
                className="home-scheme-card"
                style={{ cursor: "pointer", position: "relative" }}
                onClick={() => setSelectedScheme(scheme)}
              >
                <div className="scheme-symbol">{scheme.symbol || "🏛️"}</div>
                <div className="scheme-info" style={{ flex: 1 }}>
                  <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                    <span>{scheme.category}</span>
                    <button
                      className={`scheme-bookmark-btn ${isSchemeSaved(scheme.id) ? "saved" : ""}`}
                      type="button"
                      onClick={(e) => {
                        e.stopPropagation();
                        toggleSaveScheme(scheme);
                      }}
                      title={isSchemeSaved(scheme.id) ? (t("saved.unsave") || "Unsave") : (t("saved.save") || "Save")}
                    >
                      <Bookmark size={16} fill={isSchemeSaved(scheme.id) ? "#087f75" : "none"} color={isSchemeSaved(scheme.id) ? "#087f75" : "#64748b"} />
                      <span>{isSchemeSaved(scheme.id) ? (t("saved.saved") || "Saved") : (t("saved.save") || "Save")}</span>
                    </button>
                  </div>
                  <h3>{scheme.name}</h3>
                  <p>{scheme.description}</p>
                </div>
                <ArrowRight size={19} color="#087f75" />
              </div>
            ))}
          </div>
        </section>
      </main>

      <nav className="bottom-nav" aria-label="Main navigation">
        <button className="nav-item active" type="button"><Search size={20} /><span>{t("nav.home") || "Home"}</span></button>
        <button className="nav-item" type="button" onClick={() => setActivePanel("applications")}><FileText size={20} /><span>{t("dashboard.myApplications") || "My Applications"}</span></button>
        <button className="nav-item ai-nav-item" type="button" onClick={() => setActivePanel("chatbot")}><MessageCircle size={23} /><span>{t("nav.aiAssistant") || "AI Assistant"}</span></button>
        <button className="nav-item" type="button" onClick={() => setActivePanel("saved")}><Bookmark size={20} /><span>{t("nav.saved") || "Saved"}</span></button>
        <button className="nav-item" type="button" onClick={() => setActivePanel("profile")}><User size={20} /><span>{t("nav.profile") || "Profile"}</span></button>
      </nav>

      {activePanel === "profile" && (
        <PanelOverlay onClose={() => setActivePanel(null)}>
          <div className="panel-header"><div><p className="eyebrow">{t("profile.eyebrow") || "PROFILE"}</p><h2>{t("profile.title") || "Your profile"}</h2></div><CloseButton onClick={() => setActivePanel(null)} /></div>
          <div className="profile-panel-content">
            <div className="profile-avatar"><User size={30} /></div>
            <h3>{user?.name || t("profile.guestUser") || "User"}</h3>
            <p>{t("dashboard.profileReady") || "Your profile is ready."}</p>
            <div className="profile-details">
              <div><span>{t("login.fullName") || "Name"}</span><strong>{user?.name || "User"}</strong></div>
              <div><span>{t("profile.phone") || "Mobile Number"}</span><strong>+91 {user?.mobile || "Not available"}</strong></div>
              <div><span>{t("profile.language") || "Language"}</span><strong>{user?.language || i18n.language || "English"}</strong></div>
              <div><span>{t("profile.savedSchemesCount") || "Saved Schemes"}</span><strong>{savedSchemeIds.length}</strong></div>
            </div>
            <div className="profile-status"><CheckCircle size={17} /> {t("profile.verifiedUser") || "Account verified"}</div>
            <button className="primary-button" type="button" onClick={onLogout}>{t("profile.logout") || "Log out"}</button>
          </div>
        </PanelOverlay>
      )}

      {activePanel === "notifications" && (
        <PanelOverlay onClose={() => setActivePanel(null)}>
          <div className="panel-header"><div><p className="eyebrow">UPDATES</p><h2>Notifications</h2></div><CloseButton onClick={() => setActivePanel(null)} /></div>
          <div className="notification-item"><div className="notification-icon"><CheckCircle size={20} /></div><div><strong>Profile ready</strong><p>Your account is ready. Describe your situation to find matching schemes.</p></div></div>
          <div className="notification-item"><div className="notification-icon"><Sparkles size={20} /></div><div><strong>AI assistant available</strong><p>You can ask the SchemeMatch AI Assistant about schemes, eligibility and documents.</p></div></div>
        </PanelOverlay>
      )}

      {activePanel === "applications" && (
        <PanelOverlay onClose={() => setActivePanel(null)}>
          <div className="panel-header"><div><p className="eyebrow">APPLICATIONS</p><h2>{t("dashboard.myApplications") || "My Applications"}</h2></div><CloseButton onClick={() => setActivePanel(null)} /></div>
          <div className="empty-panel">
            <ClipboardList size={42} />
            <h3>No applications yet</h3>
            <p>Your submitted scheme applications will appear here.</p>
          </div>
        </PanelOverlay>
      )}

      {activePanel === "saved" && (
        <PanelOverlay onClose={() => setActivePanel(null)}>
          <div className="panel-header">
            <div>
              <p className="eyebrow">{t("saved.eyebrow") || "SAVED"}</p>
              <h2>{t("saved.title") || "Saved Schemes"}</h2>
            </div>
            <CloseButton onClick={() => setActivePanel(null)} />
          </div>

          {savedSchemesList.length > 0 ? (
            <div className="saved-schemes-panel-list">
              <p style={{ margin: "0 0 14px", color: "#64748b", fontSize: "14px" }}>
                {t("saved.subtitle") || "Review and manage your saved government schemes for quick access."}
              </p>
              <div className="panel-scheme-list">
                {savedSchemesList.map((scheme) => {
                  const rawUrl = scheme.officialUrl || scheme.official_url || scheme.officialWebsite || scheme.url;
                  const validUrl = rawUrl && typeof rawUrl === "string" && rawUrl.trim()
                    ? (rawUrl.trim().startsWith("http://") || rawUrl.trim().startsWith("https://") ? rawUrl.trim() : `https://${rawUrl.trim()}`)
                    : null;

                  return (
                    <div key={scheme.id} className="saved-scheme-card">
                      <div style={{ display: "flex", gap: "12px", alignItems: "flex-start" }}>
                        <div className="scheme-symbol">{scheme.symbol || "🏛️"}</div>
                        <div style={{ flex: 1 }}>
                          <span className="match-category">{scheme.category}</span>
                          <h3 style={{ margin: "4px 0 6px", color: "#10233f", fontSize: "16px" }}>{scheme.name}</h3>
                          <p style={{ margin: 0, color: "#475569", fontSize: "13px", lineHeight: "1.5" }}>{scheme.description}</p>
                        </div>
                      </div>
                      <div style={{ display: "flex", gap: "8px", marginTop: "12px", flexWrap: "wrap" }}>
                        <button
                          className="card-button"
                          type="button"
                          style={{ padding: "6px 12px", fontSize: "13px" }}
                          onClick={() => {
                            setSelectedScheme(scheme);
                            setActivePanel(null);
                          }}
                        >
                          {t("directory.viewDetails") || "View Details"}
                          <ExternalLink size={14} />
                        </button>
                        {validUrl ? (
                          <button
                            className="primary-button"
                            type="button"
                            style={{ padding: "6px 12px", fontSize: "13px" }}
                            onClick={() => window.open(validUrl, "_blank", "noopener,noreferrer")}
                          >
                            {t("directory.officialWebsite") || "Official Website"}
                            <ExternalLink size={14} />
                          </button>
                        ) : null}
                        <button
                          className="card-button"
                          type="button"
                          style={{ padding: "6px 10px", fontSize: "13px", color: "#dc2626", borderColor: "#fecaca" }}
                          onClick={() => toggleSaveScheme(scheme)}
                          title={t("saved.unsave") || "Remove from saved"}
                        >
                          <Trash2 size={14} />
                          {t("saved.remove") || "Remove"}
                        </button>
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>
          ) : (
            <div className="empty-panel">
              <Bookmark size={42} color="#087f75" />
              <h3>{t("saved.emptyTitle") || "No saved schemes yet"}</h3>
              <p>{t("saved.emptyDesc") || "Click the Save button on any scheme to keep track of it here."}</p>
            </div>
          )}
        </PanelOverlay>
      )}

      {activePanel === "schemes" && (
        <PanelOverlay onClose={() => setActivePanel(null)}>
          <div className="panel-header">
            <div>
              <p className="eyebrow">{t("directory.eyebrow") || "SCHEME DIRECTORY"}</p>
              <h2>{t("directory.title") || "Available Government Schemes"}</h2>
            </div>
            <CloseButton onClick={() => setActivePanel(null)} />
          </div>

          <div className="directory-search-bar" style={{ margin: "0 0 16px", position: "relative" }}>
            <Search size={18} color="#64748b" style={{ position: "absolute", left: "14px", top: "50%", transform: "translateY(-50%)" }} />
            <input
              type="text"
              placeholder={t("directory.searchPlaceholder") || "Search schemes by name, keyword or category..."}
              value={directorySearch}
              onChange={(e) => {
                setDirectorySearch(e.target.value);
                setDirectoryLimit(30);
              }}
              style={{
                width: "100%",
                padding: "12px 14px 12px 42px",
                borderRadius: "10px",
                border: "1.5px solid #cbdbe0",
                fontSize: "14px",
                outline: "none",
                boxSizing: "border-box"
              }}
            />
          </div>

          <p style={{ margin: "0 0 14px", color: "#64748b", fontSize: "13px" }}>
            Showing {Math.min(directoryLimit, filteredDirectorySchemes.length)} of {filteredDirectorySchemes.length} schemes. Click any scheme to view details.
          </p>

          <div className="panel-scheme-list" style={{ maxHeight: "460px", overflowY: "auto" }}>
            {filteredDirectorySchemes.slice(0, directoryLimit).map((scheme) => (
              <div
                key={scheme.id}
                className="panel-scheme-row"
                style={{ cursor: "pointer", display: "flex", alignItems: "center", gap: "10px" }}
                onClick={() => {
                  setSelectedScheme(scheme);
                  setActivePanel(null);
                }}
              >
                <div className="scheme-symbol">{scheme.symbol || "🏛️"}</div>
                <div className="scheme-info" style={{ flex: 1 }}>
                  <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                    <span>{scheme.category}</span>
                    <button
                      className={`scheme-bookmark-btn ${isSchemeSaved(scheme.id) ? "saved" : ""}`}
                      type="button"
                      onClick={(e) => {
                        e.stopPropagation();
                        toggleSaveScheme(scheme);
                      }}
                      title={isSchemeSaved(scheme.id) ? (t("saved.unsave") || "Unsave") : (t("saved.save") || "Save")}
                    >
                      <Bookmark size={15} fill={isSchemeSaved(scheme.id) ? "#087f75" : "none"} color={isSchemeSaved(scheme.id) ? "#087f75" : "#64748b"} />
                      <span>{isSchemeSaved(scheme.id) ? (t("saved.saved") || "Saved") : (t("saved.save") || "Save")}</span>
                    </button>
                  </div>
                  <h3>{scheme.name}</h3>
                  <p>{scheme.description}</p>
                </div>
                <ChevronRight size={18} />
              </div>
            ))}

            {filteredDirectorySchemes.length > directoryLimit && (
              <button
                className="card-button"
                type="button"
                style={{ width: "100%", marginTop: "14px", padding: "10px", textAlign: "center" }}
                onClick={() => setDirectoryLimit((prev) => prev + 30)}
              >
                Load More Schemes ({filteredDirectorySchemes.length - directoryLimit} remaining)
              </button>
            )}

            {filteredDirectorySchemes.length === 0 && (
              <div style={{ textAlign: "center", padding: "30px 10px", color: "#64748b" }}>
                <p>No schemes matched "{directorySearch}". Try a different keyword like "farmer", "health", "housing", "scholarship", "women".</p>
              </div>
            )}
          </div>
        </PanelOverlay>
      )}

      {selectedScheme && (
        <PanelOverlay onClose={() => setSelectedScheme(null)}>
          <div className="panel-header">
            <div>
              <p className="eyebrow">SCHEME DETAILS</p>
              <h2>{selectedScheme.name}</h2>
            </div>
            <CloseButton onClick={() => setSelectedScheme(null)} />
          </div>
          <div className="scheme-panel-content">
            <div className="scheme-symbol large">{selectedScheme.symbol || "🏛️"}</div>
            <h3>{selectedScheme.name}</h3>
            <span className="scheme-panel-category">{selectedScheme.category}</span>
            <p>{selectedScheme.description}</p>

            {selectedScheme.benefits && (
              <div style={{ margin: "16px 0", textAlign: "left" }}>
                <strong style={{ display: "block", marginBottom: "6px", color: "#1e293b", fontSize: "14px" }}>{t("directory.keyBenefits") || "Key Benefits"}:</strong>
                <ul style={{ margin: 0, paddingLeft: "20px", color: "#475569", fontSize: "14px" }}>
                  {selectedScheme.benefits.map((b, i) => (
                    <li key={i} style={{ marginBottom: "4px" }}>{b}</li>
                  ))}
                </ul>
              </div>
            )}

            {selectedScheme.eligibility && (
              <div style={{ margin: "16px 0", textAlign: "left" }}>
                <strong style={{ display: "block", marginBottom: "6px", color: "#1e293b", fontSize: "14px" }}>{t("directory.eligibility") || "Eligibility Criteria"}:</strong>
                <ul style={{ margin: 0, paddingLeft: "20px", color: "#475569", fontSize: "14px" }}>
                  {selectedScheme.eligibility.map((e, i) => (
                    <li key={i} style={{ marginBottom: "4px" }}>{e}</li>
                  ))}
                </ul>
              </div>
            )}

            {selectedScheme.documents && (
              <div style={{ margin: "16px 0", textAlign: "left" }}>
                <strong style={{ display: "block", marginBottom: "6px", color: "#1e293b", fontSize: "14px" }}>{t("directory.documents") || "Required Documents"}:</strong>
                <ul style={{ margin: 0, paddingLeft: "20px", color: "#475569", fontSize: "14px" }}>
                  {selectedScheme.documents.map((d, i) => (
                    <li key={i} style={{ marginBottom: "4px" }}>{d}</li>
                  ))}
                </ul>
              </div>
            )}

            {(() => {
              const rawUrl =
                selectedScheme.officialUrl ||
                selectedScheme.official_url ||
                selectedScheme.officialWebsite ||
                selectedScheme.url;

              const validUrl = rawUrl && typeof rawUrl === "string" && rawUrl.trim()
                ? (rawUrl.trim().startsWith("http://") || rawUrl.trim().startsWith("https://") ? rawUrl.trim() : `https://${rawUrl.trim()}`)
                : null;

              return (
                <div style={{ display: "flex", gap: "10px", marginTop: "20px", flexWrap: "wrap" }}>
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
                      style={{ display: "flex", alignItems: "center", justifyContent: "center", gap: "8px", flex: 1 }}
                    >
                      {t("directory.officialWebsite") || "Official Website"}
                      <ExternalLink size={16} />
                    </button>
                  ) : (
                    <button
                      className="primary-button"
                      type="button"
                      disabled
                      style={{ opacity: 0.6, cursor: "not-allowed", flex: 1 }}
                    >
                      {t("directory.officialUnavailable") || "Official website unavailable"}
                    </button>
                  )}

                  <button
                    className={`card-button ${isSchemeSaved(selectedScheme.id) ? "saved" : ""}`}
                    type="button"
                    onClick={() => toggleSaveScheme(selectedScheme)}
                    style={{ display: "flex", alignItems: "center", justifyContent: "center", gap: "8px" }}
                  >
                    <Bookmark size={18} fill={isSchemeSaved(selectedScheme.id) ? "#087f75" : "none"} color="#087f75" />
                    {isSchemeSaved(selectedScheme.id) ? (t("saved.saved") || "Saved") : (t("saved.save") || "Save Scheme")}
                  </button>

                  <button
                    className="card-button"
                    type="button"
                    onClick={() => {
                      setSelectedScheme(null);
                      setActivePanel("chatbot");
                    }}
                    style={{ display: "flex", alignItems: "center", justifyContent: "center", gap: "8px" }}
                  >
                    <Bot size={18} /> {t("ai.askAi") || "Ask AI"}
                  </button>
                </div>
              );
            })()}
          </div>
        </PanelOverlay>
      )}

      {activePanel === "chatbot" && (
        <div className="panel-overlay" onClick={() => setActivePanel(null)}>
          <div className="chatbot-card" onClick={(event) => event.stopPropagation()}>
            <div className="panel-header">
              <div className="chatbot-title">
                <div className="chatbot-icon"><Bot size={23} /></div>
                <div>
                  <h2>{t("ai.title") || "SchemeMatch AI"}</h2>
                  <span>{t("ai.subtitle") || "Ask your questions"}</span>
                </div>
              </div>
              <CloseButton onClick={() => setActivePanel(null)} />
            </div>
            <div className="chat-messages">
              {chatMessages.map((message, index) => (
                <div key={`${message.role}-${index}`} className={`chat-message ${message.role === "user" ? "user" : "bot"}`}>
                  {message.content}
                </div>
              ))}
              {chatLoading && <div className="chat-message bot">{t("common.loading") || "Thinking..."}</div>}
              <div ref={chatMessagesEndRef} />
            </div>
            <div className="chat-input-row">
              <input
                type="text"
                placeholder={t("ai.placeholder") || "Ask anything about government schemes..."}
                value={chatInput}
                onChange={(event) => setChatInput(event.target.value)}
                onKeyDown={handleChatKeyDown}
                disabled={chatLoading}
              />
              <button
                type="button"
                className={`voice-mic-btn ${chatListening ? "listening" : ""}`}
                onClick={handleChatVoice}
                title={chatListening ? "Listening..." : "Speak question"}
                aria-label="Voice input"
              >
                <Mic size={18} color={chatListening ? "#ef4444" : "#087f75"} />
              </button>
              <button type="button" onClick={sendChatMessage} disabled={!chatInput.trim() || chatLoading} aria-label="Send message">
                <Send size={18} />
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

function CloseButton({ onClick }) {
  return <button className="panel-close" type="button" onClick={onClick} aria-label="Close"><X size={20} /></button>;
}

function PanelOverlay({ children, onClose }) {
  return <div className="panel-overlay" onClick={onClose}><div className="panel-card" onClick={(event) => event.stopPropagation()}>{children}</div></div>;
}

export default App;
