import { useState } from "react";

const COLORS = {
  bg: "#0e0f13",
  surface: "#16181f",
  card: "#1c1f2a",
  border: "#272b38",
  amber: "#f0a500",
  amberDim: "#b37a00",
  amberGlow: "rgba(240,165,0,0.12)",
  cyan: "#00c9b1",
  red: "#e05252",
  green: "#3ecf8e",
  blue: "#4f8ef7",
  text: "#e8eaf0",
  muted: "#7b8099",
  dimmed: "#4a4f63",
};

const style = {
  page: {
    background: COLORS.bg,
    minHeight: "100vh",
    fontFamily: "'Georgia', serif",
    color: COLORS.text,
    display: "flex",
    flexDirection: "column",
  },
  nav: {
    display: "flex",
    alignItems: "center",
    gap: "4px",
    padding: "0 24px",
    background: COLORS.surface,
    borderBottom: `1px solid ${COLORS.border}`,
    height: "56px",
    position: "sticky",
    top: 0,
    zIndex: 100,
    overflowX: "auto",
  },
  navBtn: (active) => ({
    padding: "6px 14px",
    borderRadius: "6px",
    border: "none",
    cursor: "pointer",
    fontFamily: "'Georgia', serif",
    fontSize: "13px",
    fontWeight: active ? "700" : "400",
    background: active ? COLORS.amber : "transparent",
    color: active ? "#0e0f13" : COLORS.muted,
    transition: "all 0.15s",
    whiteSpace: "nowrap",
    letterSpacing: "0.02em",
  }),
  main: {
    flex: 1,
    padding: "32px 28px",
    maxWidth: "1100px",
    width: "100%",
    margin: "0 auto",
    boxSizing: "border-box",
  },
  pageTitle: {
    fontSize: "28px",
    fontWeight: "700",
    letterSpacing: "-0.02em",
    marginBottom: "4px",
    fontFamily: "'Georgia', serif",
  },
  subtitle: {
    fontSize: "14px",
    color: COLORS.muted,
    marginBottom: "28px",
  },
  card: {
    background: COLORS.card,
    border: `1px solid ${COLORS.border}`,
    borderRadius: "12px",
    padding: "20px",
  },
  amberLine: {
    width: "36px",
    height: "3px",
    background: COLORS.amber,
    borderRadius: "2px",
    marginBottom: "20px",
  },
  badge: (color = COLORS.amber) => ({
    display: "inline-flex",
    alignItems: "center",
    padding: "3px 10px",
    borderRadius: "20px",
    fontSize: "11px",
    fontWeight: "700",
    letterSpacing: "0.08em",
    background: color + "22",
    color: color,
    border: `1px solid ${color}44`,
    textTransform: "uppercase",
  }),
  btn: (variant = "primary") => ({
    padding: "10px 20px",
    borderRadius: "8px",
    border: variant === "outline" ? `1px solid ${COLORS.border}` : "none",
    cursor: "pointer",
    fontFamily: "'Georgia', serif",
    fontSize: "14px",
    fontWeight: "600",
    background: variant === "primary" ? COLORS.amber : variant === "ghost" ? "transparent" : COLORS.card,
    color: variant === "primary" ? "#0e0f13" : COLORS.text,
    transition: "all 0.15s",
    letterSpacing: "0.01em",
  }),
  input: {
    background: COLORS.card,
    border: `1px solid ${COLORS.border}`,
    borderRadius: "8px",
    padding: "10px 14px",
    color: COLORS.text,
    fontFamily: "'Georgia', serif",
    fontSize: "14px",
    outline: "none",
    width: "100%",
    boxSizing: "border-box",
  },
  tag: (color) => ({
    display: "inline-block",
    padding: "2px 8px",
    borderRadius: "4px",
    fontSize: "11px",
    fontWeight: "700",
    background: color + "22",
    color: color,
    letterSpacing: "0.06em",
    textTransform: "uppercase",
  }),
  pill: (active) => ({
    padding: "6px 14px",
    borderRadius: "20px",
    border: `1px solid ${active ? COLORS.amber : COLORS.border}`,
    background: active ? COLORS.amberGlow : "transparent",
    color: active ? COLORS.amber : COLORS.muted,
    cursor: "pointer",
    fontSize: "13px",
    fontFamily: "'Georgia', serif",
    transition: "all 0.15s",
  }),
};

// ─── FLASHCARDS ───────────────────────────────────────────────────────────────
const categories = [
  "All", "Full Practice Exam", "Gold Scenarios", "ILCS Crime Classifications",
  "Detective Part 2 Scenarios", "Most Appropriate",
  "Least Appropriate", "Legal Trap", "Digital Evidence", "Mini Scenarios"
];

const sampleCards = [
  { id: 1, category: "Gold Scenarios", difficulty: "Easy", title: "CPD Procedure - G02-01-03", code: "G02-01-03", bookmarked: false },
  { id: 2, category: "ILCS Crime Classifications", difficulty: "Medium", title: "720 ILCS 5/12-3 — Simple Battery", code: "ILCS-5/12-3", bookmarked: true },
  { id: 3, category: "Legal Trap", difficulty: "Hard", title: "Miranda Rights — Custodial Interrogation", code: "LT-024", bookmarked: false },
  { id: 4, category: "Most Appropriate", difficulty: "Medium", title: "Witness Interview Protocol", code: "MA-011", bookmarked: false },
  { id: 5, category: "Digital Evidence", difficulty: "Hard", title: "Chain of Custody — Digital Devices", code: "DE-007", bookmarked: true },
  { id: 6, category: "Gold Scenarios", difficulty: "Easy", title: "Use of Force Documentation", code: "G03-02-01", bookmarked: false },
  { id: 8, category: "Mini Scenarios", difficulty: "Easy", title: "Domestic Dispute — First Response", code: "MS-003", bookmarked: true },
];

const difficultyColor = { Easy: COLORS.green, Medium: COLORS.amber, Hard: COLORS.red };

