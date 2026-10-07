import json
cells = open("cells.json").read(); h = json.load(open("headline.json"))
n = h["n"]; p10 = 100 * h["d10"] / n; p35 = 100 * h["d35"] / n
s2 = json.load(open("session2.json"))
bars = "".join(f'<div><span>{k.replace("-1000000","+")} stations (n={v["n"]:,})</span><i style="width:{v["decided_share"]*60:.1f}%"></i>{100*v["decided_share"]:.0f} %</div>' for k, v in s2["by_nst"].items())
bars += f'<div><span>not given (n={s2["nst_missing"]["n"]:,})</span><i style="width:{s2["nst_missing"]["decided_share"]*60:.1f}%"></i>{100*s2["nst_missing"]["decided_share"]:.0f} %</div>'
page = open("template.html").read()
page = page.replace("%%BARS%%", bars).replace("%%NSTTOP%%", f'{100*s2["by_nst"]["81-1000000"]["decided_share"]:.0f}').replace("%%NSTMISS%%", f'{100*s2["nst_missing"]["n"]/s2["n"]:.0f} %').replace("%%REV%%", "100")
for k, v in {"%%CELLS%%": cells, "%%N%%": f"{n:,}", "%%P10%%": f"{p10:.1f}", "%%P35%%": f"{p35:.1f}",
             "%%D10%%": f"{h['d10']:,}", "%%D35%%": f"{h['d35']:,}",
             "%%ERRD%%": f"{100*h['share_err_1.6_to_2.0']['d10']:.1f}", "%%ERRS%%": f"{100*h['share_err_1.6_to_2.0']['solved']:.1f}",
             "%%MEDD%%": str(h["median_depthError"]["d10"]), "%%MEDS%%": str(h["median_depthError"]["solved"])}.items():
    page = page.replace(k, v)
open("index.html", "w").write(page)
