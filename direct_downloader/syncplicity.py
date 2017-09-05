"""Submodule of direct_downloader, provides a Syncplicity wrapper class."""

import re
import requests as req
from .model import FileHoster


class Syncplicity(FileHoster):
    """Wrapper class for Syncplicity."""

    def process(self, print_only=False):
        """Process the provided sharing link.

        Args:
            print_only (bool): the direct link will be printed instead of downloaded
        """
        session = req.Session()
        token = self.sharing_link.split('/')[-2]

        hidden = r'(?s)(<input.*?type=\"hidden\".*?>)'
        name_value = r'(?s)name=\"(.*?)\".*?value=\"(.*?)\"'
        data = {'ctl00$MainContent$btnDownloadNonIRM': 'Herunterladen'}

        resp = session.get(self.sharing_link)
        for item in re.findall(hidden, resp.text):
            k, v = re.findall(name_value, item)[0]
            data[k] = v
        resp = session.post(self.sharing_link + '?token={}'.format(token), data=data, stream=True)
        self.resp_headers = resp.headers

        self.direct_link = resp.url
        self.filename = self.find_filename(resp.headers)
        if print_only:
            print(self.direct_link)
        else:
            self.download()
