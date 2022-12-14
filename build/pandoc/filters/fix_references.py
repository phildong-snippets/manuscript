import panflute as pf
import json
import re

REF_PATH = "./output/references.json"


def action(elem, doc):
    return


def main(doc=None):
    with open(REF_PATH, "r") as rfile:
        ref = json.load(rfile)
    for ent in ref:
        for field, val in ent.items():
            if isinstance(val, str):
                val = re.sub(r"&lt;", r"<", val)
                val = re.sub(r"&gt;", r">", val)
                val = re.sub("\u2010", "-", val)
                val = re.sub(r"<em>(.*)</em>", r"<i>\g<1></i>", val)
                ent[field] = val
    with open(REF_PATH, "w") as rfile:
        json.dump(ref, rfile)
    return pf.run_filter(action, doc=doc)


if __name__ == "__main__":
    main()
