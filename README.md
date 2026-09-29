# The Unofficial Guide

<!--Name: Anshika Choudhary, Corpus: Campus life -->

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
```
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
| 1. Retrieved chunks contain the answer | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 2. Every answer names a source | 5 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 3. Gate stops out-of-corpus questions | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 4. Answer chunk has whole sentences, no mid-sentence cut | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 5. Numeric answers reproduce the number exactly | 5 of 5 | 4/4 | 4/4 | 4/4 | MET |

<!-- Underneath, paste the REAL output for each criterion from one of your
     runs — the actual text your system produced, not a description of it.
     Name the file and function that produced it. -->

### Criterion 1, 2, 4 and 5 — run 1
Question: What time does The Atrium's sandwich selection typically run out?
Best distance: 0.295 (passed the gate)
Produced by: run_eval.py::main → store.py::search → generate.py::answer_from_chunks

The Atrium's sandwiches are typically picked clean by 1:15
(dining_the_atrium.txt and dining_the_atrium_followup.txt).

### Criterion 3 — the gate, run once 
Produced by: run_eval.py::check_out_of_scope, cutoff 0.6

| What is the capital of Mongolia? | 0.825 | refused |
| How do I change the oil in a diesel engine? | 0.934 | refused |

### The scorer's false negative — run 1
Question: How does a work-study job affect financial aid...?
Best distance: 0.1918 (passed the gate)
Marked fail by scorer.py::judge

Work-study earnings do not count against your financial aid the way ordinary
income does, whereas non-work-study campus jobs do count.

Source: admin_campus_jobs_and_financial_aid.txt


## Verdicts

<!-- MET or MISSED for each of the five, against the target you wrote last
     unit — not a new one. Plus a sentence on how you decided. That sentence
     matters most where it was close.

     If your target said 4 of 5 and your runs came out 4, 3, 4, that's a MISS.
     The target has to hold, not show up occasionally.

     Milestone 2. -->

| # | Criterion | Verdict | How I decided |
|---|---|---|---|
| 1 | Retrieved chunks contain the answer (4 of 5) | MET | 5/5 on all three runs. I judged this on the retrieved sources, not on `scorer.py` — the scorer marked work-study fail, but the document holding the answer came back first at distance 0.1918 every run. The criterion is about retrieval, and retrieval worked. |
| 2 | Every answer names a source (5 of 5) | MET | I read all 15 answers in the run log and every one names a `.txt` file, either inline or on a `Source:` line. No run produced a bare answer. |
| 3 | Gate stops out-of-corpus questions (4 of 5) | MET | 5/5 refused. Nearest out-of-scope question was 0.825 against a 0.6 cutoff, so nothing was close to slipping through. One deterministic pass, same number in all three runs. |
| 4 | Answer chunk has whole sentences, no mid-sentence cut (4 of 5) | MET | 5/5, but met by construction rather than by luck — `chunker.py::split_documents` cuts only at blank lines between paragraphs, so a mid-sentence split is structurally impossible. This criterion could not have failed given the chunker I built. |
| 5 | Numeric answers reproduce the number exactly (5 of 5) | MET | All numeric values matched the source: `20 to 25 minutes`, `1:15`, `week two`, `second week of March`. No rounding, no ranging. Only four of my five questions have a numeric answer, so the denominator is 4 rather than 5. |

- I revised criteria 5 from expecting all 5 answers to have exact same numbers as the source documents to expecting every numeric value in an answer to match the source document exactly.

## Diagnoses

**No criterion was missed.** All five criteria were MET across three runs. Even though two things went wrong but neither of them happened in the pipeline.

**The pattern: both problems were in the measurement, not the system.** Across
all five questions and all three runs, every stage did its job — loading,
chunking, embedding, retrieval and generation. Retrieval put the correct
document first every time, with best distances between 0.19 and 0.39 against a
0.6 cutoff. Generation stayed inside the sources and cited a file in all 15
answers. What broke was how I was counting.

1. `scorer.py::judge` marked a correct answer wrong, three runs out of
three. Question 4 asks how work-study affects financial aid. The system
answered:

Work-study earnings do not count against your financial aid the way ordinary
income does, whereas non-work-study campus jobs do count.

Source: admin_campus_jobs_and_financial_aid.txt

That is correct, grounded and cited. It was marked fail because `judge` does a
substring test and my `expects` was `"doesn't count"` while the source document and the answer says "don't count". 

The opposite thing happened with question 3. My original `expects` for question 3 was `"W"`. Both sides get lowercased, so that tested whether the letter `w` appeared anywhere in the answer, which it always does. That question would have passed unconditionally, including on a wrong answer. One mechanism, two opposite failure modes, and the false pass is the one I would never have noticed.

I judged criterion 1 by reading the retrieved sources rather than by trusting
the scorer's column, which is why it reports 5/5.

2. Criterion 5 had an unreachable denominator. I wrote it as "all 5 test
questions where the answer includes a specific number," but only four of my
five answers contain a number. The criterion counted questions when what I was
actually checking was values. Revised in `criteria.md`, with the original left
in place.

---

### Were my targets set low?

Partly, yes. Clearing all five on the first attempt says more about the test
than about the system.

Three things made it easy. All five of my questions are single-document
lookups with the answer sitting in one sentence and none is about a topic only a document or two mentions. My five out-of-scope questions are from a different world entirely (Mongolia, diesel engines, Rust), so the gate was separating 0.19–0.39 from 0.82–0.93, a gap of 0.53 with nothing in it. And `campus_life` is a clean, purpose-written corpus with no contradictions or duplicates to trip over.

**The criterion I would tighten is 4.** As written it cannot fail.
`chunker.py::split_documents` cuts only at blank lines between paragraphs, so a
mid-sentence split is structurally impossible — I was measuring a property of
my chunker's design rather than an outcome of a run. A criterion that cannot
fail measures nothing.

I would replace it with: **for at least 4 of 5 questions, the chunk containing
the answer covers no more than one topic.** That is checkable by reading, and
it would currently fail on `housing_old_brewhouse.txt#1`, where heating,
laundry prices and noise still share a chunk because my 150-character floor
merged them. That is a real weakness in my chunking that criterion 4 as
written was never going to catch.

