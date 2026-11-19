# Project 25 — T2 assemblage analysis

*KsK T2: four fields, bodies, statements, territorialisations, cutting edges (ATP 88, 503-505); "neither base nor superstructure"
(ATP 90). Failure: field 4 stays empty or without consequence, or the fields are filled without a movement between them.*

## Session 1 — 2026-11-18

- **Field 1, bodies.** The product (a jar, a vial, a pump, a lot of 465 homeopathic bottles); the people who hold it, eat it, take it,
  are treated with it; the firm; its consignees (distributors, pharmacies, hospitals); the FDA's recall staff; the weekly report's pages.
- **Field 2, statements.** Three acts, each an incorporeal transformation datable to the day (ATP 80-81, via KsK §4.2): the firm's first
  notice (a product in commerce becomes a product being called back — `recall_initiation_date`), the FDA's classification (a recalled
  product becomes a Class I, II or III hazard — `center_classification_date`), the enforcement report (a classified recall becomes a
  public entry — `report_date`). Nothing in the bodies changes at any of the three; what the product is, in law and in the register, does.
- **Field 3, territorialisations.** The voluntary recall (the field definition: recalls "are almost always voluntary"), the three classes,
  the weekly cadence of the report. The cadence shows in the numbers: classification to listing is 7 or 8 days, median, in every centre
  and class (`explore1.json`).
- **Field 4, cutting edges.** Where the assemblage leaves its territory: the press release, a statement the firm makes to the public
  outside the register (event 80601's first notice). And, in the other direction, the classification itself for drugs: the gravest drug
  recalls take longest to be named grave (median 53 days to classification against 21 for Class II), every year since 2012.

**Movement between fields.** A statement in field 2 (the classification as Class I) is the slowest act exactly where field 1 is most
exposed (drugs taken by people). The weekly report (field 3) adds nothing to the difference; the difference is produced before it.

**Did it touch a decision?** Yes. Field 4's press release changed what the page may claim (the register's wait, not the public's) and
wrote session 2's question: for how many recalls, by class, is the register the first public notice — `initial_firm_notification` other
than a press release — and how long do those wait? Not triggered.

## Session 2 — 2026-11-19

- **Field 2, statements, split.** The firm's first notice is two different statements depending on its addressee: a letter to consignees
  transforms a product in a pharmacy into a product to be pulled from the shelf; a press release transforms it, for everyone who holds one,
  into a danger. The register records which (`initial_firm_notification`) — and in 4,571 events records a form's own list of every method
  instead, a statement that says nothing about its own addressee.
- **Field 3, territorialisations.** The form's sentence ("Two or more of the following: …") is a territory in the strict sense: the
  entry form's options, carried into the record as text. In food it stands where the answer should be in 3,164 of 7,955 classed events.
- **Field 4, cutting edges.** The press release is not where the register speeds up: drug Class I recalls begun with one are listed later
  (61.5 days) than those told to customers only (50). The cutting edge runs the other way — outside the register, the FDA's device Early
  Alerts (from November 2024) publish likely Class I recalls in weeks, a second public word the register does not hold.

**Movement between fields.** The gravest drug recalls are the most often announced (field 2) and the slowest to be classed (session 1);
the register's weekly rhythm (field 3) is the same for both. So the register's lag is not a choice about who has been told.

**Did it touch a decision?** Yes. The ambiguity of the form's sentence decided that no count may call the register "the first public
word" — only "may be"; and field 4's second public word (Early Alerts) names session 3's choice: whether the work holds the register's
waits as they are, or sets them against the words the public did get. Not triggered.
