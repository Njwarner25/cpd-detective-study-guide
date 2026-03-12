import { useState } from "react";
import { BookOpen, FileText, Bookmark, Trophy, Zap, Clock, ChevronRight, BarChart3, Star, Shield, Scale, Search, FileQuestion, Target, AlertTriangle, Monitor, PenTool, TrendingUp, Award, Users, Menu, X, Home, Layers, ClipboardList, User } from "lucide-react";

const userData = {
  name: "Nathaniel Warner",
  flashcardsTotal: 136,
  flashcardsStudied: 9,
  scenariosTotal: 20,
  scenariosCompleted: 9,
  bookmarked: 0,
  avgScore: null,
  responses: 3,
  rank: 12,
};

const categories = [
  { id: "gold", name: "Gold Scenarios", icon: Star, desc: "Complex detective scenarios with real-world dilemmas", count: 15, color: "#f59e0b" },
  { id: "ilcs", name: "ILCS Crime Classifications", icon: Scale, desc: "Illinois Compiled Statutes crime classifications and sentencing", count: 20, color: "#8b5cf6" },
  { id: "part2", name: "Part 2 Scenarios", icon: PenTool, desc: "Timed written scenarios with AI grading", count: 20, color: "#3b82f6" },
  { id: "ranking", name: "Ranking Questions", icon: BarChart3, desc: "Priority-ordering with differential weighting", count: 40, color: "#06b6d4" },
  { id: "most", name: "Most Appropriate", icon: Target, desc: "Select the MOST appropriate action", count: 40, color: "#10b981" },
  { id: "least", name: "Least Appropriate", icon: AlertTriangle, desc: "Select the LEAST appropriate action", count: 40, color: "#ef4444" },
  { id: "legal", name: "Legal Trap", icon: Shield, desc: "Tricky legal and constitutional questions", count: 10, color: "#f97316" },
  { id: "digital", name: "Digital Evidence", icon: Monitor, desc: "Digital evidence handling and preservation", count: 8, color: "#14b8a6" },
  { id: "mini", name: "Mini Scenarios", icon: FileQuestion, desc: "Short written scenarios using R.E.A.C.T.I.O.N.", count: 15, color: "#a855f7" },
];

const leaderboard = [
  { rank: 1, name: "Bradley Anderson", avg: 87.3, best: 92 },
  { rank: 2, name: "Bell", avg: 85, best: 85 },
  { rank: 3, name: "Brandon Lange", avg: 65, best: 65 },
  { rank: 4, name: "Anabel Preciado", avg: 62.5, best: 85 },
  { rank: 5, name: "rena maritote", avg: 60, best: 60 },
];

const part2Sections = [
  { name: "Written Scenarios", desc: "Full 20-minute timed scenarios with AI grading", count: 20, icon: PenTool, color: "#3b82f6" },
  { name: "Ranking Questions", desc: "Rank actions in correct priority order using I/O differential weighting", count: 40, icon: BarChart3, color: "#06b6d4" },
  { name: "Most Appropriate", desc: "Select the BEST action for each detective scenario", count: 30, icon: Target, color: "#10b981" },
  { name: "Least Appropriate", desc: "Select the WORST action for each detective scenario", count: 30, icon: AlertTriangle, color: "#ef4444" },
  { name: "Legal Trap", desc: "Tricky legal and constitutional questions where the obvious answer is wrong", count: 30, icon: Shield, color: "#f97316" },
  { name: "Digital Evidence", desc: "Modern digital evidence handling and technology scenarios", count: 10, icon: Monitor, color: "#14b8a6" },
  { name: "Mini Scenarios", desc: "Short written scenarios with AI grading", count: 10, icon: FileQuestion, color: "#a855f7" },
];

const recentActivity = [
  { type: "scenario", title: "Gold Scenario #4", score: 78, date: "2 hours ago" },
  { type: "flashcard", title: "CPD Procedure - G02-01-03", result: "Correct", date: "Yesterday" },
  { type: "test", title: "25 Question Quiz", score: 68, date: "2 days ago" },
];

const testOptions = [
  { name: "25 Question Quiz", desc: "Quick practice test", time: "~15 min", icon: Zap, color: "#3b82f6" },
  { name: "50 Question Test", desc: "Standard practice exam", time: "~30 min", icon: FileText, color: "#8b5cf6" },
  { name: "Full Practice Exam", desc: "105 questions — Simulates actual test", time: "~90 min", icon: Trophy, color: "#f59e0b" },
];

