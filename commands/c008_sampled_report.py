import json
from os import makedirs
from os.path import join
from datetime import datetime

from ionospheredata.settings import ARTIFACTS_DIR

"""
Task.
Generate report on sampled data. Required pages:
1. Title page with description, general sampling information and table with all samplings;
2. Page per segment;
"""

REPORT_DIR = join(ARTIFACTS_DIR, 'sampling_report')
SAMPLINGS_DIR = join(ARTIFACTS_DIR, 'samplings')
makedirs(REPORT_DIR, exist_ok=True)

index_tpl = """<!DOCTYPE html>
<html>
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
        <title>DE-2 data processing. Data filtration and tracks depiction</title>
        <!-- Latest compiled and minified CSS -->
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css"
        integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
        <link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.0.12/css/all.css"
        integrity="sha384-G0fIWCsCzJIMAVNQPfjH08cyYaUtMwjJwqiRKxxE/rx96Uroj1BtIQ6MLJuheaO9" crossorigin="anonymous">
    </head>
    <body>
      <div class="container-fluid">
        <div width="100%" class="processing-description">
            {processing_description}
        </div>
        <div width="100%" class="samplings-table">
            <h3>
                <a  name="samplings-navigation"></a>
                Samplings quick access
            </h3>
            <div>{sampling_links}</div>
            <table class="table table-sm table-hover">
                {processing_table}
            </table>
        </div>
      </div>
    <body>
</html>
"""

processing_description = """
<h1>Incentive</h1>
<p>
    Processing DE2 data is tedious for many reasons. Some data files are confusing or just contain data we can not trust
    these we filtered on the previous stages. But other thing is that data is unevenly spaces which makes it hard to
    process with convenient digital signal processing algorithms.
</p>
<p>
    There's a number of publications related to DSP of unevenly spaced data which can be used in such situations to
    extract maximum precision on very long segments of data. But there's no convenient libraries to perform this
    analysis quickly as this methodologies are quite new and still require a lot of work. Here's some worth to be
    mentioned:
    <ol>
        <li><a href='http://www.eckner.com/papers/unevenly_spaced_time_series_analysis.pdf'>
            A Framework for the Analysis of Unevenly Spaced Time Series Data.
        </a></li>
        <li><a href='https://www.nonlin-processes-geophys.net/18/389/2011/npg-18-389-2011.pdf'>
            Comparison of correlation analysis techniques for irregularly sampled time series.
        </a></li>
        <li><a href='http://eckner.com/papers/Algorithms%20for%20Unevenly%20Spaced%20Time%20Series.pdf'>
            Algorithms for Unevenly Spaced Time Series: Moving Averages and Other Rolling Operators.
        </a></li>
        <li><a href='http://www.ipgp.fr/~tarantola/Files/Professional/Papers_PDF/GeneralizedNonlinear_original.pdf'>
            Generalized nonlinear inverse problems solved using the least squares criterion.
        </a></li>
        <li><a href='http://adsbit.harvard.edu/cgi-bin/nph-iarticle_query?1979AJ.....84..116M&defaultprint=YES&filetype=.pdf'>
            Fourier transforms of data sampled in unequally spaced segments.
        </a></li>
        <li><a href='http://eckner.com/papers/Trend%20and%20Seasonality%20Estimation%20for%20Unevenly%20Spaced%20Time%20Series.pdf'>
            A Note on Trend and Seasonality Estimation for Unevenly Spaced Time Series.
        </a></li>
    </ol>
</p>
<h1>Small idea on a big scale</h1>
<p>
    Here is used different approach. One which is simpler and can faster give us information for analysis.
    Iterating through samplings from 2 seconds to 198 seconds (~1700 km) data sliced into continuous segments for a
    fixed sampling. Each of this segments I was looking for evenly spaced series of data where intermediate data
    points are dropped giving us evenly spaced time series suitable for classical DSP algorithms like FFT and moving
    average. Among all possible fittings ones producing the longest time series were selected.
</p>
<p>Procedure can be described within following steps:
    <ol>
        <li>
            Slice entire "good" data [specified in a <a href='http://weralwolf.com/masters/'>previous report</a>]
            into segments without gapes bigger than fixed sampling;
        </li>
        <li>Drop segments shorter than 200 * sqrt(sampling) as too short to care about at this stage;</li>
        <li>
            Find all possible fittings of evenly spaced series in boundaries of each segment and
            select one produced longest time series;
        </li>
        <li>
            Calculate moving averages of selected time series [since data have gaps even for continuous series
            by UT moving averages were computed on continuous pieces];
        </li>
        <li>Subtract averages from data obtaining density oscillations for O, N, N<sub>2</sub>, He, Ar;</li>
        <li>Apply ideal spectral filtering on [2500 km, 100 km]</li>
        <li>Extract trend from filtered frequencies, low frequencies space, and high for noise.</li>
    </ol>
</p>
<h2>Number of tracks and their total duration</h2>
<img src='../c6.segments_stats.png' width='100%' />
<h2>Additional notes</h2>
<p>
    <ol>
        <li>Time series are continuous against UT;</li>
        <li>Moving average computed for continuous data segments;</li>
        <li>To simplify generalized computing of FFTs absent data were filled up with zeros (marked red);</li>
    </ol>
</p>
"""

