# Project 1L Research Source Library

## 1. Purpose

## 2. Source Categories
- trader notes
- playbooks
- research papers
- forum threads
- open-source repos
- platform strategy writeups
- friend / external trader ideas
- discretionary observations

## 3. Candidate Family Intake Template
- family name
- source
- market logic
- why it might exist
- required data
- likely best condition
- likely failure mode
- implementation difficulty
- whether it deserves a pre-code evidence memo

## 4. Current Priority Queue

### 1. Time-of-Day Mean Reversion (Lunch Lull Fade)
- **family name:** lunch_break_reversion
- **source:** QuantConnect Algorithm.Python (MeanReversionLunchBreakAlpha)
- **source url:** https://github.com/QuantConnect/Lean/blob/master/Algorithm.Python/Alphas/MeanReversionLunchBreakAlpha.py
- **market logic:** The directional price momentum established from the prior close into the NY lunch hour (12:00 PM) frequently exhausts and reverses as volume drops off.
- **instrument style:** ETFs / Equities
- **likely portable to Project 1L:** Yes, intimately fits MES/MNQ session volume profiles.
- **required data complexity:** Very low. Requires only simple time-bound boundaries and price momentum measurements.
- **status:** parent-family candidate
- **note:** Provides a direct, mechanically isolated test of the "lunch time reversal" trading floor adage.

### 3. Share Class Spread Reversion
- **family name:** share_class_reversion
- **source:** QuantConnect Algorithm.Python (ShareClassMeanReversionAlpha)
- **source url:** https://github.com/QuantConnect/Lean/blob/master/Algorithm.Python/Alphas/ShareClassMeanReversionAlpha.py
- **market logic:** Two highly correlated assets (e.g., VIA and VIAB share classes) generally trade at a stable premium/discount. If this spread deviates strongly from a short-term moving average, the lagging asset is bought and the leading is shorted until the spread normalizes.
- **instrument style:** Equities / Pairs
- **likely portable to Project 1L:** Yes, heavily leverages the newly minted MES/MNQ context-engine extension.
- **required data complexity:** Low (requires synchronized bars and a moving average of the spread difference).
- **status:** child-branch idea / useful context
- **note:** Provides a concrete implementation roadmap for exactly how to size and trigger pairs utilizing our new `context_family` engine upgrade.

### 4. QC-001 — spread_residual_cointegration
- **family name:** spread_residual_cointegration
- **source:** QuantConnect research tutorial based on George J. Miao
- **source url:** https://www.quantconnect.com/research/15347/intraday-dynamic-pairs-trading-using-correlation-and-cointegration-approach/
- **source quality:** medium
- **horizon:** intraday / short-horizon spread trading
- **market logic:** identify close substitutes, estimate a stationary spread residual, trade extreme residual deviations back toward equilibrium
- **why it might exist:** close substitute relationships can temporarily dislocate under stress, liquidity shocks, or short-term imbalance, then mean-revert
- **required data:** synchronized two-instrument bars, rolling formation window, residual/z-score tracking, contract-roll handling if futures
- **likely best condition:** stable substitute relationships, liquid instruments, stressed but orderly tape
- **likely failure mode:** relationship instability, regime shift, roll/carry distortion, fees/slippage overwhelming small edge
- **implementation difficulty:** medium-high
- **transfer risk to Project 1L:** medium-high
- **memo_gate:** YES
- **current status:** rejected after Dev-A (MES/MNQ pilot)
- **note:** Pilot parent `mes_mnq_relative_value_spread_v1` ran Dev-A (EXP-20260310-005, PF 0.75, −$308.25, 47 trades). No raw life. Fixed 1:1 ratio produced beta leakage rather than relative-value isolation — avg loser (−$76) exceeded avg winner (+$64.89). No child branching, no ratio tuning, no rescue optimization. The QC-001 lane is parked; paired-spread infrastructure (two-leg accounting, execution audit, engine Outcome B timing) is preserved for future qualifying families. Return to source-library screening before opening a new spread family.

### 5. AST-001 — time_series_momentum
- **family name:** time_series_momentum
- **source:** awesome-systematic-trading (Paper: Time Series Momentum Effect)
- **market logic:** An asset's own past returns over a 1-12 month horizon historically predict its future performance directionally, independently of spatial cross-sectional momentum.
- **why it might exist:** Initial under-reaction to news followed by herd behavior and slow-moving capital flows that sustain trends.
- **likely instruments:** Equities, Futures, Commodities, Bonds
- **implementation difficulty:** Low
- **memo_gate:** YES

### 6. AST-002 — asset_growth_anomaly
- **family name:** asset_growth_anomaly
- **source:** awesome-systematic-trading (Paper: Asset Growth Effect)
- **market logic:** Companies that rapidly grow their total assets (via expansion, acquisitions, etc.) tend to severely underperform in the following periods compared to companies with low asset growth.
- **why it might exist:** Managerial empire-building, misallocation of capital, and investor over-extrapolation of past success ignoring diminished returns on new capital.
- **likely instruments:** Equities
- **implementation difficulty:** Medium (requires robust quarterly fundamental data)
- **memo_gate:** YES

### 7. AST-003 — earnings_reversal_fade
- **family name:** earnings_reversal_fade
- **source:** awesome-systematic-trading (Paper: Reversal During Earnings-Announcements)
- **market logic:** Stocks exhibiting the strongest recent price momentum (winners) frequently experience a sharp, short-term price reversal precisely during their earnings announcement windows.
- **why it might exist:** Momentum traders locking in profits, "buy the rumor, sell the news" behavior, and liquidity provision dynamics around known volatility events.
- **likely instruments:** Equities
- **implementation difficulty:** Medium (requires an earnings calendar data overlay)
- **memo_gate:** YES

### 8. AST-004 — overnight_intraday_seasonality
- **family name:** overnight_intraday_seasonality
- **source:** awesome-systematic-trading (Paper: Overnight Seasonality in Bitcoin / Market Sentiment Overnight Anomaly)
- **market logic:** The holding-period returns occurring strictly overnight (close to open) exhibit systematic, predictable divergence from the daytime (open to close) returns, varying by sentiment regime or day of the week.
- **why it might exist:** Institutional rebalancing happens intraday while retail trading drives the overnight/open; illiquidity in overnight markets magnifies structural flows.
- **likely instruments:** Index Futures (MES/MNQ), Cryptocurrencies
- **implementation difficulty:** Low
- **memo_gate:** YES

