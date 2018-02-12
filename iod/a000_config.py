from os.path import abspath
from os.path import dirname
from os.path import join
from os.path import realpath

DE2_DATA_DIR = abspath(join(dirname(__file__), '..', '..', 'de2'))
DE2_NACS_DIR = join(DE2_DATA_DIR, 'neutral_gas_nacs', 'n_T_1s_ascii', 'data')
DE2_WATS_DIR = join(DE2_DATA_DIR, 'neutral_gas_wats', 'n_T_v_2s_ascii')
NFFT = 2**16
