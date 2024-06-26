import os

import pandas as pd

from docx_utils import make_diff, process_text, split_article

SRC_FILE = "input/manuscript.md"
ORG_FOLDER = "content"
OUTPUT_FOLDER = "input/content"
DIFF_FOLDER = "input/diff"
CITATION_FILE = "output/citations.tsv"

if __name__ == "__main__":
    # load data
    with open(SRC_FILE) as f:
        src_ls = f.readlines()
        article = split_article(src_ls)
    with open(os.path.join(ORG_FOLDER, "01.abstract.md")) as f:
        abstract_org = f.readlines()
    with open(os.path.join(ORG_FOLDER, "02.main.md")) as f:
        main_org = f.readlines()
    with open(os.path.join(ORG_FOLDER, "90.back-matter.md")) as f:
        back_org = f.readlines()
    cite_dict = (
        pd.read_csv(CITATION_FILE, sep="\t")[["short_id", "input_id"]]
        .set_index("short_id")
        .squeeze()
        .to_dict()
    )
    abstract_new = process_text(article["abstract"], cite_dict)
    main_new = process_text(article["main"], cite_dict)
    back_new = process_text(article["back-matter"], cite_dict)
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    os.makedirs(DIFF_FOLDER, exist_ok=True)
    with open(os.path.join(OUTPUT_FOLDER, "01.abstract.md"), mode="w") as f:
        f.writelines(abstract_new)
    with open(os.path.join(OUTPUT_FOLDER, "02.main.md"), mode="w") as f:
        f.writelines(main_new)
    with open(os.path.join(OUTPUT_FOLDER, "90.back-matter.md"), mode="w") as f:
        f.writelines(back_new)
    with open(os.path.join(DIFF_FOLDER, "abstract.html"), mode="w") as f:
        f.write(make_diff(abstract_org, abstract_new))
    with open(os.path.join(DIFF_FOLDER, "main.html"), mode="w") as f:
        f.write(make_diff(main_org, main_new))
    with open(os.path.join(DIFF_FOLDER, "back.html"), mode="w") as f:
        f.write(make_diff(back_org, back_new))