### 9. AST-005 — turn_of_the_month_effect
- **family name:** turn_of_the_month_effect
- **source:** awesome-systematic-trading (Paper: Turn of the Month in Equity Indexes)
- **market logic:** Equity indexes consistently generate a disproportionate amount of their total annual return during the specific window surrounding the turn of the month (e.g., last day of the month through the first three days of the new month).
- **why it might exist:** Institutional month-end window dressing, systematic salary distributions entering retirement accounts naturally bidding up the broad market.
- **likely instruments:** Equity Index Futures (MES)
- **implementation difficulty:** Very Low
- **memo_gate:** YES

### 10. AST-006 — country_etf_pairs
- **family name:** country_etf_pairs
- **source:** awesome-systematic-trading (Paper: Pairs Trading with Country ETFs)
- **market logic:** Broad macroeconomic relationships keep the equity indices of highly connected economies tracking together. When performance significantly diverges, shorting the outperforming country and buying the underperforming country captures the reversion to the mean.
- **why it might exist:** Global capital flows temporarily overreact to localized noise, but interlinked underlying supply chains and trade balances force long-term convergence.
- **likely instruments:** Country ETFs or global equity index futures
- **implementation difficulty:** Medium-High (requires multi-leg pairs engine)
- **memo_gate:** YES

### 11. AST-007 — vol_adjusted_momentum
- **family name:** vol_adjusted_momentum
- **source:** awesome-systematic-trading (Paper: Momentum and Reversal Combined with Volatility Effect)
- **market logic:** Going long low-volatility momentum winners and shorting high-volatility momentum losers generates a massively improved risk-adjusted return over pure price momentum.
- **why it might exist:** High-volatility losers are experiencing panic and distress (making shorting them dangerous or crowded), while low-volatility winners reflect steady, quiet institutional accumulation.
- **likely instruments:** Equities
- **implementation difficulty:** Medium (requires rolling historical volatility calculation)
- **memo_gate:** YES

### 12. AST-008 — combined_fscore_reversal
- **family name:** combined_fscore_reversal
- **source:** awesome-systematic-trading (Paper: Combining Fundamental FSCORE and Equity Short-Term Reversals)
- **market logic:** Filtering short-term price reversal candidates by Piotroski F-Score (financial health) drastically improves the win-rate of the reversal. Buy financially strong companies (high F-score) that just took a short-term hit; short weak companies (low F-score) experiencing a short-term pump.
- **why it might exist:** Distinguishes between temporary liquidity-driven price drops (healthy company) and fundamental permanent impairment (weak company).
- **likely instruments:** Equities
- **implementation difficulty:** High (requires multi-variable financial statement data parsing)
- **memo_gate:** YES

## 4A. Parked Captures — Quantpedia Sweep 1

### QP-001 — wti_brent_spread_reversion
- **family name:** wti_brent_spread_reversion
- **source:** Quantpedia strategy summary
- **source url:** https://quantpedia.com/strategies/trading-wti-brent-spread
- **source quality:** medium
- **horizon:** short- to medium-horizon futures spread trading
- **market logic:** trade dislocations in the WTI/Brent crude spread when the relationship deviates meaningfully from a modeled fair-value / residual estimate and then mean-reverts
- **why it might exist:** close substitute crude benchmarks can temporarily dislocate because of localized flow, contract-specific pressure, storage/transport effects, or temporary imbalance, then partially reconverge
- **required data:** synchronized two-leg futures bars, spread construction, model/residual tracking, contract-roll handling, spread-aware costs
- **likely best condition:** liquid overlapping sessions, stable substitute relationship, orderly but stressed tape
- **likely failure mode:** structural spread regime shift, roll distortion, persistent fundamental divergence, cost drag
- **implementation difficulty:** medium-high
- **transfer risk to Project 1L:** medium-high
- **memo_gate:** YES
- **current status:** parked parent-family candidate
- **note:** important because it is a second real paired-futures family; helps test whether spread infrastructure would have reusable value beyond QC-001

### QP-002 — commodity_term_structure_momentum
- **family name:** commodity_term_structure_momentum
- **source:** Quantpedia strategy summary
- **source url:** https://quantpedia.com/strategies/term-structure-effect-in-commodities
- **source quality:** medium
- **horizon:** medium-horizon commodity futures allocation / ranking
- **market logic:** combine momentum and term-structure signals in commodity futures and favor contracts/segments where both signals align
- **why it might exist:** momentum and carry/term-structure can capture different but complementary information about trend persistence, inventory pressure, and risk premia
- **required data:** commodity futures chain data, continuous-contract construction, term-structure/basis estimation, portfolio ranking logic
- **likely best condition:** broad diversified commodity universe, stable roll construction, persistent cross-sectional dispersion
- **likely failure mode:** weak signal alignment, roll/noise contamination, crowded factor exposure, turnover drag
- **implementation difficulty:** medium
- **transfer risk to Project 1L:** medium
- **memo_gate:** YES
- **current status:** parked parent-family candidate
- **note:** attractive because it is futures-native and does not require immediate paired-leg execution infrastructure

### QP-003 — commodity_factor_crowding_overlay
- **family name:** commodity_factor_crowding_overlay
- **source:** Quantpedia research blog summary
- **source url:** https://quantpedia.com/crowding-in-commodity-factor-strategies/
- **source quality:** medium
- **horizon:** medium-horizon regime / overlay filter
- **market logic:** use crowding measures derived from commodity futures positioning to reduce or avoid exposure when factor trades are crowded and expected returns are weaker
- **why it might exist:** crowded trades compress future returns and increase unwind risk; low-crowding periods may preserve more of the factor premium
- **required data:** CFTC positioning data, factor/strategy crowding estimation, overlay logic tied to an existing commodity factor family
- **likely best condition:** factor strategies with measurable crowding cycles and sufficient lag-tolerant holding periods
- **likely failure mode:** crowding proxy instability, publication decay, timing lag, data complexity overwhelming practical benefit
- **implementation difficulty:** medium-high
- **transfer risk to Project 1L:** high
- **memo_gate:** NO
- **current status:** research-only overlay candidate
- **note:** keep as a future overlay/filter concept rather than a standalone first-wave strategy family

