import unittest
import json
import tempfile
from pathlib import Path
from rolesleuth.parser import HARParser

class TestHARParser(unittest.TestCase):
    def test_parse_valid_har(self):
        sample_har = {
            "log": {
                "entries": [
                    {
                        "request": {
                            "method": "GET",
                            "url": "https://api.example.com/v1/users/1",
                            "headers": [{"name": "Host", "value": "api.example.com"}]
                        }
                    }
                ]
            }
        }
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".har") as tf:
            json.dump(sample_har, tf)
            tf_name = tf.name

        try:
            reqs = HARParser.parse_file(tf_name, target_domain="api.example.com")
            self.assertEqual(len(reqs), 1)
            self.assertEqual(reqs[0].method, "GET")
            self.assertEqual(reqs[0].url, "https://api.example.com/v1/users/1")
        finally:
            Path(tf_name).unlink(missing_ok=True)

if __name__ == "__main__":
    unittest.main()