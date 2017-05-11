"""Submodule of direct_downloader, provides a YandexDisk wrapper class."""

import requests as req
from direct_downloader.model import FileHoster


class YandexDisk(FileHoster):
    """Wrapper class for YandexDisk."""

    URL = 'https://cloud-api.yandex.net/v1/disk/public/resources/download?public_key={}'

    def process(self, print_only=False):
        """Process the provided sharing link.

        Args:
            print_only (bool): the direct link will be printed instead of downloaded
        """
        response = req.get(self.URL.format(self.sharing_link))
        self.direct_link = response.json()['href']
        fname = self.direct_link.split('&')[1].split('=')[1]
        self.filename = self.make_filenames_great_again(fname)
        if print_only:
            print(self.direct_link)
        else:
            self.download()
