import panflute as pf

SEC_TITLE = "Tables"
tables = []


def action(elem, doc):
    if (
        isinstance(elem, pf.elements.Table)
        and hasattr(elem.parent, "identifier")
        and "tbl" in elem.parent.identifier
    ):
        tables.append(elem)
        return []


def finalize(doc):
    doc.content.extend(
        [
            pf.RawBlock(r"\newpage", format="latex"),
            pf.Header(pf.elements.Str(SEC_TITLE), level=1),
            *tables,
        ]
    )


def main():
    pf.run_filter(action, finalize=finalize)


if __name__ == "__main__":
    main()
