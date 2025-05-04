import panflute as pf


def action(elem, doc):
    if hasattr(elem, "attributes") and "custom-style" in elem.attributes:
        del elem.attributes["custom-style"]
        return elem


def main():
    pf.run_filter(action)


if __name__ == "__main__":
    main()
