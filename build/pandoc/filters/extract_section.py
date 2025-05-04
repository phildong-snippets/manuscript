import panflute as pf

EXTRACT_SECTIONS = {"Supplementary Materials"}


def action(elem, doc):
    return


def finalize(doc):
    new_blocks = []
    extract_mode = False
    extract_level = None
    for elem in doc.content:
        if isinstance(elem, pf.Header):
            header_text = pf.stringify(elem)
            if header_text in EXTRACT_SECTIONS:
                extract_mode = True
                extract_level = elem.level
            elif extract_mode and elem.level <= extract_level:
                extract_mode = False
                extract_level = None
        if extract_mode:
            new_blocks.append(elem)
    doc.content = new_blocks


def main(doc=None):
    return pf.run_filter(action, finalize=finalize, doc=doc)


if __name__ == "__main__":
    main()
