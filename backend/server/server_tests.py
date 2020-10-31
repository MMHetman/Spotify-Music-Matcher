import unittest

from backend.server.app import app


class ServerTests(unittest.TestCase):
    def setUp(self) -> None:
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        self.test_client = app.test_client()

    def test_root(self):
        audio_file = open('test.mp3', 'rb')

        response = self.test_client.post(
            "/",
            data={
                "file": (audio_file, 'test.mp3'),
            },
            content_type="multipart/form-data"
        )

        self.assertEqual(response.status_code, 200)

unittest.main()
