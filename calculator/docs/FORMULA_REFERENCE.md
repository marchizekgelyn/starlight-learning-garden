# Formula reference and calculator mathematical conventions

**Scientific**: order of operations, exponents, complex arithmetic; `sin`, `cos`, `tan` can use radians or degrees, switched by UI. Symbolic derivatives and graph sampling use radians. The scientific engine supports 4,096 characters per expression.

**Simple interest**: I = P·r·t. Amount = P(1+r·t). APR r is represented as a fraction internally; the interface accepts an input like `5` for 5%.

**Periodic compound interest**: A=P(1+r/n)^(n·t). Effective annual yield: APY=(1+r/n)^n−1. Continuous compounding: A=P·exp(r·t).

**Amortizing loan payment**: PMT=P·i/[1−(1+i)^(-N)]; i=APR/payments per year. At zero interest PMT=P/N. Extra payments reduce balance. Fixed costs like taxes, insurance, HOA and PMI are separate unless entered in the enhanced full mortgage model.

**Savings with end-of-month recurring contributions**: FV=P(1+i)^N+C·[((1+i)^N−1)/i]. At i=0, FV=P+C·N. Other compounding/deposit timing choices require separately defined models.

**Net present value**: NPV=Σ CF_t/(1+r)^t, with first cash flow at time 0. Internal rate of return is a root of NPV(r)=0 and can be nonexistent or multiple for non-conventional cash flows.

**Refinance recovery**: break-even months≈upfront fees/monthly payment savings. Compare total interest and term as well: smaller monthly payments alone do not imply a cheaper mortgage.

**Derivative**: for f(x)=x^n, f′(x)=n·x^(n−1). Symbolic rules include sum, product, quotient, chain, power and selected elementary functions. Numerical derivative uses a centered high-order finite difference.

**Definite integral**: numerical area using adaptive Simpson quadrature. A polynomial antiderivative uses ∫c·x^n dx=c·x^(n+1)/(n+1)+C. Other arbitrary indefinite integrals are not currently generated.

**Taylor approximation**: P_n(x)=Σ from k=0 to n of f^(k)(a)(x−a)^k/k!. The implemented Taylor tool supports degree 0–8 and expressions representable by the symbolic derivative subset.

**Matrix determinant/inverse**: pivoting-based Gaussian elimination and Gauss–Jordan inversion. Matrices limited to 8×8, numbers use binary64 precision.

**Linear regression**: b=Σ(x−x̄)(y−ȳ)/Σ(x−x̄)^2; a=ȳ−b·x̄. Pearson correlation r normalizes by both sums of squares.

**Binomial**: P(X=k)=C(n,k)p^k(1−p)^(n−k). **Poisson**: P(X=k)=e^(−λ) λ^k/k!. Normal density and cumulative probability use an error function approximation; inverse quantiles use bisection.

**Exact fractions**: rational input is reduced using arbitrary-precision BigInt numerator/denominator. Decimal representation of a repeating rational is only an approximation; exact rational output remains a fraction.

**Unit systems**: conversions use explicit dimension tables. Celsius/Fahrenheit/Kelvin require affine offsets. Binary (KiB) and decimal (KB) data units are distinct.
