# Acceptance criteria — The Unofficial Guide

Five criteria that say what "working" means for this system, written in unit 1
**before** any results existed.

An acceptance criterion names a target: a number, a count, a rate, or something
a person could plainly observe. *"Retrieval works"* is an opinion. *"For at
least 4 of my 5 test questions, the top results include a chunk containing the
answer"* is a criterion.

Under each one, write a sentence or two on **why that target** and not a
stricter or looser one. A reason that says something about your corpus or your
pipeline earns credit; *"80% seemed reasonable"* does not.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## 1. Retrieved chunks contain the answer

For at least 4 of my 5 test questions, the retrieved chunks include one that
contains the answer.

**Why this target:**
<!-- e.g. "One of my questions is about a topic only two documents mention, so
     I expect that one to be hard." -->
Forcing a retrieval system to be perfect would make the test fail on noise rather than on real problems; 4/5 still means only one acceptable miss across a small,deliberately varied set of questions.
---

## 2. Every answer names a source

Every answer the system produces names at least one source document.

**Why this target:**
<!-- Why all five and not four? What about your setup makes that achievable —
     or what would have to go wrong for it not to be? -->
A system that cites sometimes and not other times isn't "mostly trustworthy" because you never know which answer you're getting. 
---

## 3. The relevance gate stops out-of-corpus questions

When I ask a question my documents clearly don't cover, the relevance gate
stops it and the system returns "I don't have enough information about that" —
in at least 4 of 5 tries.

<!-- The five questions are the ones in `OUT_OF_SCOPE` at the bottom of
     `questions.py`, and `run_eval.py` puts them through the gate and writes
     what happened into your run log. Swap them for your own if you'd rather —
     just keep five of them, or the "4 of 5" above has nothing to be 4 of. -->

**Why this target:**
<!-- What did your distances look like when you set the cutoff in Milestone 4?
     Was there a clean gap, or did the two groups overlap? -->
Same logic as #1. If I force the gate to be perfect about saying "I don't know," it'll start blocking the legitimate questions that can be answered therefore 4/5 tries is acceptable.
---

## 4. Chunk-size check
For at least 4 of the 5 test questions, the chunk with the answer has the whole sentence(s).
<!-- For at least 4 of the 5 test questions, the chunk that contains the answer contains the full supporting sentence(s) intact with no cut off mid-sentence at the start or end of the chunk. -->



**Why this target:**
A couple of these documents (housing lottery, Kestrel Commons follow-up) pack two related facts into adjacent sentences — I don't want to force a chunk size so large that unrelated documents get merged just to guarantee zero splits. One tolerated split is a signal to look at chunk size, not a hard failure.

---

## 5. Every question that has numeric answer produces exact number
For all 5 test questions where the answer includes a specific number (minutes, hours, a week number), the system's output reproduces that number exactly (no rounding, no ranging).
<!-- Why all five and not four? What is the reason for this strictness -->



**Why this target:**
These documents are full of close, similar-looking numbers (6 hrs vs 9-11 hrs, "week two" vs "week six", "20 to 25 minutes," "1:15" vs "1:30") that are easy to blend or round under paraphrase, and a wrong number reads as confidently as a right one.


---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 2 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath it, like this:

         ## 1. Retrieved chunks contain the answer

         For at least 4 of my 5 test questions, the retrieved chunks include
         one that contains the answer.

         **Why this target:** ...

         > **Revised in unit 2:** For at least 4 of 5 questions, the top three
         > results contain the answer.
         >
         > **Why revised:** I couldn't judge "the chunks include one that
         > contains the answer" the same way twice — I scored two questions
         > differently on Monday than on Wednesday. The new version is
         > something I can actually check.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "I said 4 of 5 but got 2 of 5, so 2 of 5 is more realistic."

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.

     The whole reason the originals stay visible is so someone can see what you
     said before you knew the answer.
     ───────────────────────────────────────────────────────────────────────── -->
