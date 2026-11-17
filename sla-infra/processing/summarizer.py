# processing/summarizer.py

import pandas as pd
from typing import List, Dict

def summarize_window(records: List[Dict], window: str) -> Dict[str, float]:
    """
    Compute mean per KPI over the last `window` (e.g. "1h", "1d").
    records: [ {"kpi": "...", "value": ..., "ts": ...}, ... ]
    """
    if not records:
        return {}

    df = pd.DataFrame(records)
    df['ts'] = pd.to_datetime(df['ts'], unit='ms')
    df.set_index('ts', inplace=True)

    agg = df.groupby('kpi')['value'].resample(window).mean()
    last = agg.groupby('kpi').last()
    return last.to_dict()

