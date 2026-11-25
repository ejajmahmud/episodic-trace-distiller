"""Tests for Episodic Trace Distiller."""
import unittest
from episodic_trace_distiller.core import EpisodicTraceDistiller


class TestEpisodicTraceDistiller(unittest.TestCase):
    def setUp(self):
        self.distiller = EpisodicTraceDistiller()

    def test_distills_error_to_recovery_lesson(self):
        lesson = self.distiller.distill([
            {"tool": "compile", "status": "error", "error": "missing header"},
            {"tool": "install_dev", "status": "ok", "args": {"lib": "ssl"}},
            {"tool": "compile", "status": "ok"},
        ])
        self.assertEqual(lesson["kind"], "recovery_lesson")
        self.assertTrue(lesson["resolved"])
        self.assertIn("missing header", lesson["trigger"])
        self.assertIn("install_dev", lesson["verified_fix"])

    def test_distills_unresolved_failure(self):
        lesson = self.distiller.distill([{"tool": "deploy", "status": "error", "error": "auth_denied"}])
        self.assertEqual(lesson["kind"], "failure_warning")
        self.assertFalse(lesson["resolved"])

    def test_empty_trace_returns_none(self):
        self.assertIsNone(self.distiller.distill([]))
