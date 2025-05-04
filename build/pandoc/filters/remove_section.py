import panflute as pf

REMOVE_SECTIONS = {"Supplementary Materials"}


def action(elem, doc):
    return


def finalize(doc):
    new_blocks = []
    skip_mode = False
    skip_level = None
    for elem in doc.content:
        if isinstance(elem, pf.Header):
            header_text = pf.stringify(elem)
            if header_text in REMOVE_SECTIONS:
                skip_mode = True
                skip_level = elem.level
                continue
            elif skip_mode and elem.level <= skip_level:
                skip_mode = False
        if not skip_mode:
            new_blocks.append(elem)
    doc.content = new_blocks


def main(doc=None):
    return pf.run_filter(action, finalize=finalize, doc=doc)


if __name__ == "__main__":
    main()
