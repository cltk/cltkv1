"""Script for provisioning build server.

Use: `$ python cltk/utils/download.py`
"""

import os

from stanfordnlp.utils.resources import download  # type: ignore


def get_stanfordnlp_models(force_update=True):
    """Download language models, from the ``stanfordnlp`` project,
    that are supported by the CLTK or in scope. More here:
    `<https://stanfordnlp.github.io/stanfordnlp/models.html>_.
    """
    ud_models_for_cltk = [
        "grc_perseus",
        "grc_proiel",
        "la_ittb",
        "la_perseus",
        "la_proiel",
        "cu_proiel",  # Old Church Slavonic
        "fro_srcmf",  # Old French
    ]

    stanford_dir = os.path.expanduser("~/stanfordnlp_resources/")
    if os.path.isdir(stanford_dir) and not force_update:
        return
    for model in ud_models_for_cltk:
        download(
            download_label=model,
            resource_dir=stanford_dir,
            confirm_if_exists=True,
            force=force_update,
        )


if __name__ == "__main__":
    get_stanfordnlp_models()
