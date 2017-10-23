"""Submodule of direct_downloader, provides a OneDrive wrapper class."""

import re
import requests as req
from .model import FileHoster


class OneDrive(FileHoster):
    """Wrapper class for OneDrive."""

    URL = 'https://api.onedrive.com/v1.0/shares/{}/root?expand=children'

    def process(self, print_only=False):
        """Process the provided sharing link.

        Args:
            print_only (bool): the direct link will be printed instead of downloaded
        """
        rgx = re.compile(r'(s\![a-zA-Z0-9]+)')
        sharing_id = rgx.findall(self.sharing_link)[0]

        shared_items = req.get(self.URL.format(sharing_id)).json()['children']
        if len(shared_items) == 1:
            self.filename = shared_items[0]['name']
            self.direct_link = shared_items[0]['@content.downloadUrl']
        else:
            raise RuntimeError('Shared more than one file!')

        if print_only:
            print(self.direct_link)
        else:
            self.download()
