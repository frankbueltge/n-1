# Project 14 — T3, the pragmatics audit turned on the material

*KsK T3: "what passes and does not pass in such a transformation, what remains irreducible and what flows" (ATP 147, via KsK T3).
Failure: the translation test changes only the wording, not the project design.*

## Session 1 — 2026-10-20

**On the material.** Every Tatoeba link is one person's translation test, and the 29 losses read tonight say what did not pass
(`bridges.json`, estimates). What does not pass splits in two: a word's sense or an idiom (12 of 29), and, as often, the grammar of
address and measure: **who is spoken to** (formal or close, one or several: 9), **how many or how much** (several/many, too many/one
too many, fair/considerable, one or several "they": 4), **gender** (3), **aspect** (1). One category per loss, assigned in `bridges.py`. Where the proposition flows, the order-word's address
(ATP 76-79, via KsK 4.2) is what the chain drops. Read with the bridge, half of the losses (15) are **in no single link**: each step can
be read as faithful, and the middle sentence holds a form with two readings ("you", "vous", "Lei", "they", "arrivé", "a number of"). The
irreducible remainder is not in a language but between two.

**What it changed (the decision).** Before the bridges were read, the project's question was "how often" (SELECTION.md). After, the
count stands, and the problem moves to **the hinge**: the forms in a bridge language that let two faithful translations disagree. That
is a design change for session 2, not a wording change: its registration will count hinge forms across the graph (which bridge
sentences sit in the middle of disagreeing chains), not re-read the rate. Counterfactual (estimate): without the bridge reading, session 2
would have drawn a larger sample to narrow the 95 % interval around 19.7 %.

**On the project's own sentence.** "About one translation of a translation in five no longer says quite the same thing" was run through
the test: carried into a reader's language it becomes "one in five translations is wrong", which the page must not say. The page now
says beside each table that no translation is marked as an error, and the "other losses" are introduced as choices. That part changed
wording only, and is recorded as such.

**Failure criterion:** not triggered (the bridge reading moved the next session's question). The wording half of the audit, alone,
would have triggered it.

## Session 2 — 2026-10-21

**On the material.** Session 1 found the order-word's address (ATP 76-79, via KsK 4.2) to be what a chain most often drops. Tonight
counted it for one pair of languages across the whole collection (`session2.json`): French and Russian translations linked directly
disagree on who is addressed in 0.2 % of 107,712 pairs; joined through an English sentence with "you", in 68.6 % of 115,640 chains.
What passes through English "you" is the proposition; what does not pass is the address, and it does not pass in either direction:
through "you", the far translator's tu or vous is about as likely to match as a coin (52.9 % agreement over all paths, linked or not,
`explore2.json`, exploratory). What remains irreducible is not in a language, as session 1 said, and also not only between two: it is in
**the act of linking**. People join the pairs that fit; the indirect pairs are the remainder of that joining, and so they are mostly the
pairs that cross (59.3 % of agreeing paths linked, 0.14 % of disagreeing).

**What it changed (the decision).** Session 1's count read "one translation of a translation in five" as a property of chains. Tonight
shows that for this hinge the rate is made by the linking: the indirect set is selected against agreement. That moves the project's
question again, for session 3: not "how often does a chain lose" but **what the collection's own linking leaves unjoined**. It also
corrects session 1's page sentence, which presented 19.7 % as what happens to a sentence carried twice; the page now says, beside the
new chart, that the English chains disagree more than chance "not by the English sentence's doing". Counterfactual (estimate): without
the independence baseline registered in P9, the 68.6 % would have been read as "English loses the address", which is half true.

**On the session's own sentence.** "The pairs nobody joined are mostly the ones that cross" was run through the test: carried into a
contributor's reading it could become "Tatoeba links only what agrees", which is not shown (59.3 % of agreeing paths are linked, not all;
and the reason for each link is unknown). The page says "have since been linked directly by someone" and gives both shares.

**Failure criterion:** not triggered: the baseline and the linking count changed session 3's question, not only a wording.
