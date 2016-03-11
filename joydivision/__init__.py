import rasterio as rio
import numpy as np
import click
import json

from shapely.geometry import Polygon, LineString

__version__ = '1.1.1'

def offset_rad_poly(lngs, lats, valRow, bounds, scaling_factor):
    return np.concatenate([
        np.dstack([lngs, lats + valRow * scaling_factor])[0],
        [[bounds.right, lats[-1]]],
        [[bounds.right, bounds.bottom]],
        [[bounds.left, bounds.bottom]],
        [[bounds.left, lats[0]]]
        ])

def offset_rad_line(lngs, lats, valRow, bounds, scaling_factor):
    return np.concatenate([
        np.dstack([lngs, lats + valRow * scaling_factor])[0],
        [[bounds.right, lats[-1]]]
        ])

def make_point_grid(rows, cols, bounds):
    return np.array(
        [
            np.arange(bounds.left, bounds.right, ((bounds.right - bounds.left) / float(cols))) for i in range(rows)
        ]), np.rot90(np.array([
            np.arange(bounds.bottom, bounds.top, ((bounds.top - bounds.bottom) / float(rows))) for i in range(cols)
        ])
    )


def joydivision(inputfile, row_interval, col_interval, scaling_factor, nodata_set, bidx, gtype):
    with rio.open(inputfile) as src:
        bounds = src.bounds
        rasVals = np.zeros((
            int(src.height / float(row_interval)),
            int(src.width / float(col_interval))
            ), dtype=src.meta['dtype'])

        src.read(bidx, out=rasVals)
        cellsize = src.affine.a

    if nodata_set:
        rasVals[np.where(rasVals == src.nodata)] = nodata_set

    rows, cols = rasVals.shape

    lngs, lats, = make_point_grid(rows, cols, bounds)


    for r in xrange(rows):

        xy = offset_rad_line(lngs[r], lats[r], rasVals[r], bounds, scaling_factor)

        if gtype == 'LineString':
            polygon = LineString(xy.tolist())
            polygon = polygon.simplify(cellsize)

            click.echo(json.dumps({
                "type": "Feature",
                "properties": {
                    'row': r
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [xy for xy in polygon.coords]
                }
            }))

        else:
            polygon = Polygon(xy.tolist())
            polygon = polygon.simplify(cellsize)

            click.echo(json.dumps({
                "type": "Feature",
                "properties": {
                    'row': r
                },
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[xy for xy in polygon.exterior.coords]]
                }
            }))

if __name__ == '__main__':
    joydivision()