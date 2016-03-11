# Moothedata command.

import sys

import click
import rasterio

import joydivision as jd

from joydivision import __version__ as joy_version


@click.command(short_help="")
@click.argument('inputfile', type=click.Path(exists=True), required=True)
@click.option('--row-interval', '-r', default=1, type=int, help="Row interval to sample on [default = 1]")
@click.option('--col-interval', '-c', default=1, type=int, help="Column interval to sample on [default = 1]")
@click.option('--scaling-factor', '-f', default=1.0, type=float, help="Value to scale y-offset by [default = 1.0]")
@click.option('--nodata-set', '-n', default=None, help="Value to set nodata to [default = None]")
@click.option('--bidx', default=1, type=int, help="Band to joyifiy [DEFAULT=1]")
@click.option('--gtype', '-t', default='LineString', type=click.Choice(['Polygon', 'LineString']),  help="Output geom type [default = LineString]")
@click.version_option(version=joy_version, message='%(version)s')
@click.pass_context
def joydivision(ctx, inputfile, row_interval, col_interval, scaling_factor, nodata_set, bidx, gtype):
    '''
    LOVE\n
        WILL\n
            TEAR\n
                US\n
                    APART'''
    jd.joydivision(inputfile, row_interval, col_interval, scaling_factor, nodata_set, bidx, gtype)
