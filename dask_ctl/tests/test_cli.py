from distributed import LocalCluster
from subprocess import check_output
from dask_ctl.cli import autocomplete_cluster_names


def test_list_discovery():
    assert b"proxycluster" in check_output(["daskctl", "discovery", "list"])


def test_list():
    with LocalCluster(name="testcluster", scheduler_port=8786) as _:
        output = check_output(["daskctl", "cluster", "list"])

        assert b"Name" in output

        # Rich truncates output on small displays and check_output seems to set a small
        # terminal size so these strings are truncated.
        # TODO Figure out how to set the terminal size in check_output.
        #
        # assert b"dask_ctl.proxy.ProxyCluster" in output
        # assert b"Running" in output


def test_create(simple_spec_path):
    output = check_output(["daskctl", "cluster", "create", "-f", simple_spec_path])
    assert b"Created" in output


def test_autocompletion():
    with LocalCluster(scheduler_port=8786) as _:
        assert len(autocomplete_cluster_names(None, None, "")) == 1
        assert len(autocomplete_cluster_names(None, None, "proxy")) == 1
        assert len(autocomplete_cluster_names(None, None, "local")) == 0
