import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import DetectiveExamDashboard from './App';

describe('DetectiveExamDashboard', () => {
  // ── Rendering ──────────────────────────────────────────────

  it('renders without crashing', () => {
    render(<DetectiveExamDashboard />);
    expect(screen.getByText('Welcome back, Nate')).toBeInTheDocument();
  });

  it('renders all 4 stat cards with correct values', () => {
    render(<DetectiveExamDashboard />);
    // Stat labels appear in both nav and stat cards, so use getAllByText
    expect(screen.getAllByText('Flashcards').length).toBeGreaterThanOrEqual(2); // nav + stat
    expect(screen.getAllByText('Scenarios').length).toBeGreaterThanOrEqual(2);  // nav + stat
    expect(screen.getByText('Bookmarked')).toBeInTheDocument();
    expect(screen.getByText('Avg Score')).toBeInTheDocument();
    expect(screen.getByText('136')).toBeInTheDocument();
    expect(screen.getByText('9 studied')).toBeInTheDocument();
    expect(screen.getByText('9 completed')).toBeInTheDocument();
    expect(screen.getByText('3 responses')).toBeInTheDocument();
  });

  // ── Sidebar Navigation ────────────────────────────────────

  it('renders all navigation items', () => {
    render(<DetectiveExamDashboard />);
    expect(screen.getByText('Dashboard')).toBeInTheDocument();
    expect(screen.getAllByText('Flashcards').length).toBeGreaterThanOrEqual(1);
    expect(screen.getAllByText('Practice Tests').length).toBeGreaterThanOrEqual(1);
    expect(screen.getByText('Part 2 Exam')).toBeInTheDocument();
    expect(screen.getAllByText('Scenarios').length).toBeGreaterThanOrEqual(1);
    expect(screen.getAllByText('Rankings').length).toBeGreaterThanOrEqual(1);
    expect(screen.getByText('Profile')).toBeInTheDocument();
  });

  it('switches active tab on nav click', async () => {
    render(<DetectiveExamDashboard />);
    // Get nav buttons from the sidebar nav element
    const nav = document.querySelector('nav');
    const buttons = nav.querySelectorAll('button');
    // Second button is "Flashcards" nav item
    const flashcardsBtn = buttons[1];
    await userEvent.click(flashcardsBtn);
    expect(flashcardsBtn).toHaveStyle('color: rgb(96, 165, 250)');
  });

  // ── Sidebar Toggle ────────────────────────────────────────

  it('collapses sidebar when toggle button is clicked', async () => {
    render(<DetectiveExamDashboard />);
    expect(screen.getByText('Nate Warner')).toBeInTheDocument();

    const sidebar = screen.getByText('Detective Exam').closest('aside');
    const toggleBtn = sidebar.querySelector('button');
    await userEvent.click(toggleBtn);

    expect(screen.queryByText('Nate Warner')).not.toBeInTheDocument();
    expect(screen.queryByText('Detective Exam')).not.toBeInTheDocument();
  });

  it('re-expands sidebar after collapsing', async () => {
    render(<DetectiveExamDashboard />);
    const sidebar = screen.getByText('Detective Exam').closest('aside');
    const toggleBtn = sidebar.querySelector('button');

    await userEvent.click(toggleBtn);
    expect(screen.queryByText('Nate Warner')).not.toBeInTheDocument();

    const toggleBtnAfter = sidebar.querySelector('button');
    await userEvent.click(toggleBtnAfter);
    expect(screen.getByText('Nate Warner')).toBeInTheDocument();
  });

  // ── Search / Category Filtering ───────────────────────────

  it('renders all 9 study categories by default', () => {
    render(<DetectiveExamDashboard />);
    expect(screen.getByText('Gold Scenarios')).toBeInTheDocument();
    expect(screen.getByText('ILCS Crime Classifications')).toBeInTheDocument();
    expect(screen.getByText('Part 2 Scenarios')).toBeInTheDocument();
    // These appear in multiple places, just verify they exist
    expect(screen.getAllByText('Ranking Questions').length).toBeGreaterThanOrEqual(1);
    expect(screen.getAllByText('Most Appropriate').length).toBeGreaterThanOrEqual(1);
    expect(screen.getAllByText('Least Appropriate').length).toBeGreaterThanOrEqual(1);
    expect(screen.getAllByText('Legal Trap').length).toBeGreaterThanOrEqual(1);
    expect(screen.getAllByText('Digital Evidence').length).toBeGreaterThanOrEqual(1);
    expect(screen.getAllByText('Mini Scenarios').length).toBeGreaterThanOrEqual(1);
  });

  it('filters categories based on search input', async () => {
    render(<DetectiveExamDashboard />);
    const searchInput = screen.getByPlaceholderText('Search topics...');

    await userEvent.type(searchInput, 'gold');

    expect(screen.getByText('Gold Scenarios')).toBeInTheDocument();
    // ILCS should be gone from categories (it only appears there)
    expect(screen.queryByText('ILCS Crime Classifications')).not.toBeInTheDocument();
  });

  it('shows no matching categories for non-matching search', async () => {
    render(<DetectiveExamDashboard />);
    const searchInput = screen.getByPlaceholderText('Search topics...');

    await userEvent.type(searchInput, 'xyznonexistent');

    // Gold Scenarios only appears in the categories section, so it should be gone
    expect(screen.queryByText('Gold Scenarios')).not.toBeInTheDocument();
    // ILCS only in categories
    expect(screen.queryByText('ILCS Crime Classifications')).not.toBeInTheDocument();
  });

  it('search is case insensitive', async () => {
    render(<DetectiveExamDashboard />);
    const searchInput = screen.getByPlaceholderText('Search topics...');

    await userEvent.type(searchInput, 'ILCS');

    expect(screen.getByText('ILCS Crime Classifications')).toBeInTheDocument();
    expect(screen.queryByText('Gold Scenarios')).not.toBeInTheDocument();
  });

  // ── Practice Tests ────────────────────────────────────────

  it('renders all 3 practice test options with times', () => {
    render(<DetectiveExamDashboard />);
    // "25 Question Quiz" appears in both test options and recent activity
    expect(screen.getAllByText('25 Question Quiz').length).toBeGreaterThanOrEqual(1);
    expect(screen.getByText('50 Question Test')).toBeInTheDocument();
    expect(screen.getByText('Full Practice Exam')).toBeInTheDocument();
    expect(screen.getByText('~15 min')).toBeInTheDocument();
    expect(screen.getByText('~30 min')).toBeInTheDocument();
    expect(screen.getByText('~90 min')).toBeInTheDocument();
  });

  // ── Leaderboard ───────────────────────────────────────────

  it('renders leaderboard with all 5 entries', () => {
    render(<DetectiveExamDashboard />);
    expect(screen.getByText('Bradley Anderson')).toBeInTheDocument();
    expect(screen.getByText('Bell')).toBeInTheDocument();
    expect(screen.getByText('Brandon Lange')).toBeInTheDocument();
    expect(screen.getByText('Anabel Preciado')).toBeInTheDocument();
    expect(screen.getByText('rena maritote')).toBeInTheDocument();
  });

  it('displays user rank in leaderboard section', () => {
    render(<DetectiveExamDashboard />);
    expect(screen.getByText('#12')).toBeInTheDocument();
  });

  // ── Part 2 Exam Section ───────────────────────────────────

  it('renders Part 2 Detective Exam section with premium badge', () => {
    render(<DetectiveExamDashboard />);
    expect(screen.getByText('Part 2 — Detective Exam')).toBeInTheDocument();
    expect(screen.getByText('Premium')).toBeInTheDocument();
    expect(screen.getByText("How You're Graded")).toBeInTheDocument();
    expect(screen.getByText('R.E.A.C.T.I.O.N. Framework')).toBeInTheDocument();
  });

  it('renders Part 2 scenario types', () => {
    render(<DetectiveExamDashboard />);
    expect(screen.getByText('Written Scenarios')).toBeInTheDocument();
    expect(screen.getAllByText('Ranking Questions').length).toBeGreaterThanOrEqual(1);
  });

  // ── Recent Activity ───────────────────────────────────────

  it('renders recent activity with scores', () => {
    render(<DetectiveExamDashboard />);
    expect(screen.getByText('Gold Scenario #4')).toBeInTheDocument();
    expect(screen.getByText('CPD Procedure - G02-01-03')).toBeInTheDocument();
    expect(screen.getByText('Score: 78%')).toBeInTheDocument();
    expect(screen.getByText('Correct')).toBeInTheDocument();
    expect(screen.getByText('Score: 68%')).toBeInTheDocument();
    expect(screen.getByText('2 hours ago')).toBeInTheDocument();
    expect(screen.getByText('Yesterday')).toBeInTheDocument();
    expect(screen.getByText('2 days ago')).toBeInTheDocument();
  });

  // ── User Info ─────────────────────────────────────────────

  it('displays user info in sidebar', () => {
    render(<DetectiveExamDashboard />);
    expect(screen.getByText('NW')).toBeInTheDocument();
    expect(screen.getByText('Nate Warner')).toBeInTheDocument();
    expect(screen.getByText('Rank #12')).toBeInTheDocument();
  });
});