### QP-004 — fx_futures_basket_mean_reversion
- **family name:** fx_futures_basket_mean_reversion
- **source:** Quantpedia own-research article
- **source url:** https://quantpedia.com/how-to-build-mean-reversion-strategies-in-currencies/
- **source quality:** medium
- **horizon:** monthly / broad-horizon cross-sectional mean reversion
- **market logic:** measure deviation of each FX futures contract from a basket mean, then long undervalued contracts and short overvalued contracts on a recurring rebalance
- **why it might exist:** currency relationships can overshoot around carry, macro positioning, and short-term sentiment, then partially revert toward basket-relative equilibrium
- **required data:** continuous FX futures series, basket construction, deviation scoring, monthly rebalance logic, long/short portfolio handling
- **likely best condition:** diversified currency basket, stable futures carry representation, moderate cross-sectional dispersion
- **likely failure mode:** persistent macro trends overpowering reversion, basket-definition instability, portfolio crowding, carry/trend interaction
- **implementation difficulty:** medium
- **transfer risk to Project 1L:** medium-high
- **memo_gate:** YES
- **current status:** parked parent-family candidate
- **note:** broad-horizon rather than near-term intraday work, but worth saving now because Project 1L is no longer limiting source capture to intraday only

### QP-005 — futures_time_series_momentum
- **family name:** futures_time_series_momentum
- **source:** Quantpedia strategy summary
- **source url:** https://quantpedia.com/strategies/time-series-momentum-effect
- **source quality:** medium
- **horizon:** medium- to long-horizon trend-following
- **market logic:** each futures contract’s own past excess return predicts its future return; trade the sign/persistence of that contract’s trend rather than ranking it against peers
- **why it might exist:** behavioral under-reaction and delayed over-reaction can create serial return persistence across futures markets
- **required data:** continuous futures series, excess-return calculation, volatility/risk scaling, monthly rebalance logic, multi-market portfolio handling
- **likely best condition:** diversified futures universe with persistent medium-horizon trends and robust risk scaling
- **likely failure mode:** sharp trend reversals, sideways regimes, crowding, portfolio construction errors, transaction-cost drag
- **implementation difficulty:** medium
- **transfer risk to Project 1L:** medium
- **memo_gate:** NO
- **current status:** anchor library family / benchmark reference
- **note:** this is a major canonical family that belongs in the library even if it is not an immediate memo candidate

## 4B. Parked Captures — SSRN/RePEc Sweep 1

### SSRN-001 — hedging_demand_intraday_momentum
- **family name:** hedging_demand_intraday_momentum
- **source:** SSRN (Hedging demand and market intraday momentum)
- **source url:** https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3841051 (approx)
- **source quality:** high
- **horizon:** intraday
- **market logic:** The return during the last 30 minutes before the market close is positively predicted by the return during the rest of the day, driven by gamma hedging demands of options market makers and leveraged ETFs.
- **why it might exist:** Structural hedging needs force market participants to execute in the direction of the daily trend near the close.
- **required data:** Intraday continuous futures data (1-min or 5-min).
- **likely instruments:** Equity index futures (ES/NQ)
- **likely best condition:** High option open interest, high market volatility, strong directional trend prior to the final hour.
- **likely failure mode:** Low volatility days, regime shifts in ETF flows.
- **implementation difficulty:** low
- **transfer risk to Project 1L:** low
- **memo_gate:** YES
- **current status:** rejected after Dev-A
- **note:** Parent implemented and tested on MES 1m bars (Dev-A window 2023-02-26 to 2023-08-31). Failed: 36 trades, 36.1% win rate, profit factor 0.43, avg winner $22 vs avg loser -$30. No raw life; no rescue optimization or child branching justified.

### SSRN-002 — vix_spx_cross_market_lead_lag
- **family name:** vix_spx_cross_market_lead_lag
- **source:** SSRN / RePEc (Cross-Market Trading and the Lead-Lag Relationship Between VIX and SPX)
- **source url:** Search SSRN / RePEc
- **source quality:** high
- **horizon:** intraday / high-frequency
- **market logic:** VIX futures systematically lead SPX futures in price discovery, particularly when cross-market trading and hedging activities by VIX dealers are high.
- **why it might exist:** Dealers hedge VIX futures exposure in the highly liquid SPX futures market, causing the volatility derivative market to lead the underlying cash/index futures market.
- **required data:** Synchronized high-frequency (tick or 1-second) data for both VIX and SPX futures.
- **likely instruments:** VIX futures, ES futures
- **likely best condition:** High volatility regimes, active hedging periods.
- **likely failure mode:** Excessive transaction costs overwhelming the micro-alpha, latency disadvantage.
- **implementation difficulty:** high
- **transfer risk to Project 1L:** high
- **memo_gate:** NO
- **current status:** research-only overlay candidate
- **note:** Shows the value of the dual-instrument engine, though high-frequency execution may be out of scope for the current Project 1L replay engine.

### SSRN-003 — overnight_intraday_reversal
- **family name:** overnight_intraday_reversal
- **source:** SSRN (Overnight-Intraday Reversal Strategy)
- **source url:** Search SSRN
- **source quality:** high
- **horizon:** intraday
- **market logic:** Buy futures with low past overnight returns and sell futures with high past overnight returns, generating significant intraday excess returns that revert the overnight gap.
- **why it might exist:** Liquidity constraints and retail over-reaction during the illiquid overnight session are systematically reversed by institutional flow during the regular session.
- **required data:** Separate overnight (globex) vs regular trading hours (RTH) session data.
- **likely instruments:** Broad futures universe (equity, commodity, currency)
- **likely best condition:** High overnight gap variance.
- **likely failure mode:** Trend days where the overnight gap is fundamentally driven and continues intraday.
- **implementation difficulty:** low
- **transfer risk to Project 1L:** low
- **memo_gate:** YES
- **current status:** rejected after Dev-B
- **note:** Parent advanced through spec and Dev-A (EXP-20260310-001, PF 1.36, +$1,007.50), but failed out-of-sample Dev-B confirmation (EXP-20260310-002, PF 0.75, −$691.25). Win rate collapsed 37.2% → 26.7% out of sample. No promotion, no rescue optimization, no child branching. Cross-sectional-to-single-instrument transfer is the likely source of instability.

