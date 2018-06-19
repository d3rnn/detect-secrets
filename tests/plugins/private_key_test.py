from __future__ import absolute_import
from __future__ import unicode_literals

import pytest

from detect_secrets.plugins.private_key import PrivateKeyDetector
from tests.util.file_util import create_file_object_from_string


class TestPrivateKeyDetector(object):

    @pytest.mark.parametrize(
        'file_content',
        [
            (
                '-----BEGIN RSA PRIVATE KEY-----\n'
                'super secret private key here\n'
                '-----END RSA PRIVATE KEY-----'
            ),
            (
                'some text here\n'
                '-----BEGIN PRIVATE KEY-----\n'
                'yabba dabba doo'
            ),
        ]
    )
    def test_analyze(self, file_content):
        logic = PrivateKeyDetector()

        f = create_file_object_from_string(file_content)
        output = logic.analyze(f, 'mock_filename')
        assert len(output) == 1
        for potential_secret in output:
            assert 'mock_filename' == potential_secret.filename
