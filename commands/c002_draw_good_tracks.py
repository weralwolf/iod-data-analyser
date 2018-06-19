from matplotlib import use as setRenderingBackend  # isort:skip noqa:E402
setRenderingBackend('Agg')  # isort:skip

from os.path import join, basename  # noqa:E402
from datetime import datetime  # noqa:E402
from commands.utils.logger import logger  # noqa:E402

import numpy as np  # noqa:E402
import matplotlib.pyplot as plt  # noqa:E402
from mpl_toolkits.basemap import Basemap  # noqa:E402

from ionospheredata.utils import list_datafiles  # noqa:E402
from ionospheredata.parser import FileParser, SourceNACSRow, SourceWATSRow  # noqa:E402
from ionospheredata.settings import TRACKS_DIR, ARTIFACTS_DIR, DE2SOURCE_NACS_DIR, DE2SOURCE_WATS_DIR  # noqa:E402


def chunkup(RowParser, filename):
    data = FileParser(RowParser, filename)
    ut = data.get('ut', transposed=True)[0]
    lat = data.get('lat', transposed=True)[0]
    lon = data.get('lon', transposed=True)[0]

    chunks = list()
    sidx = 0
    threshold = 500 / 8.9  # Lets set it at the moment as 500 km gap is long enough to treat as different track
    for idx in range(1, len(ut)):
        if ut[idx] - ut[idx - 1] > threshold:
            chunks.append([list(lat[sidx:idx]), list(lon[sidx:idx]), list(ut[sidx:idx])])
            sidx = idx

    chunks.append([list(lat[sidx:]), list(lon[sidx:]), list(ut[sidx:])])
    logger.info('\t\t{} :points // {}: chunks at {}'.format(len(ut), len(chunks), basename(filename)))
    return chunks


def date_signature(ut_start, ut_end):
    return '{} - {}'.format(datetime.utcfromtimestamp(ut_start).strftime('%H:%M:%S'), datetime.utcfromtimestamp(ut_end).strftime('%H:%M:%S'))


def draw_chunks(year, day, nacs_chunks, wats_chunks, destination_dir=None):
    # Used to draw polar cups: https://github.com/matplotlib/basemap/issues/350
    poles_save_to = None if destination_dir is None else join(destination_dir, '{}-{}-poles.png'.format(year, day))
    mercat_save_to = None if destination_dir is None else join(destination_dir, '{}-{}-mercator.png'.format(year, day))
    track_colors = [
        '#A7414A',
        '#282726',
        '#6A8A82',
        '#A37C27',
        '#563838',
        '#720017',
        '#763F02',
        '#04060F',
        '#03353E',
        '#C1403D',
        '#52591F',
    ]
    water_color = '#A7DBDB'
    land_color = '#E0E4CC'

    fig = plt.figure(figsize=(20, 10), dpi=75)

    npole = plt.subplot2grid((1, 2), (0, 0))
    npole_map = Basemap(
        projection='npstere',
        lon_0=0.,
        boundinglat=45.,
        ax=npole
    )
    npole_map.drawparallels(np.arange(-90., 120., 15.), labels=[1, 0, 0, 0], linewidth=0.1)
    npole_map.drawmeridians(np.arange(0., 420., 30.), labels=[1, 0, 1, 1], linewidth=0.1)
    npole_map.drawcoastlines(linewidth=0.2)
    npole_map.drawmapboundary(fill_color=None)  # fill_color=water_color)
    npole_map.fillcontinents(color=land_color, lake_color=water_color, alpha=0.3)
    nlegend = []

    for n, (lat, lon, ut) in enumerate(nacs_chunks):
        line = npole_map.plot(lon, lat, linestyle='-', linewidth=1, latlon=True, color=track_colors[n % len(track_colors)])
        nlegend.append([line[0], 'nacs, {}'.format(date_signature(ut[0], ut[-1]))])

    for n, (lat, lon, ut) in enumerate(wats_chunks):
        line = npole_map.plot(lon, lat, linestyle='dotted', linewidth=2, latlon=True, color=track_colors[n % len(track_colors)])
        nlegend.append([line[0], 'wats, {}'.format(date_signature(ut[0], ut[-1]))])

    leg = plt.legend(*zip(*nlegend))
    leg.get_frame().set_alpha(0.3)

    spole = plt.subplot2grid((1, 2,), (0, 1))
    spole_map = Basemap(
        projection='spstere',
        lon_0=180.,
        boundinglat=-45.,
        ax=spole
    )
    spole_map.drawparallels(np.arange(-90., 120., 15.), labels=[1, 0, 0, 0], linewidth=0.1)
    spole_map.drawmeridians(np.arange(0., 420., 30.), labels=[1, 0, 1, 1], linewidth=0.1)
    spole_map.drawcoastlines(linewidth=0.2)
    spole_map.drawmapboundary(fill_color=None)  # fill_color=water_color)
    spole_map.fillcontinents(color=land_color, lake_color=water_color, alpha=0.3)
    slegend = []

    for n, (lat, lon, ut) in enumerate(nacs_chunks):
        line = spole_map.plot(lon, lat, linestyle='-', linewidth=1, latlon=True, color=track_colors[n % len(track_colors)])
        slegend.append([line[0], 'nacs, {}'.format(date_signature(ut[0], ut[-1]))])

    for n, (lat, lon, ut) in enumerate(wats_chunks):
        line = spole_map.plot(lon, lat, linestyle='dotted', linewidth=2, latlon=True, color=track_colors[n % len(track_colors)])
        slegend.append([line[0], 'wats, {}'.format(date_signature(ut[0], ut[-1]))])

    leg = plt.legend(*zip(*slegend))
    leg.get_frame().set_alpha(0.3)

    fig.suptitle('Polar cups. Year: {}. Day: {}. Chunks N/W: {} / {}'.format(year, day, len(nacs_chunks), len(wats_chunks)))
    if destination_dir is not None:
        plt.savefig(poles_save_to, dpi=300, papertype='a0', orientation='landscape')
        plt.clf()
    else:
        plt.show()
    plt.close(fig)
    fig = plt.figure(figsize=(12, 10), dpi=75)
    mercator_map = Basemap(
        llcrnrlon=-180., llcrnrlat=-75., urcrnrlon=180., urcrnrlat=85.,
        projection='merc'
    )
    mercator_map.drawcoastlines(linewidth=0.2)
    mercator_map.drawmapboundary(fill_color=None)  # fill_color=water_color)
    mercator_map.fillcontinents(color=land_color, lake_color=water_color, alpha=0.3)
    mercator_map.drawparallels(np.arange(-75, 85, 30), labels=[1, 0, 0, 0], linewidth=0.1)
    mercator_map.drawmeridians(np.arange(-180, 180, 45), labels=[0, 0, 0, 1], linewidth=0.1)
    mlegend = []

    for n, (lat, lon, ut) in enumerate(nacs_chunks):
        line = mercator_map.plot(lon, lat, linestyle='-', linewidth=1, latlon=True, color=track_colors[n % len(track_colors)])
        mlegend.append([line[0], 'nacs, {}'.format(date_signature(ut[0], ut[-1]))])

    for n, (lat, lon, ut) in enumerate(wats_chunks):
        line = mercator_map.plot(lon, lat, linestyle='dotted', linewidth=2, latlon=True, color=track_colors[n % len(track_colors)])
        mlegend.append([line[0], 'wats, {}'.format(date_signature(ut[0], ut[-1]))])

    leg = plt.legend(*zip(*mlegend))
    leg.get_frame().set_alpha(0.3)

    plt.title('Mercator projection. Year: {}. Day: {}. Chunks N/W: {} / {}'.format(year, day, len(nacs_chunks), len(wats_chunks)))
    if destination_dir is not None:
        plt.savefig(mercat_save_to, dpi=300, papertype='a0', orientation='landscape')
        plt.clf()
    else:
        plt.show()
    plt.close(fig)