### SSRN-004 — structural_term_structure_seasonality
- **family name:** structural_term_structure_seasonality
- **source:** SSRN (Seasonality in Commodity Futures Term Structure)
- **source url:** Search SSRN
- **source quality:** medium
- **horizon:** multi-month / seasonal
- **market logic:** Agricultural and energy futures exhibit highly predictable seasonal oscillations in their term structure (e.g., backwardation before harvest/winter, contango after). Trading these predictable shape changes yields structural alpha.
- **why it might exist:** Physical supply/demand mismatches, storage costs, and convenience yields are tied to immutable weather/harvest cycles.
- **required data:** Full futures chain data, continuous roll logic, historical seasonal averages.
- **likely instruments:** Natural Gas, Wheat, Heating Oil
- **likely best condition:** Normal weather cycles, structural supply constraints.
- **likely failure mode:** Extreme weather anomalies, geopolitical supply shocks breaking the seasonal pattern.
- **implementation difficulty:** medium-high
- **transfer risk to Project 1L:** medium
- **memo_gate:** YES
- **current status:** parked parent-family candidate
- **note:** A classic structural risk premium trade; requires term-structure modeling infrastructure.

### SSRN-005 — high_frequency_cross_market_activity
- **family name:** high_frequency_cross_market_activity
- **source:** SSRN (High-Frequency Cross-Market Trading Activity: A Model-Free Approach)
- **source url:** Search SSRN
- **source quality:** medium
- **horizon:** intraday / high-frequency
- **market logic:** High-frequency cross-market activity measures (relative volume spikes between cash and futures) can sharply identify impending lead-lag relationships and regime shifts.
- **why it might exist:** Informed order flow fragments across related markets; tracking the relative intensity reveals where price discovery is currently initiating.
- **required data:** Synchronized tick/volume data across cash and futures pairs.
- **likely instruments:** Treasuries (Cash/Futures), ES (SPY/Futures), EUR/USD
- **likely best condition:** High volatility, fragmenting institutional flow.
- **likely failure mode:** Noise replacing signal, execution latency.
- **implementation difficulty:** high
- **transfer risk to Project 1L:** high
- **memo_gate:** NO
- **current status:** research-only overlay candidate
- **note:** Valuable as a volume-based regime filter rather than a standalone directional strategy.

### SSRN-006 — commodity_intraday_momentum_reversal
- **family name:** commodity_intraday_momentum_reversal
- **source:** SSRN (Intraday Reversal and Momentum in Chinese Commodity Futures)
- **source url:** Search SSRN
- **source quality:** medium
- **horizon:** intraday
- **market logic:** Commodity futures exhibit strong intraday momentum in the first half of the session followed by a distinct reversal in the second half, heavily influenced by option market maker hedging.
- **why it might exist:** Initial price discovery and trend establishment gives way to inventory unwinding and mean reversion as the day ends.
- **required data:** Intraday futures data, option open interest/implied volatility overlay.
- **likely instruments:** Liquid commodity futures (Gold, Copper, Crude)
- **likely best condition:** High option trading volume acting as the tail wagging the dog.
- **likely failure mode:** Pure trend days lacking late-day reversion.
- **implementation difficulty:** medium
- **transfer risk to Project 1L:** medium
- **memo_gate:** YES
- **current status:** parked parent-family candidate
- **note:** Highlights the necessity of incorporating option market mechanics into intraday futures strategies.

### SSRN-007 — order_flow_imbalance_momentum
- **family name:** order_flow_imbalance_momentum
- **source:** Academic Consensus / SSRN (Predictive power of order flow imbalance)
- **source url:** Search SSRN
- **source quality:** medium
- **horizon:** micro-horizon (minutes)
- **market logic:** A persistent imbalance between market buy orders and market sell orders (measured via footprint or tick data) linearly predicts directional price movement over the next immediate horizon.
- **why it might exist:** Market orders consume resting liquidity; persistent imbalance depletes the limit order book on one side, mechanically forcing price discovery to the next level.
- **required data:** Tick data with bid/ask volume split (Level 2 or footprint).
- **likely instruments:** ES, NQ, Treasuries
- **likely best condition:** Large-tick, thick limit order book instruments.
- **likely failure mode:** Spoofing, hidden liquidity absorbing the flow, rapid shifting of the imbalance.
- **implementation difficulty:** high
- **transfer risk to Project 1L:** high
- **memo_gate:** NO
- **current status:** reference archetype
- **note:** This is the theoretical endpoint for intraday momentum, but requires Level 2/Tick data which Project 1L cannot currently ingest.

### SSRN-008 — statistical_arbitrage_energy_pairs
- **family name:** statistical_arbitrage_energy_pairs
- **source:** SSRN (Pairs trading in futures markets)
- **source url:** Search SSRN
- **source quality:** high
- **horizon:** medium-horizon
- **market logic:** Applying cointegration and Filterbank CNNs to inter-commodity energy pairs to trade the spread (e.g., WTI/RBOB crack spread, or Heating Oil/Gasoline).
- **why it might exist:** Physical refining relationships and substitution effects bind energy prices together; temporary supply shocks create tradeable dislocations.
- **required data:** Multiple synchronized continuous futures contracts.
- **likely instruments:** Energy complex (CL, HO, RB, NG)
- **likely best condition:** Stable macroeconomic regimes with isolated local supply shocks.
- **likely failure mode:** Structural shifts in refining margins, systemic energy crises altering the cointegration vector.
- **implementation difficulty:** medium-high
- **transfer risk to Project 1L:** medium
- **memo_gate:** YES
- **current status:** parked parent-family candidate
- **note:** A more rigorously defined counterpart to the QP-001 WTI/Brent spread, utilizing advanced statistical bounds rather than simple moving averages.

## 4C. Parked Captures — arXiv Microstructure Sweep 1

