# NextCure Intelligence System v0.8.5

Peer Landscape + ADC Regime clarity patch on top of v0.8.4.

## What changed

- Reworked Peer Landscape into a clearer CEO-facing section.
- Added a short plain-English explanation above the peer chart.
- Replaced the ambiguous single 5D peer chart with a 5D / 30D / 90D timeframe comparison chart.
- Added peer summary cards for NXTC, strongest 5D peer, strongest 90D peer, and weakest 5D peer.
- Moved the raw peer table behind a granular detail expander.
- Fixed Strategy & Timing ADC Regime so it extrapolates from capital-flow posture instead of showing `Unavailable` when channel data exists.
- Added an ADC Regime Explanation insight that describes what the regime means and why.

## Run

```bash
pip install -r requirements.txt
streamlit run app.py
```
