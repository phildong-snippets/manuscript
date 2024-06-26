import panflute as pf
import re
import os
import xml.etree.ElementTree as ET

ROOT_PATH = "./content"


def action(elem, doc):
    if isinstance(elem, pf.Image):
        fpath = os.path.join(ROOT_PATH, elem.url)
        if fpath.endswith(".svg"):
            dpi = float(doc.get_metadata("dpi", 100))
            svg = ET.parse(fpath).getroot()
            pat = re.compile(r"([\d\.]+)px")
            try:
                width = float(re.search(pat, svg.attrib["width"]).group(1))
                height = float(re.search(pat, svg.attrib["height"]).group(1))
                elem.attributes["width"] = "{}in".format(width / dpi)
                elem.attributes["height"] = "{}in".format(height / dpi)
            except (AttributeError, KeyError):
                pass
            return elem


def main(doc=None):
    return pf.run_filter(action, doc=doc)


if __name__ == "__main__":
    main()