### ARXIV-001 — order_flow_imbalance
- **family name:** order_flow_imbalance
- **source:** arXiv q-fin (Order Flow Imbalance in High-Frequency Trading)
- **source url:** Search arXiv q-fin
- **source quality:** high
- **horizon:** intraday / high-frequency
- **market logic:** The net difference between limit buy orders and limit sell orders (along with matching market orders) at the best bid/ask creates directional pressure that reliably predicts the next immediate price tick.
- **why it might exist:** Price moves are mechanically governed by the depletion of liquidity at the top of the book; OFI quantifies exactly this depletion before the price actually shifts.
- **required data:** Limit Order Book Top-of-Book stream (Level 1 with volume at bid/ask).
- **likely instruments:** Highly liquid, large-tick futures (Treasuries, ES).
- **likely best condition:** Thick static order books, distinct regime shifts in flow.
- **likely failure mode:** Spoofing distorting the imbalance, execution latency preventing capture of the micro-alpha.
- **implementation difficulty:** high
- **transfer risk to Project 1L:** high
- **memo_gate:** NO
- **current status:** reference archetype
- **note:** The canonical microstructure concept. Project 1L lacks Level 1/2 data natively, making this a pure reference architecture for future engine upgrades.

### ARXIV-002 — extreme_ofi_pinning
- **family name:** extreme_ofi_pinning
- **source:** arXiv q-fin (Extreme Order Flow Imbalance and Price Movements)
- **source url:** Search arXiv q-fin
- **source quality:** high
- **horizon:** intraday
- **market logic:** Strange microstructural reality: extreme absolute order flow imbalance does *not* linearly predict large price impact; instead, it often predicts price "pinning" where the market absorbs massive flow without breaking a level, until a sudden, delayed violent release.
- **why it might exist:** Large institutional limit orders ("icebergs") act as absolute walls, absorbing all incoming market orders and causing massive OFI without price movement, until exhausted.
- **required data:** High-frequency volume imbalance metrics.
- **likely instruments:** ES, NQ, Treasuries
- **likely best condition:** Key technical levels, high volume periods.
- **likely failure mode:** Misinterpreting the pinning duration, getting run over before the release.
- **implementation difficulty:** high
- **transfer risk to Project 1L:** high
- **memo_gate:** YES
- **current status:** parked parent-family candidate
- **note:** A contrarian take on standard OFI that might be synthesizable using 1-minute volume heuristics instead of raw Level 2 data.

### ARXIV-003 — lob_queue_imbalance_momentum
- **family name:** lob_queue_imbalance_momentum
- **source:** arXiv q-fin (Queue Imbalance as a One-Tick-Ahead Price Predictor in a Limit Order Book)
- **source url:** Search arXiv q-fin
- **source quality:** high
- **horizon:** micro-horizon (tick/seconds)
- **market logic:** The ratio of volume resting on the best bid versus the best ask predicts the literal next price tick direction with extremely high statistical significance.
- **why it might exist:** Direct mechanical necessity of order-driven matching engines.
- **required data:** Level 1 Top-of-Book stream.
- **likely instruments:** All order-driven futures.
- **likely best condition:** Orderly tape, non-toxic flow.
- **likely failure mode:** Execution slippage, toxic flow (adverse selection).
- **implementation difficulty:** high
- **transfer risk to Project 1L:** high
- **memo_gate:** NO
- **current status:** reference archetype
- **note:** Requires execution speeds and data granularity drastically beyond Project 1L's current scope.

### ARXIV-004 — vwap_micro_mean_reversion
- **family name:** vwap_micro_mean_reversion
- **source:** arXiv q-fin / Empirical Microstructure (VWAP Execution & Intraday Reversion)
- **source url:** Search arXiv q-fin
- **source quality:** medium
- **horizon:** intraday
- **market logic:** Intraday prices exhibit a reliable U-shaped volume curve. During the midday lull (low volume, narrow range), price strongly reverts back to the rolling VWAP after short, low-volume deviations.
- **why it might exist:** Institutional algorithms execute VWAP-pegged orders; when retail or noise traders push the price away from VWAP on low volume, the passive algorithmic bidding inevitably pulls it back.
- **required data:** Continuous 1-min or 5-min bars with volume.
- **likely instruments:** ES, NQ
- **likely best condition:** Midday session (11:30 AM - 1:30 PM EST), low VIX, non-trend days.
- **likely failure mode:** News shocks breaking the lull, structural trend days ignoring VWAP gravity.
- **implementation difficulty:** low
- **transfer risk to Project 1L:** low
- **memo_gate:** YES
- **current status:** parked parent-family candidate
- **note:** Highly relevant, immediately testable, and deeply futures-native.

### ARXIV-005 — multi_level_spoofing_imbalance
- **family name:** multi_level_spoofing_imbalance
- **source:** arXiv q-fin (Multi-level Imbalance and Spoofing)
- **source url:** Search arXiv q-fin
- **source quality:** medium
- **horizon:** intraday / high-frequency
- **market logic:** Look beyond the best bid/ask Level 1 to Level 3/4. Massive imbalances placed far from the touch are often "spoofing" orders meant to artificially move the mid-price without executing. Trade the expected *reversion* when the spoof is pulled.
- **why it might exist:** Manipulative liquidity illusion pushes HFT algos to jump the queue; once the fake liquidity vanishes, the price vacuum collapses.
- **required data:** Deep Limit Order Book data (Level 2/3).
- **likely instruments:** Historically susceptible futures (e.g., precious metals before regulation, thinly traded indices).
- **likely best condition:** Low latency, highly detailed order book reconstruction.
- **likely failure mode:** The order isn't a spoof and represents real toxic iceberg flow.
- **implementation difficulty:** high
- **transfer risk to Project 1L:** high
- **memo_gate:** NO
- **current status:** research-only overlay candidate
- **note:** Theoretically fascinating but impossible to trade without deep book data and extreme latency advantages.

