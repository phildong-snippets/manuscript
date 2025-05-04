import panflute as pf

TARGET_SECTION = "Supplementary Materials"
TARGET_ELEMS = [(pf.Image, "fig"), (pf.Table, None), (pf.Div, "lst")]
TOC_TITLE = "Table of Contents for {}".format(TARGET_SECTION)
elements = []
current_section = None


def action(elem, doc):
    global current_section
    if isinstance(elem, pf.Header):
        current_section = pf.stringify(elem)
    if current_section == TARGET_SECTION:
        for tgt in TARGET_ELEMS:
            if isinstance(elem, tgt[0]):
                if tgt[1] is None or tgt[1] in elem.identifier:
                    elements.append(elem)
                    return elem
    return elem


def finalize(doc):
    toc = []
    for elem in elements:
        if isinstance(elem, pf.Image):
            cap = squeeze(elem)
        elif isinstance(elem, pf.Table):
            cap = squeeze(elem.caption)
        elif isinstance(elem, pf.Div):
            cap = squeeze(elem.content[0])
        brks = [i for i, e in enumerate(cap) if isinstance(e, pf.SoftBreak)]
        ibrk = brks[0]
        item = pf.ListItem(pf.Plain(*cap[:ibrk]))
        toc.append(item)
    toc = pf.BulletList(*toc)
    doc.content.extend(
        [
            pf.RawBlock(r"\newpage", format="latex"),
            pf.Header(pf.elements.Str(TOC_TITLE), level=1),
            toc,
        ]
    )


def squeeze(elem):
    if hasattr(elem, "content"):
        if len(elem.content) == 1:
            return squeeze(elem.content[0])
        else:
            return elem.content
    return elem


def main():
    pf.run_filter(action, finalize=finalize)


if __name__ == "__main__":
    main()