page_tpl = """<!DOCTYPE html>
<html>
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
        <title>DE-2 data processing. Data filtration and tracks depiction</title>
        <!-- Latest compiled and minified CSS -->
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css"
        integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
        <link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.0.12/css/all.css"
        integrity="sha384-G0fIWCsCzJIMAVNQPfjH08cyYaUtMwjJwqiRKxxE/rx96Uroj1BtIQ6MLJuheaO9" crossorigin="anonymous">
    </head>
    <body>
      <div class="container-fluid">
        <h1>{start_date} - {end_date}</h1>
        <h2>
            <a href="../samplings/{sampling:0>3}/{datafile}"><i class="fas fa-cart-arrow-down"></i></a>
            Sampling: {sampling} sec / Points no.: {points} / Duration: {duration:.2f} sec
        </h2>
        <!--
        # <div>
        #     <h3>Segment data</h3>
        #     <img src="../samplings/{sampling:0>3}/{alldata}" width="100%" />
        # </div>
        -->
        <div>
            <h3>O density</h3>
            <img src="../samplings/{sampling:0>3}/{o_trend}" width="100%" />
            <img src="../samplings/{sampling:0>3}/{o_wave}" width="100%" />
        </div>
        <!--
        # <div>
        #     <h3>N density</h3>
        #     <img src="../samplings/{sampling:0>3}/{n_trend}" width="100%" />
        #     <img src="../samplings/{sampling:0>3}/{n_wave}" width="100%" />
        # </div>
        # <div>
        #     <h3>N<sub>2</sub> density</h3>
        #     <img src="../samplings/{sampling:0>3}/{n2_trend}" width="100%" />
        #     <img src="../samplings/{sampling:0>3}/{n2_wave}" width="100%" />
        # </div>
        # <div>
        #     <h3>He density</h3>
        #     <img src="../samplings/{sampling:0>3}/{he_trend}" width="100%" />
        #     <img src="../samplings/{sampling:0>3}/{he_wave}" width="100%" />
        # </div>
        # <div>
        #     <h3>Ar density</h3>
        #     <img src="../samplings/{sampling:0>3}/{ar_trend}" width="100%" />
        #     <img src="../samplings/{sampling:0>3}/{ar_wave}" width="100%" />
        # </div>
        -->
      </div>
    <body>
</html>"""


def main():
    table_data = ''
    general_header = """<tr>
    <th>Details</th>
    <th scope="col">#</th>
    <th scope="col">Data</th>
    <th scope="col">Start</th>
    <th scope="col">End</th>
    <th scope="col">Duration, (s)</th>
    <th scope="col">N</th>
    </tr>"""
    sampling_links = []
    for sampling in [1]:  # range(1, 199):
        table_data += """<thead class="thead-dark">
        <tr><th scope="col" colspan="7">
        <h3>
            <a name="sampling-{sampling}"></a>
            <a href="#samplings-navigation"><i class="fas fa-arrow-up"></i></a>
            Segments for sampling {sampling} seconds
        </h3>
        </th></tr>
        {general_header}
        </thead>""".format(
            sampling=sampling,
            general_header=general_header,
        )
        sampling_links.append('<a href="#sampling-{sampling}">{sampling}</a>'.format(sampling=sampling))
        sampling_dir = join(SAMPLINGS_DIR, '{:0>3}'.format(sampling))
        segments_data = sorted(json.load(open(join(sampling_dir, '000_list.json'))), key=lambda x: x['segment'][0])
        table_data += '<tbody>'

        for ne, segment in enumerate(segments_data):
            if 'filename' not in segment:
                continue

            datafile_name = segment['filename'][:-3]
            page_params = dict(
                ar_trend=datafile_name + 'ar density.trend.png',
                ar_wave=datafile_name + 'ar density.wave.png',
                he_trend=datafile_name + 'he density.trend.png',
                he_wave=datafile_name + 'he density.wave.png',
                n_trend=datafile_name + 'n density.trend.png',
                n_wave=datafile_name + 'n density.wave.png',
                n2_trend=datafile_name + 'n2 density.trend.png',
                n2_wave=datafile_name + 'n2 density.wave.png',
                o_trend=datafile_name + 'o density.trend.png',
                o_wave=datafile_name + 'o density.wave.png',
                alldata=datafile_name + 'png',
                sampling=sampling,
                datafile=segment['filename'],
                start_date=datetime.fromtimestamp(segment['segment'][0]).strftime('%Y.%j at %H:%M:%S'),
                end_date=datetime.fromtimestamp(segment['segment'][1]).strftime('%Y.%j at %H:%M:%S'),
                duration=segment['duration'],
                points=segment['points'],
            )

            report_page_name = '{sampling:0>3}_{datafile}html'.format(
                sampling=sampling,
                datafile=datafile_name,
            )
            table_data += """<tr>
            <td scope="row">{global_index}</td>
            <td><a href="{report_page_name}"><i class="fas fa-camera"></i></a></td>
            <td><a href="../samplings/{sampling:0>3}/{datafile}"><i class="fas fa-cart-arrow-down"></i></a></td>
            <td>{start_date}</th><th>{end_date}</th><th>{duration:.0f}</th><th>{points}</td>
            </tr>""".format(
                report_page_name=report_page_name,
                global_index='{:0>3}.{:0>3}'.format(sampling, ne),
                **page_params,
            )

            with open(join(REPORT_DIR, report_page_name), 'w') as report_page:
                report_page.write(page_tpl.format(**page_params))

        table_data += '</tbody>'

    with open(join(REPORT_DIR, 'index.html'), 'w') as report_index:
        report_index.write(index_tpl.format(
            processing_description=processing_description,
            processing_table=table_data,
            sampling_links=', '.join(sampling_links),
        ))


if __name__ == '__main__':
    main()
