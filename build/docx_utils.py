import functools as fct
import re
from difflib import HtmlDiff


def semantic_lining(str_ls):
    res_ls = []
    for iline, line in enumerate(str_ls):
        s_ls = re.split(r"(\S+\s\S+\s\S+(?<!fig|i\.e|e\.g|\sal)[\.\;]\**)\s", line)
        if len(s_ls) > 1:
            s_ls_merge = [
                s_ls[i] + s_ls[i + 1] + "\n" for i in range(0, len(s_ls) - 1, 2)
            ]
            if len(s_ls) % 2 == 1 and s_ls[-1] != "":
                s_ls_merge.append(s_ls[-1])
            res_ls.extend(s_ls_merge)
        else:
            res_ls.append(line)
    return res_ls


def normalize_links(line):
    return re.sub(r"\[(\[.*?\])\{\.underline\}\](\(.*?\))", r"\1\2", line)


def normalize_figure_captions(str_ls):
    res_ls = []
    skip_idx = []
    for iline, line in enumerate(str_ls):
        if iline in skip_idx:
            continue
        if re.search(r"\!\[Figure.*\]\(media.*\)", line):
            caption = re.search(
                r"Figure\s(?:S)?\d+[\:\.]\s(.*)", str_ls[iline + 2]
            ).group(1)
            line = re.sub(r"\!\[Figure.*?\]", "\n".join(["![", caption, "]"]), line)
            res_ls.extend([l + "\n" for l in line.rstrip("\n").split("\n")])
            skip_idx.extend([iline + 1, iline + 2])
        else:
            res_ls.append(line)
    return res_ls


def anchor_figure(line):
    return re.sub(
        r"\[\]\{(\#fig\:.*) \.anchor\}\!\[(.*)\]\((.*)\)\{(.*)\}",
        r"![\2](\3){\1 \4}",
        line,
    )


def ref_internal(line):
    return re.sub(r"\[(.*?)\]\(\#(?!ref-)[a-z-].*?\)", r"[\1]", line)


def ref_figure(line):
    return re.sub(r"[fF]igure\s\[(?:S)?\d+\]\(\#(.*?)\)", r"{@\1}", line)


def citations(line, cite_dict):
    line, nsub = re.subn(
        r"\[\d+\]\(\#ref-(.*?)\)", lambda m: "@" + cite_dict[m.group(1)], line
    )
    if nsub > 0:
        line = re.sub(
            r"\\\[(@.*?)\\\]",
            lambda m: "[{}]".format(re.sub(r",(?=@)", r";", m.group(1))),
            line,
        )
    return line


def split_article(src_ls):
    # ln_author = src_ls.index("## Authors\n")
    ln_abstract = src_ls.index("## Abstract\n")
    ln_main = src_ls.index("## Introduction\n")
    ln_back = src_ls.index("## References\n")
    return {
        "front-matter": src_ls[:ln_abstract],
        "abstract": src_ls[ln_abstract:ln_main],
        "main": src_ls[ln_main:ln_back],
        "back-matter": src_ls[ln_back:],
    }


def process_text(src_ls, cite_dict=None):
    src_ls = list(map(anchor_figure, src_ls))
    src_ls = list(map(ref_figure, src_ls))
    src_ls = list(map(ref_internal, src_ls))
    src_ls = list(map(lambda s: s.replace("\u00A0", " "), src_ls))
    src_ls = normalize_figure_captions(src_ls)
    src_ls = semantic_lining(src_ls)
    if cite_dict is not None:
        src_ls = list(map(fct.partial(citations, cite_dict=cite_dict), src_ls))
    # src_ls = list(map(normalize_links, src_ls))
    return src_ls


def make_diff(org_ls, new_ls):
    diff = HtmlDiff(wrapcolumn=90)
    return diff.make_file(org_ls, new_ls)