function StatCard({ icon: Icon, value, label, sublabel, color, progress }) {
  return (
    <div style={{
      background: "linear-gradient(135deg, rgba(30,41,59,0.9), rgba(15,23,42,0.95))",
      borderRadius: 16,
      padding: "24px 20px",
      border: `1px solid ${color}22`,
      position: "relative",
      overflow: "hidden",
      transition: "all 0.3s ease",
      cursor: "pointer",
    }}
    onMouseEnter={e => { e.currentTarget.style.transform = "translateY(-2px)"; e.currentTarget.style.borderColor = `${color}55`; e.currentTarget.style.boxShadow = `0 8px 32px ${color}15`; }}
    onMouseLeave={e => { e.currentTarget.style.transform = "translateY(0)"; e.currentTarget.style.borderColor = `${color}22`; e.currentTarget.style.boxShadow = "none"; }}
    >
      <div style={{ position: "absolute", top: -20, right: -20, width: 80, height: 80, borderRadius: "50%", background: `${color}08` }} />
      <div style={{ display: "flex", alignItems: "center", gap: 12, marginBottom: 16 }}>
        <div style={{ background: `${color}18`, borderRadius: 10, padding: 8, display: "flex", alignItems: "center", justifyContent: "center" }}>
          <Icon size={20} color={color} />
        </div>
        <span style={{ color: "#94a3b8", fontSize: 13, fontWeight: 500, letterSpacing: 0.5 }}>{label}</span>
      </div>
      <div style={{ fontSize: 32, fontWeight: 700, color: "#f1f5f9", marginBottom: 4 }}>{value}</div>
      {sublabel && <div style={{ color: "#64748b", fontSize: 13 }}>{sublabel}</div>}
      {progress !== undefined && (
        <div style={{ marginTop: 12, height: 4, borderRadius: 2, background: "#1e293b" }}>
          <div style={{ height: "100%", borderRadius: 2, background: `linear-gradient(90deg, ${color}, ${color}aa)`, width: `${Math.min(progress, 100)}%`, transition: "width 1s ease" }} />
        </div>
      )}
    </div>
  );
}

function RankBadge({ rank }) {
  const medals = { 1: "\u{1F947}", 2: "\u{1F948}", 3: "\u{1F949}" };
  if (medals[rank]) return <span style={{ fontSize: 20 }}>{medals[rank]}</span>;
  return <span style={{ color: "#64748b", fontWeight: 600, fontSize: 14, width: 24, textAlign: "center", display: "inline-block" }}>{rank}</span>;
}

