# Proof of Concept: Robust MAD Filter

This directory contains a standalone extraction of the **Median Absolute Deviation (MAD)** outlier filter from the LogicFortress v3 execution engine.

## Rationale: Robust Statistics for Finance
Standard outlier detection often uses **Standard Deviation (Sigma)**. However, in financial data:
1.  **Mean Distortion**: A single massive exchange glitch (e.g., a "Fat Finger" trade) can shift the mean significantly, making it harder for Sigma-based filters to detect subsequent anomalies.
2.  **Robustness**: The **Median** is a robust statistic. It is insensitive to outliers. By using the Median of Deviations (MAD), we establish a "stable floor" for pricing that isn't buckled by temporary market chaos.

## Implementation Details
- **Formula**: `deviation = |x - median(x)|`, `MAD = median(deviation)`
- **Penny Stock Shield**: Included logic to handle cases where `MAD = 0`, preventing "all-or-nothing" filtering on frozen/low-float assets.

## How to Run the Demo
Ensure you have `pandas` and `numpy` installed in your environment.

```bash
python demo.py
```

## Institutional Context
In the full **LogicFortress v3** system, this filter sits at **Layer 1 (The Price Lake)**, ensuring that machine learning models and execution algorithms never "see" exchange glitches as valid price markers.
