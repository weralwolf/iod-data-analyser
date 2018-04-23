from os.path import join, abspath, dirname, realpath

BASE_DIR = join(realpath(dirname(__file__)), '..')
ARTEFACTS_DIR = join(BASE_DIR, '_artifacts')
CACHE_DIR = join(ARTEFACTS_DIR, 'objects')
TRACKS_DIR = join(ARTEFACTS_DIR, 'tracks')

DE2_DATA_DIR = abspath(join(BASE_DIR, '..', 'de2'))
DE2_NACS_DIR = join(DE2_DATA_DIR, 'neutral_gas_nacs', 'n_T_1s_ascii', 'data')
DE2_WATS_DIR = join(DE2_DATA_DIR, 'neutral_gas_wats', 'n_T_v_2s_ascii')
NFFT = 2**16
