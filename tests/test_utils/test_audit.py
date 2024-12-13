from datetime import datetime

import pytest

from slumber.utils.audit import AuditType, Event, log_event, setup_audit


@pytest.fixture
def audit_config():
    return {"file_name": "audit.log"}


@pytest.fixture
def sample_event():
    return Event(
        type=AuditType.APP_START,
        timestamp=datetime(2024, 1, 1, 12, 0),
        description="Test startup",
        extra={"version": "1.0.0"},
    )


def test_setup_audit(tmpdir, audit_config, sample_event):
    setup_audit(tmpdir, audit_config.copy())
    log_event(sample_event)

    audit_file = tmpdir / "audit.log"
    assert audit_file.exists()

    content = audit_file.read_text(encoding="utf-8")
    assert "APP_START" in content
    assert "2024-01-01T12:00:00" in content
    assert "Test startup" in content
    assert "version" in content
