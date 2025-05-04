import os
import re
import shutil
import argparse

import numpy as np
from skimage.measure import label

from docx_utils import dedup_labels

parser = argparse.ArgumentParser()
parser.add_argument("letter_path")
parser.add_argument("output_path")
parser.add_argument("-m", "--manu_path", default="content/02.main.md")
parser.add_argument(
    "-p",
    "--pattern",
    default=r"(?:INSERT(\d+)-(\d+))?(?:LABEL(\d+)-(\d+))?(?:(NOSTY))?",
)
parser.add_argument("--letter_style", default="Quoted Change")
parser.add_argument("--manu_style", default="Revision Text")
args = parser.parse_args()


def complete_path(p, fname):
    if os.path.isfile(p):
        return p
    elif os.path.exists(p) and os.path.isfile(os.path.join(p, fname)):
        return os.path.join(p, fname)
    else:
        raise FileNotFoundError(p)


if __name__ == "__main__":
    manu_path = complete_path(args.manu_path, "02.main.md")
    lt_path = complete_path(args.letter_path, "rebuttal_letter.md")
    with open(manu_path, encoding="utf-8") as f:
        manu_org = f.readlines()
    with open(lt_path, encoding="utf-8") as f:
        reb_org = f.readlines()
    reb_new = []
    quoted_line = np.zeros(len(manu_org), dtype=int)
    sty_ls = []
    for ln in reb_org:
        match = re.search(args.pattern, ln)
        ins0, ins1, lab0, lab1, nosty = match.groups()
        if any([ins0, ins1, lab0, lab1]):
            if ins0 is not None and ins1 is not None:
                ins0, ins1 = (
                    int(ins0) - 1,
                    int(ins1) - 1,
                )  # offset by 1 since line number in IDE are 1-indexed
            else:
                ins0, ins1 = -1, -1
            if lab0 is not None and lab1 is not None:
                lab0, lab1 = (
                    int(lab0) - 1,
                    int(lab1) - 1,
                )  # offset by 1 since line number in IDE are 1-indexed
            else:
                lab0, lab1 = -1, -1
            sty = not bool(nosty)
            if ins0 >= 0 and ins1 >= 0:
                prefix = ln[: match.span()[0]]
                lns = []
                for l in manu_org[ins0 : ins1 + 1]:
                    l = re.sub(r"\s\[\@doi\:.*?\]", "", l)
                    l = re.sub(r"\s\[\@isbn\:.*?\]", "", l)
                    # l = re.sub(r"\{#tbl:.*\}", "", l)
                    # l = re.sub(r"\[(.*?)\]", r"\1", l)
                    lns.append(l)
                if sty:
                    lns[0] = "[" + lns[0]
                    lns[-1] = (
                        lns[-1].rstrip("\n")
                        + ']{custom-style="'
                        + args.letter_style
                        + '"}\n'
                    )
                lns = [prefix + l for l in lns]
                reb_new.extend(lns)
            if lab0 > 0 and lab1 > 0:
                quoted_line[lab0 : lab1 + 1] = 1
                sty_ls.append(sty)
        else:
            reb_new.append(ln)
    reb_new = dedup_labels(reb_new)
    labs, nlab = label(quoted_line, return_num=True)
    manu_new = []
    last_ln = 0
    for ilab, sty in zip(range(1, nlab + 1), sty_ls):
        idxs = np.nonzero(labs == ilab)[0]
        ln0, ln1 = idxs[0], idxs[-1]
        manu_new.extend(manu_org[last_ln:ln0])
        lns = manu_org[ln0 : ln1 + 1].copy()
        if sty:
            for esc_pat in ["Table: ", "Listing: "]:
                if lns[0].startswith(esc_pat):
                    lns[0] = esc_pat + "[" + lns[0][len(esc_pat) :]
                    break
            else:
                lns[0] = "[" + lns[0]
            lns[-1] = (
                lns[-1].rstrip("\n") + ']{custom-style="' + args.manu_style + '"}\n'
            )
        manu_new.extend(lns)
        last_ln = ln1 + 1
    manu_new.extend(manu_org[last_ln:])
    manu_out_path = os.path.join(args.output_path, os.path.basename(manu_path))
    lt_out_path = os.path.join(args.output_path, os.path.basename(lt_path))
    shutil.rmtree(args.output_path, ignore_errors=True)
    shutil.copytree(os.path.dirname(manu_path), os.path.dirname(manu_out_path))
    with open(manu_out_path, encoding="utf-8", mode="w") as f:
        f.writelines(manu_new)
    with open(lt_out_path, encoding="utf-8", mode="w") as f:
        f.writelines(reb_new)