def draw_tracks(destination_dir=None):
    nacs_ignores = [join(DE2SOURCE_NACS_DIR, fname.strip()) for fname in open(join(ARTIFACTS_DIR, 'nacs.ignore.txt'), 'r').readlines()]
    nacs_goodfiles = [fname for fname in list_datafiles(DE2SOURCE_NACS_DIR) if fname not in nacs_ignores]

    wats_ignores = [join(DE2SOURCE_WATS_DIR, fname.strip()) for fname in open(join(ARTIFACTS_DIR, 'wats.ignore.txt'), 'r').readlines()]
    wats_goodfiles = [fname for fname in list_datafiles(DE2SOURCE_WATS_DIR) if fname not in wats_ignores]

    files_by_days = {}
    for filename in nacs_goodfiles:
        year_day = basename(filename)[:7]
        if year_day not in files_by_days:
            files_by_days[year_day] = {
                'nacs': [],
                'wats': [],
            }
        files_by_days[year_day]['nacs'].append(filename)

    for filename in wats_goodfiles:
        year_day = basename(filename)[:7]
        if year_day not in files_by_days:
            files_by_days[year_day] = {
                'nacs': [],
                'wats': [],
            }
        files_by_days[year_day]['wats'].append(filename)

    for yearday in sorted(files_by_days.keys()):
        logger.info('{}: Year/Day'.format(yearday))
        logger.info('\t{}: Number of files'.format(len(files_by_days[yearday])))
        nacs_chunks = sum([chunkup(SourceNACSRow, filename) for filename in files_by_days[yearday]['nacs']], [])
        wats_chunks = sum([chunkup(SourceWATSRow, filename) for filename in files_by_days[yearday]['wats']], [])
        logger.info('\t{}: Total NACS chunks'.format(len(nacs_chunks)))
        logger.info('\t{}: Total WATS chunks'.format(len(wats_chunks)))
        year_value = yearday[:4]
        day_value = yearday[4:]
        draw_chunks(year_value, day_value, nacs_chunks, wats_chunks, destination_dir)


def main():
    draw_tracks(TRACKS_DIR)


if __name__ == '__main__':
    main()
