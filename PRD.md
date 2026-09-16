# Product Requirements Document
## Adaptive Oral Learning Platform
**Working name:** (TBD)  
**Version:** 0.1  
**Date:** 11 Sep 2026  
**Status:** Draft for founder review

---

## 1. One-line product

An app where you upload what you’re studying, say what you need to achieve, and practice by **speaking your answers out loud** — then get a clear report on what you know, what’s weak, and what to retest.

**Tagline options:**
- Prove it out loud.
- Your notes aren’t enough — we find the gaps, then examine you.
- An adaptive viva for any subject.

---

## 2. Problem

Most study tools help you **read, summarize, or quiz yourself in writing**.

Real exams, interviews, and viva voce need you to **explain out loud**. Students often:
- Memorize notes but freeze when asked to speak
- Don’t know what they’re missing until it’s too late
- Get a score with no clear “what to fix next”
- Feel overwhelmed by apps with too many modes, agents, and menus

Existing tools either tutor you (StudyFetch), turn docs into podcasts/quizzes (NotebookLM), or drill flashcards. Few run a **goal-based oral exam** that also **fills knowledge gaps** and **adapts** to mistakes.

---

## 3. Who it’s for (v1)

**Primary:** Students preparing for exams or oral assessments (school, college, certifications) who already have notes/PDFs.

**Secondary (later):** Professionals preparing for interviews / defenses; teachers who want oral practice for a class.

**Languages (v1):** English + Hindi, including Hinglish answers. More languages later.

---

## 4. Product promise (what users should feel)

1. **Simple** — three steps, always.
2. **Fair** — judged on understanding, not accent or perfect English.
3. **Honest** — tells you what’s weak and why, with sources.
4. **Useful next step** — one clear retest, not a wall of options.

---

## 5. The simple user flow

Keep the product to **one loop**. No dashboards full of modes on day one.

```
1. Upload          2. Set goal         3. Practice          4. See results
   your material  →  what you need   →  speak answers     →  strengths,
   (PDF / text)      to achieve         to questions         weak spots,
                                                            then retest
```

### Screen-by-screen (v1)

| Step | What the user sees | What they do |
|------|--------------------|--------------|
| **Home** | “Start practice” | Tap once |
| **Upload** | Drag PDF or paste text | Add material |
| **Goal** | Short form: subject, exam/date (optional), target (e.g. “score 80%”, “explain Gauss’s Law”) | Fill 3–5 fields |
| **Preparing** | Progress: “Reading your notes… Finding gaps… Building your practice set…” | Wait (with plain status, not jargon) |
| **Practice** | One question at a time. Listen → speak (or type in v1). Next. | Answer |
| **Results** | Readiness %, Strong / Weak / Misconceptions, 3 next actions | Review |
| **Retest** | “Practice weak areas (5 questions)” | One tap |

**Overwhelm rules:**
- Never show internal agents, rubrics, or “knowledge graphs” to the user
- One question on screen at a time
- Default path is always: Upload → Goal → Practice → Results → Retest
- Advanced settings (language, typed vs voice, difficulty) live behind a single “Settings” link

---

## 6. Features — keep / cut

### Must ship (MVP — Phase 1)

| Feature | User-facing name | Why it stays |
|---------|------------------|--------------|
| Upload PDF, Markdown, plain text | **Upload notes** | Core input |
| Learning goal (subject, level, target, optional deadline) | **What’s your goal?** | Makes practice purposeful |
| Auto topic map from notes | (Hidden; shown as “Topics we’ll cover”) | Structure without complexity |
| Fill gaps with trusted sources when notes are incomplete | **We filled a few gaps from trusted sources** | Key differentiator — shown as a short list + links |
| Generate a short practice set (e.g. 10 questions) | **Your practice set** | Not endless quiz bank |
| Typed answers first | **Type your answer** | Ship quality before voice |
| Fair scoring on understanding | **How you did** | Deterministic score from rubrics (backend) |
| Weak areas + misconceptions in plain language | **What to fix** | Actionable |
| One-tap targeted retest | **Retest weak areas** | Closes the loop |
| English + Hindi UI / answers | **Language** | Product requirement |

### Should ship soon (Phase 2–4)

| Feature | User-facing name |
|---------|------------------|
| Citations for every important claim / question | **See sources** |
| Adaptive next question (harder / follow-up / diagnostic) | Feels like “the app listens to you” — no separate mode |
| Mastery per topic over time | **Your progress** (simple bars) |
| Voice: hear questions + speak answers | **Speak your answer** |
| STT confidence → “Could you say that again?” | Prevents unfair penalties |

### Explicitly later (do not clutter MVP)

- Avatars, gamification, leaderboards, classrooms
- Dozens of question modes
- Video / YouTube / scanned notes (after PDF/text works)
- Full 22-language support
- Mobile apps / phone IVR (web-first is fine)
- Teacher dashboards / LMS sync
- Spaced repetition & long-term forgetting models

---

## 7. Differentiators (what we say vs competitors)

Say this in marketing and keep it true in the product:

| Us | Them |
|----|------|
| **Goal-based oral practice** — built for explaining out loud | StudyFetch: voice *tutor* / study suite |
| **We research what’s missing for your goal**, then examine you | NotebookLM: stays inside your uploads (chat); audio is a podcast, not an exam |
| **Scores understanding with clear criteria**, not “sounds right” | Flashcard apps: memory drills |
| **Finds misconceptions**, not just wrong answers | Most quiz tools: right/wrong only |
| **Adapts the next question** from your weak spots | Static quiz generators |
| **Simple 4-step loop** | Feature-heavy study platforms |

**Closest watch-outs:** LearnCastAI (oral exam simulator), OralExam.ai / Orazio (institutional viva). We win on **goal → gap research → adaptive oral mastery** + simpler consumer UX.

**Moat (internal — not user-facing jargon):** Knowledge model + learner model + assessment engine + adaptive question policy. Replaceable: raw RAG, TTS, STT vendors.

---

## 8. What “simple” means in the UI copy

| Don’t say | Do say |
|-----------|--------|
| Scope Agent / Research Agent | Preparing your practice |
| Knowledge graph / embeddings | Topics we’ll cover |
| Rubric evaluation | How you did |
| Hybrid RAG / provenance | See sources |
| Misconception ontology | Common mix-ups we noticed |
| Adaptive question policy | Next question based on your answers |

---

## 9. Practice session rules (so it never feels chaotic)

1. **One question at a time** — no question list dump mid-session  
2. **Progress bar** — “Question 3 of 10”  
3. **Skip / I don’t know** — always allowed; counted as weak, not shameful  
4. **No answer key shown during the session**  
5. **After each answer (optional light mode):** short “Got it / Needs work” — full report only at the end  
6. **Session length default:** 10 questions (~10–15 min typed; shorter when voice lands)  
7. **End state is always Results → Retest**, never a dead end

---

## 10. Results screen (the product’s “aha”)

```
Overall readiness: 74%

Strong
✓ Coulomb’s Law
✓ Electric Field

Needs work
⚠ Gauss’s Law
⚠ Electric Potential

Common mix-ups
• Mixes up electric field and electric flux
• Thinks Gauss’s Law only works with symmetry

Next (pick one)
1. Retest weak areas (5 questions)     ← primary button
2. Review Gauss’s Law (sources)
3. Practice electric flux
```

No raw model dumps. No multi-agent logs. Three actions max.

---

## 11. How it works (for the team — keep out of the app)

Five intelligent parts behind the scenes (not five products):

1. **Scope** — turn goal into requirements  
2. **Research** — find only missing knowledge; prefer user notes → curriculum → reputable sources → web  
3. **Curriculum** — topic map, blueprint, rubrics, reference answers  
4. **Examiner** — ask, follow up, adapt  
5. **Evaluator** — concepts, claims, misconceptions; **final % score calculated by backend rules**, not free-form LLM scoring  

**Provenance:** every question and score ties back to sources (for debugging and “See sources”).

**Safety:** never send reference answers/rubrics to the client; treat web content as untrusted; validate outputs against schemas.

---

## 12. MVP build order (aligned to simplicity)

| Phase | Ship | User feels |
|-------|------|------------|
| **1 – Core** | Upload + goal + topics + 10 typed questions + rubric scoring + weakness report + retest | “This actually judges if I understand” |
| **2 – Grounded** | Chunking, retrieval, citations on questions/feedback | “I can trust why it asked that” |
| **3 – Research** | Gap detection + focused web research + source ranking | “It filled what my notes missed” |
| **4 – Adaptive** | Mastery, follow-ups, misconception probes | “It listens and adjusts” |
| **5 – Voice** | TTS questions + STT answers + re-ask on unclear speech | “Real viva practice” |
| **6+** | Long-term progress, study plans, more languages, classrooms | Habit & scale |

**Decision:** Phase 1 is the quality gate. Do not block MVP on voice.

---

## 13. Success metrics

| Metric | Target (first 90 days post-MVP) |
|--------|----------------------------------|
| Users who finish a full first session | ≥ 60% of those who set a goal |
| Users who start a retest after results | ≥ 40% |
| “Practice felt fair” (in-app rating) | ≥ 4.0 / 5 |
| Session overwhelm / drop-off mid-upload-goal | < 25% |
| Human agreement with AI topic “needs work” labels (spot checks) | Track weekly; improve, don’t invent a fake bar yet |

---

## 14. Out of scope for v1

- Claiming “CBSE-approved” or official board scoring  
- Replacing teachers or proctoring high-stakes exams  
- Social / viral loops  
- Perfect fluency coaching (that’s Speak/ELSA territory — optional later, separate from subject score)

---

## 15. Open decisions

1. Final product name & brand  
2. Web-only vs mobile wrapper for v1  
3. Free tier limits (sessions / uploads)  
4. Whether light “Got it / Needs work” appears after every question or only at the end  
5. Primary GTM: India exam prep first vs global English first  

---

## 16. Summary for stakeholders

We’re building a **simple oral practice loop**: upload notes, set a goal, answer out loud (typed first), get a clear readiness report, retest weak spots.

We differentiate by combining **gap-filling research**, **fair understanding-based scoring**, and **adaptive follow-up** — without burying the user in AI features.

If the app ever needs a tooltip to explain a button, the flow isn’t simple enough yet.
