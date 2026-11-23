#!/usr/bin/env python3
"""Curated supplemental topic catalog and generated fully worked numerical activities.
Produces deterministic lesson data and visual metadata; no runtime generation or network.
"""
import json,math,re,random,pathlib
ROOT=pathlib.Path(__file__).resolve().parent.parent
# Every topic is categorized by a worked-example generator; topic titles are hand selected.
BANK=[
'''count: One-to-one correspondence;Counting on from any number;Counting backwards from 100;Skip counting by twos;Skip counting by fives;Skip counting by tens;Number patterns to 1000;Ordinal numbers;Writing numbers in expanded form;Ordering numbers on a number line;Even and odd numbers;Estimating quantities;Comparing equal-sized groups;Number bonds to ten
add: Addition facts to 10;Addition facts to 20;Doubles and near doubles;Making ten;Commutative property of addition;Associative property of addition;Missing addends;Three-number addition;Word problems with joining;Word problems with adding to
subtract: Subtraction facts within 20;Counting back to subtract;Related addition and subtraction facts;Missing subtrahends;Finding differences;Story problems with separating;Word problems with comparing
geometry: Naming circles and rectangles;Sorting two-dimensional shapes;Three-dimensional shape vocabulary;Partitioning circles and rectangles;Symmetry introduction
place: Tens and ones using blocks;Tens and ones in expanded notation;Place value to 120''',
'''place: Hundreds tens and ones;Place value charts to 1000;Expanded form with three digits;Compare three-digit numbers;Rounding to nearest ten;Rounding to nearest hundred;Regrouping with base-ten blocks;Mental calculation with tens and hundreds;Skip counting by 25
add: Three-digit addition without regrouping;Three-digit addition with regrouping;Column addition algorithms;Addition word problems with unknowns;Properties of addition;Estimate sums before calculating
subtract: Three-digit subtraction without borrowing;Three-digit subtraction with borrowing;Subtraction using compensation;Subtracting across zeros;Multistep subtraction word problems;Checking subtraction with addition
multiply: Arrays and repeated addition;Equal groups;Counting multiplication patterns;Multiplication as rectangular area
money: Money amounts and change;Comparing shopping prices;Representing dollars and cents
fraction: Halves thirds and fourths;Equal-size fractions on diagrams;Fraction of a set
measure: Estimating lengths;Metric length comparisons;Capacity and mass;Using a ruler;Measuring to a nearest unit
time: Reading clocks to five minutes;Minutes hours and days;Elapsed time within an hour
geometry: Quadrilaterals and polygons;Lines and line segments;Composing shapes''',
'''multiply: Multiplication fact families;Multiplication by zero and one;Multiplication by 3 and 4;Multiplication by 6 and 7;Multiplication by 8 and 9;Distributive property;Two-digit times one-digit;Multiplication with arrays;Area model of multiplication;Missing factors;Multiplication word problems
 divide: Division as sharing;Division as grouping;Division fact families;Remainders in everyday contexts;Division with multiplication checks;One-digit quotients;Division word problems
fraction: Fractions as unit parts;Unit fractions on number lines;Equivalent fractions with models;Comparing fractions with equal numerators;Comparing fractions with equal denominators;Fractions greater than one;Fraction of a set
measure: Perimeter of polygons;Area of rectangles;Area using unit squares;Metric unit conversions
 time: Elapsed time through noon;Reading schedules;Time durations in minutes
 geometry: Classifying angles;Quadrilateral attributes;Parallel and perpendicular lines;Symmetry of polygons
 stats: Pictographs and bar graphs;Frequency tables;Interpreting scaled graphs
money: Purchase totals and change''',
'''place: Multi-digit place value to millions;Expanded form with large numbers;Rounding to powers of ten;Whole-number estimation
add: Adding five-digit numbers;Multi-step addition and subtraction;Estimation of whole-number sums
subtract: Subtracting multi-digit numbers;Subtraction across multiple zeros
multiply: Two-digit by two-digit multiplication;Multiplication area model;Partial products multiplication;Three-digit multiplication;Factors and factor pairs;Prime and composite numbers;Multiples and divisibility
 divide: Long division with remainders;Quotient estimation;Division by two-digit divisors;Interpreting remainders
fraction: Equivalent fraction rules;Simplifying fractions;Improper fractions;Mixed numbers;Fraction addition using models;Fraction subtraction with like denominators;Comparing fractions on a number line
 decimal: Decimal tenths and hundredths;Decimal place value chart;Decimal comparisons;Decimal addition introduction
geometry: Angle measurement with a protractor;Acute right and obtuse angles;Adjacent and supplementary angles;Parallel line diagrams;Reflection symmetry;Rotational symmetry
measure: Converting meters and centimeters;Customary units of length;Converting minutes to hours
stats: Line plots with fractions;Reading multiseries charts''',
'''decimal: Decimal place value to thousandths;Multi-digit decimal addition;Multi-digit decimal subtraction;Decimal multiplication;Decimal division;Estimating decimal products;Rounding decimals;Money calculations with decimals
fraction: Fraction equivalence and simplification;Adding fractions with different denominators;Subtracting unlike fractions;Mixed-number addition;Mixed-number subtraction;Multiplying fractions;Fraction scaling;Dividing unit fractions by integers;Dividing integers by unit fractions;Fraction word problems
powers: Powers of ten;Scientific notation introduction;Multiplying by powers of ten;Decimal exponents and estimation
geometry: Coordinate grids in first quadrant;Graphing ordered pairs;Classifying polygons by attributes;Converting between squares and cubes;Solid net diagrams
area: Finding areas of polygons;Areas of composite shapes;Rectangular prism surface area
volume: Volume of right rectangular prisms;Volume with unit cubes;Composite volume models
ratio: Whole-number ratios introduction;Patterns in input-output tables
stats: Data distributions on line plots;Averages introduction;Interpreting trends from charts''',
'''integer: Opposites and signed numbers;Ordering negative integers;Number lines with negatives;Absolute value;Addition of signed numbers;Subtraction of signed numbers;Multiplication of signed numbers;Division of signed numbers;Signed arithmetic in temperature
ratio: Comparing ratios;Ratio tables;Unit rates;Equivalent ratios;Part-to-part and part-to-whole ratios;Double number lines;Speed and unit rates;Unit price comparisons;Converting units with ratios
percent: Understanding percent;Fractions decimals and percentages;Percent of a whole;Percent as proportional reasoning;Percent bar models;Tax and tip introduction;Discount calculations
fraction: Dividing fractions;Complex fractions;Common-denominator reasoning
algebra: Writing algebraic expressions;Combining like terms;Distributive property of multiplication;Substituting values;Simplifying linear expressions;Inequality models;Solving one-variable equations
geometry: Finding missing angles;Triangles and angle sums;Coordinate plane with four quadrants
area: Areas of triangles;Areas of parallelograms;Area of irregular regions
stats: Median mode and mean;Interquartile range;Data variability;Dot plots and box plots
prob: Experimental probability;Theoretical probability;Sample spaces
finance: Introductory savings interest;Comparing discount options''',
'''ratio: Proportional relationships;Graphs of proportional relationships;Constant of proportionality;Unit rate tables;Scale factors and maps;Proportional equations;Similar figures and scale drawings
percent: Percent increase;Percent decrease;Percent error;Markdown and markup;Sales tax rates;Simple interest;Percent change over time
integer: Rational number operations;Adding negative fractions;Multiplying signed fractions;Dividing signed decimals
algebra: Multistep linear equations;Equations with parentheses;Variables on both sides;Two-step inequalities;Solving compound word problems;Rewriting formulas;Translating statements into algebra
linear: Slope as unit rate;Linear equation tables;Graphing straight lines;Intercepts and slope;Linear modeling of costs
geometry: Angle relationships with transversals;Triangle congruence criteria;Polygon interior angles;Circumference of circles;Circle area formulas;Composite figure area;Surface areas of prisms;Scale drawings
prob: Compound probability;Independent events;Dependent events;Tree diagrams for outcomes;Random sampling;Simple simulations
stats: Comparing sample means;Mean absolute deviation;Outliers and distribution shape
finance: APR versus APY introduction;Discount calculations and unit costs''',
'''linear: Slope from two points;Slope-intercept equations;Point-slope form;Linear functions and mappings;Linear inequalities;Graphing systems of equations;Elimination and substitution;Rate of change;Piecewise linear models;Domain and range
algebra: Distributive equations;Equations with fractions;Multistep inequalities;Variable isolation;Proportional equations;Scientific notation arithmetic
powers: Integer exponents;Negative exponents;Zero-exponent rule;Exponent laws;Standard and scientific notation
roots: Square roots;Cube roots;Square root equations;Perfect squares and cubes;Irrational number estimates
pythag: Pythagorean theorem problems;Distance on the coordinate plane;Pythagorean triples;Converse of the theorem
geometry: Congruent transformations;Translations in the plane;Rotations about a point;Reflections across an axis;Dilations and similar shapes;Volume of spheres;Volume of cylinders;Volume of cones
stats: Scatter plots;Trend lines;Correlation versus causation;Two-way frequency tables;Relative frequency
prob: Counting principle;Basic permutations
finance: Linear earning models;Comparing loan offers with simple interest''',
'''algebra: Variables and expression evaluation;Algebraic identities;Properties of equality;Multistep equation solving;Literal equations;Equations with fractions;Inequalities in one variable;Absolute-value equations;Absolute-value inequalities;Function inputs and outputs;Function domain and range;Function composition introduction
linear: Graphing linear functions;Intercept form;Point-slope form;Parallel lines;Perpendicular lines;Systems by graphing;Systems by elimination;Systems by substitution;Mixture word problems;Distance-rate-time models;Linear regression introduction;Piecewise linear graphs
powers: Exponential expression rules;Negative exponent simplification;Radical expressions;Rational exponent introduction
polynomial: Adding and subtracting polynomials;Multiplying monomials;Multiplying binomials;FOIL distributive methods;Factoring a GCF;Factoring trinomials;Factoring difference of squares;Completing the square
quadratic: Quadratic equation solutions;Quadratic graphs and vertices;Factoring quadratic expressions;Quadratic discriminant;Quadratic formula;Maximum and minimum quadratic models
stats: Relative-frequency tables;Describing bivariate data;Comparing distributions
finance: Income budgeting equations;Annual simple interest word problems''',
'''geometry: Postulates and deductive reasoning;Points lines planes and rays;Segment addition and midpoint;Angle bisectors;Vertical and adjacent angles;Parallel lines and transversals;Triangle angle-sum theorem;Exterior triangle angles;Isosceles triangle properties;Triangles by side length;Triangles by angle type;Congruence by SSS;Congruence by SAS;Congruence by ASA;Congruence by AAS;Right-triangle HL congruence;Proving triangle relationships;Similar triangles by AA;Similar triangles by SAS;Similar triangles by SSS;Triangle proportionality theorem;Medians altitudes and angle bisectors;Centroids orthocenters circumcenters;Triangle inequalities;Quadrilateral classifications;Parallelogram properties;Rectangle properties;Rhombus properties;Square properties;Trapezoid properties;Circle chord theorems;Inscribed angles;Central angles;Tangents and secants;Arc length of circles;Sector areas;Polygon angle sums;Regular polygons and apothems;Reflections rotations and translations;Dilations and similarity;Coordinate geometry proofs;Volume of prisms;Volume of pyramids;Volume of cones;Volume of spheres;Surface areas of solids
pythag: Right-triangle similarity;Geometric proof of the Pythagorean theorem;Special right triangles 45-45-90;Special right triangles 30-60-90;Geometric distance problems
trig: Right-triangle sine cosine and tangent;Inverse trigonometric ratios;Heights and distances with trig
area: Composite shape area;Triangle and parallelogram area;Heron formula introduction''',
'''polynomial: Long division of polynomials;Synthetic division;Remainder theorem;Factor theorem;Polynomial roots;Multiplicity of zeros;End behavior of polynomials;Complex polynomial zeros;Polynomial identity proofs;Polynomial inequalities
quadratic: Conic sections and parabolas;Quadratic transformations;Completing squares in conics;Discriminants and roots
exp: Exponential growth and decay;Compound interest with exponents;Exponential equations;Growth and decay constants;Half-life mathematics;Continuous exponential models
log: Logarithm definitions;Properties of logarithms;Change-of-base formula;Natural logarithms;Solving logarithmic equations;Logarithmic graphs;Exponential and log inverses;Domain restrictions for logarithms
rational: Rational expression domains;Rational expression multiplication;Rational expression division;Rational expression addition;Rational equations;Removable discontinuities;Vertical asymptotes;Horizontal and slant asymptotes
radical: Radical addition and multiplication;Rationalizing denominators;Rational exponent equations
complex: Imaginary unit and powers;Complex number operations;Complex conjugates;Modulus of complex numbers;Complex solutions to quadratics
sequence: Arithmetic sequence formulas;Geometric sequence formulas;Finite arithmetic series;Finite geometric series;Recursive definitions;Mathematical induction introduction
matrix: Matrices and augmented systems;Matrix addition;Matrix multiplication;Matrix determinants;Inverse of a 2 by 2 matrix;Solving systems with matrices
stats: Binomial distributions introduction;Probability of independent events;Expected values and discrete variables
finance: Compound APR and effective yield;Loan payments with fixed rates;Net present value introduction''',
'''trig: Radian measure and arc length;Reference angles;Unit circle coordinates;Trigonometric graph transformations;Sinusoid amplitude and period;Sine and cosine identities;Pythagorean identities;Sum and difference identities;Double-angle identities;Half-angle identities;Trigonometric equations;Inverse trigonometric functions;Law of sines;Law of cosines;Triangle area with sine
functions: Function notation and composition;Inverse functions;Transformations of functions;Even and odd functions;Piecewise-defined functions;Parametric representation introduction;Polynomial function analysis;Rational function analysis
exp: Exponential growth models;Exponential regression principles;Population models and doubling time
log: Logarithm as inverse;Exponential and logarithmic derivatives preview;Logistic growth introduction
sequence: Recursive sequences;Arithmetic progression sums;Geometric progression sums;Finite telescoping series;Binomial theorem;Pascal triangle
vector: Two-dimensional vectors;Magnitude and direction;Vector addition;Scalar multiplication;Dot product;Orthogonal vectors;Component form;Vector projections
polar: Polar coordinates;Cartesian-to-polar conversions;Polar graphs;Symmetry in polar coordinates
complex: Complex plane coordinates;Polar form of complex numbers;De Moivre theorem;Roots of unity
limit: Rates of change toward a limit;Numerical approaches to limits;Continuity at a point;One-sided limits
geometry: Ellipse equations;Hyperbola equations;Conic eccentricity
finance: Continuous compounding;Compound interest growth comparisons''',
'''limit: Limit laws;One-sided limits;Two-sided limits;Removable discontinuities;Jump discontinuities;Infinite discontinuities;Limits at infinity;Squeeze theorem;Trigonometric limits;Continuity on intervals;Intermediate value theorem;Epsilon-delta intuition;Limit indeterminate forms
 derivative: Definition of derivative;Derivative as tangent slope;Differentiability and continuity;Power rule;Sum and difference rules;Product rule;Quotient rule;Chain rule;Derivatives of sine and cosine;Derivatives of tangent;Derivatives of exponential functions;Derivatives of logarithms;Inverse trig derivatives;Implicit differentiation;Higher derivatives;Derivative of inverse functions;Logarithmic differentiation
 applications_derivative: Position velocity and acceleration;Marginal cost and revenue;Optimization of area;Optimization of volume;Related rates;Linear approximation;Differentials and error;Mean value theorem;Rolle theorem;Critical points;Local extrema;Absolute extrema on closed intervals;First derivative test;Second derivative test;Concavity and inflection points;Curve sketching;Newton method;L Hopital rule
 integral: Riemann sums;Left right and midpoint sums;Trapezoidal area estimates;Definite integral notation;Signed area and accumulation;Antiderivative basics;Indefinite integral and constants;Power-rule integration;Area between a curve and axis;Average value of a function;Net change theorem
 ftc: Fundamental theorem of calculus I;Fundamental theorem of calculus II;Definite integrals from antiderivatives;Accumulation functions;Substitution introduction
 finance: Continuous interest derivatives;Marginal financial rates of change''',
'''integral: Integration by substitution;Integration by parts;Tabular integration by parts;Trigonometric integrals;Trigonometric substitution;Partial fraction decomposition;Rational function integration;Completing the square for integrals;Reduction formulas;Numerical integration errors;Midpoint quadrature;Trapezoidal quadrature;Simpson integration;Integration of logarithms;Improper integrals with infinite bounds;Improper integrals with singularities;Comparison for improper integrals
 volume: Volumes by slicing;Solids of revolution with disks;Solids of revolution with washers;Shell method;Cross-sectional volume models
 applications_derivative: Work with variable forces;Fluid force and pressure;Center of mass;Moments of mass;Average values in applications
 arc: Arc length of graphs;Surface area of revolution;Arc length for parametric curves;Arc length in polar form
 sequence: Sequence convergence;Monotone sequences;Bounded sequences;Finite sums and sigma notation;Recursive sequences and fixed points
 series: Convergence and divergence of series;Geometric infinite series;Telescoping series;Integral test;P-series test;Comparison test;Limit comparison test;Alternating series test;Absolute and conditional convergence;Ratio test;Root test;Series test selection;Power series;Radius of convergence;Interval of convergence;Taylor series;Maclaurin series;Taylor remainder bounds;Binomial series;Differentiating power series;Integrating power series;Series solutions near a point
 parametric: Parametric curve plotting;Eliminating a parameter;Parametric derivatives;Parametric second derivatives;Tangents to parametric curves;Areas with parametric curves
 polar: Polar coordinates and curves;Polar symmetry;Polar tangent slopes;Polar enclosed area;Polar region intersection areas;Polar arc length
 differential: Separable differential equations;Exponential decay differential equations;Logistic differential equations;Slope fields introduction
 finance: Present value as integration;Continuous cash flow models;Savings and annuity calculations'''
]
assert len(BANK)==14
FAMILIES={
'count':('Use a number line or a grouped collection to associate quantities with numerals. Check successive changes carefully.','Counting helps establish order, magnitude, and stable numerical representation.'),
'place':('Group digits according to powers of ten; moving one place left multiplies value by 10.','An expanded number is the sum of its place-value contributions.'),
'add':('Combine parts, using place value or number bonds to simplify the sum.','Addition preserves a total when terms are rearranged.'),
'subtract':('Represent the difference between a starting amount and an amount removed.','Subtraction can be checked by adding the difference to the subtracted amount.'),
'multiply':('Multiplication counts equal groups and can be visualized as rectangular arrays.','Use the distributive property to break a product into smaller products.'),
'divide':('Division finds how many equal groups can be made or the size of each group.','Check your quotient by multiplying it by the divisor.'),
'money':('Line up currency units and calculate totals or change from known prices.','Always label answers in dollars or cents and round monetary results to cents.'),
'measure':('Convert by applying a consistent unit factor; write units in every step.','An equivalent measurement has a different number but represents the same magnitude.'),
'time':('Convert hours to minutes by multiplying by 60, then add or subtract durations.','Using one unit first prevents mismatched time arithmetic.'),
'fraction':('Use the numerator for selected parts and denominator for equal pieces in the whole.','Equivalent fractions are obtained by multiplying numerator and denominator by the same nonzero factor.'),
'decimal':('Write decimals in aligned place-value columns and track every decimal digit.','Ten hundredths make one tenth and ten tenths make one whole.'),
'percent':('Rewrite the percent as a decimal by dividing by 100, then multiply the baseline.','The original amount is the reference when finding percent change.'),
'ratio':('Keep the order of compared quantities and scale both parts by the same factor.','Equivalent ratios represent the same proportional relationship.'),
'integer':('Use a signed number line and preserve sign rules when adding or multiplying.','A negative product results from one positive and one negative factor.'),
'powers':('Exponents count repeated multiplication; use exponent laws only for compatible bases.','For nonzero a, a^m × a^n = a^(m+n).'),
'roots':('The principal square root is the nonnegative number whose square is the radicand.','Check the result by squaring it; extraneous roots can appear in equations.'),
'algebra':('Undo operations in reverse order and perform the same operation on both sides.','An equation represents equality, so balanced transformations preserve its solution.'),
'linear':('In y=mx+b, m describes constant slope and b describes initial value.','Slope is change in y divided by the corresponding change in x.'),
'geometry':('Sketch and label known lengths, angles and shape properties before calculating.','A valid geometric argument uses definitions and established properties.'),
'area':('Decompose complicated regions into simpler shapes with known area formulas.','Square units measure area; preserve the correct dimensions.'),
'volume':('Multiply base area by height for a prism; other solids require appropriate formulas.','Cubic units measure volume, not square units.'),
'angle':('Use the angle-sum relationships appropriate to the figure.','Angles about a straight line total 180 degrees, and a full turn totals 360.'),
'pythag':('For a right triangle, the squares of the legs add to the hypotenuse square.','The Pythagorean theorem applies only to right triangles.'),
'prob':('Write favorable outcomes over the total equally likely outcomes.','A probability lies between zero and one, inclusive.'),
'stats':('Organize observations and distinguish measures of center from measures of spread.','The mean is the total divided by the number of observations.'),
'polynomial':('Group like powers and apply exponent and factorization rules.','A polynomial is a finite sum of nonnegative integer powers of a variable.'),
'quadratic':('For y=ax²+bx+c with a≠0, the axis of symmetry is x=−b/(2a).','The sign of a determines whether the parabola opens up or down.'),
'exp':('Use exponential models when a quantity changes by a fixed fraction per period.','Compounding multiplies a balance by (1+r) at each complete period.'),
'log':('A logarithm gives the exponent required to obtain a value from a base.','Logarithmic inputs must be positive for real-valued logs.'),
'rational':('A rational function is a quotient of polynomials on a domain excluding zero denominators.','Classify canceled holes separately from uncanceled vertical asymptotes.'),
'radical':('Radical expressions use fractional exponents and are constrained by the domain.','A real square root requires a nonnegative radicand.'),
'complex':('Use i²=−1 and collect real and imaginary parts separately.','Complex conjugation flips the sign of the imaginary part.'),
'sequence':('Express the nth term through a pattern or recurrence, then verify initial terms.','An arithmetic sequence adds a constant difference at each step.'),
'matrix':('Use consistent row-column dimensions and compute entries systematically.','For matrix multiplication the inner dimensions must match.'),
'functions':('Specify the function rule and its domain; a valid input has one output.','Track how vertical/horizontal transformations affect a graph.'),
'trig':('Use the unit circle and angle identities to connect sine and cosine.','In calculus, trigonometric derivatives use radians.'),
'vector':('Resolve vectors into components before adding or taking dot products.','Magnitude in 2D is sqrt(x²+y²).'),
'polar':('Represent a point with radius r and angle θ measured from the polar axis.','Convert using x=r cosθ and y=r sinθ.'),
'limit':('Analyze what a function approaches as x tends to a value, independent of the actual value at that point.','Numerical values suggest a limit but do not constitute proof.'),
'derivative':('Differentiate to find instantaneous rate of change and tangent-line slope.','Check the applicable product, quotient, power and chain rules.'),
'applications_derivative':('Formulate the model, take its derivative, and interpret its units and critical points.','A critical point may be a maximum, minimum, or neither.'),
'integral':('The definite integral represents signed accumulated change and can be approximated by Riemann sums.','Differentiate an antiderivative to verify an indefinite-integral result.'),
'ftc':('Use a valid antiderivative and subtract the lower-endpoint value from the upper-endpoint value.','The fundamental theorem connects accumulation and differentiation.'),
'arc':('Break a curve into small line segments and take their limiting total length.','Arc-length integrands involve the square root of one plus slope squared.'),
'series':('Test whether partial sums approach a finite value; different tests have different hypotheses.','The nth-term test can show divergence but cannot establish convergence.'),
'parametric':('Treat x and y as functions of a parameter; use dy/dx=(dy/dt)/(dx/dt) where valid.','The same geometric curve can be traced at different speeds.'),
'differential':('Relate a derivative to an unknown function and choose an appropriate solution method.','A differential equation requires initial conditions for a unique solution in many cases.'),
'finance':('Convert a percentage to a decimal and write down the compounding period before computing.','A loan APR and an investment APY are not automatically interchangeable.')
}

