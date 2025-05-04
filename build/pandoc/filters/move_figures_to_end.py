import panflute as pf

SEC_TITLE = "Figures"
figures = []


def action(elem, doc):
    if isinstance(elem, pf.elements.Image):
        figures.append(pf.Para(elem))
        return []


def finalize(doc):
    doc.content.extend(
        [
            pf.RawBlock(r"\newpage", format="latex"),
            pf.Header(pf.elements.Str(SEC_TITLE), level=1),
            *figures,
        ]
    )


def main():
    pf.run_filter(action, finalize=finalize)


if __name__ == "__main__":
    main()