Secondary: criterion 3's target of 4 of 5 is safe when the out-of-scope
questions are that far away. A harder version would swap them for
campus-shaped questions my corpus doesn't answer like "what are the wait times at
the campus health centre?", here the gate would be under actual pressure.

## The Improvement

**What I changed:** I changed the `MIN_CHUNK` in `config.py`, from 150 to 100.
Nothing else was touched: same corpus, same top-k of 5, same 0.6
cutoff, same `expects` phrases, same `scorer.py`.

Effect on the index: 96 chunks -> 103, average length 293 -> 276, shortest 178 -> 143. Eight documents are chunked differently.

Also, 0.2953 was the worst-case in my unit 1 cutoff table and it now measures 0.3860. The gap narrows from 0.53 to 0.44, which means my threshold of 0.6 is still unreached.

**Why I picked it:** My diagnosis said criterion 4 could not fail, because my
chunker only cuts at blank lines. The real weakness it was failing to catch
was `housing_old_brewhouse.txt`, where the 150 floor merged the heating
paragraph (110 characters) with the laundry and noise paragraph, leaving three
unrelated topics sharing one chunk. Lowering the floor to 100 separates them.

### Run Log — After

<!-- Same format, same five criteria, three runs each.
     `python run_eval.py --label after` -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 2. Every answer names a source | 5 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 3. Gate stops out-of-corpus questions | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 4. Answer chunk has whole sentences, no mid-sentence cut | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 5. Numeric values in an answer match the source exactly | all | 4/4 | 4/4 | 4/4 | MET |

Identical to the before table, row for row.

**Did it help?**

