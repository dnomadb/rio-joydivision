import rasterio as rio
import numpy as np
import click
import json

__version__ = '1.1.1'

def offset_rad(lngs, lats, valRow, bounds):
    return np.concatenate([
        np.dstack([lngs, lats + valRow / 2000.0])[0],
        [[bounds.right, bounds.bottom]],
        [[bounds.left, bounds.bottom]],
        [[bounds.left, lats[0]]]
        ])

def make_point_grid(rows, cols, bounds):
    return np.array(
        [
            np.arange(bounds.left, bounds.right, ((bounds.right - bounds.left) / float(cols))) for i in range(rows)
        ]), np.rot90(np.array([
            np.arange(bounds.bottom, bounds.top, ((bounds.top - bounds.bottom) / float(rows))) for i in range(cols)
        ])
    )


def joydivision(inputfile, row_interval, col_interval, scaling_factor, nodata_set):
    with rio.open(inputfile) as src:
        bounds = src.bounds
        rasVals = np.zeros((
            int(src.height / float(row_interval)),
            int(src.width / float(col_interval))
            ), dtype=src.meta['dtype'])

        src.read(1, out=rasVals)

    if nodata_set:
        rasVals[np.where(rasVals == src.nodata)] = nodata_set

    rows, cols = rasVals.shape

    lngs, lats, = make_point_grid(rows, cols, bounds)

    for r in xrange(rows):
        xy = offset_rad(lngs[r], lats[r], rasVals[r], bounds)
        click.echo(json.dumps({
            "type": "Feature",
            "properties": {
                'row': r
            },
            "geometry": {
                "type": "Polygon",
                "coordinates": [xy.tolist()]
            }
        }))

if __name__ == '__main__':
    joydivision()