from matplotlib import use as setRenderingBackend  # isort:skip noqa:E402
setRenderingBackend('TkAgg')  # isort:skip

from os import listdir  # noqa:E402
from json import load as load_json  # noqa:E402
from math import ceil, sqrt, floor  # noqa:F402
from fnmatch import fnmatch  # noqa:E402
from os.path import join, basename  # noqa:E402

import seaborn as sns  # noqa:E402
from numpy import array  # noqa:E402
from matplotlib import pyplot as plt  # noqa:E402

from ionospheredata.settings import ARTIFACTS_DIR  # noqa:E402

sns.set(style='ticks')


def round(x):
    return ceil(x) if x - floor(x) > 0.5 else floor(x)


def disambiguate(measurements, key_function):
    present = set()
    unique = []
    for element in measurements:
        key = key_function(element)
        if key not in present:
            present.add(key)
            unique.append(element)
    return unique


def load_samplings(device_key, unique=False):
    jsons_names = sorted([join(ARTIFACTS_DIR, fnm) for fnm in listdir(ARTIFACTS_DIR) if fnmatch(fnm, '{}.*.sampling.by_ut.json'.format(device_key))])

    for fname in jsons_names:
        filedata = load_json(open(fname))
        if len(filedata) == 0:
            continue

        if unique:
            filedata = disambiguate(filedata, lambda x: x['indexes'][1])

        yield fname, filedata


def calculate_statistics(device_key, unique=False):
    metrics = []
    for fname, filedata in load_samplings(device_key, unique):
        metrics.append(dict(
            sampling=int(basename(fname)[5:9]),
            resolution_min=min([x['resolution'] for x in filedata]),
            duration_avg=sum([x['duration'] for x in filedata]) / len(filedata),
            duration_max=max([x['duration'] for x in filedata]),
            duration_min=min([x['duration'] for x in filedata]),
        ))

    return (
        [x['sampling'] for x in metrics],
        [x['resolution_min'] for x in metrics],
        [x['duration_avg'] for x in metrics],
        [x['duration_max'] for x in metrics],
        [x['duration_min'] for x in metrics]
    )


def draw_statistics():
    samp_nacs, res_nacs, duration_nacs_avg, duration_nacs_max, duration_nacs_min = calculate_statistics('nacs', True)
    samp_wats, res_wats, duration_wats_avg, duration_wats_max, duration_wats_min = calculate_statistics('wats', True)

    fig, ax = plt.subplots()
    ax.plot(samp_nacs, res_nacs, '.')
    ax.plot(samp_wats, res_wats, '.')
    ax.legend(['NACS min sampling', 'WATS min sampling'])
    ax.set(xlabel='sampling (s)', ylabel='resolution', title='Min resolution under fixes samplings in DE2 data')
    plt.show()

    fig, ax = plt.subplots()
    ax.plot(samp_nacs, duration_nacs_avg, '.')
    ax.plot(samp_wats, duration_wats_avg, 'x')
    ax.plot(samp_nacs, [250 * sqrt(x) for x in samp_nacs], linewidth=0.1)
    ax.legend(['NACS avg duration', 'WATS avg duration', 'Minimal considered duration'])
    ax.set(xlabel='sampling (s)', ylabel='duration (s)', title='Avg duration under fixes samplings in DE2 data')
    plt.show()

    fig, ax = plt.subplots()
    ax.plot(samp_nacs, duration_nacs_min, '.')
    ax.plot(samp_nacs, duration_nacs_avg, 'x')
    ax.plot(samp_nacs, duration_nacs_max, '.')
    ax.plot(samp_nacs, [250 * sqrt(x) for x in samp_nacs], linewidth=0.1)
    ax.legend(['NACS min duration', 'NACS avg duration', 'NACS max duration', 'Minimal considered duration'])
    ax.set(xlabel='sampling (s)', ylabel='duration (s)', title='Min / avg / max continous data duration under fixes samplings in DE2 NACS data')
    plt.show()

    fig, ax = plt.subplots()
    ax.plot(samp_wats, duration_wats_min, '.')
    ax.plot(samp_wats, duration_wats_avg, 'x')
    ax.plot(samp_wats, duration_wats_max, '.')
    ax.plot(samp_nacs, [250 * sqrt(x) for x in samp_nacs], linewidth=0.1)
    ax.legend(['WATS min duration', 'WATS avg duration', 'WATS max duration', 'Minimal considered duration'])
    ax.set(xlabel='sampling (s)', ylabel='duration (s)', title='Min / avg / max continous data duration under fixes samplings in DE2 WATS data')
    plt.show()


def calculate_distributions(device_key, unique=False):
    metrics = []
    for fname, filedata in load_samplings(device_key, unique):
        sampling_value = int(basename(fname)[5:9])
        metrics.append(dict(
            sampling=[sampling_value] * len(filedata),
            resolutions=[x['resolution'] for x in filedata],
            durations=[x['duration'] for x in filedata]
        ))

    return (
        list(sum([x['sampling'] for x in metrics], [])),
        list(sum([x['resolutions'] for x in metrics], [])),
        list(sum([x['durations'] for x in metrics], [])),
    )


def draw_distributions():
    nacs_sampling, nacs_resolutions, nacs_durations = calculate_distributions('nacs', unique=True)
    sns.jointplot(x=array(nacs_sampling), y=array(nacs_durations), kind='kde', linewidth=2)
    plt.title('NACS durations')
    sns.jointplot(x=array(nacs_sampling), y=array(nacs_resolutions), kind='kde', linewidth=2)
    plt.title('NACS resolutions')
    plt.show()

    wats_sampling, wats_resolutions, wats_durations = calculate_distributions('wats', unique=True)
    sns.jointplot(x=array(wats_sampling), y=array(wats_durations), kind='kde', linewidth=2)
    plt.title('WATS durations')
    sns.jointplot(x=array(wats_sampling), y=array(wats_resolutions), kind='kde', linewidth=2)
    plt.title('WATS resolutions')
    plt.show()


def main():
    # draw_distributions()
    draw_statistics()


if __name__ == '__main__':
    main()
