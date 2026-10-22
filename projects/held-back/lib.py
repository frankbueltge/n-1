"""Project 15: shared reading of the coded file. The file is never committed; its path and hash are."""
import hashlib, os
import pandas as pd

PATH = os.environ.get('HELD_BACK_DTA', '/tmp/claude-0/-home-user-n-1/fc2cde3e-6a77-59a1-af4d-cbfbcd3e8cb5/scratchpad/zso.dta')
SHA256 = 'eb5458352ee99b50ae00ecf7ffaadcf5cdae191d6bd900b3a6038db2114e618e'
COLS = ['country', 'cow_id', 'treaty_id', 'rat_yr', 'article', 'para', 'provision_id', 'art_function',
        'reservation', 'declaration', 'resdec_yr', 'withdrawal', 'withdrawal_res', 'wdraw_yr']


def load():
    h = hashlib.sha256(open(PATH, 'rb').read()).hexdigest()
    assert h == SHA256, h
    with pd.io.stata.StataReader(PATH) as r:
        labels = r.value_labels()
    df = pd.read_stata(PATH, columns=COLS, convert_categoricals=False)
    df.attrs['rows_without_treaty'] = int(df['treaty_id'].isna().sum())
    df = df[df['treaty_id'].notna()].copy()
    df['treaty'] = df['treaty_id'].map(lambda t: labels['treaty_id'][t].split('. ', 1)[1])
    df['rat_yr'] = df['rat_yr'].dt.year.astype('float64')  # stored as a Stata date; only its year is used
    df['held'] = (df['reservation'] == 1) | (df['declaration'] == 1)
    return df, labels