def example_for(kind,seed):
    # Deterministic, semantically appropriate worked problems with precise solutions.
    rng=random.Random(seed*7919+113);a=rng.randint(2,12);b=rng.randint(2,11);c=rng.randint(1,7)
    if kind=='count': return (f'Count forward {b} from {a}.',f'Start at {a}; advance one at a time until {b} moves have passed. > {a} + {b} = {a+b}.',f'What number is {c} after {a+b}?',str(a+b+c),'Count forward the requested number of steps.')
    if kind=='place': p=10**rng.randint(1,3);return (f'Write {a} groups of {p} plus {b} ones as a number.',f'Each group represents {p}. > Multiply {a}×{p} = {a*p}. > Add {b} to make {a*p+b}.',f'Calculate {c}×{p} + {a}.',str(c*p+a),'Expand the place value before adding.')
    if kind=='add':return (f'Find {a} + {b}.',f'Combine {a} and {b} equal units. > The result is {a+b}. > Check with {b}+{a}.',f'{a+c} + {b+c} = ?',str(a+b+2*c),'Make a ten or add the tens and ones separately.')
    if kind=='subtract':return (f'{a+b} − {a} = ?',f'Start at {a+b}. > Remove {a} units. > The remainder is {b}.',f'{a+b+c} − {a} = ?',str(b+c),'Subtract from the original amount.')
    if kind=='multiply':return (f'{a} equal groups of {b} make {a*b}.',f'Write repeated addition of {b} for {a} groups. > Multiply {a}×{b}. > Total = {a*b}.',f'What is {a+c}×{b}?',str((a+c)*b),'Use an area model or multiply each part.')
    if kind=='divide':return (f'Split {a*b} into {a} equal groups.',f'{a*b}÷{a} equals the number in each group. > Because {a}×{b}={a*b}, the quotient is {b}.',f'Compute {(a+c)*b} ÷ {b}.',str(a+c),'Use the inverse multiplication fact.')
    if kind=='money':return (f'Buy {a} items at $2 each.',f'Multiply {a}×$2. > The cost is ${a*2:.2f}. > Compare the cost against your budget.',f'What is the dollar cost of {b} items at $3 each?',str(b*3),'Multiply item count by price per item.')
    if kind=='measure':return (f'Convert {a} meters to centimeters.',f'1 meter = 100 centimeters. > Multiply {a}×100. > Result {a*100} centimeters.',f'{b} meters equals how many centimeters?',str(b*100),'Multiply meters by 100.')
    if kind=='time':return (f'Convert {a} hours into minutes.',f'An hour contains 60 minutes. > Multiply {a}×60. > There are {a*60} minutes.',f'How many minutes in {b} hours?',str(b*60),'Multiply the hours by sixty.')
    if kind=='fraction':return (f'Find {a}/{a+b} of {(a+b)*c} objects.',f'Divide total {(a+b)*c} by {a+b}: each unit fraction is {c}. > Take {a} parts, obtaining {a*c}.',f'Find {b}/{a+b} of {(a+b)*c} objects.',str(b*c),'First find the value of one equal part.')
    if kind=='decimal':return (f'Add {a/10:.1f} + {b/10:.1f}.',f'Convert tenths to integers: {a} tenths plus {b} tenths. > Get {a+b} tenths. > Divide by ten: {(a+b)/10:.1f}.',f'{(a+c)/10:.1f} + {(b+c)/10:.1f} = ?',str((a+b+2*c)/10),'Align the decimal points.')
    if kind=='percent':return (f'Find {a*5}% of {b*20}.',f'Convert {a*5}% to {a*5/100:g}. > Multiply by {b*20}. > Result = {a*b}.',f'Find {b*5}% of {a*20}.',str(a*b),'Percent means per one hundred.')
    if kind=='ratio':return (f'Scale the ratio {a}:{b} by {c}.',f'Multiply both terms by {c}. > {a*c}:{b*c} preserves the same relationship.',f'If {a}:{b} is scaled by {c+1}, what is the first part?',str(a*(c+1)),'Multiply both components by the same number.')
    if kind=='integer':return (f'Calculate −{a} + {b}.',f'Start at −{a}. > Move {b} units right. > The sum is {b-a}.',f'Calculate −{a+c} + {b}.',str(b-a-c),'Start at the negative number and move right.')
    if kind=='powers':return (f'Evaluate {a}².',f'Multiply {a} by itself. > {a}² = {a*a}.',f'Calculate {b}³.',str(b**3),'Cube means multiply the base three times.')
    if kind in ('roots','radical'):return (f'Find √({a*a}).',f'{a}×{a} = {a*a}. > The principal square root is {a}.',f'Find √({b*b}).',str(b),'The principal square root is nonnegative.')
    if kind=='algebra':return (f'Solve {a}x + {b} = {a*c+b}.',f'Subtract {b} from both sides. > Divide the result by {a}. > x = {c}.',f'Solve {b}x + {a} = {b*(c+2)+a}. Enter x.',str(c+2),'Undo addition and then multiplication.')
    if kind=='linear':return (f'Evaluate y={a}x+{b} at x={c}.',f'Multiply slope {a} by {c}. > Add intercept {b}. > y={a*c+b}.',f'In y={b}x+{a}, what is y at x={c+1}?',str(b*(c+1)+a),'Substitute x, multiply by slope, then add intercept.')
    if kind=='geometry':return (f'A triangle has two angles {a*3}° and {b*4}°.',f'Triangle interior angles total 180°. > Add the known angles: {a*3+b*4}°. > Third angle is {180-a*3-b*4}°.',f'A triangle has angles {a*2}° and {b*3}°. Find the third.',str(180-a*2-b*3),'Interior triangle angles sum to 180 degrees.')
    if kind=='area':return (f'Area of rectangle width {a}, height {b}.',f'Area = base × height. > Multiply {a}×{b}. > Area = {a*b} square units.',f'Area of a rectangle {a+c} by {b+c}?',str((a+c)*(b+c)),'Multiply both dimensions; use square units.')
    if kind=='volume':return (f'Rectangular prism dimensions {a}, {b}, and {c}.',f'Volume = length×width×height. > {a}×{b}×{c} = {a*b*c} cubic units.',f'Volume of a prism {a+1} by {b} by {c}?',str((a+1)*b*c),'Multiply all three dimensions.')
    if kind=='angle':return (f'Find supplementary angle to {a*7}°.',f'Angles on a straight line sum to 180°. > 180−{a*7} = {180-a*7}°.',f'Find complement of {b*5}°.',str(90-b*5),'Complementary angles add to 90°.')
    if kind=='pythag':return (f'Right triangle with legs 3 and 4.',f'Apply 3² + 4² = 9+16 = 25. > Hypotenuse is √25 = 5.',f'Right triangle legs {3*c} and {4*c}. Hypotenuse?',str(5*c),'Scale the 3–4–5 right triangle.')
    if kind=='prob':return (f'{a} favorable outcomes out of {a+b} equally likely results.',f'Probability = favorable/total. > P = {a}/({a+b}) ≈ {a/(a+b):.6f}.',f'{b} favorable outcomes out of {a+b}. Give a decimal.',str(b/(a+b)),'Favorable divided by total outcomes.')
    if kind=='stats':return (f'Find mean of {a},{b},{c}.',f'Add values to get {a+b+c}. > Divide by 3. > Mean = {(a+b+c)/3:.6f}.',f'Mean of {a},{a+2},{a+4}?',str(a+2),'Sum observations and divide by count.')
    if kind=='polynomial':return (f'Evaluate f(x)=x²+{a}x+{b} at x={c}.',f'Compute {c}²={c*c}. > Compute {a}×{c}={a*c}. > Add {b} to obtain {c*c+a*c+b}.',f'Find f({c+1}) for f(x)=x²+{a}x+{b}.',str((c+1)**2+a*(c+1)+b),'Square x first, multiply coefficient, then add.')
    if kind=='quadratic':return (f'Find vertex x-coordinate of f(x)={a}x²+{b*2}x+{c}.',f'The axis is −b/(2a). > Here b={b*2}, a={a}. > x=−{b}/{a} = {-b/a:.6f}.',f'For f(x)={b}x²+{a*2}x+{c}, find the vertex x-coordinate.',str(-a/b),'Use −b/(2a), not −b/a.')
    if kind=='exp':return (f'Grow {a*100} at {c*10}% for two years.',f'Convert rate to {c/10:.1f}. > Multiply initial amount by (1+{c/10:.1f})². > Value = {a*100*(1+c/10)**2:.4f}.',f'Grow {b*100} by {c*10}% for one year.',str(b*100*(1+c/10)),'Multiply once by 1 plus the decimal growth rate.')
    if kind=='log':return (f'Calculate log base {a} of {a*a}.',f'{a}²={a*a}. > The logarithm asks which exponent yields {a*a}. > Answer 2.',f'What is log base {b} of {b*b*b}?','3','Logarithm is the inverse of exponentiation.')
    if kind=='rational':return (f'Analyze f(x)=1/(x−{a}).',f'The denominator vanishes when x−{a}=0. > Solve x={a}. > x={a} is excluded from the real domain.',f'For g(x)=1/(x−{b}), find the excluded x-value.',str(b),'Set denominator to zero.')
    if kind=='complex':return (f'Compute ({a}+{b}i)+({c}−{a}i).',f'Add real terms: {a}+{c}={a+c}. > Add imaginary coefficients: {b}−{a}={b-a}. > Result {a+c}+({b-a})i.',f'What is the real part of ({a}+{b}i)+({c}+2i)?',str(a+c),'Add the real coefficients separately.')
    if kind=='sequence':return (f'Arithmetic sequence starts {a} and increases by {b}.',f'General nth term is {a}+(n−1)×{b}. > The fourth term is {a}+3×{b}={a+3*b}.',f'Find the fifth term of start {a}, step {b}.',str(a+4*b),'The fifth term has four increments.')
    if kind=='matrix':return (f'Add matrices [[{a},{b}],[{c},1]] and [[1,2],[3,4]].',f'Add matching positions. > Entry (1,1) = {a}+1={a+1}. > Entry (2,2)=1+4=5.',f'What is top-left entry of [[{a},{b}],[1,2]]+[[{c},4],[3,5]]?',str(a+c),'Matrix addition is entrywise.')
    if kind=='functions':return (f'Let f(x)={a}x+{b}. Evaluate f({c}).',f'Substitute x={c}. > Multiply {a}×{c}. > Add {b} to get {a*c+b}.',f'If f(x)={b}x+{c}, calculate f({a}).',str(a*b+c),'Replace every x by the requested input.')
    if kind=='trig':return (f'Use the unit circle to evaluate sin(π/6).',f'π/6 radians is 30°. > Unit-circle y-coordinate is 1/2. > sin(π/6)=0.5.',f'What is sin(π/2)?','1','At 90° on the unit circle the y-coordinate is 1.')
    if kind=='vector':return (f'Add vectors ({a},{b}) and ({c},−{b}).',f'Add x-components: {a}+{c}={a+c}. > Add y-components: {b}−{b}=0. > Sum = ({a+c},0).',f'Find the x-component of ({a},{b})+({c},{c}).',str(a+c),'Add corresponding components.')
    if kind=='polar':return (f'Convert polar r={a}, θ=0 into x.',f'x=r cosθ. > cos(0)=1. > x={a}.',f'For polar r={b}, θ=π/2, what is the y-coordinate?',str(b),'y=r sinθ.')
    if kind=='limit':return (f'Evaluate lim x→{a} of (x+{b}).',f'The function x+{b} is continuous. > Substitute x={a}. > Limit = {a+b}.',f'Find lim x→{c} of (3x+{a}).',str(3*c+a),'Polynomials are continuous at finite inputs.')
    if kind=='derivative':return (f'Differentiate x³ and evaluate at x={a}.',f'Power rule gives d(x³)/dx=3x². > Substitute {a}. > Slope = 3×{a}² = {3*a*a}.',f'Find derivative of x² at x={b}.',str(2*b),'Differentiate first: 2x.')
    if kind=='applications_derivative':return (f'Position is s(t)={a}t². Find speed at t={c}.',f'Differentiate s to get v(t)={2*a}t. > Substitute t={c}. > v={2*a*c} distance units/time.',f'For s(t)={b}t², find velocity at t={c}.',str(2*b*c),'Velocity is the first derivative of position.')
    if kind=='integral':return (f'Integrate {a}x on [0,{c}].',f'Antiderivative is ({a}/2)x². > At {c}, evaluate {a}×{c}²/2. > The value is {a*c*c/2:.6f}.',f'Integrate {b}x from 0 to {c}.',str(b*c*c/2),'Use ∫kx dx = kx²/2 and evaluate bounds.')
    if kind=='ftc':return (f'Calculate ∫₀^{c} {a} dx.',f'An antiderivative of {a} is {a}x. > F({c})−F(0)={a*c}.',f'Calculate ∫₀^{c+1} {b} dx.',str(b*(c+1)),'Constant-height rectangle has area height × width.')
    if kind=='arc':return (f'Arc length of y={a}x on [0,{c}].',f'Derivative is constant {a}. > Length=∫₀^{c} √(1+{a*a})dx. > L={c}√{1+a*a}.',f'Length of y={b}x on [0,{c}]?',str(c*math.sqrt(1+b*b)),'Length of straight segment is width × sqrt(1+slope²).')
    if kind=='series':return (f'Infinite geometric series with first term {a} and ratio 1/2.',f'|r|=0.5<1, so it converges. > Sum=a/(1−r)={a}/(1−1/2)={2*a}.',f'Sum infinite series with first term {b}, ratio 1/2.',str(2*b),'Infinite geometric sum a/(1−r), only for |r|<1.')
    if kind=='parametric':return (f'x(t)=t², y(t)={a}t. Find dy/dx at t={c}.',f'dx/dt=2t, dy/dt={a}. > dy/dx={a}/(2t). > At t={c}, slope={a/(2*c):.6f}.',f'For x=t², y={b}t, find dy/dx at t={c}.',str(b/(2*c)),'Divide dy/dt by dx/dt.')
    if kind=='differential':return (f'Solve dy/dt={a}y with initial value y(0)={b}.',f'Separation gives ln|y|={a}t+C. > The initial condition sets scale {b}. > y(t)={b}e^({a}t).',f'If dy/dt={c}y, what is y′(0) for y(0)={b}?',str(b*c),'Use the differential equation at time zero.')
    if kind=='finance':return (f'Calculate one year of simple interest on ${a*100} at {c}% APR.',f'Convert rate to {c/100:g}. > Interest = {a*100}×{c/100:g}×1. > Earn ${a*c:.2f}.',f'Interest on ${b*100} at {c}% for one year?',str(b*c),'Simple interest is principal × annual rate × time.')
    return example_for('algebra',seed)

