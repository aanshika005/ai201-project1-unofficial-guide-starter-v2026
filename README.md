# The Unofficial Guide

<!-- Replace this line with your name and which corpus you picked. -->

> **This file is your submission.** Fill it in as you go — most sections get
> written during the milestone that produces them, not at the end.
>
> How the starter works, and every command you'll need, is in `RUNNING.md`.
> Leave that file alone.
>
> **Paste everything as text.** No screenshots, no video. A typed table gets
> full credit; a picture of the same table gets none.
>
> Delete these instruction blocks as you replace them. The `<!-- -->` comments
> are notes to you and don't show up when the page renders — you can leave them
> or remove them.

---

# Unit 1

## What This Does

This is a retrieval-augmented question answering system over `campus_life`, a corpus of 88 short posts about student life at a university — dining halls, dorms, courses, and the administrative rules nobody explains properly. You ask it a question in plain English and it answers from those documents, naming the file it used.

It answers specific, factual questions the corpus actually covers: when housing lottery numbers come out, whether a late drop shows as a W, how long the lunch queue at Kestrel Commons runs. It is not a general chatbot — a relevance cutoff measured against the corpus stops questions the documents don't cover, and the system says it doesn't have enough information rather than guessing.

## Chunking Strategy

**Chunk size:** no fixed size — paragraph boundaries, with a 150-character floor
**Overlap:** 0

<!-- What about YOUR documents made you pick these numbers? Short posts and
     long sectioned guides don't want the same chunking, and "800 seemed
     reasonable" earns nothing. Point at something you noticed when you read
     the documents in Milestone 1.

     If you changed your mind partway through, say so and say why. That's worth
     more than pretending you got it right first time.

     Milestone 3. -->

     Since chunk size applies to all the 88 documents not just one file I chose 150 because if I would I gone lower like 100 the chunks across all 88 documents would have shrunk and lose their meaning but by keeping it 150 I only risk accumlating information in chunks but they still be meaningful.

For example:
     At current MIN_CHUNK = 150, Old Brewhouse becomes 2 chunks, and the second one is:

     The bad: the heating is uneven... Laundry costs $1.50 wash, $1.50 dry... On noise: sound carries strangely...

     Heating, laundry, and noise all in one chunk. So "how much is laundry at Old Brewhouse?" retrieves a chunk that is mostly about other things.

     Lower the floor to MIN_CHUNK = 100 and it becomes 3 chunks, with laundry and noise on their own:

     Laundry costs $1.50 wash, $1.50 dry, coin only, and the machines are old. On noise: sound carries strangely...

I've kept overlap at zero because I split on paragraph breaks rather than character counts. Overlap exists to repair sentences severed by a blind cut, and a blank line never falls mid-sentence, so there is nothing to repair.

## Sample Chunks

<!-- Five chunks, pasted as text. Label each one and name the file it came from
     AND the function that produced it — the grader checks your code against
     what you claim here.

     `python app.py chunks -n 5` prints all three for you. Copy them straight
     across.

     Milestone 3. -->

**Chunk 1** — source: `admin_add_drop_deadline.txt#0` — produced by: `chunker.py::split_documents`

On the add/drop deadline

You can add a course through the end of the second week. Dropping is a longer window — through the end of week six — but a drop after week two shows as a W on your transcript. Nothing anywhere on the registrar's site says this plainly, and students find out from each other.

**Chunk 2** — source: `course_biol_160_workload.txt#0` — produced by: `chunker.py::split_documents`

Workload for BIOL 160 Cell Biology

People keep asking so: 9 to 11 hours a week, the heaviest first-year course by reputation. That's real time, not optimistic time.

It's front-loaded — the first month is heavier than the rest, partly because you're learning the format.

**Chunk 3** — source: `course_math_220_exams.txt#0` — produced by: `chunker.py::split_documents`

MATH 220 Linear Algebra — assessment

Two midterms and a cumulative final. Curved to a b- median.

The problem sets are the course; the lectures make sense afterwards rather than during.

**Chunk 4** — source: `dining_the_ridgeway_cafe_followup.txt#0` — produced by: `chunker.py::split_documents`

Re: The Ridgeway Café

Adding to what people have said about The Ridgeway Café. The wait figure of 10 to 15 minutes at 12:30 matches what I've seen. If you're trying to eat between classes, go before 11:45 and it's a different building entirely.

Also worth saying: seating is tight; about 40 seats for a building of 900. Nobody tells you this at orientation.

**Chunk 5** — source: `housing_morrow_house.txt#0` — produced by: `chunker.py::split_documents`

Morrow House — what it's actually like

Just finished a year in this building. Built 1954, partially renovated 2008. Rooms are singles and doubles, hall bathrooms.

The good: cheapest housing tier by about $900 a year, and the singles are real singles.

## Sample Answer

<!-- One complete question and answer, pasted as text, with the source line
     visible. Milestone 4. -->
**top-k:** 5
**My relevance cutoff:** 0.6

I measured both groups with `measure_cutoff.py`, which runs the five questions
in `questions.py` and the five in `OUT_OF_SCOPE` through retrieval only.

| Group | Best | Worst |
|---|---|---|
| In-corpus (5 questions) | 0.1918 | 0.2953 |
| Out-of-scope (5 questions) | 0.8246 | 0.9340 |

The two groups are separated by a gap of 0.53 with nothing in it. Every
in-corpus question matched below 0.30; the nearest out-of-scope question was 0.8246 ("What is the capital of Mongolia?", which matched a HIST 118 chunk).

