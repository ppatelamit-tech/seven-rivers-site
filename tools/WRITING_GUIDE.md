# Seven Rivers Psychiatry — Writing guide for the blog

This file is the brief for anyone (human or scheduled task) drafting an essay for the Writing section. The two published essays in `posts/` are the reference voice; read both before drafting.

## Who it is for

Patients and curious readers, not colleagues. Someone deciding whether to get care, or in care and trying to understand it. Assume intelligence; do not assume vocabulary.

## Voice

- Declarative and calm. Short sentences doing real work, then one long sentence that earns its length.
- First person, singular, sparingly ("I hear", "I want to defend"). The practice is "this practice" or "here", never "we".
- Lead with the thing patients actually say or experience, then the mechanism behind it, then what this practice does differently and why.
- One reframing line per essay, set as a blockquote, in the middle, not at the end. It should be quotable on its own.
- Defend the conventional view fairly before departing from it. The posts argue by steelman, not by strawman.
- Concrete over abstract: thirty-minute visits, two weeks at a starting dose, the drive home. No "holistic", "journey", "wellness", "empower", "unpack", "navigate" (except the river sense), "space" as a verb.
- No bullet points, no headings inside the essay, no numbered lists, no em dashes. Paragraphs only, five to eight of them, 650 to 950 words.
- The river vocabulary is the house metaphor and the only one: currents, confluence, crossing, headwaters, the far bank. Use it lightly, once or twice, never forced.
- Close on movement, not on reassurance. The last paragraph should land on what becomes possible, in one or two sentences, and stop.
- Title: sentence case, no colon, five to eight words. Mark the word or phrase for the display emphasis with *asterisks* in the front matter.

## Standing frameworks (the practice's own ideas; draw on them, do not invent new ones)

- Two currents: Healing (regulation, support, safety first) and Ascent (calibrated challenge, trainable emotional performance). Mental health is free movement between them.
- Symptoms as animals to manage: not a tiger to cast out, a dog to train.
- The evaluation is two 60-minute sessions on separate days; the gap is method, not scheduling.
- Diagnosis as hypothesis to be attacked, not a label to be copied forward. Anchoring is the oldest error in medicine.
- Deprescribing and "I tried that and it didn't work" usually meaning two weeks at a starting dose.

## Hard rules (clinical and legal)

- Nothing that reads as individual medical advice. No dosing numbers, no "if you have X, take Y", no comparisons that recommend one drug over another for the reader.
- Do not name specific medications except as general illustration of a class, and only when the essay needs it. Never state a medication fact (half-life, interaction, side-effect rate) unless it is textbook-stable; when in doubt, cut it.
- No diagnostic criteria recited, no claims about what "most psychiatrists" do beyond what is common knowledge (visit length, billing pressure).
- Suicide, self-harm, and crisis: do not write about methods, and any essay touching these ends by pointing to 988 in one plain sentence.
- No patient stories, even composite or anonymized. Patterns only ("the most common complaint I hear").
- No promises about outcomes. "Changes what patients expect" is fine; "will cure" is not.
- Controlled substances: do not write about the practice's prescribing policy for them in a blog post. That lives on the services page.
- Every draft is reviewed and approved by Dr. Patel before it is published. Drafts go in `drafts/`, never directly in `posts/`.

## Categories (use one, exactly as written)

- On practice
- On the two currents
- On diagnosis
- On medication
- On the mind

## Topic queue (take the top one not yet drafted or published; add new ideas at the bottom)

1. The dog, not the tiger: what it means to manage a symptom instead of eliminating it (On the mind)
2. Why your diagnosis should be a hypothesis (On diagnosis)
3. "I tried that and it didn't work": what a real medication trial looks like (On medication)
4. Sleep is the first question, not the last (On diagnosis)
5. What a good psychiatric note should let you argue with (On practice)
6. When to stop a medication, and why that decision gets the least attention (On medication)
7. Support and challenge are not opposites: how to tell which one you need this month (On the two currents)
8. The difference between a bad week and a disorder (On diagnosis)
9. Why "chemical imbalance" was a useful lie and what replaces it (On medication)
10. What telehealth makes easier, and the one thing it makes harder (On practice)

## How a post gets published

1. Draft: write `drafts/<slug>.md` in the format shown at the top of `tools/build_blog.py`.
2. Review: Dr. Patel reads it, edits or approves.
3. Publish: move the file to `posts/`, run `python3 tools/build_blog.py`, commit `posts/`, `blog/`, and the removed draft, push to `main`. Netlify deploys on push.
