from json import load
from unittest import TestCase
from src import alerts

# Fetch list of test cases
with open('tests/cases.json') as json_file:
    cases = load(json_file)

class TestAlerts(TestCase):
    def test_alert(self):
        for case in cases:
            with self.subTest(case=case):
                with self.assertRaises(SystemExit) as cm:
                    alerts.list_alerts(case["feed"])
                self.assertEqual(cm.exception.code, case["code"])
