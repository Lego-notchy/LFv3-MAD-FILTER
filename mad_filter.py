import pandas as pd
import numpy as np
import logging

# Configure local logging for standalone use
logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)

def apply_robust_mad_filter(df: pd.DataFrame, threshold: float = 10.0) -> pd.DataFrame:
    """
    Robust MAD (Median Absolute Deviation) Filter.
    
    Identifies and masks exchange glitches and anomalous spikes that standard 
    standard-deviation filters (Sigma) often miss due to mean-distortion.
    
    Args:
        df: Pandas DataFrame containing 'ticker' and 'close' columns.
        threshold: The number of MADs away from the median to trigger masking.
        
    Returns:
        DataFrame with anomalous 'close' prices replaced by NaN.
    """
    # 1. Calculate median price per ticker (Robust Central Tendency)
    medians = df.groupby('ticker')['close'].transform('median')
    
    # 2. Calculate absolute deviation from the median
    deviation = (df['close'] - medians).abs()
    
    # 3. Calculate the MAD (Median Absolute Deviation) per ticker
    # We apply the MAD formula: median(|x_i - median(x)|)
    mad = deviation.groupby(df['ticker']).transform('median')
    
    # 4. Generate the Anomaly Mask
    # Constraint: we must shield penny stocks where MAD might be exactly 0
    # to avoid division-by-zero or infinite masking.
    anomaly_mask = (deviation > (threshold * mad)) & (mad > 0)
    
    anomalies_count = anomaly_mask.sum()
    if anomalies_count > 0:
        logger.warning(f"[MAD FILTER] Detected {anomalies_count} anomalies. Masking to NaN.")
    
    # 5. Apply masking
    df_cleaned = df.copy()
    df_cleaned.loc[anomaly_mask, 'close'] = np.nan
    
    return df_cleaned

if __name__ == "__main__":
    # Internal Unit Test for Standalone PoC
    print("Self-Testing MAD Filter...")
    data = {
        'ticker': ['AAPL'] * 10,
        'close': [150, 151, 150, 152, 1100, 151, 150, 152, 151, 150] # 1100 is a clear glitch
    }
    df_test = pd.DataFrame(data)
    df_result = apply_robust_mad_filter(df_test)
    
    assert pd.isna(df_result.loc[4, 'close']), "MAD Filter failed to mask the glitch!"
    print("SUCCESS: Standalone MAD Filter functional.")
