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