export default function DetectiveExamDashboard() {
  const [activeTab, setActiveTab] = useState("home");
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [searchQuery, setSearchQuery] = useState("");

  const navItems = [
    { id: "home", label: "Dashboard", icon: Home },
    { id: "cards", label: "Flashcards", icon: Layers },
    { id: "tests", label: "Practice Tests", icon: ClipboardList },
    { id: "part2", label: "Part 2 Exam", icon: PenTool },
    { id: "scenarios", label: "Scenarios", icon: FileText },
    { id: "rankings", label: "Rankings", icon: Trophy },
    { id: "profile", label: "Profile", icon: User },
  ];

  const filteredCategories = categories.filter(c =>
    c.name.toLowerCase().includes(searchQuery.toLowerCase())
  );

  return (
    <div style={{ display: "flex", minHeight: "100vh", background: "#0b1120", fontFamily: "'Inter', -apple-system, BlinkMacSystemFont, sans-serif", color: "#e2e8f0" }}>

      {/* Sidebar */}
      <aside style={{
        width: sidebarOpen ? 260 : 72,
        background: "linear-gradient(180deg, #0f172a 0%, #0b1120 100%)",
        borderRight: "1px solid #1e293b",
        transition: "width 0.3s ease",
        display: "flex",
        flexDirection: "column",
        position: "fixed",
        top: 0,
        left: 0,
        height: "100vh",
        zIndex: 50,
        overflow: "hidden",
      }}>
        {/* Logo */}
        <div style={{ padding: "20px 16px", display: "flex", alignItems: "center", gap: 12, borderBottom: "1px solid #1e293b" }}>
          <div style={{
            width: 40, height: 40, borderRadius: 10,
            background: "linear-gradient(135deg, #3b82f6, #8b5cf6)",
            display: "flex", alignItems: "center", justifyContent: "center",
            flexShrink: 0,
          }}>
            <Shield size={22} color="#fff" />
          </div>
          {sidebarOpen && (
            <div style={{ overflow: "hidden" }}>
              <div style={{ fontSize: 15, fontWeight: 700, color: "#f1f5f9", whiteSpace: "nowrap" }}>Detective Exam</div>
              <div style={{ fontSize: 11, color: "#64748b", whiteSpace: "nowrap" }}>Study Guide</div>
            </div>
          )}
          <button onClick={() => setSidebarOpen(!sidebarOpen)} style={{
            marginLeft: "auto", background: "none", border: "none", color: "#64748b",
            cursor: "pointer", padding: 4, borderRadius: 6, display: "flex",
            flexShrink: 0,
          }}>
            {sidebarOpen ? <X size={18} /> : <Menu size={18} />}
          </button>
        </div>

        {/* Nav Items */}
        <nav style={{ padding: "12px 8px", flex: 1 }}>
          {navItems.map(item => (
            <button key={item.id} onClick={() => setActiveTab(item.id)} style={{
              display: "flex", alignItems: "center", gap: 12, width: "100%",
              padding: sidebarOpen ? "10px 12px" : "10px 0",
              justifyContent: sidebarOpen ? "flex-start" : "center",
              background: activeTab === item.id ? "linear-gradient(90deg, #3b82f620, transparent)" : "transparent",
              border: "none", borderRadius: 10, color: activeTab === item.id ? "#60a5fa" : "#94a3b8",
              cursor: "pointer", marginBottom: 2, transition: "all 0.2s",
              borderLeft: activeTab === item.id ? "3px solid #3b82f6" : "3px solid transparent",
              fontSize: 14, fontWeight: activeTab === item.id ? 600 : 400,
            }}>
              <item.icon size={20} />
              {sidebarOpen && <span>{item.label}</span>}
            </button>
          ))}
        </nav>

        {/* User at bottom */}
        {sidebarOpen && (
          <div style={{ padding: "16px", borderTop: "1px solid #1e293b", display: "flex", alignItems: "center", gap: 12 }}>
            <div style={{
              width: 36, height: 36, borderRadius: "50%",
              background: "linear-gradient(135deg, #3b82f6, #8b5cf6)",
              display: "flex", alignItems: "center", justifyContent: "center",
              fontSize: 14, fontWeight: 700, color: "#fff",
            }}>NW</div>
            <div>
              <div style={{ fontSize: 13, fontWeight: 600, color: "#e2e8f0" }}>Nate Warner</div>
              <div style={{ fontSize: 11, color: "#64748b" }}>Rank #{userData.rank}</div>
            </div>
          </div>
        )}
      </aside>

      {/* Main Content */}
      <main style={{ flex: 1, marginLeft: sidebarOpen ? 260 : 72, transition: "margin-left 0.3s ease" }}>
        {/* Top Bar */}
        <header style={{
          padding: "16px 32px",
          borderBottom: "1px solid #1e293b",
          display: "flex", alignItems: "center", justifyContent: "space-between",
          background: "rgba(11,17,32,0.8)",
          backdropFilter: "blur(12px)",
          position: "sticky", top: 0, zIndex: 40,
        }}>
          <div>
            <h1 style={{ margin: 0, fontSize: 22, fontWeight: 700, color: "#f1f5f9" }}>
              Welcome back, Nate
            </h1>
            <p style={{ margin: "4px 0 0", color: "#64748b", fontSize: 14 }}>
              Keep up the great work — you're making progress!
            </p>
          </div>
          <div style={{ position: "relative" }}>
            <Search size={16} style={{ position: "absolute", left: 12, top: "50%", transform: "translateY(-50%)", color: "#475569" }} />
            <input
              type="text"
              placeholder="Search topics..."
              value={searchQuery}
              onChange={e => setSearchQuery(e.target.value)}
              style={{
                background: "#1e293b", border: "1px solid #334155", borderRadius: 10,
                padding: "8px 12px 8px 36px", color: "#e2e8f0", fontSize: 14, width: 240,
                outline: "none",
              }}
              onFocus={e => e.target.style.borderColor = "#3b82f6"}
              onBlur={e => e.target.style.borderColor = "#334155"}
            />
          </div>
        </header>

        <div style={{ padding: "28px 32px", maxWidth: 1200 }}>

          {/* Stats Row */}
          <div style={{ display: "grid", gridTemplateColumns: "repeat(4, 1fr)", gap: 16, marginBottom: 32 }}>
            <StatCard icon={BookOpen} value={userData.flashcardsTotal} label="Flashcards" sublabel={`${userData.flashcardsStudied} studied`} color="#3b82f6" progress={(userData.flashcardsStudied / userData.flashcardsTotal) * 100} />
            <StatCard icon={FileText} value={userData.scenariosTotal} label="Scenarios" sublabel={`${userData.scenariosCompleted} completed`} color="#10b981" progress={(userData.scenariosCompleted / userData.scenariosTotal) * 100} />
            <StatCard icon={Bookmark} value={userData.bookmarked} label="Bookmarked" sublabel="Save cards to review" color="#f59e0b" />
            <StatCard icon={TrendingUp} value={userData.avgScore || "\u2014"} label="Avg Score" sublabel={`${userData.responses} responses`} color="#8b5cf6" />
          </div>

          {/* Quick Start + Leaderboard Row */}
          <div style={{ display: "grid", gridTemplateColumns: "1fr 380px", gap: 24, marginBottom: 32 }}>

            {/* Practice Tests */}
            <div>
              <h2 style={{ fontSize: 17, fontWeight: 700, color: "#f1f5f9", marginBottom: 16, display: "flex", alignItems: "center", gap: 8 }}>
                <Zap size={18} color="#f59e0b" /> Quick Start — Practice Tests
              </h2>
              <div style={{ display: "flex", flexDirection: "column", gap: 12 }}>
                {testOptions.map((test, i) => (
                  <div key={i} style={{
                    background: "linear-gradient(135deg, rgba(30,41,59,0.8), rgba(15,23,42,0.9))",
                    borderRadius: 14, padding: "18px 20px",
                    border: "1px solid #1e293b",
                    display: "flex", alignItems: "center", gap: 16,
                    cursor: "pointer", transition: "all 0.2s",
                  }}
                  onMouseEnter={e => { e.currentTarget.style.borderColor = `${test.color}44`; e.currentTarget.style.transform = "translateX(4px)"; }}
                  onMouseLeave={e => { e.currentTarget.style.borderColor = "#1e293b"; e.currentTarget.style.transform = "translateX(0)"; }}
                  >
                    <div style={{ background: `${test.color}18`, borderRadius: 12, padding: 10, display: "flex" }}>
                      <test.icon size={22} color={test.color} />
                    </div>
                    <div style={{ flex: 1 }}>
                      <div style={{ fontSize: 15, fontWeight: 600, color: "#f1f5f9" }}>{test.name}</div>
                      <div style={{ fontSize: 13, color: "#64748b", marginTop: 2 }}>{test.desc}</div>
                    </div>
                    <div style={{ display: "flex", alignItems: "center", gap: 6, color: "#475569", fontSize: 13 }}>
                      <Clock size={14} /> {test.time}
                    </div>
                    <ChevronRight size={18} color="#475569" />
                  </div>
                ))}
              </div>
            </div>

            {/* Leaderboard */}
            <div style={{
              background: "linear-gradient(135deg, rgba(30,41,59,0.6), rgba(15,23,42,0.8))",
              borderRadius: 16, padding: 24,
              border: "1px solid #1e293b",
            }}>
              <h2 style={{ fontSize: 17, fontWeight: 700, color: "#f1f5f9", marginBottom: 20, display: "flex", alignItems: "center", gap: 8 }}>
                <Trophy size={18} color="#f59e0b" /> Top Performers
              </h2>
              <div style={{ display: "flex", flexDirection: "column", gap: 8 }}>
                {leaderboard.map((user, i) => (
                  <div key={i} style={{
                    display: "flex", alignItems: "center", gap: 12, padding: "10px 12px",
                    borderRadius: 10, background: i === 0 ? "rgba(245,158,11,0.06)" : "transparent",
                    border: i === 0 ? "1px solid rgba(245,158,11,0.15)" : "1px solid transparent",
                  }}>
                    <RankBadge rank={user.rank} />
                    <span style={{ flex: 1, fontSize: 14, fontWeight: i < 3 ? 600 : 400, color: i < 3 ? "#f1f5f9" : "#94a3b8" }}>{user.name}</span>
                    <span style={{ fontSize: 13, fontWeight: 600, color: "#10b981", minWidth: 50, textAlign: "right" }}>{user.avg}%</span>
                    <span style={{ fontSize: 12, color: "#64748b", minWidth: 40, textAlign: "right" }}>{user.best}%</span>
                  </div>
                ))}
              </div>
              <div style={{
                marginTop: 16, padding: "10px 12px", borderRadius: 10,
                background: "rgba(59,130,246,0.08)", border: "1px solid rgba(59,130,246,0.15)",
                display: "flex", alignItems: "center", gap: 8, fontSize: 13,
              }}>
                <Users size={14} color="#60a5fa" />
                <span style={{ color: "#94a3b8" }}>Your rank:</span>
                <span style={{ fontWeight: 600, color: "#60a5fa" }}>#{userData.rank}</span>
              </div>
            </div>
          </div>

          {/* Part 2 — Detective Exam */}
          <div style={{
            background: "linear-gradient(135deg, rgba(30,41,59,0.7), rgba(15,23,42,0.9))",
            borderRadius: 18, padding: 28, marginBottom: 32,
            border: "1px solid rgba(139,92,246,0.2)",
            position: "relative", overflow: "hidden",
          }}>
            <div style={{ position: "absolute", top: 0, left: 0, right: 0, height: 3, background: "linear-gradient(90deg, #8b5cf6, #3b82f6, #8b5cf6)" }} />
            <div style={{ display: "flex", alignItems: "center", gap: 12, marginBottom: 6 }}>
              <h2 style={{ fontSize: 20, fontWeight: 700, color: "#f1f5f9", margin: 0, display: "flex", alignItems: "center", gap: 10 }}>
                <PenTool size={20} color="#8b5cf6" />
                Part 2 — Detective Exam
              </h2>
              <span style={{
                background: "linear-gradient(135deg, #f59e0b, #d97706)", color: "#fff",
                fontSize: 10, fontWeight: 700, padding: "3px 10px", borderRadius: 20,
                letterSpacing: 1, textTransform: "uppercase",
              }}>Premium</span>
            </div>
            <p style={{ color: "#64748b", fontSize: 14, margin: "0 0 20px" }}>
              I/O Solutions mixed-method exam simulation with AI grading
            </p>

            {/* Grading Info Badges */}
            <div style={{ display: "flex", gap: 12, marginBottom: 20 }}>
              <div style={{
                background: "rgba(139,92,246,0.08)", border: "1px solid rgba(139,92,246,0.2)",
                borderRadius: 10, padding: "10px 16px", flex: 1,
                display: "flex", alignItems: "center", gap: 10, cursor: "pointer",
              }}>
                <Award size={18} color="#8b5cf6" />
                <div>
                  <div style={{ fontSize: 13, fontWeight: 600, color: "#e2e8f0" }}>How You're Graded</div>
                  <div style={{ fontSize: 11, color: "#64748b" }}>I/O Solutions methodology</div>
                </div>
              </div>
              <div style={{
                background: "rgba(59,130,246,0.08)", border: "1px solid rgba(59,130,246,0.2)",
                borderRadius: 10, padding: "10px 16px", flex: 1,
                display: "flex", alignItems: "center", gap: 10, cursor: "pointer",
              }}>
                <Target size={18} color="#3b82f6" />
                <div>
                  <div style={{ fontSize: 13, fontWeight: 600, color: "#e2e8f0" }}>R.E.A.C.T.I.O.N. Framework</div>
                  <div style={{ fontSize: 11, color: "#64748b" }}>Structured response guide</div>
                </div>
              </div>
            </div>

            {/* Part 2 Scenario Types */}
            <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 10 }}>
              {part2Sections.map((sec, i) => (
                <div key={i} style={{
                  background: "rgba(15,23,42,0.6)",
                  borderRadius: 12, padding: "14px 16px",
                  border: `1px solid ${sec.color}15`,
                  display: "flex", alignItems: "center", gap: 14,
                  cursor: "pointer", transition: "all 0.2s",
                }}
                onMouseEnter={e => { e.currentTarget.style.borderColor = `${sec.color}40`; e.currentTarget.style.transform = "translateX(3px)"; }}
                onMouseLeave={e => { e.currentTarget.style.borderColor = `${sec.color}15`; e.currentTarget.style.transform = "translateX(0)"; }}
                >
                  <div style={{ background: `${sec.color}15`, borderRadius: 10, padding: 8, display: "flex", flexShrink: 0 }}>
                    <sec.icon size={18} color={sec.color} />
                  </div>
                  <div style={{ flex: 1, minWidth: 0 }}>
                    <div style={{ fontSize: 14, fontWeight: 600, color: "#f1f5f9" }}>{sec.name}</div>
                    <div style={{ fontSize: 12, color: "#64748b", whiteSpace: "nowrap", overflow: "hidden", textOverflow: "ellipsis" }}>{sec.desc}</div>
                  </div>
                  <div style={{
                    background: `${sec.color}15`, color: sec.color,
                    fontSize: 13, fontWeight: 700, borderRadius: 20,
                    minWidth: 36, height: 36, display: "flex", alignItems: "center", justifyContent: "center",
                    flexShrink: 0,
                  }}>{sec.count}</div>
                  <ChevronRight size={16} color="#475569" />
                </div>
              ))}
            </div>
          </div>

          {/* Study Categories */}
          <h2 style={{ fontSize: 17, fontWeight: 700, color: "#f1f5f9", marginBottom: 16, display: "flex", alignItems: "center", gap: 8 }}>
            <Layers size={18} color="#8b5cf6" /> Study Categories
          </h2>
          <div style={{ display: "grid", gridTemplateColumns: "repeat(3, 1fr)", gap: 14, marginBottom: 32 }}>
            {filteredCategories.map((cat) => (
              <div key={cat.id} style={{
                background: "linear-gradient(135deg, rgba(30,41,59,0.7), rgba(15,23,42,0.85))",
                borderRadius: 14, padding: "20px 18px",
                border: `1px solid ${cat.color}15`,
                cursor: "pointer", transition: "all 0.25s ease",
                position: "relative", overflow: "hidden",
              }}
              onMouseEnter={e => { e.currentTarget.style.borderColor = `${cat.color}40`; e.currentTarget.style.transform = "translateY(-2px)"; e.currentTarget.style.boxShadow = `0 8px 24px ${cat.color}10`; }}
              onMouseLeave={e => { e.currentTarget.style.borderColor = `${cat.color}15`; e.currentTarget.style.transform = "translateY(0)"; e.currentTarget.style.boxShadow = "none"; }}
              >
                <div style={{ position: "absolute", top: -30, right: -30, width: 80, height: 80, borderRadius: "50%", background: `${cat.color}06` }} />
                <div style={{ display: "flex", alignItems: "center", gap: 10, marginBottom: 10 }}>
                  <div style={{ background: `${cat.color}15`, borderRadius: 8, padding: 6, display: "flex" }}>
                    <cat.icon size={18} color={cat.color} />
                  </div>
                  <span style={{ fontSize: 14, fontWeight: 600, color: "#f1f5f9" }}>{cat.name}</span>
                </div>
                <p style={{ color: "#64748b", fontSize: 12, margin: "0 0 12px", lineHeight: 1.5 }}>{cat.desc}</p>
                <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between" }}>
                  <span style={{ fontSize: 12, color: "#475569" }}>{cat.count} questions</span>
                  <ChevronRight size={16} color={cat.color} style={{ opacity: 0.6 }} />
                </div>
              </div>
            ))}
          </div>

          {/* Recent Activity */}
          <h2 style={{ fontSize: 17, fontWeight: 700, color: "#f1f5f9", marginBottom: 16, display: "flex", alignItems: "center", gap: 8 }}>
            <Clock size={18} color="#06b6d4" /> Recent Activity
          </h2>
          <div style={{
            background: "linear-gradient(135deg, rgba(30,41,59,0.6), rgba(15,23,42,0.8))",
            borderRadius: 16, border: "1px solid #1e293b", overflow: "hidden",
          }}>
            {recentActivity.map((item, i) => (
              <div key={i} style={{
                padding: "16px 20px",
                display: "flex", alignItems: "center", gap: 14,
                borderBottom: i < recentActivity.length - 1 ? "1px solid #1e293b" : "none",
              }}>
                <div style={{
                  width: 8, height: 8, borderRadius: "50%",
                  background: item.type === "scenario" ? "#8b5cf6" : item.type === "flashcard" ? "#3b82f6" : "#10b981",
                }} />
                <div style={{ flex: 1 }}>
                  <span style={{ fontSize: 14, fontWeight: 500, color: "#e2e8f0" }}>{item.title}</span>
                  <span style={{ fontSize: 12, color: "#475569", marginLeft: 8 }}>
                    {item.score ? `Score: ${item.score}%` : item.result}
                  </span>
                </div>
                <span style={{ fontSize: 12, color: "#475569" }}>{item.date}</span>
              </div>
            ))}
          </div>

        </div>
      </main>
    </div>
  );
}
