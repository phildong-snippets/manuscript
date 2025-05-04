import panflute as pf
import re
import os
import xml.etree.ElementTree as ET

ROOT_PATH = "./content"
UNITS = {
    "px": 1,
    "pt": 1,
}  # convesion ratio from different units to pixels, empirically determined


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
                pat = re.compile("([\d\.]+({}))".format("|".join(UNITS.keys())))
                w, h = re.search(pat, svg.attrib["width"]).group(1), re.search(
                    pat, svg.attrib["height"]
                ).group(1)
                w_scal, h_scal = UNITS[w[-2:]], UNITS[h[-2:]]
                width = float(w[:-2]) * w_scal
                height = float(h[:-2]) * h_scal
            except AttributeError:
                width = float(svg.attrib["width"])
                height = float(svg.attrib["height"])
            elem.attributes["width"] = "{}in".format(width / dpi)
            elem.attributes["height"] = "{}in".format(height / dpi)
            pf.debug(
                "width: {:.1f}px {:.2f}in; height: {:.1f}px {:.2f}in; file: {}".format(
                    width, width / dpi, height, height / dpi, os.path.basename(fpath)
                )
            )
            return elem


def main(doc=None):
    return pf.run_filter(action, doc=doc)


if __name__ == "__main__":
    main()
