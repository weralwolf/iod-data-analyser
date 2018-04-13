import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

from iod.a000_config import DE2_NACS_DIR, DE2_WATS_DIR
from ionospheredata.parser import FileParser, NACSRow, WATSRow
from ionospheredata.utils import list_datafiles, local_preload

from os.path import join, dirname, realpath, basename


CURRENT_DIR = realpath(dirname(__file__))
NACS_IMAGES_DIR = join(CURRENT_DIR, "_tracks", "nacs")
WATS_IMAGES_DIR = join(CURRENT_DIR, "_tracks", "wats")


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
            chunks.append([lat[sidx:idx], lon[sidx:idx]])
            sidx = idx

    chunks.append([lat[sidx:], lon[sidx:]])
    print("\t\t{} :points // {}: chunks at {}".format(len(ut), len(chunks), basename(filename)))
    return chunks


def draw_chunks(year, day, chunks, destination_dir=None):
    poles_save_to = None if destination_dir is None else join(destination_dir, "{}-{}-poles.png".format(year, day))
    mercat_save_to = None if destination_dir is None else join(destination_dir, "{}-{}-mercator.png".format(year, day))
    track_colors = [
        "#A7414A",
        "#282726",
        "#6A8A82",
        "#A37C27",
        "#563838",
        "#720017",
        "#763F02",
        "#04060F",
        "#03353E",
        "#C1403D",
        "#52591F",
    ]
    linestyles = ["dotted"]  #, "-", "--", "-.", ":"]
    # water_color = "#7ACCC8"
    # land_color = "#A3D39C"
    water_color = "#A7DBDB"
    land_color = "#E0E4CC"

    fig = plt.figure()

    npole = plt.subplot2grid((1, 2), (0, 0))
    spole = plt.subplot2grid((1, 2,), (0, 1))

    npole_map = Basemap(
        projection='npstere',
        lon_0=0.,
        boundinglat=45.,
        ax=npole
    )
    npole_map.drawparallels(np.arange(-90., 120., 15.), labels=[1, 0, 0, 0], linewidth=0.1)
    npole_map.drawmeridians(np.arange(0., 420., 30.), labels=[1, 0, 1, 1], linewidth=0.1)
    npole_map.drawcoastlines(linewidth=0.2)
    # npole_map.drawcountries()
    npole_map.drawmapboundary(fill_color=None)  # fill_color=water_color)
    npole_map.fillcontinents(color=land_color, lake_color=water_color, alpha=0.3)

    spole_map = Basemap(
        projection='spstere',
        lon_0=180.,
        boundinglat=-45.,
        ax=spole
    )
    spole_map.drawparallels(np.arange(-90., 120., 15.), labels=[1, 0, 0, 0], linewidth=0.1)
    spole_map.drawmeridians(np.arange(0., 420., 30.), labels=[1, 0, 1, 1], linewidth=0.1)
    spole_map.drawcoastlines(linewidth=0.2)
    # spole_map.drawcountries()
    spole_map.drawmapboundary(fill_color=None)  # fill_color=water_color)
    spole_map.fillcontinents(color=land_color, lake_color=water_color, alpha=0.3)

    for n, (lat, lon) in enumerate(chunks):
        npole_map.plot(lon, lat, linestyle=linestyles[n % len(linestyles)], linewidth=2, latlon=True, color=track_colors[n % len(track_colors)])
        spole_map.plot(lon, lat, linestyle=linestyles[n % len(linestyles)], linewidth=2, latlon=True, color=track_colors[n % len(track_colors)])

    fig.suptitle('Polar cups. Year: {}. Day: {}. Chunks: {}'.format(year, day, len(chunks)))
    if destination_dir is not None:
        plt.savefig(poles_save_to, dpi=300, papertype='a0', orientation='landscape')
        plt.clf()
    else:
        plt.show()

    mercator_map = Basemap(
        llcrnrlon=-180., llcrnrlat=-75., urcrnrlon=180., urcrnrlat=85.,
        # llcrnrlon=90., llcrnrlat=-75., urcrnrlon=105., urcrnrlat=65.,
        projection='merc'
    )
    mercator_map.drawcoastlines(linewidth=0.2)
    # mercator_map.drawcountries()
    mercator_map.drawmapboundary(fill_color=None)  # fill_color=water_color)
    mercator_map.fillcontinents(color=land_color, lake_color=water_color, alpha=0.3)
    mercator_map.drawparallels(np.arange(-75, 85, 30), labels=[1, 0, 0, 0], linewidth=0.1)
    mercator_map.drawmeridians(np.arange(-180, 180, 45), labels=[0, 0, 0, 1], linewidth=0.1)

    for n, (lat, lon) in enumerate(chunks):
        mercator_map.plot(lon, lat, linestyle=linestyles[n % len(linestyles)], linewidth=2, latlon=True, color=track_colors[n % len(track_colors)])

    plt.title('Mercator projection. Year: {}. Day: {}. Chunks: {}'.format(year, day, len(chunks)))
    if destination_dir is not None:
        plt.savefig(mercat_save_to, dpi=300, papertype='a0', orientation='landscape')
        plt.clf()
    else:
        plt.show()


def draw_tracks(key, RowParser, dirname, destination_dir=None):
    ignores = [join(dirname, fname.strip()) for fname in open(join(CURRENT_DIR, "README.{}.IGNORE.txt".format(key.upper())), 'r').readlines()]
    goodfiles = [fname for fname in list_datafiles(dirname) if fname not in ignores]
    files_by_days = {}
    for filename in goodfiles:
        year_day = basename(filename)[:7]
        if year_day not in files_by_days:
            files_by_days[year_day] = []
        files_by_days[year_day].append(filename)

    for yearday in sorted(files_by_days.keys())[:3]:
        print("{}: Year/Day".format(yearday))
        print("\t{}: Number of files".format(len(files_by_days[yearday])))
        chunks = sum([chunkup(RowParser, filename) for filename in files_by_days[yearday]], [])
        print("\t{}: Total chunks".format(len(chunks)))
        for n, (lon, lat) in enumerate(chunks):
            print("\t\t{}. {} elements ".format(n, len(lon)))
        year_value = yearday[:4]
        day_value = yearday[4:]
        draw_chunks(year_value, day_value, chunks, destination_dir)


if __name__ == "__main__":
    # draw_tracks('nacs', NACSRow, DE2_NACS_DIR)  #, NACS_IMAGES_DIR)
    draw_tracks('wats', WATSRow, DE2_WATS_DIR)  #, WATS_IMAGES_DIR)

# User to draw polar cups: https://github.com/matplotlib/basemap/issues/350