def make():
    per_grade=[];visual=[];families={}
    for grade,raw in enumerate(BANK):
        lessons=[];pos=0
        for line in raw.splitlines():
            if not line.strip():continue
            family,topics=line.strip().split(':',1)
            family=family.strip();assert family in FAMILIES,family
            for topic in topics.split(';'):
                topic=topic.strip()
                if not topic:continue
                pos+=1;seed=grade*10000+pos
                ex,steps,q,ans,hint=example_for(family,seed)
                objective,context=FAMILIES[family]
                lesson={'id':f'{grade}-expand-{pos}','gradeIndex':grade,'title':topic,'idea':f'{topic}: {objective} {context}',
                        'example':ex,'steps':steps.split(' > '),'question':q,'answer':ans,'hint':hint,
                        'duration':8 if grade<8 else 14,'family':family,'visualKey':f'g{grade+1:02}-t{pos:03}'}
                lessons.append(lesson)
                visual.append({'id':lesson['visualKey'],'lessonId':lesson['id'],'gradeIndex':grade,'topic':topic,'family':family,
                               'title':topic,'caption':context,'image':f'assets/visuals/{lesson["visualKey"]}.png',
                               'expression':{'linear':'x^2','quadratic':'x^2-4*x+3','trig':'sin(x)','integral':'x^2','derivative':'x^3','exp':'exp(x/3)','log':'ln(x)','rational':'1/(x-2)','series':'1/x','functions':'x^2','limit':'(x^2-4)/(x-2)'}.get(family,'')})
                families[family]=families.get(family,0)+1
        per_grade.append(lessons)
    return per_grade,visual,families

if __name__=='__main__':
    per_grade,visual,families=make()
    (ROOT/'js/expanded-curriculum.js').write_text('/** ATLAS supplemental authored learning topics + deterministic worked problems. */\nexport const EXTRA_LESSONS='+json.dumps(per_grade,ensure_ascii=False,separators=(',',':'))+';\n',encoding='utf8')
    (ROOT/'data/visuals.json').write_text(json.dumps(visual,ensure_ascii=False,separators=(',',':')),encoding='utf8')
    (ROOT/'data/curriculum-index.json').write_text(json.dumps({'counts':[len(a) for a in per_grade],'families':families,'lessons':[{'grade':i+1,'id':d['id'],'title':d['title'],'objective':d['idea'],'workedExample':d['example'],'steps':d['steps'],'practice':d['question'],'solution':d['answer'],'hint':d['hint']} for i,a in enumerate(per_grade) for d in a]},ensure_ascii=False,indent=2),encoding='utf8')
    print('Supplemental lessons',sum(map(len,per_grade)),'per grade',list(map(len,per_grade)),'visuals',len(visual))