I can't tell from this test even though 8 documents are chunked differently now and my reference file `housing_old_brewhouse.txt` now splits into three chunks with laundry prices standing on their own. But every distance in the after run is identical to the before run to four decimal places, including the out-of-scope ones:

| Question | Before | After |
|---|---|---|
| Work-study vs non-work-study | 0.1918 | 0.1918 |
| Kestrel Commons wait times | 0.2345 | 0.2345 |
| Add/drop after week two | 0.2607 | 0.2607 |
| The Atrium sandwiches | 0.2953 | 0.2953 |
| Housing lottery number | 0.3860 | 0.3860 |

That is not a bug and not a null result. The eight re-chunked documents are:

course_cs_210.txt          housing_innisfree_hall.txt
course_stat_150.txt        housing_morrow_house.txt
housing_calder_annexe.txt  housing_old_brewhouse.txt
housing_fenwick_court.txt  housing_tamsin_court.txt

None of them is the top match for any of my ten questions. All nine documents
my questions actually retrieve are short posts that stay whole under either
floor, so their embeddings are unchanged and their distances cannot move.

**My test set cannot detect improvement.** All five of my questions are
single-document lookups against short posts, so none of them used the files that changed after chunking. To measure this properly I would have needed a question
about one of the long multi-topic housing posts like "how much is laundry at Old
Brewhouse?", as this question shares a chunk with heating and noise at a floor of 150 and stands alone at 100.

I have deliberately not added that question. Changing the test between the
before and after runs would make the comparison meaningless.

## What's Still Broken
All the targets/criterion are satisfied but the following things need to be fixed:
1. scorer.py needs to updated in a way that it compares the meaning of provided answer with the expected answer instead of just comparing the substrings in the provided answer. It marked a correct work-study answer fail on all six runs, before and after, because the document says "don't count" and my `expects` says "doesn't count". The same mechanism produces false passes: my original `expects` of `"W"` matched the letter w in any answer, so that question would have passed even on a wrong answer. I caught that one by reading, but I would not catch the next one.

2. Lowering `MIN_CHUNK` to 100 separated laundry prices from heating in `housing_old_brewhouse.txt`, but the document still doesn't come apart cleanly. Chunk #2 holds laundry prices and the noise paragraph together; chunk #1 holds "the good" and the heating complaint. Two topics per chunk instead of three is an improvement, but not a fix.

## What I'd Do Differently
Even though I already changed my chunker for criterion 4 but it didn't change much in the chunking process so  I'd have written it about what my chunker can actually get wrong i.e., whether a chunk holds more than one topic. All five of my questions ask about short single-topic posts, so none of them touches the long multi-topic documents my chunker was built to handle. I changed the chunking and every distance stayed identical to four decimal places. Next time I'd write at least one question per document shape in the corpus, so the test can see the component I spend the most time on.

Also, I'd change the 'scorer.py' to accept a list of acceptable phrases rather than a single string, and reject any `expects` shorter than three characters so a single letter can't match everything.

## Why I stopped
I stopped because Milestone 4 strictly said only one change should be done. I had already changed the chunking once, and changing it again along with fixing the scorer would have left me unable to say which change did what. It is the first thing I would do next.

I'm also short on time because I'm between a lot of things nowadays.

## How I Used AI
Whenever I was trying to run the run_eval file the gemini service was busy so I asked claude to make changes to the generate.py file because it only handles 429 (resource exhausted/ rate limit) as retryable and 503 was not accounted for thats why when gemini was busy my whole program was crashing instead of automatically trying again. The change made it treat 503 as the same way as 429.

Secondly, When I made changes in the chunking mechanism I was unable to spot the difference on my own initially as all the numbers in the result file were still the same. I asked claude and it pointed out the 8 files that were different from the previously chunked files. It mentioned the name of the files and also helped with understand the justification of why all the numbers were still same in the result file.

## Stretch: A second measured improvement
I am making a second change and logging it the same way: fixing
`scorer.py::judge` so it no longer relies on a single bare substring match.

