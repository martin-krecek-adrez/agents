from __future__ import annotations

from copy import deepcopy
from datetime import date
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
from check_agents_size import check_sizes
from check_runtime_inventory import has_scheduled_workflow, validate_inventory

TODAY = date(2026, 10, 2)


class OperatingChecksTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name).resolve()
        self.budget = {"dbt-cloud/AGENTS.md": {
            "max_bytes": 16000, "owner": "martin", "reviewed_on": "2026-10-02",
            "reason": "Approved detailed dbt rules",
        }}

    def tearDown(self) -> None:
        self.temp.cleanup()

    def write(self, name: str, text: str) -> None:
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)

    def test_size_exception_is_exact_and_retains_warning(self) -> None:
        self.write("dbt-cloud/AGENTS.md", "x" * 13958)
        self.write("dbt-cloud/models/AGENTS.md", "x" * 13000)
        rows = check_sizes(self.root, self.budget, TODAY)
        self.assertEqual([level for level, _ in rows], ["WARN", "FAIL"])
        self.assertIn("reviewed cap 16000", rows[0][1])

    def test_size_exception_is_still_bounded(self) -> None:
        self.write("dbt-cloud/AGENTS.md", "x" * 16001)
        rows = check_sizes(self.root, self.budget, TODAY)
        self.assertTrue(any(level == "FAIL" and "16000" in message for level, message in rows))

    def test_invalid_exception_cannot_silently_disable_limit(self) -> None:
        self.write("dbt-cloud/AGENTS.md", "x" * 13000)
        for value in (None, {}, {"max_bytes": True}, {"max_bytes": 999999}):
            with self.subTest(value=value):
                rows = check_sizes(self.root, {"dbt-cloud/AGENTS.md": value}, TODAY)
                self.assertGreaterEqual(sum(level == "FAIL" for level, _ in rows), 2)

    def inventory(self) -> dict:
        self.write("mews/wrangler.jsonc", '{"triggers":{"crons":[]}}')
        return {"version": 1, "components": [{
            "id": "mews", "repository": "mews", "runtime": "Cloudflare",
            "trigger": "Airflow", "outputs": "R2", "owner": "Data Engineering",
            "health_check": "Read latest source manifest", "reviewed_on": "2026-10-02",
            "source_refs": [{"path": "mews/wrangler.jsonc", "required_patterns": [r'"crons"\s*:\s*\[\s*\]']}],
        }]}

    def test_inventory_detects_scheduler_contract_change(self) -> None:
        payload = self.inventory()
        self.assertEqual(validate_inventory(self.root, payload, TODAY), [])
        self.write("mews/wrangler.jsonc", '{"triggers":{"crons":["0 * * * *"]}}')
        self.assertTrue(any("source contract changed" in message for _, message in validate_inventory(self.root, payload, TODAY)))

    def test_inventory_rejects_missing_health_and_duplicate_component(self) -> None:
        payload = self.inventory()
        payload["components"].append(deepcopy(payload["components"][0]))
        self.assertTrue(any("Duplicate" in message for _, message in validate_inventory(self.root, payload, TODAY)))
        del payload["components"][0]["health_check"]
        self.assertTrue(any("health_check" in message for _, message in validate_inventory(self.root, payload, TODAY)))

    def test_inventory_rejects_unsafe_and_unowned_source_paths(self) -> None:
        for name in ("../outside", "/etc/hosts", "old/AGENTS.md", "commission-tier-monitoring/AGENTS.md", ".sdlc-state/AGENTS.md"):
            with self.subTest(name=name):
                payload = self.inventory()
                payload["components"][0]["source_refs"][0]["path"] = name
                self.assertTrue(any(level == "FAIL" for level, _ in validate_inventory(self.root, payload, TODAY)))

    def test_inventory_reports_missing_source_file_and_stale_review(self) -> None:
        payload = self.inventory()
        payload["components"][0]["reviewed_on"] = "2026-01-01"
        (self.root / "mews/wrangler.jsonc").unlink()
        rows = validate_inventory(self.root, payload, TODAY)
        self.assertTrue(any(level == "WARN" for level, _ in rows))
        self.assertTrue(any("source file is missing" in message for _, message in rows))

    def test_workflow_must_be_inside_the_named_scheduled_dag(self) -> None:
        source = '''
from airflow import DAG
from schedules import CronTriggerTimetable
DAG_ID = "mews"
with DAG(dag_id=DAG_ID, schedule=CronTriggerTimetable("0 0 * * *")):
    task = CloudflareWorkflowOperator(workflow_name="mews-scheduler")
'''
        self.assertTrue(has_scheduled_workflow(source, "mews", "mews-scheduler"))
        self.assertFalse(has_scheduled_workflow(source.replace('schedule=CronTriggerTimetable("0 0 * * *")', 'schedule=None'), "mews", "mews-scheduler"))
        self.assertFalse(has_scheduled_workflow(source.replace('    task =', '    pass\ntask ='), "mews", "mews-scheduler"))
        self.assertFalse(has_scheduled_workflow(source, "other-dag", "mews-scheduler"))


if __name__ == "__main__":
    unittest.main()