I kept 0.6. Any cutoff between about 0.35 and 0.80 would separate these ten questions identically, so the exact number is not doing much work — what the measurement shows is that the gap is wide, not that 0.6 is precisely tuned. 0.6 sits near the middle with room on both sides, which leaves headroom for a harder question than the five I wrote.

**What this doesn't prove.** All five out-of-scope questions are from a
different world entirely — engines, football, Rust. They were never going to land near my documents. The real test of the gate is a question that is campus-shaped but unanswered by my corpus, and I haven't measured those.

**Question:** is the housing lottery random?

**Answer:** Best distance 0.254, cutoff 0.6
The housing lottery is not entirely random; rising sophomores get a randomly drawn number, but juniors and seniors are ordered by accumulated credit hours first, with random tie-breaks.

Source: `admin_housing_lottery.txt`

Sources retrieved: admin_housing_lottery.txt, admin_parking_permits.txt,
advising_registration.txt, housing_innisfree_hall.txt, housing_morrow_house.txt
```



## How I Used AI

<!-- Two specific moments. For each: what you asked for, what came back, and
     what you changed about it.

     "I asked Claude to write the chunking function from my notes. It ignored
     the overlap, so I added that myself" is the level of detail we're after.
     "I used AI to help me code" is not.

     Milestone 5. -->

**1.** In Milestone 4, Claude gave me measure_cutoff.py to use instead of doing each question manually which I didn't ask for but I used it and also did the retrieval manually to see the difference. I looked at the code of measure_cutoff and I learnt the process to automate retrieval.

**2.**I was having a hard time understanding why overlap should be 0. I asked Claude and the first explanation didn't land, so I asked again and got a worked example of a sentence being cut mid-price by a fixed-size chunker. That made it clear overlap is a repair for blind cutting, which my paragraph-based chunker doesn't do. I wrote the README justification in my own words from that.

<!-- ── Stretch features ─────────────────────────────────────────────────────
     Doing one? Say so here BEFORE you start. A feature this README never
     claims earns nothing.
     ───────────────────────────────────────────────────────────────────────── -->

---

# Unit 2

<!-- These sections get ADDED to what's already above. Don't delete or rewrite
     unit 1 — the point is that someone can see what you said before you knew
     how it went. -->

## Run Log — Before

<!-- Your five criteria, three runs each. `python run_eval.py --label before`
     runs the questions, puts the OUT_OF_SCOPE ones through the gate, and
     writes it all into results/ for you. Targets come from criteria.md; the
     verdict column is your call.

     Criterion 3 is measured in one deterministic pass rather than three, so
     the same number goes in all three run columns. That's correct, not lazy.

     Milestone 1. -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 |  |  |  |  |
| 2. Every answer names a source | 5 of 5 |  |  |  |  |
| 3. Gate stops out-of-corpus questions | 4 of 5 |  |  |  |  |
| 4. | | | | | |
| 5. | | | | | |

<!-- Underneath, paste the REAL output for each criterion from one of your
     runs — the actual text your system produced, not a description of it.
     Name the file and function that produced it. -->

## Verdicts

<!-- MET or MISSED for each of the five, against the target you wrote last
     unit — not a new one. Plus a sentence on how you decided. That sentence
     matters most where it was close.

     If your target said 4 of 5 and your runs came out 4, 3, 4, that's a MISS.
     The target has to hold, not show up occasionally.

     Milestone 2. -->

| # | Criterion | Verdict | How I decided |
|---|---|---|---|
| 1 |  |  |  |
| 2 |  |  |  |
| 3 |  |  |  |
| 4 |  |  |  |
| 5 |  |  |  |

## Diagnoses

<!-- For each miss: which stage caused it, and how. The stage alone isn't
     enough — you need the mechanism.

     Not a diagnosis: "Question 3 didn't work."
     A diagnosis:     "Question 3 asks about laundry costs. The answer is in
                       one sentence that got split across two chunks, so
                       neither chunk on its own contains it."

     The five stages: loading → chunking → embedding → retrieval → generation.

     Look for a pattern. If three misses all ask about numbers, that's one
     problem, not three.

     Missed nothing? Say so, then say honestly whether your targets were set
     low, and which one you'd tighten and to what.

     Milestone 3. -->

## The Improvement

**What I changed:**

**Why I picked it:**

<!-- Connect it to a specific diagnosis above in one sentence. If you can't,
     you picked a fix because it sounded impressive. -->

### Run Log — After

<!-- Same format, same five criteria, three runs each.
     `python run_eval.py --label after` -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 |  |  |  |  |
| 2. Every answer names a source | 5 of 5 |  |  |  |  |
| 3. Gate stops out-of-corpus questions | 4 of 5 |  |  |  |  |
| 4. | | | | | |
| 5. | | | | | |

**Did it help?**

<!-- Say plainly whether it did, and how you know. If it made things worse,
     say that — a change that backfired, honestly reported, earns full credit
     and is more interesting than one that worked. What matters is that you can
     tell.

     Milestone 4. -->

## What's Still Broken

<!-- For each criterion still missed after your fix: what you'd do about it,
     and why you stopped where you did.

     "I ran out of time" is fine if it's true. Pretending nothing is left is
     not.

     Milestone 5. -->

## What I'd Do Differently

<!-- Knowing what you know now — which of your five criteria would you write
     differently, and why?

     Milestone 5. -->