### ARXIV-006 — non_synchronous_lead_lag
- **family name:** non_synchronous_lead_lag
- **source:** arXiv q-fin (Mining the lead-lag relationship from non-synchronous and high-frequency data)
- **source url:** Search arXiv q-fin
- **source quality:** high
- **horizon:** intraday / spread
- **market logic:** Extracting lead-lag parameters from noisy, non-synchronous tick data allows a trader to definitively map which instrument (or cash vs future) is initiating price discovery, and trade the lagging instrument correspondingly.
- **why it might exist:** Information enters one market slightly faster due to liquidity, dominant participant location, or asset class structure, dragging correlated assets along milliseconds/seconds later.
- **required data:** High-frequency non-synchronous tick data, robust cross-correlation engines.
- **likely instruments:** Index Futures vs Cash ETFs, Cross-currency futures, VIX/SPX.
- **likely best condition:** High volume, clear information asymmetry.
- **likely failure mode:** Regime shifts where the leader suddenly becomes the laggard.
- **implementation difficulty:** high
- **transfer risk to Project 1L:** medium-high
- **memo_gate:** YES
- **current status:** parked parent-family candidate
- **note:** The engine's matched-timestamp rule explicitly prevents this trade; this capture proves the necessity of a purely asynchronous engine extension for future lead-lag work.

### ARXIV-007 — exogenous_shock_order_flow
- **family name:** exogenous_shock_order_flow
- **source:** arXiv q-fin (Exogenous Shocks and Order Flow Surprises)
- **source url:** Search arXiv q-fin
- **source quality:** medium
- **horizon:** intraday
- **market logic:** Sudden exogenous shocks (news events, macro prints) create immediate "surprises" in order flow. The resulting price trajectory is governed not just by price impact, but by *cross-impact* across the entire term structure (e.g., SOFR futures).
- **why it might exist:** Market makers universally adjust their quotes across all correlated contracts instantly during a shock, creating temporary liquidity gaps and predictable cross-asset ripple effects.
- **required data:** Continuous futures data, economic event flags, multi-contract correlation mapping.
- **likely instruments:** Interest Rate Futures (SOFR, Eurodollar)
- **likely best condition:** Non-farm payrolls, CPI prints, Fed statements.
- **likely failure mode:** Widened bid-ask spreads during the shock destroying the alpha.
- **implementation difficulty:** medium-high
- **transfer risk to Project 1L:** medium
- **memo_gate:** YES
- **current status:** parked parent-family candidate
- **note:** Valuable for navigating macro-event volatility, easily adaptable if limited to 1-minute bars around known news events.

### ARXIV-008 — lob_local_volatility_multiplier
- **family name:** lob_local_volatility_multiplier
- **source:** arXiv q-fin (Local volatility, Order books, etc.)
- **source url:** Search arXiv q-fin
- **source quality:** high
- **horizon:** intraday / dynamic hedging
- **market logic:** The bid-ask spread in an order book acts as a direct multiplier on the implied "local volatility." Wide spreads inherently generate higher volatility regimes. Strategies dynamically scale exposure or entirely avoid trading when the order book spread widens past a statistical threshold.
- **why it might exist:** Wide spreads equal low liquidity; low liquidity equals violent price variance for any given order size.
- **required data:** Bid-Ask spread width over time.
- **likely instruments:** All futures.
- **likely best condition:** Highly volatile sessions requiring dynamic risk sizing.
- **likely failure mode:** The spread compresses immediately after exiting, leaving the strategy under-exposed.
- **implementation difficulty:** medium
- **transfer risk to Project 1L:** medium
- **memo_gate:** NO
- **current status:** research-only overlay candidate
- **note:** Extremely useful as a dynamic filter for existing ORB / intraday strategies: if spread/atr ratio is too high, abort the trade.

## 4D. Parked Captures — CME Sweep 1

### CME-001 — treasury_yield_curve_spread
- **family name:** treasury_yield_curve_spread
- **source:** CME Group (Inter-Commodity Spreads - ICS)
- **source url:** Search CME Group Education
- **source quality:** high
- **horizon:** medium- to long-horizon
- **market logic:** Actively trade the relative yield difference between distinct maturity points on the U.S. Treasury curve (e.g., 2-Year vs 10-Year, or 5-Year vs 30-Year) via exchange-recognized spread ratios.
- **why it might exist:** Central bank policy actions anchor the front end of the curve, while growth/inflation expectations drive the long end, creating structural steepening or flattening trends.
- **required data:** Multiple Treasury futures contracts, DV01 (Dollar Value of a Basis Point) weighting ratios provided by CME.
- **likely instruments:** ZT (2Y), ZF (5Y), ZN (10Y), ZB (30Y)
- **likely best condition:** Macro regime shifts, Federal Reserve tightening/easing cycles.
- **likely failure mode:** Yield curve pegging by central banks (e.g., yield curve control), inaccurate DV01 weighting causing directional delta bleed.
- **implementation difficulty:** medium-high
- **transfer risk to Project 1L:** medium
- **memo_gate:** YES
- **current status:** parked parent-family candidate
- **note:** Represents the bedrock of fixed-income relative value. Strongly highlights the need for dynamic multi-leg position sizing inside the Project 1L engine.

### CME-002 — energy_crack_spread
- **family name:** energy_crack_spread
- **source:** CME Group (Energy Crack Spreads)
- **source url:** Search CME Group Education
- **source quality:** high
- **horizon:** medium-horizon
- **market logic:** Trade the theoretical refining margin by simultaneously buying crude oil and selling the refined products (gasoline and heating oil/diesel) in specific ratios, famously the 3:2:1 or 5:3:2 spread.
- **why it might exist:** Refiners physically operate on these margins. If the spread gets too tight, refiners cut production (crashing crude demand, raising product supply), forcing the spread to mean-revert back to profitable levels.
- **required data:** 3 distinct continuous futures contracts (CL, RB, HO), fixed volumetric scaling ratios.
- **likely instruments:** WTI Crude (CL), RBOB Gasoline (RB), NY Harbor ULSD (HO)
- **likely best condition:** Summer driving season ramps, winter heating disruptions, refinery outages.
- **likely failure mode:** Structural shifts in refinery capacity or global substitution breaking the historical bound.
- **implementation difficulty:** medium-high
- **transfer risk to Project 1L:** medium
- **memo_gate:** YES
- **current status:** parked parent-family candidate
- **note:** The archetype for industrial margin mean-reversion. A perfect, structurally-bounded test for our future asynchronous multi-leg engine.

