"""Submodule of direct_downloader, provides a basic wrapper class for file hoster."""

import cgi
import requests as req
import sys
from abc import ABC, abstractmethod
from .format import sizeof_fmt


class FileHoster(ABC):
    """Basic wrapper class for file hoster."""

    CHUNK_SIZE = 4096

    def __init__(self, sharing_link):
        """Initialize a new FileHoster object.

        Args:
            sharing_link (str): sharing link from a file hoster
        """
        self.sharing_link = sharing_link
        self.direct_link = None
        self.resp_headers = None
        self.filename = None
        super(FileHoster, self).__init__()

    def download(self):
        """Download the specified file from the filehoster."""
        bytes_written = 0
        bytes_total = None
        response = req.get(self.direct_link, stream=True)
        if 'Content-Length' in response.headers.keys():
            bytes_total = int(response.headers['Content-Length'])
        with open(self.filename, 'wb') as file_:
            for chunk in response.iter_content(self.CHUNK_SIZE):
                if chunk:
                    file_.write(chunk)
                    file_.flush()
                    bytes_written += self.CHUNK_SIZE
                    if bytes_total is None:
                        self.write_progress('{:>10}'.format(sizeof_fmt(bytes_written)))
                    else:
                        progress = int(int(bytes_written/bytes_total*100)/5)
                        bar = '#'*progress
                        self.write_progress('[{:20}] {:>10}/{:>9}'.format(
                                                                    bar,
                                                                    sizeof_fmt(bytes_written),
                                                                    sizeof_fmt(bytes_total)))
        print('\nFinished image download {}'.format(self.filename))

    @staticmethod
    def write_progress(msg):
        """Write the download progress to stdout.

        Args:
            msg (str): progress message
        """
        sys.stdout.write('\rDownloading image {}'.format(msg))
        sys.stdout.flush()

    @staticmethod
    def find_filename(headers):
        """Check the response headers for the filename.

        Returns:
            str: filename
        """
        for key, value in headers.items():
            if key == 'Content-Disposition':
                data = cgi.parse_header(value)[-1]
                if 'filename' in data.keys():
                    return FileHoster.make_filenames_great_again(data['filename'])
                elif 'filename*' in data.keys():
                    fname = data['filename*'].replace('UTF-8', '')
                    fname = fname.replace('\'', '').replace('%20', '_')
                    return FileHoster.make_filenames_great_again(fname)

    @staticmethod
    def make_filenames_great_again(filename):
        """Remove nasty chars and spaces from the filename.

        Args:
            filename (str): raw filename
        Returns:
            str: improved filename
        """
        for char in filename:
            if not char.isalnum() and char not in ['_', '-', '.']:
                filename = filename.replace(char, '_')
        return filename

    @abstractmethod
    def process(self):
        """Abstract method to process the sharing link.

        Needs to be individual implemented for each file hoster.
        """
        pass
