import panflute as pf
import re
import subprocess
import os
import sys

ROOT_PATH = "./content"
CVT_ARGS = ["-z", "0.6", "-d", "500"]


def action(elem, doc):
    if isinstance(elem, pf.Image):
        fpath = os.path.join(ROOT_PATH, elem.url)
        elem.url = convert_pdf(fpath)
        tex_im = pf.tools.convert_text(
            pf.Para(elem), input_format="panflute", output_format="latex"
        )
        tex_im = re.sub(r"\\caption", r"\\captionof{figure}", tex_im)
        tex_im = re.sub(r"\\begin{figure}", r"\\begin{center}", tex_im)
        tex_im = re.sub(r"\\end{figure}", r"\\end{center}", tex_im)
        return pf.RawInline(tex_im, format="latex")


def convert_pdf(im_path):
    basename, _ = os.path.splitext(im_path)
    outname = basename + ".pdf"
    cmd = ["rsvg-convert"] + CVT_ARGS + ["-f", "pdf", "-o", outname, im_path]
    sys.stderr.write("Running %s\n" % " ".join(cmd))
    subprocess.call(cmd, stdout=sys.stderr.fileno())
    return outname


def main(doc=None):
    return pf.run_filter(action, doc=doc)


if __name__ == "__main__":
    main()