### CME-003 — equity_smallcap_largecap_spread
- **family name:** equity_smallcap_largecap_spread
- **source:** CME Group (Equity Index Intermarket Spreads)
- **source url:** Search CME Group Education
- **source quality:** medium
- **horizon:** short- to medium-horizon
- **market logic:** Trade the relative outperformance of the Russell 2000 against the S&P 500 (buying RTY, selling ES) based on macroeconomic factors like domestic growth vs multinational currency exposure.
- **why it might exist:** Divergent economic factors impact highly-domestic small caps differently than gigantic, globally-exposed tech/large caps, leading to cyclical rotation.
- **required data:** Synchronized ES and RTY futures, volatility weighting or CME recognized 2:1 nominal ratio.
- **likely instruments:** Micro E-mini S&P (MES), Micro E-mini Russell 2000 (M2K)
- **likely best condition:** Early-cycle economic recoveries (favoring small caps) vs late-cycle safety flights (favoring large caps).
- **likely failure mode:** Correlation converging to 1.0 during severe systemic liquidations, causing the spread to violently fail as all equities drop together.
- **implementation difficulty:** low
- **transfer risk to Project 1L:** low
- **memo_gate:** YES
- **current status:** parked parent-family candidate
- **note:** Highly executable immediately on Project 1L's current dual-instrument engine architecture since it operates synchronously in the same equity complex.

### CME-004 — sofr_fedfunds_basis
- **family name:** sofr_fedfunds_basis
- **source:** CME Group (SOFR Spreads and Packs)
- **source url:** Search CME Group Education
- **source quality:** high
- **horizon:** short- to medium-horizon
- **market logic:** Trade the spread between the Secured Overnight Financing Rate (SOFR) and the effective Federal Funds rate, capturing the basis between secured repo lending and unsecured interbank lending.
- **why it might exist:** Liquidity crunches or regulatory capital constraints can temporarily detach secured repo rates from the Fed's target unsecured rate, eventually normalizing via arbitrage.
- **required data:** SR1/SR3 futures, ZQ futures.
- **likely instruments:** 1-Month SOFR (SR1), 30-Day Fed Funds (ZQ)
- **likely best condition:** End-of-quarter/end-of-year balance sheet window dressing by major banks, repo market dislocations.
- **likely failure mode:** The Federal Reserve aggressively steps in with massive repo facilities, instantly flattening the volatility.
- **implementation difficulty:** medium
- **transfer risk to Project 1L:** high
- **memo_gate:** NO
- **current status:** reference archetype
- **note:** An advanced institutional basis trade. Too esoteric for immediate Project 1L focus, but an excellent reference for secured vs unsecured structural bounding.

### CME-005 — agricultural_calendar_spread
- **family name:** agricultural_calendar_spread
- **source:** CME Group (Term Structure / Agricultural Spreads)
- **source url:** Search CME Group Education
- **source quality:** medium
- **horizon:** seasonal / multi-month
- **market logic:** A calendar spread (buying a deferred month, selling a near month) on crops like Wheat or Corn to capture the transition heavily dominated by seasonal planting and harvest cycles.
- **why it might exist:** Old-crop vs new-crop supply dynamics create extreme, predictable backwardation or contango shapes that must physically resolve as the harvest hits the silos.
- **required data:** Full futures chain strips.
- **likely instruments:** ZC (Corn), ZW (Wheat), ZS (Soybeans)
- **likely best condition:** Normal weather years, predictable inventory levels.
- **likely failure mode:** Extreme unseasonable droughts or massive geopolitical export bans overriding the seasonal cycle.
- **implementation difficulty:** high
- **transfer risk to Project 1L:** high
- **memo_gate:** NO
- **current status:** research-only overlay candidate
- **note:** Validates the concept from the SSRN sweep previously. Requires significant infrastructure upgrade to handle simultaneous multi-expiry contract processing.

### CME-006 — treasury_calendar_roll_arbitrage
- **family name:** treasury_calendar_roll_arbitrage
- **source:** CME Group (Treasury Calendar Spreads)
- **source url:** Search CME Group Education
- **source quality:** medium
- **horizon:** days (specifically around the quarterly roll)
- **market logic:** Provide liquidity or extract micro-inefficiencies in the calendar spread pricing precisely during the massive quarterly institutional futures roll (transitioning from front month to next month).
- **why it might exist:** The sheer mechanical volume of institutions forced to roll their exposure simultaneously strains the calendar spread order book, allowing nimble traders to capture the bid-ask or small mispricings.
- **required data:** Highly granular Level 2 data on the exact calendar spread instrument during roll week.
- **likely instruments:** ES roll spread, ZN roll spread.
- **likely best condition:** High open interest rollover days.
- **likely failure mode:** Being steamrolled by identical, faster HFT algorithms.
- **implementation difficulty:** high
- **transfer risk to Project 1L:** high
- **memo_gate:** NO
- **current status:** reference archetype
- **note:** A pure microstructure liquidity provision play, not a directional strategy. Good theoretical anchor for why calendar spreads exist independently.

## 4E. Parked Captures — HFT / Microstructure Advanced Lane

