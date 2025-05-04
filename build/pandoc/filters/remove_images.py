import panflute as pf


def action(elem, doc):
    if isinstance(elem, pf.elements.Image):
        elem.url = ""


def main():
    pf.run_filter(action)


if __name__ == "__main__":
    main()
