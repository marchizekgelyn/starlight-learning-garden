# ATLAS Finance Engine — Technical Specification (v2.0)

## Units and input contracts

All APR inputs are **percent points**; 5 means 5%, not 500% and not 0.05%. Time in years unless explicitly months. Principal and balances are in assumed USD for presentation. Formulas are currency-agnostic but the user interface formats USD. NPV cash flows occur at successive year endpoints from time 0. Zero and negative APR are accepted where mathematical formulas permit, subject to validation; loan scenarios may not represent commercially available offers.

## Methods

- **Simple interest:** `I=P×r×t`; ending amount `P+I`.
- **Compounded balance:** `A=P(1+r/n)^(nt)`, nominal annual rate `r`, n credited periods per year, t years.
- **Continuous balance:** `A=Pe^(rt)`.
- **Effective yield:** `EAR=(1+r/n)^n−1`.
- **Amortizing payment:** `PMT=P i / (1−(1+i)^(−N))`, periodic rate `i=r/frequency`, count `N=years×frequency`. Zero rate: `PMT=P/N`.
- **Extra-principal loan:** amortizes with scheduled payment plus extra principal, capped at outstanding principal and accrued interest; final payment adjusted. Returns all per-period rows.
- **Debt payoff:** fixed monthly payment. Rejects `payment <= first-month interest` to prevent non-amortizing results.
- **Savings with monthly deposits:** `FV=P(1+i)^N + C[(1+i)^N−1]/i`, with end-of-month deposits by default. Optional start-of-period treatment exists in the engine API.
- **Savings goal:** solve the above for contribution C.
- **Inflation:** future price `P(1+r)^t`; purchasing power `P/(1+r)^t`.
- **Investment CAGR:** `(ending/beginning)^(1/years)−1`, excludes intermediate deposits/withdrawals.
- **NPV:** `sum_t CF_t/(1+r)^t`.
- **IRR:** numerical root of NPV; certain cashflow sequences can admit multiple roots or no roots.

## Double precision, rounding and disclosure warnings

The engine uses JavaScript 64-bit floating point and stable `log1p`/`expm1` transformations to reduce cancellation error for near-zero interest rates. Final monetary figures show two decimals, but intermediate month-by-month calculations keep full floating-point values. This can create discrepancies compared with creditor rounding conventions. No actual fees, variable-rate changes, daily average balances, loan insurance, jurisdiction-specific protections, tax treatment, or forecasts are represented.

## Reusable and testable APIs

`js/finance.js` exports the individually testable pure functions. `js/finance-ui.js` renders scenario tables, charts, and full CSV amortization exports. The scientific parser also exposes `simpleinterest`, `compoundinterest`, `continuousinterest`, `apy`, `loanpmt`, `savingsfv`, `financenpv` and `financeirr` as bounded mathematical functions, with argument checks.
