import importlib.util
from pathlib import Path


MODULE_PATH = Path(__file__).with_name("monitor.py")
spec = importlib.util.spec_from_file_location("monitor", MODULE_PATH)
monitor = importlib.util.module_from_spec(spec)
spec.loader.exec_module(monitor)


class FakeAddr:
    def __init__(self, port):
        self.port = port


class FakeConn:
    def __init__(self, port, pid, status):
        self.laddr = FakeAddr(port)
        self.pid = pid
        self.status = status


def test_check_listening_ports_reports_process_name_and_handles_access_denied(monkeypatch, capsys):
    fake_connections = [
        FakeConn(22, 100, monitor.psutil.CONN_LISTEN),
        FakeConn(9999, 200, monitor.psutil.CONN_LISTEN),
    ]

    def fake_net_connections(kind="tcp"):
        return fake_connections

    def fake_process(pid):
        if pid == 100:
            return type("FakeProcess", (), {"name": lambda self: "sshd"})()
        raise monitor.psutil.AccessDenied(pid)

    monkeypatch.setattr(monitor.psutil, "net_connections", fake_net_connections)
    monkeypatch.setattr(monitor.psutil, "Process", fake_process)

    monitor.check_listening_ports()

    output = capsys.readouterr().out
    assert "Port" in output
    assert "Process" in output
    assert "sshd" in output
    assert "Access denied" in output
    assert "22" in output
    assert "9999" in output
