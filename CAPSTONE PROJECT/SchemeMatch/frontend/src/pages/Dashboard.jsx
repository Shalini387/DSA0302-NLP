import {
  Bell,
  User,
  ArrowRight,
  Search,
  FileText,
  CheckCircle
} from "lucide-react";

function Dashboard({ onStart }) {
  return (
    <div className="dashboard">

      <header className="topbar">

        <div className="brand">
          <div className="brand-mark">S</div>
          <span>SchemeMatch</span>
        </div>

        <div className="top-actions">

          <button className="icon-button">
            <Bell size={20} />
          </button>

          <button className="profile-button">
            <User size={18} />
            <span>Profile</span>
          </button>

        </div>

      </header>

      <main className="dashboard-content">

        <section className="welcome-section">

          <p className="eyebrow">
            PERSONALIZED ELIGIBILITY
          </p>

          <h1>
            Find government schemes
            <br />
            you're eligible for.
          </h1>

          <p className="welcome-text">
            Tell us about your situation in your own words.
            We'll analyze your information and identify suitable schemes.
          </p>

        </section>

        <section className="analysis-card">

          <div className="analysis-icon">
            <Search size={22} />
          </div>

          <div className="analysis-content">

            <h2>Check your eligibility</h2>

            <p>
              Describe your situation naturally. For example:
              "I am a farmer with 2 acres of land..."
            </p>

            <button
              className="primary-button"
              onClick={onStart}
            >
              Start Eligibility Check
              <ArrowRight size={18} />
            </button>

          </div>

        </section>

        <section className="stats-section">

          <div className="section-header">
            <h2>Your eligibility overview</h2>
          </div>

          <div className="stats-grid">

            <div className="stat-card">

              <div className="stat-icon blue">
                <FileText size={20} />
              </div>

              <h3>12</h3>

              <p>Schemes available</p>

            </div>

            <div className="stat-card">

              <div className="stat-icon green">
                <CheckCircle size={20} />
              </div>

              <h3>3</h3>

              <p>Highly matched</p>

            </div>

            <div className="stat-card">

              <div className="stat-icon orange">
                <Search size={20} />
              </div>

              <h3>5</h3>

              <p>Potential matches</p>

            </div>

          </div>

        </section>

        <section className="recommendations">

          <div className="section-header">

            <div>

              <p className="eyebrow">
                RECOMMENDED
              </p>

              <h2>
                Explore popular schemes
              </h2>

            </div>

            <button className="text-button">
              View all
              <ArrowRight size={16} />
            </button>

          </div>

          <div className="scheme-grid">

            <div className="scheme-card">

              <div className="scheme-top">

                <div className="scheme-symbol">
                  ₹
                </div>

                <span className="match-badge">
                  98% Match
                </span>

              </div>

              <h3>
                PM-KISAN
              </h3>

              <p>
                Financial support for eligible farmer families.
              </p>

              <button className="card-button">
                View details
                <ArrowRight size={16} />
              </button>

            </div>

            <div className="scheme-card">

              <div className="scheme-top">

                <div className="scheme-symbol">
                  🎓
                </div>

                <span className="match-badge">
                  92% Match
                </span>

              </div>

              <h3>
                Education Scholarship
              </h3>

              <p>
                Financial assistance for eligible students.
              </p>

              <button className="card-button">
                View details
                <ArrowRight size={16} />
              </button>

            </div>

          </div>

        </section>

      </main>

    </div>
  );
}

export default Dashboard;