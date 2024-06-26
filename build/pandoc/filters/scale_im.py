import panflute as pf
import re
import os
import xml.etree.ElementTree as ET

ROOT_PATH = "./content"


def action(elem, doc):
    if isinstance(elem, pf.Image):
        if (
            elem.attributes.get("width") is not None
            or elem.attributes.get("height") is not None
        ):
            return
        fpath = os.path.join(ROOT_PATH, elem.url)
        if fpath.endswith(".svg"):
            dpi = float(doc.get_metadata("dpi"))
            svg = ET.parse(fpath).getroot()
            try:
                pat = re.compile(r"([\d\.]+)(px|pt)")
                width = float(re.search(pat, svg.attrib["width"]).group(1))
                height = float(re.search(pat, svg.attrib["height"]).group(1))
            except AttributeError:
                width = float(svg.attrib["width"])
                height = float(svg.attrib["height"])
            elem.attributes["width"] = "{}in".format(width / dpi)
            elem.attributes["height"] = "{}in".format(height / dpi)
            return elem


def main(doc=None):
    return pf.run_filter(action, doc=doc)


if __name__ == "__main__":
    main()