### HFT-001 — mes_mnq_hawkes_lead_lag
- **family name:** mes_mnq_hawkes_lead_lag
- **source:** academic literature — Hawkes process models in high-frequency finance; multi-asset Hawkes lead-lag inference; non-synchronous microstructure noise literature
- **source quality:** high (established literature, legitimate mathematical framework)
- **horizon:** ultra-short / event-driven (millisecond to sub-second)
- **market logic:** MES and MNQ can enter transient asymmetric lead-lag states where one instrument temporarily drives price discovery and the other lags. A Hawkes process model can detect these states in real time and trade the laggard instrument in the direction of the leader's impulse, expecting the laggard to catch up before the state collapses.
- **why it might exist:** different participant pools, different notional sizes, different liquidity at the top of book, and intraday flow imbalances can cause one leg to update faster than the other for short windows
- **required data:** MBP/MBO tick data, order-by-order event streams, co-location or near-co-location execution, online Hawkes calibration
- **likely instruments:** MES, MNQ
- **likely best condition:** active intraday sessions with clear momentum impulses, short windows of directional imbalance
- **likely failure mode:** Hawkes fits with poor statistical significance, regime instability invalidating the calibration, execution latency overwhelming the alpha window, signal leakage from using a future laggard move in signal definition
- **implementation difficulty:** very high
- **transfer risk to Project 1L:** very high — requires event-driven stack, MBP/MBO data, millisecond execution; not buildable on current bar-replay engine
- **memo_gate:** NO (for current stack) — YES (for future HFT stack)
- **current status:** parked — valid advanced research lane / future HFT lane only
- **note:** Academically legitimate. Hawkes processes are established in HFT finance. Multi-asset Hawkes lead-lag modeling and lead-lag inference under non-synchronous microstructure noise are real literatures. Cannot be built on the current Project 1L bar-replay stack. Park until a future event-driven, MBP/MBO, low-latency stack exists. Key rejection criteria for now: (1) spread definition as written uses a future laggard move — not an executable real-time signal; (2) online Hawkes calibration is under-specified; (3) execution assumptions require colocation and millisecond fills.

---

## 4F. Possible Memo Candidates — Tractable Descendants

### MC-001 — mes_mnq_short_horizon_relative_impulse
- **family name:** mes_mnq_short_horizon_relative_impulse
- **source:** derivative of HFT-001 Hawkes lane — reduced to a bar-replay-compatible parent hypothesis
- **source quality:** first-principles structural argument (no single confirming primary paper; the mechanism is argued from the underlying lead-lag logic applied to short 1m bar windows)
- **horizon:** intraday / very short-bar (1m bars; expected hold 1–5 bars)
- **market logic:** MES and MNQ sometimes diverge sharply over a short 1–3 bar window due to transient relative-pressure differences (one leg moves, the other underreacts). The underreacting leg then catches up. This is a bar-level proxy for the Hawkes lead-lag state, without requiring tick data or online calibration. Entry is against the laggard (buy the slower leg in the direction of the faster leg's move) when the divergence exceeds a threshold. Exit is either convergence or a short time stop.
- **why it might exist:** same underlying asymmetric flow mechanism as HFT-001 but observable at the 1m bar level if the lag is large enough to survive bar aggregation
- **required data:** synchronized 1m MES and MNQ bars — already in Project 1L data catalog
- **likely instruments:** MES, MNQ
- **likely best condition:** strong intraday directional impulse where one leg moves clearly first; active session hours
- **likely failure mode:** 1m bars may aggregate away the signal entirely (lag too short to survive bar aggregation); noise trader divergences that do not converge; slippage on entry and exit overwhelming the modest bar-level price differential
- **implementation difficulty:** low-medium (two-leg execution infrastructure already exists from QC-001 pilot)
- **transfer risk to Project 1L:** low — bar-replay compatible, 1m synchronized bars, existing dual-leg engine
- **memo_gate:** YES — gated pending source screen confirmation of the bar-level predictability claim
- **current status:** possible memo candidate — needs source screen before memo is written
- **note:** This is the tractable bar-replay descendant of HFT-001. It preserves the core mechanism hypothesis (short-lived asymmetric lead-lag states between MES and MNQ create temporary relative-value dislocations) but removes the Hawkes calibration, colocation assumptions, tick data dependence, and future-return leakage from the signal. Approved mechanism language: "MES/MNQ short-horizon relative-impulse / underreaction mean reversion." Do not write memo until a source screen confirms bar-level predictability evidence.

---

## 4G. Active Implementation Candidates

### AC-002 — price_gap_reversion_v1
- **family name:** price_gap_reversion
- **source:** QuantConnect Algorithm.Python (PriceGapMeanReversionAlpha)
- **source url:** https://github.com/QuantConnect/Lean/blob/master/Algorithm.Python/Alphas/PriceGapMeanReversionAlpha.py
- **market logic:** When an asset gaps open by an extreme standard deviation (e.g., >3x historical volatility), the initial momentum is an overreaction and price will retreat toward the prior close.
- **instrument style:** Equities (top dollar volume), but portable to Futures
- **likely portable to Project 1L:** Yes. Project 1L has strong gap calculation logic already built for day opens.
- **required data complexity:** Low to medium (requires rolling daily standard deviation / volatility).
- **status:** active — Gate A pending
- **note:** The key differentiation from standard gap fades is requiring an extreme 3x vol outlier, filtering out ordinary noise.

---

## 4H. Parked Candidates - Inconclusive Rejections

### PC-001 — mes_mnq_co_oc_extreme_reversal_v1
- **family name:** mes_mnq_co_oc_extreme_reversal_v1
- **source:** CO–OC overnight–intraday reversal literature applied to MES/MNQ pair; closure-driven relative displacement mechanism
- **source quality:** mechanism-first; documented CO–OC reversal effect in equity index futures; futures-native application
- **horizon:** intraday — enter at 08:31 CT bar open, exit on convergence or time stop
- **market logic:** measure overnight return for each leg (`r_on = ln(open_0830 / prior_cash_close)`). Compute `delta_on = r_on_MNQ - r_on_MES`. Long the overnight loser, short the overnight winner if divergence is extreme. Expect partial relative reversal during the cash session as overnight positioning pressure unwinds.
- **spread unit:** 3 MES vs 2 MNQ (fixed ex-ante, notional-approximate balance)
- **required data:** synchronized 1m MES and MNQ bars; prior cash close for each leg — all in catalog
- **likely instruments:** MES, MNQ
- **current status:** **park — inconclusive / regime-specific / insufficient sample**
- **note:** Gate A passed. Redesigned parent (extreme >= 2 sigma threshold) materially improved over the distorted original unfiltered parent. Profit Factor increased to 1.68. However, extended Dev-A across 20 months (2022-01-01 to 2023-08-31) produced only 8 total trades, failing to meet the minimum 20-trade floor. All observed trades clustered in Spring/Summer 2023. The setup is highly regime-specific, inconclusive due to small sample size. Do not judge family as invalid, but do not promote. Parked pending larger dataset or regime identification tool.

---

## 5. Rejected / Exhausted Idea Neighborhoods

## 6. Notes To Convert Into Formal Specs
