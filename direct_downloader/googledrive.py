"""Submodule of direct_downloader, provides a GoogleDrive wrapper class."""

import re
import requests as req
from direct_downloader.model import FileHoster


class GoogleDrive(FileHoster):
    """Wrapper class for GoogleDrive."""

    URL = 'https://docs.google.com/uc?export=download'

    def process(self, print_only=False):
        """Process the provided sharing link.

        Args:
            print_only (bool): the direct link will be printed instead of downloaded
        """
        rgx = re.compile("([a-zA-Z0-9]{28})")
        file_id = rgx.findall(self.sharing_link)[0]
        session = req.Session()
        response = session.get(self.URL, params={'id': file_id}, stream=True)
        if response.status_code != 200:
            raise RuntimeError('There is nothing available for the ID {}'.format(file_id))

        token = None
        for key, value in response.cookies.items():
            if key.startswith('download_warning'):
                token = value
        if token:
            response = session.get(self.URL,
                                   params={'id': file_id, 'confirm': token},
                                   stream=True)

        self.direct_link = response.url
        self.resp_headers = response.headers

        self.filename = self.find_filename(self.resp_headers)

        if print_only:
            print(self.direct_link)
        else:
            self.download()