function FlashcardsPage({ onNavigate }) {
  const [activeCat, setActiveCat] = useState("All");
  const [search, setSearch] = useState("");
  const [studying, setStudying] = useState(false);
  const [cardIdx, setCardIdx] = useState(0);
  const [flipped, setFlipped] = useState(false);

  const filtered = sampleCards.filter(c =>
    (activeCat === "All" || c.category === activeCat) &&
    (c.title.toLowerCase().includes(search.toLowerCase()))
  );

  if (studying) {
    const card = filtered[cardIdx] || filtered[0];
    return (
      <div style={{ ...style.page, justifyContent: "center", alignItems: "center", padding: "20px" }}>
        <div style={{ width: "100%", maxWidth: "680px" }}>
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "32px" }}>
            <button onClick={() => { setStudying(false); setFlipped(false); setCardIdx(0); }} style={style.btn("ghost")}>
              ← Back to Cards
            </button>
            <span style={{ color: COLORS.muted, fontSize: "14px" }}>{cardIdx + 1} / {filtered.length}</span>
          </div>

          <div
            onClick={() => setFlipped(!flipped)}
            style={{
              background: flipped ? COLORS.amber : COLORS.card,
              border: `2px solid ${flipped ? COLORS.amber : COLORS.border}`,
              borderRadius: "20px",
              padding: "60px 48px",
              minHeight: "280px",
              display: "flex",
              flexDirection: "column",
              alignItems: "center",
              justifyContent: "center",
              cursor: "pointer",
              textAlign: "center",
              transition: "all 0.3s",
              marginBottom: "24px",
            }}
          >
            {!flipped ? (
              <>
                <div style={{ ...style.badge(COLORS.cyan), marginBottom: "20px" }}>{card.category}</div>
                <div style={{ fontSize: "24px", fontWeight: "700", marginBottom: "12px" }}>{card.title}</div>
                <div style={{ color: COLORS.muted, fontSize: "14px" }}>Code: {card.code}</div>
                <div style={{ color: COLORS.dimmed, fontSize: "12px", marginTop: "32px" }}>Tap to reveal answer</div>
              </>
            ) : (
              <>
                <div style={{ color: "#0e0f13", fontSize: "20px", fontWeight: "700", marginBottom: "12px" }}>Answer Revealed</div>
                <div style={{ color: "#0e0f1388", fontSize: "14px" }}>
                  This is where the detailed answer and explanation for {card.title} would display. Study the key concepts and memorize the key code: {card.code}.
                </div>
              </>
            )}
          </div>

          <div style={{ display: "flex", gap: "12px", justifyContent: "center" }}>
            <button disabled={cardIdx === 0} onClick={() => { setCardIdx(i => i - 1); setFlipped(false); }} style={{ ...style.btn("outline"), opacity: cardIdx === 0 ? 0.4 : 1 }}>← Prev</button>
            <button style={{ ...style.btn("outline"), background: COLORS.red + "22", color: COLORS.red, borderColor: COLORS.red + "44" }}>✗ Miss</button>
            <button style={{ ...style.btn("outline"), background: COLORS.green + "22", color: COLORS.green, borderColor: COLORS.green + "44" }}>✓ Got It</button>
            <button disabled={cardIdx === filtered.length - 1} onClick={() => { setCardIdx(i => i + 1); setFlipped(false); }} style={{ ...style.btn("outline"), opacity: cardIdx === filtered.length - 1 ? 0.4 : 1 }}>Next →</button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div style={style.page}>
      <nav style={style.nav}>
        {["Home","Cards","Tests","Part 2","Rankings","Support","ILCS","Profile","Bookmarks"].map(n => (
          <button key={n} onClick={() => onNavigate && onNavigate(n)} style={style.navBtn(n === "Cards")}>{n}</button>
        ))}
      </nav>
      <div style={style.main}>
        <div style={style.amberLine} />
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", flexWrap: "wrap", gap: "16px", marginBottom: "8px" }}>
          <div>
            <div style={style.pageTitle}>Flashcards</div>
            <div style={style.subtitle}>136 questions available · 12 studied this session</div>
          </div>
          <button onClick={() => setStudying(true)} style={style.btn("primary")}>▶ Start Studying</button>
        </div>

        <div style={{ display: "flex", gap: "12px", marginBottom: "20px" }}>
          <input
            value={search}
            onChange={e => setSearch(e.target.value)}
            placeholder="Search flashcards..."
            style={{ ...style.input, maxWidth: "320px" }}
          />
        </div>

        <div style={{ display: "flex", flexWrap: "wrap", gap: "8px", marginBottom: "28px" }}>
          {categories.map(cat => (
            <button key={cat} onClick={() => setActiveCat(cat)} style={style.pill(activeCat === cat)}>{cat}</button>
          ))}
        </div>

        <div style={{ display: "grid", gap: "10px" }}>
          {filtered.map(card => (
            <div key={card.id} style={{
              ...style.card,
              display: "flex",
              alignItems: "center",
              gap: "16px",
              transition: "border-color 0.15s",
              cursor: "pointer",
            }}>
              <div style={{ flex: 1 }}>
                <div style={{ display: "flex", alignItems: "center", gap: "10px", marginBottom: "6px" }}>
                  <span style={style.tag(difficultyColor[card.difficulty])}>{card.difficulty}</span>
                  <span style={{ color: COLORS.muted, fontSize: "12px" }}>{card.category}</span>
                </div>
                <div style={{ fontWeight: "600", fontSize: "15px" }}>{card.title}</div>
                <div style={{ color: COLORS.dimmed, fontSize: "12px", marginTop: "2px" }}>{card.code}</div>
              </div>
              <div style={{ color: card.bookmarked ? COLORS.amber : COLORS.dimmed, fontSize: "20px" }}>
                {card.bookmarked ? "★" : "☆"}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

// ─── PRACTICE TESTS ───────────────────────────────────────────────────────────
const testModes = [
  { label: "25 Question Quiz", desc: "Quick practice test", time: "~15 min", icon: "⚡", color: COLORS.cyan, questions: 25 },
  { label: "50 Question Test", desc: "Standard practice exam", time: "~30 min", icon: "📋", color: COLORS.amber, questions: 50 },
  { label: "Full 105 Exam", desc: "Complete simulation", time: "~60 min", icon: "🎯", color: COLORS.red, questions: 105 },
];

const sampleQuestions = [
  {
    q: "Under Illinois law, what constitutes 'aggravated battery' as opposed to simple battery?",
    choices: [
      "Any battery committed against a person over 18 years old",
      "Battery causing great bodily harm, permanent disability, or committed against protected class members",
      "Battery involving any weapon regardless of injury",
      "Battery committed in a public place witnessed by at least two persons"
    ],
    correct: 1,
  },
  {
    q: "During a custodial interrogation, at what point must Miranda warnings be given?",
    choices: [
      "Before any police contact with the suspect",
      "Only when the suspect specifically requests an attorney",
      "Prior to questioning a person who is in custody",
      "Only after formal arrest and booking"
    ],
    correct: 2,
  },
];

function PracticeTestsPage({ onNavigate }) {
  const [selected, setSelected] = useState(null);
  const [qIdx, setQIdx] = useState(0);
  const [answers, setAnswers] = useState({});
  const [showResult, setShowResult] = useState(false);

  if (selected !== null && !showResult) {
    const q = sampleQuestions[qIdx % sampleQuestions.length];
    const totalQ = selected.questions;
    const displayIdx = qIdx + 1;
    const answered = answers[qIdx];

    return (
      <div style={{ ...style.page }}>
        <div style={{ background: COLORS.surface, borderBottom: `1px solid ${COLORS.border}`, padding: "16px 28px", display: "flex", justifyContent: "space-between", alignItems: "center" }}>
          <button onClick={() => { setSelected(null); setQIdx(0); setAnswers({}); }} style={style.btn("ghost")}>✕ Exit Test</button>
          <div style={{ display: "flex", alignItems: "center", gap: "16px" }}>
            <span style={{ color: COLORS.muted, fontSize: "14px" }}>Question {displayIdx} of {Math.min(totalQ, sampleQuestions.length * 10)}</span>
            <div style={{ width: "120px", height: "6px", background: COLORS.border, borderRadius: "3px" }}>
              <div style={{ width: `${(displayIdx / totalQ) * 100}%`, height: "100%", background: COLORS.amber, borderRadius: "3px", transition: "width 0.3s" }} />
            </div>
          </div>
          <span style={{ ...style.badge(COLORS.cyan) }}>{selected.label}</span>
        </div>

        <div style={{ ...style.main, maxWidth: "720px" }}>
          <div style={{ ...style.card, marginBottom: "20px", padding: "32px" }}>
            <div style={{ color: COLORS.muted, fontSize: "12px", marginBottom: "16px", letterSpacing: "0.1em", textTransform: "uppercase" }}>Question {displayIdx}</div>
            <div style={{ fontSize: "18px", lineHeight: "1.6", fontWeight: "500" }}>{q.q}</div>
          </div>

          <div style={{ display: "grid", gap: "10px", marginBottom: "24px" }}>
            {q.choices.map((choice, i) => {
              const isSelected = answered === i;
              const isCorrect = answered !== undefined && i === q.correct;
              const isWrong = isSelected && i !== q.correct;
              const bg = isCorrect ? COLORS.green + "22" : isWrong ? COLORS.red + "22" : isSelected ? COLORS.amberGlow : COLORS.card;
              const border = isCorrect ? COLORS.green : isWrong ? COLORS.red : isSelected ? COLORS.amber : COLORS.border;

              return (
                <div key={i} onClick={() => !answered && setAnswers(a => ({ ...a, [qIdx]: i }))}
                  style={{
                    ...style.card,
                    border: `1px solid ${border}`,
                    background: bg,
                    cursor: answered === undefined ? "pointer" : "default",
                    display: "flex",
                    alignItems: "center",
                    gap: "14px",
                    padding: "16px 20px",
                    transition: "all 0.15s",
                  }}>
                  <div style={{
                    width: "28px", height: "28px", borderRadius: "50%", border: `2px solid ${border}`,
                    display: "flex", alignItems: "center", justifyContent: "center",
                    fontSize: "12px", fontWeight: "700", color: isCorrect ? COLORS.green : isWrong ? COLORS.red : isSelected ? COLORS.amber : COLORS.muted,
                    flexShrink: 0,
                  }}>
                    {String.fromCharCode(65 + i)}
                  </div>
                  <span style={{ fontSize: "15px" }}>{choice}</span>
                </div>
              );
            })}
          </div>

          <div style={{ display: "flex", justifyContent: "space-between" }}>
            <button disabled={qIdx === 0} onClick={() => { setQIdx(i => i - 1); }} style={{ ...style.btn("outline"), opacity: qIdx === 0 ? 0.4 : 1 }}>← Previous</button>
            {qIdx < sampleQuestions.length - 1
              ? <button onClick={() => setQIdx(i => i + 1)} style={style.btn("primary")}>Next Question →</button>
              : <button onClick={() => setShowResult(true)} style={{ ...style.btn("primary"), background: COLORS.green }}>Submit Test</button>
            }
          </div>
        </div>
      </div>
    );
  }

  if (showResult) {
    const score = Object.entries(answers).filter(([i, a]) => sampleQuestions[i % sampleQuestions.length].correct === a).length;
    const pct = Math.round((score / sampleQuestions.length) * 100);
    return (
      <div style={{ ...style.page, alignItems: "center", justifyContent: "center", padding: "20px" }}>
        <div style={{ ...style.card, maxWidth: "480px", width: "100%", textAlign: "center", padding: "48px 40px" }}>
          <div style={{ fontSize: "72px", fontWeight: "700", color: pct >= 70 ? COLORS.green : COLORS.red }}>{pct}%</div>
          <div style={{ fontSize: "20px", fontWeight: "600", margin: "8px 0 4px" }}>{pct >= 70 ? "Great work!" : "Keep studying!"}</div>
          <div style={{ color: COLORS.muted, marginBottom: "32px" }}>{score} of {sampleQuestions.length} correct</div>
          <button onClick={() => { setSelected(null); setQIdx(0); setAnswers({}); setShowResult(false); }} style={style.btn("primary")}>Back to Tests</button>
        </div>
      </div>
    );
  }

  return (
    <div style={style.page}>
      <nav style={style.nav}>
        {["Home","Cards","Tests","Part 2","Rankings","Support","ILCS","Profile","Bookmarks"].map(n => (
          <button key={n} onClick={() => onNavigate && onNavigate(n)} style={style.navBtn(n === "Tests")}>{n}</button>
        ))}
      </nav>
      <div style={style.main}>
        <div style={style.amberLine} />
        <div style={style.pageTitle}>Practice Tests</div>
        <div style={style.subtitle}>Multiple choice exams · 160+ questions from Illinois criminal law, constitutional law & CPD procedures</div>

        <div style={{
          background: COLORS.amber + "14",
          border: `1px solid ${COLORS.amber}44`,
          borderRadius: "10px",
          padding: "14px 18px",
          marginBottom: "28px",
          display: "flex",
          alignItems: "center",
          gap: "10px",
          color: COLORS.amber,
          fontSize: "14px",
        }}>
          ★ <strong>100 Practice Questions</strong> based on previous test administrator questions
        </div>

        <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(280px, 1fr))", gap: "16px", marginBottom: "36px" }}>
          {testModes.map(t => (
            <div key={t.label} onClick={() => setSelected(t)} style={{
              ...style.card,
              cursor: "pointer",
              borderTop: `3px solid ${t.color}`,
              transition: "transform 0.15s, border-color 0.15s",
              position: "relative",
              overflow: "hidden",
            }}>
              <div style={{ position: "absolute", top: "16px", right: "16px", fontSize: "28px" }}>{t.icon}</div>
              <div style={{ fontSize: "24px", fontWeight: "700", marginBottom: "4px", color: t.color }}>{t.questions}Q</div>
              <div style={{ fontSize: "17px", fontWeight: "600", marginBottom: "4px" }}>{t.label}</div>
              <div style={{ color: COLORS.muted, fontSize: "13px", marginBottom: "16px" }}>{t.desc}</div>
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                <span style={{ color: COLORS.dimmed, fontSize: "12px" }}>⏱ {t.time}</span>
                <button style={{ ...style.btn("primary"), padding: "7px 16px", fontSize: "13px", background: t.color }}>Start →</button>
              </div>
            </div>
          ))}
        </div>

        <div style={style.card}>
          <div style={{ fontWeight: "700", marginBottom: "16px", fontSize: "16px" }}>Your Recent Test History</div>
          <div style={{ display: "grid", gap: "10px" }}>
            {[
              { date: "Feb 26, 2026", type: "50 Question Test", score: 84, time: "28 min" },
              { date: "Feb 24, 2026", type: "25 Question Quiz", score: 76, time: "14 min" },
              { date: "Feb 21, 2026", type: "25 Question Quiz", score: 68, time: "17 min" },
            ].map((r, i) => (
              <div key={i} style={{ display: "flex", justifyContent: "space-between", alignItems: "center", padding: "12px 0", borderBottom: i < 2 ? `1px solid ${COLORS.border}` : "none" }}>
                <div>
                  <div style={{ fontWeight: "600", fontSize: "14px" }}>{r.type}</div>
                  <div style={{ color: COLORS.muted, fontSize: "12px" }}>{r.date} · {r.time}</div>
                </div>
                <div style={{ fontSize: "22px", fontWeight: "700", color: r.score >= 80 ? COLORS.green : r.score >= 70 ? COLORS.amber : COLORS.red }}>{r.score}%</div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

// ─── RANKINGS ─────────────────────────────────────────────────────────────────
const leaderboardData = [
  { rank: 1, name: "Bradley Anderson", avg: 87.3, best: 92, badge: "🏆" },
  { rank: 2, name: "Bell", avg: 85, best: 85, badge: "🥈" },
  { rank: 3, name: "Brandon Lange", avg: 65, best: 65, badge: "🥉" },
  { rank: 4, name: "Anabel Preciado", avg: 62.5, best: 85, badge: "4" },
  { rank: 5, name: "rena maritote", avg: 60, best: 60, badge: "5" },
  { rank: 6, name: "Nicholas Gallapo", avg: 58.5, best: 72, badge: "6" },
  { rank: 7, name: "Matthew", avg: 58.3, best: 75, badge: "7" },
  { rank: 8, name: "Benito Lugo", avg: 57.5, best: 60, badge: "8" },
  { rank: 9, name: "Nathaniel Warner", avg: 54.2, best: 70, badge: "9", isMe: true },
  { rank: 10, name: "Chris D", avg: 52, best: 65, badge: "10" },
];

function RankingsPage({ onNavigate }) {
  return (
    <div style={style.page}>
      <nav style={style.nav}>
        {["Home","Cards","Tests","Part 2","Rankings","Support","ILCS","Profile","Bookmarks"].map(n => (
          <button key={n} onClick={() => onNavigate && onNavigate(n)} style={style.navBtn(n === "Rankings")}>{n}</button>
        ))}
      </nav>
      <div style={style.main}>
        <div style={style.amberLine} />
        <div style={style.pageTitle}>Scenario Rankings</div>
        <div style={style.subtitle}>Complete scenarios to climb the leaderboard · Rankings based on scenario scores only</div>

        {/* Top 3 podium */}
        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr 1fr", gap: "12px", marginBottom: "28px" }}>
          {[leaderboardData[1], leaderboardData[0], leaderboardData[2]].map((p, i) => {
            const heights = ["120px", "160px", "100px"];
            const podiumColors = [COLORS.muted, COLORS.amber, "#cd7f32"];
            const podiumIdx = i === 0 ? 1 : i === 1 ? 0 : 2;
            return (
              <div key={p.rank} style={{ display: "flex", flexDirection: "column", alignItems: "center" }}>
                <div style={{ fontSize: "28px", marginBottom: "8px" }}>{p.badge}</div>
                <div style={{ fontWeight: "700", fontSize: "14px", marginBottom: "2px" }}>{p.name}</div>
                <div style={{ color: COLORS.muted, fontSize: "12px", marginBottom: "8px" }}>{p.avg}% avg</div>
                <div style={{
                  width: "100%",
                  height: heights[i],
                  background: `linear-gradient(to top, ${podiumColors[i]}33, ${podiumColors[i]}11)`,
                  border: `1px solid ${podiumColors[i]}55`,
                  borderRadius: "8px 8px 0 0",
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                  fontSize: "28px",
                  fontWeight: "900",
                  color: podiumColors[i],
                }}>{["2nd","1st","3rd"][i]}</div>
              </div>
            );
          })}
        </div>

        <div style={style.card}>
          <div style={{ display: "grid", gridTemplateColumns: "48px 1fr 80px 80px", gap: "8px", padding: "0 8px 12px", borderBottom: `1px solid ${COLORS.border}`, marginBottom: "8px" }}>
            <span style={{ color: COLORS.dimmed, fontSize: "11px", textTransform: "uppercase", letterSpacing: "0.08em" }}>Rank</span>
            <span style={{ color: COLORS.dimmed, fontSize: "11px", textTransform: "uppercase", letterSpacing: "0.08em" }}>Name</span>
            <span style={{ color: COLORS.dimmed, fontSize: "11px", textTransform: "uppercase", letterSpacing: "0.08em", textAlign: "center" }}>Avg</span>
            <span style={{ color: COLORS.dimmed, fontSize: "11px", textTransform: "uppercase", letterSpacing: "0.08em", textAlign: "center" }}>Best</span>
          </div>
          {leaderboardData.map((p) => (
            <div key={p.rank} style={{
              display: "grid",
              gridTemplateColumns: "48px 1fr 80px 80px",
              gap: "8px",
              padding: "14px 8px",
              borderRadius: "8px",
              background: p.isMe ? COLORS.amberGlow : "transparent",
              border: p.isMe ? `1px solid ${COLORS.amber}44` : "1px solid transparent",
              marginBottom: "4px",
            }}>
              <div style={{ fontWeight: "700", fontSize: "16px", color: p.rank <= 3 ? COLORS.amber : COLORS.muted }}>{p.badge}</div>
              <div style={{ fontWeight: p.isMe ? "700" : "400", color: p.isMe ? COLORS.amber : COLORS.text }}>
                {p.name} {p.isMe && <span style={{ fontSize: "11px", color: COLORS.amber }}>← You</span>}
              </div>
              <div style={{ textAlign: "center", color: COLORS.cyan, fontWeight: "600" }}>{p.avg}%</div>
              <div style={{ textAlign: "center", color: COLORS.green, fontWeight: "600" }}>{p.best}%</div>
            </div>
          ))}
        </div>

        <div style={{ marginTop: "16px", textAlign: "center" }}>
          <button style={{ ...style.btn("outline"), color: COLORS.red, borderColor: COLORS.red + "44" }}>↺ Reset My Scenario Scores</button>
        </div>
      </div>
    </div>
  );
}

// ─── PROFILE ──────────────────────────────────────────────────────────────────
function ProfilePage({ onNavigate }) {
  const stats = [
    { label: "Flashcards Studied", value: "136", icon: "📚", color: COLORS.cyan },
    { label: "Scenarios Done", value: "12", icon: "📝", color: COLORS.green },
    { label: "Avg Test Score", value: "76%", icon: "📊", color: COLORS.amber },
    { label: "Current Rank", value: "#9", icon: "🏅", color: COLORS.red },
  ];

  return (
    <div style={style.page}>
      <nav style={style.nav}>
        {["Home","Cards","Tests","Part 2","Rankings","Support","ILCS","Profile","Bookmarks"].map(n => (
          <button key={n} onClick={() => onNavigate && onNavigate(n)} style={style.navBtn(n === "Profile")}>{n}</button>
        ))}
      </nav>
      <div style={style.main}>
        {/* Hero */}
        <div style={{
          ...style.card,
          display: "flex",
          alignItems: "center",
          gap: "28px",
          marginBottom: "24px",
          padding: "32px 28px",
          background: `linear-gradient(135deg, ${COLORS.card} 60%, ${COLORS.amber}11)`,
          borderTop: `3px solid ${COLORS.amber}`,
          flexWrap: "wrap",
        }}>
          <div style={{
            width: "80px", height: "80px", borderRadius: "50%",
            background: `linear-gradient(135deg, ${COLORS.amber}44, ${COLORS.amber}22)`,
            border: `2px solid ${COLORS.amber}66`,
            display: "flex", alignItems: "center", justifyContent: "center",
            fontSize: "32px", flexShrink: 0,
          }}>👤</div>
          <div style={{ flex: 1 }}>
            <div style={{ ...style.pageTitle, marginBottom: "4px" }}>Nathaniel Warner</div>
            <div style={{ color: COLORS.muted, fontSize: "14px", marginBottom: "10px" }}>njwarner25@gmail.com</div>
            <span style={style.badge(COLORS.amber)}>Admin</span>
          </div>
          <button style={style.btn("outline")}>Edit Profile</button>
        </div>

        {/* Stats */}
        <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(180px, 1fr))", gap: "12px", marginBottom: "24px" }}>
          {stats.map(s => (
            <div key={s.label} style={{ ...style.card, textAlign: "center", padding: "20px 16px" }}>
              <div style={{ fontSize: "28px", marginBottom: "8px" }}>{s.icon}</div>
              <div style={{ fontSize: "28px", fontWeight: "700", color: s.color, marginBottom: "4px" }}>{s.value}</div>
              <div style={{ fontSize: "12px", color: COLORS.muted }}>{s.label}</div>
            </div>
          ))}
        </div>

        {/* Account Benefits */}
        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "16px", marginBottom: "24px" }}>
          <div style={style.card}>
            <div style={{ fontWeight: "700", marginBottom: "16px", fontSize: "15px" }}>Account Benefits</div>
            {["Personal progress tracking", "Sync across all devices", "Bookmarks saved to your account", "Study history preserved"].map(b => (
              <div key={b} style={{ display: "flex", alignItems: "center", gap: "10px", padding: "8px 0", borderBottom: `1px solid ${COLORS.border}`, fontSize: "14px" }}>
                <span style={{ color: COLORS.green }}>✓</span>
                <span>{b}</span>
              </div>
            ))}
          </div>
          <div style={style.card}>
            <div style={{ fontWeight: "700", marginBottom: "16px", fontSize: "15px" }}>Quick Links</div>
            {["My Bookmarks", "Test History", "Scenario Results", "Settings", "Sign Out"].map((link, i) => (
              <div key={link} style={{ display: "flex", justifyContent: "space-between", alignItems: "center", padding: "12px 0", borderBottom: i < 4 ? `1px solid ${COLORS.border}` : "none", cursor: "pointer" }}>
                <span style={{ fontSize: "14px", color: link === "Sign Out" ? COLORS.red : COLORS.text }}>{link}</span>
                <span style={{ color: COLORS.dimmed }}>›</span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

// ─── ILCS ─────────────────────────────────────────────────────────────────────
const ilcsData = [
  { code: "720 ILCS 5/9-1", title: "First Degree Murder", category: "Homicide", difficulty: "Hard" },
  { code: "720 ILCS 5/9-2", title: "Second Degree Murder", category: "Homicide", difficulty: "Hard" },
  { code: "720 ILCS 5/10-1", title: "Kidnapping", category: "Person Crimes", difficulty: "Medium" },
  { code: "720 ILCS 5/11-1.20", title: "Criminal Sexual Assault", category: "Sex Crimes", difficulty: "Hard" },
  { code: "720 ILCS 5/12-1", title: "Assault", category: "Person Crimes", difficulty: "Easy" },
  { code: "720 ILCS 5/12-3", title: "Battery", category: "Person Crimes", difficulty: "Easy" },
  { code: "720 ILCS 5/12-3.05", title: "Aggravated Battery", category: "Person Crimes", difficulty: "Medium" },
  { code: "720 ILCS 5/16-1", title: "Theft", category: "Property Crimes", difficulty: "Easy" },
  { code: "720 ILCS 5/18-1", title: "Robbery", category: "Property Crimes", difficulty: "Medium" },
  { code: "720 ILCS 5/19-1", title: "Burglary", category: "Property Crimes", difficulty: "Medium" },
  { code: "720 ILCS 5/21-1", title: "Criminal Damage to Property", category: "Property Crimes", difficulty: "Easy" },
  { code: "720 ILCS 570/401", title: "Controlled Substance Violations", category: "Drug Offenses", difficulty: "Hard" },
];

const ilcsCats = ["All", "Homicide", "Person Crimes", "Sex Crimes", "Property Crimes", "Drug Offenses"];

function ILCSPage({ onNavigate }) {
  const [search, setSearch] = useState("");
  const [cat, setCat] = useState("All");
  const [expanded, setExpanded] = useState(null);

  const filtered = ilcsData.filter(c =>
    (cat === "All" || c.category === cat) &&
    (c.code.toLowerCase().includes(search.toLowerCase()) || c.title.toLowerCase().includes(search.toLowerCase()))
  );

  return (
    <div style={style.page}>
      <nav style={style.nav}>
        {["Home","Cards","Tests","Part 2","Rankings","Support","ILCS","Profile","Bookmarks"].map(n => (
          <button key={n} onClick={() => onNavigate && onNavigate(n)} style={style.navBtn(n === "ILCS")}>{n}</button>
        ))}
      </nav>
      <div style={style.main}>
        <div style={style.amberLine} />
        <div style={style.pageTitle}>ILCS Crime Classifications</div>
        <div style={style.subtitle}>Illinois Compiled Statutes — Criminal Code reference guide</div>

        <div style={{ display: "flex", gap: "12px", marginBottom: "20px", flexWrap: "wrap" }}>
          <input value={search} onChange={e => setSearch(e.target.value)} placeholder="Search by code or crime name..." style={{ ...style.input, maxWidth: "360px" }} />
        </div>

        <div style={{ display: "flex", flexWrap: "wrap", gap: "8px", marginBottom: "28px" }}>
          {ilcsCats.map(c => (
            <button key={c} onClick={() => setCat(c)} style={style.pill(cat === c)}>{c}</button>
          ))}
        </div>

        <div style={{ display: "grid", gap: "8px" }}>
          {filtered.map((item, i) => (
            <div key={item.code} style={{
              ...style.card,
              cursor: "pointer",
              borderLeft: `3px solid ${cat === "All" ? COLORS.amber : COLORS.cyan}`,
              transition: "all 0.15s",
            }} onClick={() => setExpanded(expanded === i ? null : i)}>
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                <div style={{ flex: 1 }}>
                  <div style={{ display: "flex", alignItems: "center", gap: "10px", marginBottom: "4px" }}>
                    <span style={{ ...style.badge(COLORS.cyan), fontFamily: "monospace", fontSize: "11px" }}>{item.code}</span>
                    <span style={style.tag(difficultyColor[item.difficulty])}>{item.difficulty}</span>
                    <span style={{ color: COLORS.dimmed, fontSize: "12px" }}>{item.category}</span>
                  </div>
                  <div style={{ fontWeight: "600", fontSize: "15px" }}>{item.title}</div>
                </div>
                <span style={{ color: COLORS.dimmed, fontSize: "18px", marginLeft: "12px" }}>{expanded === i ? "▲" : "▼"}</span>
              </div>

              {expanded === i && (
                <div style={{ marginTop: "16px", padding: "16px", background: COLORS.bg, borderRadius: "8px", fontSize: "14px", color: COLORS.muted, lineHeight: "1.6" }}>
                  <strong style={{ color: COLORS.text }}>Key Elements:</strong> Study this statute carefully — {item.title} under {item.code} is commonly tested in the CPD detective exam. Know the elements, exceptions, and related case law. Pay attention to how this interacts with other related statutes in the {item.category} category.
                  <div style={{ marginTop: "12px", display: "flex", gap: "8px" }}>
                    <button style={{ ...style.btn("outline"), padding: "6px 14px", fontSize: "12px" }}>Study Flashcard</button>
                    <button style={{ ...style.btn("outline"), padding: "6px 14px", fontSize: "12px" }}>☆ Bookmark</button>
                  </div>
                </div>
              )}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

// ─── BOOKMARKS ────────────────────────────────────────────────────────────────
const bookmarkedCards = sampleCards.filter(c => c.bookmarked);

function BookmarksPage({ onNavigate }) {
  const [filter, setFilter] = useState("All");
  const cats = ["All", ...new Set(bookmarkedCards.map(c => c.category))];

  const filtered = bookmarkedCards.filter(c => filter === "All" || c.category === filter);

  return (
    <div style={style.page}>
      <nav style={style.nav}>
        {["Home","Cards","Tests","Part 2","Rankings","Support","ILCS","Profile","Bookmarks"].map(n => (
          <button key={n} onClick={() => onNavigate && onNavigate(n)} style={style.navBtn(n === "Bookmarks")}>{n}</button>
        ))}
      </nav>
      <div style={style.main}>
        <div style={style.amberLine} />
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", flexWrap: "wrap", gap: "16px", marginBottom: "8px" }}>
          <div>
            <div style={style.pageTitle}>Bookmarks</div>
            <div style={style.subtitle}>{bookmarkedCards.length} cards saved for review</div>
          </div>
          {filtered.length > 0 && <button style={style.btn("primary")}>▶ Study Bookmarked</button>}
        </div>

        <div style={{ display: "flex", flexWrap: "wrap", gap: "8px", marginBottom: "28px" }}>
          {cats.map(c => (
            <button key={c} onClick={() => setFilter(c)} style={style.pill(filter === c)}>{c}</button>
          ))}
        </div>

        {filtered.length === 0 ? (
          <div style={{ ...style.card, textAlign: "center", padding: "60px 40px" }}>
            <div style={{ fontSize: "48px", marginBottom: "16px" }}>☆</div>
            <div style={{ fontSize: "18px", fontWeight: "600", marginBottom: "8px" }}>No bookmarks yet</div>
            <div style={{ color: COLORS.muted, fontSize: "14px" }}>Star flashcards while studying to save them here for quick review.</div>
          </div>
        ) : (
          <div style={{ display: "grid", gap: "10px" }}>
            {filtered.map(card => (
              <div key={card.id} style={{
                ...style.card,
                display: "flex",
                alignItems: "center",
                gap: "16px",
                borderLeft: `3px solid ${COLORS.amber}`,
              }}>
                <div style={{ flex: 1 }}>
                  <div style={{ display: "flex", alignItems: "center", gap: "10px", marginBottom: "6px" }}>
                    <span style={style.tag(difficultyColor[card.difficulty])}>{card.difficulty}</span>
                    <span style={{ color: COLORS.muted, fontSize: "12px" }}>{card.category}</span>
                  </div>
                  <div style={{ fontWeight: "600", fontSize: "15px" }}>{card.title}</div>
                  <div style={{ color: COLORS.dimmed, fontSize: "12px", marginTop: "2px" }}>{card.code}</div>
                </div>
                <div style={{ display: "flex", gap: "8px" }}>
                  <button style={{ ...style.btn("outline"), padding: "7px 14px", fontSize: "13px" }}>Study</button>
                  <button style={{ color: COLORS.amber, background: "transparent", border: "none", cursor: "pointer", fontSize: "20px" }}>★</button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

// ─── PART 2 PAGE ─────────────────────────────────────────────────────────────
const part2Sections = [
  { id: "written", label: "Written Scenarios", desc: "Full 20-minute timed scenarios with AI grading", count: 20, color: COLORS.blue, icon: "✍️", completed: 4, framework: "Use the R.E.A.C.T.I.O.N. framework to structure your written response. Graded by AI on accuracy, completeness, and proper procedure.", sample: "You arrive at a homicide scene. The victim is found in an alley with multiple stab wounds. Describe your initial actions as the detective in charge." },
  { id: "most", label: "Most Appropriate", desc: "Select the BEST action for each detective scenario", count: 10, color: COLORS.green, icon: "✅", completed: 10, framework: "Choose the single BEST course of action. Consider legal requirements, department policy, and officer safety in your selection.", sample: "A witness to a robbery refuses to speak with you. What is the MOST appropriate action?" },
  { id: "least", label: "Least Appropriate", desc: "Select the WORST action for each detective scenario", count: 10, color: COLORS.red, icon: "🚫", completed: 3, framework: "Choose the single WORST course of action. Identify actions that violate policy, law, or sound investigative practice.", sample: "During an interrogation, the suspect invokes their right to an attorney. What is the LEAST appropriate response?" },
  { id: "legal", label: "Legal Trap", desc: "Identify legally problematic actions in complex scenarios", count: 30, color: COLORS.amber, icon: "⚖️", completed: 12, framework: "Identify the action or statement in the scenario that creates legal liability, violates constitutional rights, or could result in case suppression.", sample: "During a traffic stop, the officer smells marijuana and searches the vehicle without consent. Which action in this scenario is the legal trap?" },
  { id: "digital", label: "Digital Evidence", desc: "Handle digital evidence scenarios with proper chain of custody", count: 10, color: COLORS.blue, icon: "💾", completed: 2, framework: "Apply digital forensics best practices. Demonstrate knowledge of chain of custody, write-blockers, hashing, and proper handling of electronic devices.", sample: "You arrive at a crime scene and find a suspect's unlocked smartphone on a table. Describe the proper steps to preserve the digital evidence." },
  { id: "mini", label: "Mini Scenarios", desc: "Short scenario bursts testing quick decision-making", count: 10, color: COLORS.muted, icon: "⚡", completed: 9, framework: "Quick 2-3 sentence scenarios requiring fast, accurate decision-making. Tests instinctive application of department policy and law.", sample: "A complainant calls 911 claiming their neighbor threatened them. When you arrive, the neighbor denies everything. What do you do?" },
];

const reactionFramework = [
  { letter: "R", word: "Recognize", desc: "Identify the type of incident and your role" },
  { letter: "E", word: "Evaluate", desc: "Assess the scene, threats, and available information" },
  { letter: "A", word: "Act", desc: "Take immediate necessary actions per policy" },
  { letter: "C", word: "Communicate", desc: "Notify supervisors, partners, and dispatch" },
  { letter: "T", word: "Tenacious", desc: "Follow through on all leads and documentation" },
  { letter: "I", word: "Investigate", desc: "Conduct thorough, methodical investigation" },
  { letter: "O", word: "Organize", desc: "Compile and organize all evidence and reports" },
  { letter: "N", word: "Narrate", desc: "Write clear, accurate, legally sound reports" },
];

function Part2Page({ onNavigate }) {
  const [showReaction, setShowReaction] = useState(false);
  const [showGrading, setShowGrading] = useState(false);
  const [activeSection, setActiveSection] = useState(null);

  const totalCompleted = part2Sections.reduce((s, x) => s + x.completed, 0);
  const totalQuestions = part2Sections.reduce((s, x) => s + x.count, 0);
  const overallPct = Math.round((totalCompleted / totalQuestions) * 100);

  if (activeSection) {
    const sec = part2Sections.find(s => s.id === activeSection);
    return (
      <div style={style.page}>
        <nav style={style.nav}>
          {["Home","Cards","Tests","Part 2","Rankings","Support","ILCS","Profile","Bookmarks"].map(n => (
            <button key={n} onClick={() => { setActiveSection(null); onNavigate && onNavigate(n); }} style={style.navBtn(n === "Part 2")}>{n}</button>
          ))}
        </nav>
        <div style={style.main}>
          <button onClick={() => setActiveSection(null)} style={{ ...style.btn("ghost"), marginBottom: "20px", paddingLeft: 0 }}>← Back to Part 2</button>
          <div style={{ display: "flex", alignItems: "center", gap: "14px", marginBottom: "24px" }}>
            <span style={{ fontSize: "36px" }}>{sec.icon}</span>
            <div>
              <div style={style.pageTitle}>{sec.label}</div>
              <div style={style.subtitle}>{sec.desc}</div>
            </div>
          </div>
          <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "16px", marginBottom: "24px" }}>
            <div style={{ ...style.card, borderLeft: `3px solid ${sec.color}` }}>
              <div style={{ color: COLORS.muted, fontSize: "12px", textTransform: "uppercase", letterSpacing: "0.08em", marginBottom: "8px" }}>Your Progress</div>
              <div style={{ display: "flex", alignItems: "flex-end", gap: "8px", marginBottom: "10px" }}>
                <span style={{ fontSize: "36px", fontWeight: "700", color: sec.color }}>{sec.completed}</span>
                <span style={{ color: COLORS.muted, fontSize: "16px", marginBottom: "6px" }}>/ {sec.count} completed</span>
              </div>
              <div style={{ height: "6px", background: COLORS.border, borderRadius: "3px" }}>
                <div style={{ width: `${(sec.completed / sec.count) * 100}%`, height: "100%", background: sec.color, borderRadius: "3px" }} />
              </div>
            </div>
            <div style={style.card}>
              <div style={{ color: COLORS.muted, fontSize: "12px", textTransform: "uppercase", letterSpacing: "0.08em", marginBottom: "8px" }}>Grading Method</div>
              <div style={{ fontSize: "14px", lineHeight: "1.6" }}>{sec.framework}</div>
            </div>
          </div>
          <div style={{ ...style.card, marginBottom: "20px", borderLeft: `3px solid ${sec.color}` }}>
            <div style={{ color: COLORS.muted, fontSize: "12px", textTransform: "uppercase", letterSpacing: "0.08em", marginBottom: "12px" }}>Sample Question</div>
            <div style={{ fontSize: "16px", lineHeight: "1.7", fontStyle: "italic" }}>{sec.sample}</div>
          </div>
          <div style={{ display: "flex", gap: "12px" }}>
            <button style={{ ...style.btn("primary"), background: sec.color }}>▶ Start {sec.label}</button>
            <button style={style.btn("outline")}>View All Questions</button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div style={style.page}>
      <nav style={style.nav}>
        {["Home","Cards","Tests","Part 2","Rankings","Support","ILCS","Profile","Bookmarks"].map(n => (
          <button key={n} onClick={() => onNavigate && onNavigate(n)} style={style.navBtn(n === "Part 2")}>{n}</button>
        ))}
      </nav>
      <div style={style.main}>
        {/* Header */}
        <div style={{
          background: `linear-gradient(135deg, ${COLORS.card} 60%, ${COLORS.amber}0a)`,
          border: `1px solid ${COLORS.border}`,
          borderTop: `3px solid ${COLORS.amber}`,
          borderRadius: "12px",
          padding: "28px 28px 24px",
          marginBottom: "24px",
        }}>
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", flexWrap: "wrap", gap: "16px" }}>
            <div>
              <span style={{ ...style.badge(COLORS.amber), marginBottom: "14px", display: "inline-flex" }}>★ Premium</span>
              <div style={{ fontSize: "28px", fontWeight: "700", letterSpacing: "-0.02em", marginBottom: "6px" }}>Part 2 — Detective Exam</div>
              <div style={{ color: COLORS.muted, fontSize: "14px" }}>I/O Solutions mixed-method exam simulation with AI grading</div>
            </div>
            <div style={{ textAlign: "right" }}>
              <div style={{ fontSize: "42px", fontWeight: "700", color: COLORS.amber, letterSpacing: "-0.02em" }}>{overallPct}%</div>
              <div style={{ color: COLORS.muted, fontSize: "12px" }}>{totalCompleted} / {totalQuestions} completed</div>
            </div>
          </div>
          <div style={{ height: "6px", background: COLORS.border, borderRadius: "3px", marginTop: "20px" }}>
            <div style={{ width: `${overallPct}%`, height: "100%", background: `linear-gradient(to right, ${COLORS.amber}, ${COLORS.cyan})`, borderRadius: "3px" }} />
          </div>
        </div>

        {/* Info accordions */}
        <div style={{ display: "grid", gap: "10px", marginBottom: "28px" }}>
          <div style={{ ...style.card, cursor: "pointer" }} onClick={() => setShowGrading(!showGrading)}>
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
              <div style={{ display: "flex", alignItems: "center", gap: "10px", fontWeight: "600", fontSize: "15px" }}>
                <span style={{ color: COLORS.cyan }}>🎯</span> How You're Graded
              </div>
              <span style={{ color: COLORS.dimmed }}>{showGrading ? "▲" : "▼"}</span>
            </div>
            {showGrading && (
              <div style={{ marginTop: "16px", display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(200px, 1fr))", gap: "10px" }}>
                {[
                  { label: "Written Scenarios", method: "AI grading on accuracy, completeness & procedure" },
                  { label: "Most / Least Appropriate", method: "Binary — correct or incorrect, no partial credit" },
                  { label: "Legal Trap", method: "Identify the specific legally problematic element" },
                  { label: "Digital Evidence", method: "Chain of custody and procedural accuracy" },
                  { label: "Mini Scenarios", method: "Policy-based binary scoring" },
                ].map(g => (
                  <div key={g.label} style={{ background: COLORS.bg, borderRadius: "8px", padding: "12px 14px", border: `1px solid ${COLORS.border}` }}>
                    <div style={{ fontWeight: "600", fontSize: "13px", marginBottom: "4px" }}>{g.label}</div>
                    <div style={{ color: COLORS.muted, fontSize: "12px", lineHeight: "1.5" }}>{g.method}</div>
                  </div>
                ))}
              </div>
            )}
          </div>

          <div style={{ ...style.card, cursor: "pointer" }} onClick={() => setShowReaction(!showReaction)}>
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
              <div style={{ display: "flex", alignItems: "center", gap: "10px", fontWeight: "600", fontSize: "15px" }}>
                <span style={{ color: COLORS.amber }}>🛡️</span> R.E.A.C.T.I.O.N. Framework
              </div>
              <span style={{ color: COLORS.dimmed }}>{showReaction ? "▲" : "▼"}</span>
            </div>
            {showReaction && (
              <div style={{ marginTop: "16px", display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(220px, 1fr))", gap: "10px" }}>
                {reactionFramework.map(r => (
                  <div key={r.letter} style={{ display: "flex", alignItems: "flex-start", gap: "12px", background: COLORS.bg, borderRadius: "8px", padding: "12px 14px", border: `1px solid ${COLORS.border}` }}>
                    <div style={{
                      width: "36px", height: "36px", borderRadius: "8px",
                      background: COLORS.amber + "22", border: `1px solid ${COLORS.amber}44`,
                      display: "flex", alignItems: "center", justifyContent: "center",
                      fontWeight: "900", fontSize: "18px", color: COLORS.amber, flexShrink: 0,
                    }}>{r.letter}</div>
                    <div>
                      <div style={{ fontWeight: "700", fontSize: "13px", marginBottom: "2px" }}>{r.word}</div>
                      <div style={{ color: COLORS.muted, fontSize: "12px", lineHeight: "1.5" }}>{r.desc}</div>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>

        {/* Section cards grid */}
        <div style={{ marginBottom: "12px", fontSize: "13px", color: COLORS.muted, textTransform: "uppercase", letterSpacing: "0.08em" }}>Scenario Types</div>
        <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(300px, 1fr))", gap: "14px" }}>
          {part2Sections.map(sec => {
            const pct = Math.round((sec.completed / sec.count) * 100);
            return (
              <div key={sec.id} onClick={() => setActiveSection(sec.id)} style={{
                ...style.card,
                cursor: "pointer",
                borderLeft: `3px solid ${sec.color}`,
                transition: "transform 0.15s",
              }}>
                <div style={{ display: "flex", alignItems: "center", gap: "10px", marginBottom: "8px" }}>
                  <span style={{ fontSize: "22px" }}>{sec.icon}</span>
                  <div style={{ fontWeight: "700", fontSize: "15px" }}>{sec.label}</div>
                </div>
                <div style={{ color: COLORS.muted, fontSize: "13px", marginBottom: "14px", lineHeight: "1.5" }}>{sec.desc}</div>
                <div style={{ display: "flex", justifyContent: "space-between", marginBottom: "6px" }}>
                  <span style={{ color: COLORS.dimmed, fontSize: "12px" }}>{sec.completed} / {sec.count} done</span>
                  <span style={{ fontWeight: "700", color: sec.color, fontSize: "13px" }}>{pct}%</span>
                </div>
                <div style={{ height: "4px", background: COLORS.border, borderRadius: "2px", marginBottom: "14px" }}>
                  <div style={{ width: `${pct}%`, height: "100%", background: sec.color, borderRadius: "2px" }} />
                </div>
                <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                  <span style={style.badge(sec.color)}>{sec.count} questions</span>
                  <span style={{ color: sec.color, fontWeight: "600", fontSize: "14px" }}>Start →</span>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}

// ─── HOME PAGE ────────────────────────────────────────────────────────────────
function HomePage({ onNavigate }) {
  const statCards = [
    { label: "Flashcards", value: "136", sub: "12 studied", icon: "📚", color: COLORS.cyan, progress: 9, page: "Cards" },
    { label: "Scenarios", value: "20", sub: "12 completed", icon: "📋", color: COLORS.green, progress: 60, page: "Cards" },
    { label: "Bookmarked", value: "3", sub: "saved for review", icon: "★", color: COLORS.amber, progress: null, page: "Bookmarks" },
    { label: "Avg Score", value: "76%", sub: "4 responses", icon: "📊", color: COLORS.blue, progress: 76, page: "Tests" },
  ];

  const quickTests = [
    { label: "25 Question Quiz", desc: "Quick practice test", time: "~15 min", color: COLORS.cyan, icon: "⚡" },
    { label: "50 Question Test", desc: "Standard practice exam", time: "~30 min", color: COLORS.amber, icon: "📋" },
    { label: "Full 105 Exam", desc: "Complete simulation", time: "~60 min", color: COLORS.red, icon: "🎯" },
  ];

  const recentActivity = [
    { action: "Completed 25Q Quiz", score: "84%", time: "2 days ago", icon: "✓", color: COLORS.green },
    { action: "Studied ILCS Flashcards", score: "14 cards", time: "2 days ago", icon: "📚", color: COLORS.cyan },
    { action: "Completed Gold Scenario #7", score: "90%", time: "4 days ago", icon: "✓", color: COLORS.green },
    { action: "Bookmarked 3 cards", score: "", time: "5 days ago", icon: "★", color: COLORS.amber },
  ];

  const part2Sections = [
    { label: "Written Scenarios", count: 20, color: COLORS.blue },
    { label: "Most Appropriate", count: 10, color: COLORS.green },
    { label: "Least Appropriate", count: 10, color: COLORS.red },
    { label: "Legal Trap", count: 30, color: COLORS.amber },
    { label: "Digital Evidence", count: 10, color: COLORS.muted },
  ];

  return (
    <div style={style.page}>
      <nav style={style.nav}>
        {["Home","Cards","Tests","Part 2","Rankings","Support","ILCS","Profile","Bookmarks"].map(n => (
          <button key={n} onClick={() => onNavigate && onNavigate(n)} style={style.navBtn(n === "Home")}>{n}</button>
        ))}
      </nav>

      <div style={style.main}>
        {/* Welcome Header */}
        <div style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "flex-start",
          flexWrap: "wrap",
          gap: "16px",
          marginBottom: "32px",
          paddingBottom: "24px",
          borderBottom: `1px solid ${COLORS.border}`,
        }}>
          <div>
            <div style={{ color: COLORS.muted, fontSize: "13px", marginBottom: "4px", letterSpacing: "0.04em" }}>Welcome back,</div>
            <div style={{ fontSize: "32px", fontWeight: "700", letterSpacing: "-0.02em", marginBottom: "6px" }}>Nathaniel Warner</div>
            <div style={{ display: "flex", alignItems: "center", gap: "10px" }}>
              <div style={{ width: "8px", height: "8px", borderRadius: "50%", background: COLORS.green, boxShadow: `0 0 6px ${COLORS.green}` }} />
              <span style={{ color: COLORS.muted, fontSize: "13px" }}>Keep up the great work — you're making progress!</span>
            </div>
          </div>
          <div style={{ display: "flex", gap: "10px", flexWrap: "wrap" }}>
            <button onClick={() => onNavigate && onNavigate("Cards")} style={style.btn("outline")}>Study Cards</button>
            <button onClick={() => onNavigate && onNavigate("Tests")} style={style.btn("primary")}>▶ Start Test</button>
          </div>
        </div>

        {/* Help Us Improve AI Grading Banner */}
        <div style={{
          ...style.card,
          marginBottom: "24px",
          borderLeft: `3px solid ${COLORS.amber}`,
          background: COLORS.amber + "0a",
          display: "flex",
          alignItems: "center",
          gap: "14px",
          padding: "16px 20px",
        }}>
          <span style={{ fontSize: "22px" }}>📢</span>
          <div style={{ flex: 1 }}>
            <div style={{ fontWeight: "700", fontSize: "14px", color: COLORS.amber, marginBottom: "2px" }}>Help Us Improve AI Grading</div>
            <div style={{ color: COLORS.muted, fontSize: "13px", marginBottom: "8px" }}>After completing a scenario, you can report incorrect grades or suggest corrections. Your feedback helps improve grading accuracy for everyone.</div>
            <div style={{ display: "flex", gap: "12px" }}>
              <span onClick={() => onNavigate && onNavigate("Corrections")} style={{ color: COLORS.amber, fontSize: "13px", fontWeight: "600", cursor: "pointer" }}>View Corrections & Updates →</span>
            </div>
          </div>
        </div>

        {/* Stat Cards */}
        <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(200px, 1fr))", gap: "14px", marginBottom: "32px" }}>
          {statCards.map(s => (
            <div key={s.label} onClick={() => onNavigate && onNavigate(s.page)} style={{
              ...style.card,
              cursor: "pointer",
              borderTop: `2px solid ${s.color}44`,
              transition: "border-color 0.15s, transform 0.15s",
              position: "relative",
              overflow: "hidden",
            }}>
              <div style={{ position: "absolute", top: "12px", right: "14px", fontSize: "22px", opacity: 0.4 }}>{s.icon}</div>
              <div style={{ color: COLORS.muted, fontSize: "12px", letterSpacing: "0.06em", textTransform: "uppercase", marginBottom: "8px" }}>{s.label}</div>
              <div style={{ fontSize: "36px", fontWeight: "700", color: s.color, marginBottom: "2px", letterSpacing: "-0.02em" }}>{s.value}</div>
              <div style={{ color: COLORS.dimmed, fontSize: "12px", marginBottom: s.progress !== null ? "12px" : "0" }}>{s.sub}</div>
              {s.progress !== null && (
                <div style={{ height: "3px", background: COLORS.border, borderRadius: "2px" }}>
                  <div style={{ width: `${s.progress}%`, height: "100%", background: s.color, borderRadius: "2px", transition: "width 0.6s" }} />
                </div>
              )}
            </div>
          ))}
        </div>

        {/* Quick Start + Leaderboard row */}
        <div style={{ display: "grid", gridTemplateColumns: "1fr 320px", gap: "16px", marginBottom: "32px", alignItems: "start" }}>
          {/* Quick Start */}
          <div style={style.card}>
            <div style={{ display: "flex", alignItems: "center", gap: "8px", marginBottom: "18px" }}>
              <span style={{ fontSize: "18px" }}>⚡</span>
              <span style={{ fontWeight: "700", fontSize: "16px" }}>Quick Start — Practice Tests</span>
            </div>
            <div style={{ display: "grid", gap: "10px" }}>
              {quickTests.map(t => (
                <div key={t.label} onClick={() => onNavigate && onNavigate("Tests")} style={{
                  display: "flex",
                  alignItems: "center",
                  gap: "14px",
                  padding: "14px 16px",
                  background: COLORS.bg,
                  borderRadius: "10px",
                  border: `1px solid ${COLORS.border}`,
                  cursor: "pointer",
                  transition: "border-color 0.15s",
                }}>
                  <div style={{
                    width: "40px", height: "40px", borderRadius: "10px",
                    background: t.color + "22", border: `1px solid ${t.color}44`,
                    display: "flex", alignItems: "center", justifyContent: "center", fontSize: "18px",
                  }}>{t.icon}</div>
                  <div style={{ flex: 1 }}>
                    <div style={{ fontWeight: "600", fontSize: "14px", marginBottom: "2px" }}>{t.label}</div>
                    <div style={{ color: COLORS.muted, fontSize: "12px" }}>{t.desc}</div>
                  </div>
                  <div style={{ display: "flex", flexDirection: "column", alignItems: "flex-end", gap: "4px" }}>
                    <span style={{ color: COLORS.dimmed, fontSize: "11px" }}>⏱ {t.time}</span>
                    <span style={{ color: t.color, fontSize: "16px" }}>›</span>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Leaderboard */}
          <div style={style.card}>
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "16px" }}>
              <div style={{ display: "flex", alignItems: "center", gap: "8px" }}>
                <span style={{ fontSize: "18px" }}>🏆</span>
                <span style={{ fontWeight: "700", fontSize: "16px" }}>Top Performers</span>
              </div>
              <button onClick={() => onNavigate && onNavigate("Rankings")} style={{ ...style.btn("ghost"), padding: "4px 10px", fontSize: "12px", color: COLORS.amber }}>See all →</button>
            </div>
            <div style={{ display: "grid", gap: "4px" }}>
              {leaderboardData.slice(0, 6).map(p => (
                <div key={p.rank} style={{
                  display: "flex",
                  alignItems: "center",
                  gap: "10px",
                  padding: "10px 10px",
                  borderRadius: "8px",
                  background: p.isMe ? COLORS.amberGlow : "transparent",
                  border: p.isMe ? `1px solid ${COLORS.amber}33` : "1px solid transparent",
                }}>
                  <span style={{ width: "24px", fontSize: p.rank <= 3 ? "16px" : "13px", textAlign: "center", color: p.rank > 3 ? COLORS.dimmed : undefined }}>{p.badge}</span>
                  <span style={{ flex: 1, fontSize: "13px", fontWeight: p.isMe ? "700" : "400", color: p.isMe ? COLORS.amber : COLORS.text, whiteSpace: "nowrap", overflow: "hidden", textOverflow: "ellipsis" }}>{p.name}</span>
                  <span style={{ fontSize: "13px", color: COLORS.cyan, fontWeight: "600" }}>{p.avg}%</span>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Part 2 Section Preview */}
        <div style={{
          ...style.card,
          marginBottom: "32px",
          borderTop: `2px solid ${COLORS.amber}`,
          background: `linear-gradient(135deg, ${COLORS.card} 70%, ${COLORS.amber}08)`,
        }}>
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "18px", flexWrap: "wrap", gap: "12px" }}>
            <div style={{ display: "flex", alignItems: "center", gap: "12px" }}>
              <span style={style.badge(COLORS.amber)}>★ Premium</span>
              <span style={{ fontWeight: "700", fontSize: "17px" }}>Part 2 — Detective Exam</span>
            </div>
            <button onClick={() => onNavigate && onNavigate("Part 2")} style={{ ...style.btn("outline"), fontSize: "13px", borderColor: COLORS.amber + "55", color: COLORS.amber }}>Open Part 2 →</button>
          </div>
          <div style={{ color: COLORS.muted, fontSize: "13px", marginBottom: "18px" }}>
            I/O Solutions mixed-method exam simulation with AI grading
          </div>
          <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(150px, 1fr))", gap: "10px" }}>
            {part2Sections.map(s => (
              <div key={s.label} style={{
                background: COLORS.bg,
                border: `1px solid ${COLORS.border}`,
                borderLeft: `3px solid ${s.color}`,
                borderRadius: "8px",
                padding: "12px 14px",
              }}>
                <div style={{ fontWeight: "600", fontSize: "13px", marginBottom: "4px" }}>{s.label}</div>
                <div style={{ color: s.color, fontWeight: "700", fontSize: "20px" }}>{s.count}</div>
                <div style={{ color: COLORS.dimmed, fontSize: "11px" }}>questions</div>
              </div>
            ))}
          </div>
        </div>

        {/* Recent Activity */}
        <div style={style.card}>
          <div style={{ fontWeight: "700", fontSize: "16px", marginBottom: "18px" }}>Recent Activity</div>
          <div style={{ display: "grid", gap: "2px" }}>
            {recentActivity.map((a, i) => (
              <div key={i} style={{
                display: "flex",
                alignItems: "center",
                gap: "14px",
                padding: "12px 8px",
                borderBottom: i < recentActivity.length - 1 ? `1px solid ${COLORS.border}` : "none",
              }}>
                <div style={{
                  width: "32px", height: "32px", borderRadius: "50%",
                  background: a.color + "22", border: `1px solid ${a.color}44`,
                  display: "flex", alignItems: "center", justifyContent: "center",
                  fontSize: "14px", color: a.color, flexShrink: 0,
                }}>{a.icon}</div>
                <div style={{ flex: 1 }}>
                  <div style={{ fontSize: "14px", fontWeight: "500" }}>{a.action}</div>
                  <div style={{ color: COLORS.dimmed, fontSize: "12px" }}>{a.time}</div>
                </div>
                {a.score && <span style={{ color: a.color, fontWeight: "700", fontSize: "14px" }}>{a.score}</span>}
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

// ─── SUBMIT CORRECTION ───────────────────────────────────────────────────────
const correctionCategories = ["Score Too Low", "Score Too High", "Missing Information", "Incorrect Feedback", "Other"];

function SubmitCorrectionPage({ onNavigate, correctionContext }) {
  const [category, setCategory] = useState("");
  const [details, setDetails] = useState("");
  const [submitted, setSubmitted] = useState(false);

  const ctx = correctionContext || {};

  if (submitted) {
    return (
      <div style={{ ...style.page, alignItems: "center", justifyContent: "center", padding: "20px" }}>
        <div style={{ ...style.card, maxWidth: "520px", width: "100%", textAlign: "center", padding: "48px 40px" }}>
          <div style={{ width: "64px", height: "64px", borderRadius: "50%", background: COLORS.green + "22", border: `2px solid ${COLORS.green}44`, display: "flex", alignItems: "center", justifyContent: "center", fontSize: "28px", margin: "0 auto 20px" }}>✓</div>
          <div style={{ fontSize: "22px", fontWeight: "700", marginBottom: "8px" }}>Correction Submitted</div>
          <div style={{ color: COLORS.muted, fontSize: "14px", lineHeight: "1.6", marginBottom: "32px" }}>
            Thank you for your feedback. Our team will review your correction and update the grading if needed. You can track the status on the Corrections page.
          </div>
          <div style={{ display: "flex", gap: "12px", justifyContent: "center" }}>
            <button onClick={() => onNavigate && onNavigate("Corrections")} style={style.btn("outline")}>View My Corrections</button>
            <button onClick={() => onNavigate && onNavigate("Part 2")} style={style.btn("primary")}>Back to Scenarios</button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div style={style.page}>
      <nav style={style.nav}>
        {["Home","Cards","Tests","Part 2","Rankings","Support","ILCS","Profile","Bookmarks"].map(n => (
          <button key={n} onClick={() => onNavigate && onNavigate(n)} style={style.navBtn(n === "Support")}>{n}</button>
        ))}
      </nav>
      <div style={{ ...style.main, maxWidth: "720px" }}>
        <button onClick={() => onNavigate && onNavigate("Corrections")} style={{ ...style.btn("ghost"), marginBottom: "20px", padding: "4px 0" }}>← Back to Corrections</button>
        <div style={style.amberLine} />
        <div style={style.pageTitle}>Report a Grading Issue</div>
        <div style={style.subtitle}>Help us improve AI grading accuracy for everyone</div>

        {/* Scenario Context */}
        {ctx.title && (
          <div style={{ ...style.card, marginBottom: "20px", borderLeft: `3px solid ${COLORS.cyan}`, display: "flex", alignItems: "center", gap: "16px" }}>
            <div style={{ flex: 1 }}>
              <div style={{ color: COLORS.dimmed, fontSize: "11px", letterSpacing: "0.08em", textTransform: "uppercase", marginBottom: "6px" }}>Scenario</div>
              <div style={{ fontWeight: "600", fontSize: "15px", marginBottom: "4px" }}>{ctx.title}</div>
              <div style={{ display: "flex", alignItems: "center", gap: "10px" }}>
                {ctx.category && <span style={{ color: COLORS.muted, fontSize: "12px" }}>{ctx.category}</span>}
              </div>
            </div>
            {ctx.score !== undefined && ctx.score !== null && (
              <div style={{ fontSize: "28px", fontWeight: "700", color: ctx.score >= 80 ? COLORS.green : ctx.score >= 70 ? COLORS.amber : COLORS.red }}>{ctx.score}%</div>
            )}
          </div>
        )}

        {/* Category Selector */}
        <div style={{ ...style.card, marginBottom: "20px" }}>
          <div style={{ fontWeight: "700", marginBottom: "12px", fontSize: "15px" }}>What's the issue?</div>
          <div style={{ display: "flex", flexWrap: "wrap", gap: "8px" }}>
            {correctionCategories.map(cat => (
              <button key={cat} onClick={() => setCategory(cat)} style={style.pill(category === cat)}>{cat}</button>
            ))}
          </div>
        </div>

        {/* Details */}
        <div style={{ ...style.card, marginBottom: "20px" }}>
          <div style={{ fontWeight: "700", marginBottom: "8px", fontSize: "15px" }}>Details</div>
          <div style={{ color: COLORS.muted, fontSize: "13px", marginBottom: "12px" }}>
            Explain what you think was graded incorrectly and why. The more detail you provide, the faster we can review.
          </div>
          <textarea
            value={details}
            onChange={e => setDetails(e.target.value)}
            placeholder="e.g. I mentioned the correct General Order (G03-02-01) in my response but the AI said I didn't reference any orders..."
            style={{ ...style.input, minHeight: "160px", resize: "vertical", lineHeight: "1.6", fontSize: "14px" }}
          />
          <div style={{ color: COLORS.dimmed, fontSize: "12px", marginTop: "8px" }}>{details.length} characters</div>
        </div>

        {/* Submit */}
        <div style={{ display: "flex", justifyContent: "flex-end" }}>
          <button
            onClick={() => setSubmitted(true)}
            disabled={!category || details.length < 20}
            style={{ ...style.btn("primary"), opacity: (!category || details.length < 20) ? 0.4 : 1 }}
          >
            Submit Correction →
          </button>
        </div>
      </div>
    </div>
  );
}

// ─── CORRECTIONS HISTORY ─────────────────────────────────────────────────────
const sampleCorrections = [
  { id: 1, scenario: "Domestic Violence — Order of Protection", category: "Score Too Low", date: "Feb 27, 2026", status: "Pending", detail: "I cited G04-02 and the AI said I didn't reference any General Orders. My response clearly mentioned the order in the Notify section.", adminResponse: null },
  { id: 2, scenario: "Burglary in Progress — Scene Management", category: "Missing Information", date: "Feb 25, 2026", status: "Reviewed", detail: "The AI feedback didn't mention that I correctly identified the need to set up a perimeter. This was a key element that should have been scored.", adminResponse: "Thank you for the feedback. We've reviewed the grading rubric and updated the AI to better recognize perimeter procedures." },
  { id: 3, scenario: "Traffic Stop — Contraband Found", category: "Incorrect Feedback", date: "Feb 22, 2026", status: "Accepted", detail: "The AI said I should have called for a K-9 unit, but per CPD procedure a K-9 is not required when contraband is already in plain view.", adminResponse: "You're correct. We've updated the model answer to remove the K-9 requirement for plain-view contraband scenarios. Your score has been adjusted to 95%." },
  { id: 4, scenario: "Child Abuse Investigation", category: "Score Too Low", date: "Feb 18, 2026", status: "Rejected", detail: "I think my score should have been higher because I mentioned DCFS notification.", adminResponse: "After review, the score was accurate. While DCFS notification was mentioned, several other required elements (medical examination protocol, forensic interview scheduling) were missing from the response." },
];

const correctionStatusColor = { Pending: COLORS.amber, Reviewed: COLORS.cyan, Accepted: COLORS.green, Rejected: COLORS.red };

function CorrectionsPage({ onNavigate }) {
  const [filter, setFilter] = useState("All");
  const [expanded, setExpanded] = useState(null);
  const filters = ["All", "Pending", "Reviewed", "Accepted", "Rejected"];

  const filtered = sampleCorrections.filter(c => filter === "All" || c.status === filter);

  return (
    <div style={style.page}>
      <nav style={style.nav}>
        {["Home","Cards","Tests","Part 2","Rankings","Support","ILCS","Profile","Bookmarks"].map(n => (
          <button key={n} onClick={() => onNavigate && onNavigate(n)} style={style.navBtn(n === "Support")}>{n}</button>
        ))}
      </nav>
      <div style={style.main}>
        <div style={style.amberLine} />
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", flexWrap: "wrap", gap: "16px", marginBottom: "8px" }}>
          <div>
            <div style={style.pageTitle}>My Corrections</div>
            <div style={style.subtitle}>{sampleCorrections.length} corrections submitted · Track your feedback status</div>
          </div>
          <button onClick={() => onNavigate && onNavigate("Submit Correction")} style={style.btn("primary")}>+ Report Issue</button>
        </div>

        {/* Stats row */}
        <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(130px, 1fr))", gap: "10px", marginBottom: "24px" }}>
          {[
            { label: "Pending", count: sampleCorrections.filter(c => c.status === "Pending").length, color: COLORS.amber },
            { label: "Reviewed", count: sampleCorrections.filter(c => c.status === "Reviewed").length, color: COLORS.cyan },
            { label: "Accepted", count: sampleCorrections.filter(c => c.status === "Accepted").length, color: COLORS.green },
            { label: "Rejected", count: sampleCorrections.filter(c => c.status === "Rejected").length, color: COLORS.red },
          ].map(s => (
            <div key={s.label} style={{ ...style.card, textAlign: "center", padding: "14px 12px" }}>
              <div style={{ fontSize: "24px", fontWeight: "700", color: s.color, marginBottom: "2px" }}>{s.count}</div>
              <div style={{ fontSize: "11px", color: COLORS.muted, textTransform: "uppercase", letterSpacing: "0.06em" }}>{s.label}</div>
            </div>
          ))}
        </div>

        {/* Filters */}
        <div style={{ display: "flex", flexWrap: "wrap", gap: "8px", marginBottom: "24px" }}>
          {filters.map(f => (
            <button key={f} onClick={() => setFilter(f)} style={style.pill(filter === f)}>{f}</button>
          ))}
        </div>

        {/* Corrections List */}
        {filtered.length === 0 ? (
          <div style={{ ...style.card, textAlign: "center", padding: "60px 40px" }}>
            <div style={{ fontSize: "48px", marginBottom: "16px" }}>📋</div>
            <div style={{ fontSize: "18px", fontWeight: "600", marginBottom: "8px" }}>No corrections found</div>
            <div style={{ color: COLORS.muted, fontSize: "14px" }}>
              {filter === "All"
                ? "You haven't submitted any corrections yet. After a scenario is graded, use the Report Issue button to submit feedback."
                : `No corrections with "${filter}" status.`}
            </div>
          </div>
        ) : (
          <div style={{ display: "grid", gap: "10px" }}>
            {filtered.map((c) => (
              <div key={c.id} onClick={() => setExpanded(expanded === c.id ? null : c.id)} style={{
                ...style.card,
                cursor: "pointer",
                borderLeft: `3px solid ${correctionStatusColor[c.status]}`,
                transition: "all 0.15s",
              }}>
                <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "6px" }}>
                  <div style={{ display: "flex", alignItems: "center", gap: "10px" }}>
                    <span style={style.badge(correctionStatusColor[c.status])}>{c.status}</span>
                    <span style={{ ...style.badge(COLORS.cyan), fontSize: "10px" }}>{c.category}</span>
                  </div>
                  <div style={{ display: "flex", alignItems: "center", gap: "10px" }}>
                    <span style={{ color: COLORS.dimmed, fontSize: "12px" }}>{c.date}</span>
                    <span style={{ color: COLORS.dimmed, fontSize: "16px" }}>{expanded === c.id ? "▲" : "▼"}</span>
                  </div>
                </div>
                <div style={{ fontWeight: "600", fontSize: "15px" }}>{c.scenario}</div>

                {expanded === c.id && (
                  <div style={{ marginTop: "16px", display: "grid", gap: "12px" }}>
                    <div style={{ padding: "14px 16px", background: COLORS.bg, borderRadius: "8px", borderLeft: `3px solid ${COLORS.muted}` }}>
                      <div style={{ color: COLORS.dimmed, fontSize: "11px", letterSpacing: "0.06em", textTransform: "uppercase", marginBottom: "8px" }}>Your Feedback</div>
                      <div style={{ fontSize: "14px", color: COLORS.muted, lineHeight: "1.6" }}>{c.detail}</div>
                    </div>

                    {c.adminResponse ? (
                      <div style={{ padding: "14px 16px", background: correctionStatusColor[c.status] + "0a", borderRadius: "8px", borderLeft: `3px solid ${correctionStatusColor[c.status]}` }}>
                        <div style={{ color: correctionStatusColor[c.status], fontSize: "11px", letterSpacing: "0.06em", textTransform: "uppercase", marginBottom: "8px", fontWeight: "700" }}>Admin Response</div>
                        <div style={{ fontSize: "14px", color: COLORS.text, lineHeight: "1.6" }}>{c.adminResponse}</div>
                      </div>
                    ) : (
                      <div style={{ padding: "14px 16px", background: COLORS.bg, borderRadius: "8px", textAlign: "center" }}>
                        <span style={{ color: COLORS.dimmed, fontSize: "13px" }}>Awaiting review...</span>
                      </div>
                    )}
                  </div>
                )}
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

// ─── APP SHELL ────────────────────────────────────────────────────────────────
const PAGE_KEYS = ["Home", "Cards", "Tests", "Part 2", "Rankings", "Profile", "ILCS", "Bookmarks", "Corrections"];

export default function App() {
  const [activePage, setActivePage] = useState("Home");
  const [correctionContext, setCorrectionContext] = useState(null);

  const navigate = (page, ctx) => {
    // Map nav labels to page keys
    const map = { "Part 2": "Part 2", "Support": "Corrections" };
    if (ctx) setCorrectionContext(ctx);
    setActivePage(map[page] || page);
  };

  const pageMap = {
    "Home": () => <HomePage onNavigate={navigate} />,
    "Cards": () => <FlashcardsPage onNavigate={navigate} />,
    "Tests": () => <PracticeTestsPage onNavigate={navigate} />,
    "Part 2": () => <Part2Page onNavigate={navigate} />,
    "Rankings": () => <RankingsPage onNavigate={navigate} />,
    "Profile": () => <ProfilePage onNavigate={navigate} />,
    "ILCS": () => <ILCSPage onNavigate={navigate} />,
    "Bookmarks": () => <BookmarksPage onNavigate={navigate} />,
    "Corrections": () => <CorrectionsPage onNavigate={navigate} />,
    "Submit Correction": () => <SubmitCorrectionPage onNavigate={navigate} correctionContext={correctionContext} />,
  };

  const PageComponent = pageMap[activePage] || pageMap["Home"];

  return (
    <div style={{ minHeight: "100vh", background: COLORS.bg }}>
      {/* Top page switcher for demo */}
      <div style={{
        display: "flex",
        gap: "6px",
        padding: "10px 16px",
        background: "#08090c",
        borderBottom: `1px solid ${COLORS.border}`,
        flexWrap: "wrap",
        alignItems: "center",
      }}>
        <span style={{ color: COLORS.dimmed, fontSize: "11px", letterSpacing: "0.08em", textTransform: "uppercase", marginRight: "8px" }}>Pages</span>
        {PAGE_KEYS.map(p => (
          <button key={p} onClick={() => navigate(p)} style={{
            padding: "4px 12px",
            borderRadius: "4px",
            border: `1px solid ${activePage === p ? COLORS.amber : COLORS.border}`,
            background: activePage === p ? COLORS.amber : "transparent",
            color: activePage === p ? "#0e0f13" : COLORS.muted,
            cursor: "pointer",
            fontSize: "12px",
            fontFamily: "'Georgia', serif",
          }}>{p}</button>
        ))}
      </div>
      <PageComponent />
    </div>
  );
}
