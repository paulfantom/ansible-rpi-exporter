import os
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_files(host):
    files = [
        "/etc/systemd/system/rpi_exporter.service",
        "/usr/local/bin/rpi_exporter"
    ]
    for file in files:
        f = host.file(file)
        assert f.exists
        assert f.is_file


def test_permissions_didnt_change(host):
    dirs = [
        "/etc",
        "/root",
        "/usr",
        "/var"
    ]
    for file in dirs:
        f = host.file(file)
        assert f.exists
        assert f.is_directory
        assert f.user == "root"
        assert f.group == "root"


def test_user(host):
    assert host.group("rpi-exporter").exists
    assert "rpi-exporter" in host.user("rpi-exporter").groups
    assert host.user("rpi-exporter").shell == "/usr/sbin/nologin"
    assert host.user("rpi-exporter").home == "/"


def test_service(host):
    s = host.service("rpi_exporter")
#    assert s.is_enabled
    assert s.is_running


def test_socket(host):
    sockets = [
        "tcp://127.0.0.1:9243"
    ]
    for socket in sockets:
        s = host.socket(socket)
        assert s.is_listening
