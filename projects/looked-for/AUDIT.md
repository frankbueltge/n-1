# Project 17 — T7 smooth/striated audit

*KsK T7: the Boulez question (ATP 477, "in a smooth space-time one occupies without counting, whereas in a striated space-time one counts
in order to occupy"), the direction of the mixture (ATP 475), the translation balanced both ways (ATP 486-487). Failure: a demand for
"more smooth", or a balance that comes out one-sided. Entries are dated and written in session.*

## Entry 1 — session 1, 2026-10-23 23:30 UTC (after the registered count)

**The spaces.** (1) The index: every record a point, a name at a place at a date; maps and ranges are made by counting points. It counts
in order to occupy. (2) The survey that writes an absence: a 15 m circle for five minutes, 120 m³ of water, a trap for a night, a forest
plot, a seabed video line. An absence can only be said of a space that was fixed and searched, so it is the product of the most counted
practices the index holds: the ten largest sources of absence (72.3 % of 136,979,181) are monitoring programmes, a national forest
inventory, a disease-vector surveillance network, and, first of all, the seabed surveys the Norwegian petroleum industry is required to
make (34,459,302 absences, a quarter of all, `session1.json`). The dataset's own description (GBIF registry, dataset
`b6b4502f-ffc8-4048-a91b-af502288faa8`, read 23:30 UTC): "hovedsakelig data som er samlet inn i forbindelse med lovpålagte visuelle
miljøundersøkelser" ("mainly data collected in connection with legally required visual environmental surveys"), whose purpose is to map
species on the Norwegian red list and habitats on OSPAR's list of threatened or declining habitats. (3) The presence records that make up most of the index, much of it
observation that occupies a place without having counted the space around it.

**Direction of the mixture.** Not the expected one. The absence does not come from a smooth outside into the grid: it comes from a
stricter striation (the protocol's measured space) and is translated **down** into the index's coarser one, where the searched volume
becomes one point with a status beside it. Meanwhile the index's own default runs the other way: a record that says nothing of status is
made PRESENT. Four of the forty drawn records said nothing but a name, and the index calls all four present, without a flag; only 128,149
records in four billion carry the flag that a status was inferred from the kind of record.

**Translation, both ways.** *Overcoding:* the searched space is lost in the point; "not found here" becomes "not at this point"; analysts
filter absences out as contamination (`NEIGHBOURS.md`); silence is written as presence. *Propagation:* without the index these
137 million statements would stay in agency reports and survey archives; the index made a field for them, keeps the publisher's word
(36 of 36 readable records agree with their status, `result1.json`), and puts an oil company's seabed video and a citizen beach count in
one table where they can be read together. Two-sided; not triggered.

**What the audit changed.** Session 2's question moves to the space each absence was searched in, beginning with the largest source: what
"absent" is in a petroleum seabed survey (how many names are checked per frame or line, and which), against what it is in a forest plot.
Without the audit (estimate) the next session would have read the kingdoms and years further, which the count already shows.

## Entry 2 — session 2, 2026-10-24 01:11 UTC (after the registered count)

**The Boulez question, asked of one unit.** Entry 1 said the absence comes from a stricter striation translated down into the index. The
count says what that striation is. A Swedish forest plot (about 100 m²) asks the same 242 names every time; a California dive asks 94 to
143, by method and region; a unit of the Norwegian seabed surveys asks **thirteen**, and in 20 of 20 drawn units all thirteen are
absent. Across that dataset each of the thirteen corals is written absent about 2.65 million times (`session2b.json`), and the thirteen
were found 10,978 times in all. The space searched is not what decides what is said absent: a **form** decides it, the list a law and two
red lists put on the survey. One counts in order to occupy, and here one counts before arriving: the absences exist as boxes before the
camera reaches the seabed.

**Direction of the mixture.** Not one direction. The form striates the seabed (the corals are asked everywhere, also where none could
live); what was actually seen arrives the other way, open: 95 names in the same dataset are recorded present and never
absent (42,367 records), written because someone saw them and nobody asked. So one dataset holds both regimes, a closed
list that can only say "not here", and an open one that can only say "here".

**Translation, both ways.** *Overcoding:* in the index the form's empty boxes weigh like observations: 34 million "not there", a quarter
of the world's absences, of which 46 % concern six names never once found in the dataset. A reader of the global count (session 1) takes
the length of a legal list for a fact about the seabed. *Propagation:* without the index the empty boxes would not be readable at all;
the index keeps each unit's thirteen answers, which is what lets a reader see that a red-listed reef coral (*Desmophyllum pertusum*) was
looked for some 2.65 million times and found 5,906. Two-sided; the failure criterion did not trigger.

**What the audit changed.** It changes what session 3 must show: not the count of absences (session 1) but the ratio of question to
answer, unit by unit. The first plan for session 3 was a map of absences by place (estimate); the audit strikes it, because a map would
draw the list's length as a landscape. Session 3 is to make the form itself receivable: thirteen boxes, millions of times, and the few
times one was filled.
