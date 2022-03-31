from __init__ import FakeSession
from awscli.customizations.configure import exporter
from awscli.testutils import unittest

class TestExporterCommand(unittest.TestCase):
    def setUp(self):
        self.session = FakeSession()
        self.command = exporter.ConfigureExportCommand(self.session)

    def test_exporter_command(self):
        self.command.run()
        self.assertIn('aws_access_key_id', self.command.stdout.getvalue())
        self.assertIn('aws_secret_access_key', self.command.stdout.getvalue())