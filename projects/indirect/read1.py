"""The blind readings of session 1, as written before the key was opened (writes readings.json)."""
import json,collections
S="same";H="shifted";D="different";X="cannot read"
r={}
def put(n,cat,note="",conf="high"):
    assert n not in r, n
    r[n]=(cat,conf,note)
for n in [1,2,3,4,7,8,10,12,13,14,15,17,19,21,24,28,29,31,32,33,34,35,36,37,38,40,41,42,43,44,45,46,49,51,52,54,57,58,59,60,62,64,65,67,68,69,70,71,72,73,75,76,79,81,82,85,87,88,89,92,93,95,97,98,100,
          101,104,109,110,111,112,113,114,115,117,119,120,124,126,128,129,130,133,134,135,136,138,140,141,142,143,146,148,150,152,154,155,157,158,159,164,165,166,167,168,169,170,171,173,174,175,176,177,179,180,182,184,185,186,188,189,191,192,193,194,195,196,197,199]:
    put(n,S)
for n,note in [(6,"gender supplied by Hebrew"),(11,"formality dropped: Esperanto has none"),(22,"subject 'he' supplied by German"),(25,"'she' supplied by German"),
  (39,"'she' supplied by Russian"),(55,"gender dropped by Japanese"),(63,"formality supplied by German"),(77,"formality supplied by Italian"),(83,"masculine 'you' supplied by Kabyle"),
  (86,"Italian reads as formal 'you'"),(94,"'she' supplied by Japanese"),(105,"feminine object supplied by Russian"),(108,"feminine 'you' supplied by Hebrew"),
  (160,"feminine speaker supplied by Russian"),(163,"masculine speaker supplied by Ukrainian"),(181,"plural/formal supplied by Russian")]:
    put(n,S,note)
for n,note in [(26,""),(78,"Old Prussian, reconstructed: read by cognates"),(80,"Coastal Kadazan: read by cognates with Malay"),(90,"Marathi"),(91,"'not drunk, not drunk' becomes 'no, no'"),(96,""),(99,"archaic Hebrew phrasing"),(103,"Guarani"),(106,"Berber"),
  (131,"Italian 'Le' read as formal 'you'"),(137,"Kabyle"),(139,"Toki Pona's idiom for translator"),(144,"Klingon"),(145,"Kabyle"),(147,"'pretty' read as 'very'"),(149,"Italian 'chi e' read as formal 'you'"),(153,"jacket becomes coat"),(156,"Berber word for hot dog unsure"),(161,"Tatar"),(178,"Marathi"),(190,"Berber")]:
    put(n,S,note,"low")
for n,note,conf in [(5,"you (women, plural) becomes formal 'you' or 'she'","low"),(9,"'I never blamed you' becomes 'I never blamed her'","high"),
  (16,"informal 'you' becomes formal/plural; 'this work' becomes 'the work'","high"),(18,"'considerable return' becomes 'satisfactory return'; the Bulgarian is awkward","high"),
  (20,"'very' lost","low"),(23,"formal/plural 'you' becomes informal singular","high"),(27,"'is at the bottom of the pit' becomes 'went into the hole'","low"),
  (30,"'happen' becomes 'arrive'","low"),(47,"'we were too many' becomes 'we were one too many'","high"),(48,"'several students' becomes 'many students'","high"),
  (50,"'are trying to get extradited' becomes 'request extradition'","high"),(56,"'was looking' becomes 'looked'","high"),(61,"'forged the weapons of' becomes 'made weapons for'","high"),
  (66,"'tormented their minds' vs 'were breaking their heads': idiom or literal, unsure","low"),(84,"formal/plural 'you' becomes informal","high"),
  (102,"'boy' becomes 'child'","high"),(107,"informal 'you' becomes formal/plural","high"),(116,"'s/he does not know' becomes 'they do not know'","low"),(118,"'him' becomes 'him or her'","high"),
  (121,"'want' becomes 'need'","low"),(122,"'I'll do it' becomes 'I'll go'","high"),(123,"'Fachidiot' (narrow specialist) becomes 'learned fool'","high"),
  (125,"'guarantee of good fortune' becomes 'sultan of our happiness'","high"),(127,"'help you' becomes 'help her'","high"),(132,"'entitles' becomes 'provided' (past)","high"),
  (151,"singular 'you' becomes plural","high"),(162,"'foreign languages' becomes 'languages'","high"),(183,"'she was not making the beds' becomes 'he did not make the bed'","high"),
  (187,"'got irritated' becomes 'was frustrated'","high"),(200,"'straight up' becomes 'in one gulp'","high")]:
    put(n,H,note,conf)
put(198,D,"'She leads' becomes 'You drive'")
for n,note in [(53,"Tigre: cannot read"),(74,"Nande: cannot read"),(172,"Berber 'aɣwali': cannot read")]:
    put(n,X,note)
assert sorted(r)==list(range(1,201)), set(range(1,201))-set(r)
out={"rule":"Read blind (SELECTION.md): A and C only, kind withheld. Interpretation fixed before the key was opened: a distinction the far language's grammar must supply or cannot carry (gender, formality, a subject) counts as same; shifted when one distinction or detail is changed, or lost or added where the far language could have kept it. Every reading is a machine judgment: an estimate. 'low' = the reader is unsure of one language.",
 "estimate":True,"readings":[{"n":n,"reading":r[n][0],"confidence":r[n][1],"note":r[n][2]} for n in range(1,201)]}
json.dump(out,open("readings.json","w"),ensure_ascii=False,indent=1)
print(collections.Counter(v[0] for v in r.values()))
