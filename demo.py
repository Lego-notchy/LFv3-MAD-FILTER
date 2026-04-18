import pandas as pd
import numpy as np
from mad_filter import apply_robust_mad_filter

def generate_glitchy_data():
    """Generates synthetic stock data with various anomaly types."""
    np.random.seed(42)
    rows = 100
    base_price = 200
    
    # 1. Normal Random Walk
    prices = base_price + np.cumsum(np.random.randn(rows))
    
    # 2. Inject Anomaly: The "Fat Finger" / Exchange Glitch
    prices[25] = 1500.0  # Massive spike
    prices[50] = 5.0     # Flash crash
    prices[75] = 900.0   # Secondary spike
    
    df = pd.DataFrame({
        'ticker': ['SVRN'] * rows,
        'close': prices
    })
    return df

def run_demo():
    print("="*60)
    print(" SOVEREIGN MESH: MAD FILTER PROOF OF CONCEPT ".center(60, "#"))
    print("="*60)
    
    df = generate_glitchy_data()
    
    print("\n[STEP 1] Raw Data Ingested. Searching for anomalies...")
    # We use a threshold of 10 MADs (standard for high-resilience systems)
    df_cleaned = apply_robust_mad_filter(df, threshold=10)
    
    # Identify what was caught
    anomalies = df[df_cleaned['close'].isna()]
    
    print("\n" + "-"*60)
    print(" DETECTED ANOMALIES ".center(60))
    print("-"*60)
    if not anomalies.empty:
        for idx, row in anomalies.iterrows():
            print(f"Index {idx:2} | Price: ${row['close']:8.2f} | Status: [MASKED]")
    else:
        print("No anomalies detected.")
        
    print("-"*60)
    print(f"Operational Result: {len(anomalies)} glitches neutralized.")
    print("="*60)

if __name__ == "__main__":
    run_demo()
