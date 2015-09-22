import metasay


def test_msg():
    metadata = {'count': 3, 'dtype': 'uint8', 'driver': 'GTiff'}
    assert "Count: 3" in metasay.moothedata(metadata, 'count')
