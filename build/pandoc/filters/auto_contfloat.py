import panflute as pf
import re

ROOT_PATH = "./content"
CVT_ARGS = ["-z", "0.6", "-d", "500"]


def action(elem, doc):
    return


def finalize(doc):
    for elem in doc.content:
        if isinstance(elem, pf.Para):
            idx = elem.index
            im = elem.content[0]
            if isinstance(im, pf.Image):
                cap = im.content
                cap_break = im.attributes.get("cap_break", None)
                if cap_break is None:
                    continue
                elif cap_break == "auto":
                    # TODO
                    continue
                else:
                    cap_break = int(cap_break)
                    bk_idx = [
                        i for i in range(len(cap)) if isinstance(cap[i], pf.SoftBreak)
                    ]
                    cap_break = bk_idx[cap_break]
                cap_cont = pf.tools.convert_text(
                    pf.Para(pf.Image(*im.content[cap_break:], title="fig:")),
                    input_format="panflute",
                    output_format="latex",
                )
                cap_cont = re.sub(
                    r"\\begin{figure}",
                    r"\\begin{figure}\\ContinuedFloat\n\\captionsetup{format=cont}",
                    cap_cont,
                )
                cap_cont = re.sub(r"\\includegraphics{}", r"", cap_cont)
                cap_cont = pf.Para(pf.RawInline(cap_cont, format="latex"))
                im.content = im.content[:cap_break]
                doc.content.insert(idx + 1, cap_cont)


def main(doc=None):
    return pf.run_filter(action, finalize=finalize, doc=doc)


if __name__ == "__main__":
    main()
