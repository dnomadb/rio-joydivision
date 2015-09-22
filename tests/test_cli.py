import os.path

from click.testing import CliRunner

from metasay.scripts.cli import metasay


def test_cli_dtype():
    filename = os.path.join(os.path.dirname(__file__), 'data/float.tif')
    runner = CliRunner()
    result = runner.invoke(metasay, [filename, '--item', 'dtype'])
    assert result.exit_code == 0
    assert "Dtype: float64" in result.output
