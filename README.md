
# 🕋Force-Displacement Hysteresis Curve Analysis Tool

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![PySide6](https://img.shields.io/badge/GUI-PySide6-orange.svg)](https://pypi.org/project/PySide6/)

### 📖 Documentation

[![English](https://img.shields.io/badge/🇺🇸_English-Click-blue?style=for-the-badge)](README.md)
[![简体中文](https://img.shields.io/badge/🇨🇳_简体中文-点击-red?style=for-the-badge)](README.zh-CN.md)
[![Русский](https://img.shields.io/badge/🇷🇺_Русский-Нажмите-Yellow?style=for-the-badge)](README.ru.md)

*A desktop application for analyzing force-displacement hysteresis curves from structural cyclic loading tests*

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [System Requirements](#-system-requirements)
- [Installation](#-installation)
- [Data Format Requirements](#-data-format-requirements)
- [Analysis Methods](#-analysis-methods)
- [Smoothing Algorithms](#-smoothing-algorithms)
- [Performance Metrics](#-performance-metrics)
- [Keyboard Shortcuts](#-keyboard-shortcuts)
- [FAQ](#-frequently-asked-questions)
- [Contributing](#-contributing)
- [Citation](#-citation)

---

## 🌟 Overview

This application is designed for researchers, engineers, and students working with structural testing data. It provides automated analysis of force-displacement hysteresis curves obtained from cyclic loading tests, commonly used in earthquake engineering, structural dynamics, and material testing.

### Capabilities

- **Automated Hysteresis Loop Detection**: Identifies and extracts individual loading cycles
- **Skeleton Curve Extraction**: Derives backbone curves using two different methods
- **Advanced Smoothing**: Seven interpolation algorithms
- **Comprehensive Metrics**: Calculates structural performance indicators
- **Ductility Analysis**: Seven different methods for ductility coefficient calculation

---

## ✨ Features

### 📊 Data Analysis Features

| Feature                           | Description                                                  |
| --------------------------------- | ------------------------------------------------------------ |
| **Hysteresis Loop Extraction**    | Automatically identifies and separates individual loading cycles from continuous test data |
| **Skeleton Curve Generation**     | Two methods: (1) Outer envelope tracing, (2) Peak point connection |
| **Direction-specific Analysis**   | Analyze positive direction, negative direction, or both simultaneously |
| **Data Filtering**                | Option to retain only the first loop at each displacement level (useful for repeated cycles) |
| **Peak Detection**                | Automatic identification of local maxima and minima          |
| **Starting Point Identification** | Intelligent detection of skeleton curve origin points        |

### 📈 Visualization Features

- **Dual Plot Modes**:
  - **Dot-Line Graph**: Original data points connected by lines
  - **Smooth Curve Graph**: Interpolated smooth curves using advanced algorithms

- **Interactive Controls**:
  - Mouse wheel zoom (centered on cursor position)
  - Pan and drag navigation
  - Full matplotlib toolbar integration
  - Reset view to original extents
  - Export graphs as high-resolution images

- **Customizable Display**:
  - Toggle original data points on/off
  - Adjustable interpolation point density (100-1000 points)
  - Color-coded positive/negative curves
  - Labeled peak points and starting points
  - Professional grid and axis formatting

### 🔧 Processing Algorithms

#### Seven Smoothing Methods:

1. **PCHIP** (Piecewise Cubic Hermite Interpolating Polynomial)
   - Shape-preserving interpolation
   - No overshoot or oscillations
   - Best for: Maintaining data trends

2. **Akima** (Akima Spline Interpolation)
   - Naturally smooth curves
   - Reduced oscillations compared to cubic splines
   - Best for: Reducing fluctuations while maintaining shape

3. **Bézier Curve**
   - Ultra-smooth presentation-quality curves
   - Adjustable control point density (10-100%)
   - Best for: Visualization and presentations

4. **B-spline** (Basis Spline)
   - Super smooth curves with adjustable parameters
   - May deviate from original points for smoothness
   - Best for: Maximum smoothness when exactness isn't critical

5. **Savitzky-Golay Filter**
   - Preserves features like peaks while smoothing
   - Adjustable window size (odd numbers)
   - Best for: Noise reduction while keeping important features

6. **UnivariateSpline**
   - General-purpose with adjustable smoothness factor
   - s=0 forces exact interpolation, larger s increases smoothness
   - Best for: Flexible smoothing needs

7. **CubicSpline**
   - Passes exactly through all data points
   - Continuous second derivative at knots
   - Best for: Exact interpolation with smooth transitions

### 🧮 Ductility Calculation Methods

Seven internationally recognized methods:

| Method                       | Description                           | Application                        |
| ---------------------------- | ------------------------------------- | ---------------------------------- |
| **Geometric Method**         | Based on 75% of peak force            | General structural analysis        |
| **Energy Method**            | Based on energy dissipation           | Energy-based design                |
| **Park Method**              | Stiffness-based degradation criterion | Seismic design (Park & Ang)        |
| **Farthest Point**           | Maximum distance from peak line       | Conservative estimates             |
| **ASCE Method**              | 60% of peak force criterion           | US seismic codes                   |
| **EEEP** (Equivalent Energy) | Energy equivalence principle          | Performance-based design           |
| **Elastic Yield**            | Initial stiffness intersection        | Traditional yield point definition |

### 📑 Report

Three detailed output tabs:

1. **Graphical Display**:
   - Hysteresis curves with color-coded loops
   - Skeleton curves (positive and negative)
   - Peak points marked with stars
   - Starting points highlighted
   - Interactive legend

2. **Performance Metrics Report**:
   - File information
   - Displacement-related metrics
   - Mechanical properties
   - Energy dissipation metrics
   - Damping coefficients
   - Degradation indicators
   - Ductility coefficients

3. **Loop-by-Loop Details**:
   - Individual loop properties table
   - Peak displacement and force for each loop
   - Loop area (energy dissipation)
   - Statistical summary

---

## 💻 Requirements

### Software Requirements

- **Operating System**:
  - Windows 10/11 (64-bit)
  - macOS 10.14 or later
  - Linux (Ubuntu 18.04+, Fedora 30+, or equivalent)

- **Python**: Version 3.7 or higher

### Required Python Packages

| Package    | Version | Purpose                                |
| ---------- | ------- | -------------------------------------- |
| numpy      | ≥1.19.0 | Numerical computations                 |
| pandas     | ≥1.1.0  | Data manipulation                      |
| PySide6    | ≥6.0.0  | GUI framework                          |
| matplotlib | ≥3.3.0  | Plotting and visualization             |
| scipy      | ≥1.5.0  | Scientific computing and interpolation |
| openpyxl   | ≥3.0.0  | Excel file support                     |

---

## 🚀 Installation

### Method 1: Using pip (Recommended)

#### Step 1: Install Python

Download and install Python 3.7+ from [python.org](https://www.python.org/downloads/)

**Important**: During installation, check "Add Python to PATH"

#### Step 2: Verify Installation

Open terminal/command prompt and verify:

```bash
python --version
# Should show: Python 3.7.x or higher
```

#### Step 3: Install Dependencies

```bash
# Navigate to project directory
cd path/to/HysAnalysis_MultiLang

# Install all required packages
pip install numpy pandas PySide6 matplotlib scipy openpyxl
```

Or use requirements file:

```bash
pip install -r requirements.txt
```

#### Step 4: Run the Application

```bash
python HysAnalysis_MultiLang.py
```

### Method 2: Using Conda (Alternative)

```bash
# Create a new environment
conda create -n hys_analysis python=3.9

# Activate environment
conda activate hys_analysis

# Install packages
conda install numpy pandas matplotlib scipy openpyxl
pip install PySide6

# Run application
python HysAnalysis_MultiLang.py
```

### Method 3: Portable Executable

***\*For Windows Users:\**** Can download the standalone executable file from the [Releases page](https://github.com/GarGarfie/HysAnalysis/releases).

*Standalone executable versions for Mac/Linux will be available in future releases.*

---

## 📁 Data Format Requirements

### Supported File Formats

| Format | Extension | Notes |
|--------|-----------|-------|
| Text | `.txt` | Space or tab-delimited |
| CSV | `.csv` | Comma-separated values |
| Excel | `.xls`, `.xlsx` | First sheet used |

### Data Structure

#### Required Columns (Minimum 2)

```
Column 1: Displacement (mm)
Column 2: Force (N or kN)
```

### Format Examples

#### Example 1: Space-Delimited Text File (`.txt`)
```
0.00      0.00
0.12      1.23
0.24      2.45
0.36      3.67
-0.15    -1.89
-0.30    -3.78
...
```

#### Example 2: Tab-Delimited Text File (`.txt`)
```
0.00	0.00
0.12	1.23
0.24	2.45
0.36	3.67
-0.15	-1.89
-0.30	-3.78
...
```

#### Example 3: CSV File (`.csv`)
```
0.00,0.00
0.12,1.23
0.24,2.45
0.36,3.67
-0.15,-1.89
-0.30,-3.78
...
```

#### Example 4: CSV with Headers (Headers Ignored)
```
Displacement_mm,Force_kN
0.00,0.00
0.12,1.23
0.24,2.45
...
```

#### Example 5: Excel File (`.xlsx`)
```
     A          B
1   0.00       0.00
2   0.12       1.23
3   0.24       2.45
4   0.36       3.67
5  -0.15      -1.89
6  -0.30      -3.78
...
```

### Data Requirements

✅ **Required**:
- At least 10 data points (preferably 100+)
- Two columns minimum
- Numeric values only (no text except optional headers)
- Chronological order (time sequence of test)

✅ **Recommended**:
- 200+ data points for smooth curves
- Consistent sampling rate
- Complete loading cycles (return to near-zero)
- Both positive and negative displacement

❌ **Not Supported**:
- Multiple headers or comment rows
- Non-numeric characters in data
- Missing values (NaN, blank cells)
- Date/time stamps in data columns

### Data Quality Tips

1. **Units**:
   - Displacement typically in mm
   - Force in N (or kN)
   - Mixed units will affect metric calculations

2. **Zero Point**:
   - First point should be near (0, 0)
   - If not, tool auto-adjusts displacement offset

3. **Noise**:
   - Small measurement noise is acceptable
   - Use smoothing algorithms if needed
   - Savitzky-Golay filter good for noisy data

4. **Sampling**:
   - Higher sampling rate = better curve detail
   - Recommended: >100 points per loop
   - Minimum: ~20 points per loop

### Preprocessing (Automatic)

The tool automatically:
- Removes duplicate displacement values (keeps max force)
- Adjusts zero point to first loading
- Filters near-zero values (< 0.1% of range)
- Sorts by displacement if needed

---

## 🔬 Analysis Methods

### Skeleton Curve Extraction

#### Method 1: Outer Envelope

**Algorithm**:
1. Start from origin (0, 0)
2. For positive direction:
   - Find first point where displacement increases
   - Track maximum displacement seen so far
   - Add point if displacement > previous max + threshold
3. Repeat for negative direction

**Characteristics**:
- Creates smooth, monotonically increasing curve
- Represents absolute maximum capacity
- Standard method in most codes
- Less sensitive to individual loop variations

**Best for**:
- Standard seismic analysis
- Code-based evaluations
- Comparing different specimens
- Reporting ultimate capacity



#### Method 2: Peak Points

**Algorithm**:
1. Identify all local maxima (peaks) in force-displacement data
2. For positive peaks:
   - Find crossing point on y-axis between 1st negative and 2nd positive peak
   - Connect this starting point to each successive positive peak
3. Repeat for negative peaks

**Characteristics**:
- Captures individual cycle behavior
- May show non-monotonic changes
- More detailed representation
- Sensitive to testing protocol

**Best for**:
- Detailed cycle-by-cycle analysis
- Studies of degradation patterns
- Research on cyclic behavior
- Non-standard loading protocols



### Ductility Coefficient Calculation Methods

Ductility (μ) = Ultimate Displacement / Yield Displacement

The key difference is how "yield displacement" is defined:

#### 1. Geometric Method

**Definition**: Yield at 75% of peak force

**Calculation**:

$$
F_{yield} = 0.75 \times F_{peak}
$$

$$
μ = D_{peak} / D_{yield}
$$

Where,

$F_{yield}$ — Yield load;

$F_{peak}$ — Peak load;

$D_{yield}$ — Yield displacement;

$D_{peak}$ — Peak displacement.

**Pros**:

- Simple and intuitive
- Widely used in practice
- Easy to reproduce

**Cons**:
- Arbitrary choice of 75%
- Doesn't consider energy or stiffness

**Typical Range**: 2-6 for well-designed structures



#### 2. Energy Method

**Definition**: Based on equal energy dissipation

**Calculation**:

$$
\text{Total Energy} = \text{Area under skeleton curve}
$$

$$
D_{yield} = \frac{2 \times \text{Total Energy}}{F_{peak}}
$$

$$
\mu = \frac{D_{peak}}{D_{yield}}
$$

Where,

 $\text{Total Energy}$ - Total energy dissipation;

 $D_{yield}$ — Yield displacement;

 $D_{peak}$ — Peak displacement;

 $F_{peak}$ — Peak load;

 $\mu$ — Ductility ratio.

**Pros**:

- Energy-based (physically meaningful)
- Accounts for overall behavior

**Cons**:

- May give higher values than geometric
- Sensitive to curve shape

**Typical Range**: 3-8



#### 3. Park Method

**Definition**: Stiffness degradation to 1/3 of initial

**Calculation**:

$$
K_{initial} = \text{Initial slope of skeleton curve}
$$

$$
K_{yield} = \frac{K_{initial}}{3}
$$

$$
\text{Find displacement $D_{yield}$ where current stiffness equals $K_{yield}$}
$$

$$
\mu = \frac{D_{peak}}{D_{yield}}
$$

Where,

$K_{initial}$ — Initial stiffness;

$K_{yield}$ — Yield stiffness (1/3 of initial);

$D_{yield}$ — Yield displacement;

$D_{peak}$ — Peak displacement;

$\mu$ — Ductility ratio.

**Pros**:

- Based on stiffness degradation
- Commonly used in seismic research
- Park & Ang damage model compatibility

**Cons**:
- Requires clear initial linear region
- May be conservative

**Reference**: Park, Y., & Ang, A. H. ‐S. (1985). Mechanistic Seismic Damage Model for Reinforced Concrete. Journal of Structural Engineering, 111(4), 722–739. [https://doi.org/10.1061/(asce)0733-9445(1985)111:4(722)](https://doi.org/10.1061/(asce)0733-9445(1985)111:4(722))

**Typical Range**: 2-5



#### 4. Farthest Point Method

**Definition**: Point farthest from line connecting origin to peak

**Calculation**:

Define line from origin $(0, 0)$ to peak point $(D_{peak}, F_{peak})$

For each point $(D_i, F_i)$ on skeleton curve, calculate perpendicular distance:

$$
d_i = \frac{|F_{peak} \cdot D_i - D_{peak} \cdot F_i|}{\sqrt{D_{peak}^2 + F_{peak}^2}}
$$

$$
D_{yield} = D_i \text {  at } \max(d_i)
$$

$$
\mu = \frac{D_{peak}}{D_{yield}}
$$

Where,

$D_i$ — Displacement of point $i$;

$F_i$ — Force of point $i$;

$d_i$ — Perpendicular distance from point $i$ to line;

$D_{yield}$ — Yield displacement (at maximum distance);

$D_{peak}$ — Peak displacement;

$F_{peak}$ — Peak force;

$\mu$ — Ductility ratio.

**Pros**:

- Geometric interpretation of yielding
- Identifies clear transition point
- Independent of arbitrary thresholds

**Cons**:
- Can be affected by data noise
- May need smoothing first

**Typical Range**: 3-7



#### 5. ASCE Method

**Definition**: Yield at 60% of peak force

**Calculation**:

$$
F_{yield} = 0.60 \times F_{peak}
$$

$$
\text{Find displacement where } F = F_{yield}
$$

$$
\mu = \frac{D_{peak}}{D_{yield}}
$$

Where,

$F_{yield}$ — Yield load;

$F_{peak}$ — Peak load;

$D_{yield}$ — Yield displacement;

$D_{peak}$ — Peak displacement;

$\mu$ — Ductility ratio.

**Pros**:

- Based on US seismic codes
- Standard for ASCE 41 evaluations
- More conservative than geometric

**Cons**:
- Still arbitrary threshold
- Different from other international codes

**Reference**: ASCE 41-17 (2017). Seismic Evaluation and Retrofit of Existing Buildings. American Society of Civil Engineers. [https://doi.org/10.1061/9780784414859](https://doi.org/10.1061/9780784414859)

**Typical Range**: 2-5



#### 6. EEEP (Equivalent Energy Elastic-Plastic)

**Definition**: Bilinear curve with equal energy

**Calculation**:

$$
E_{actual} = \text{Area under skeleton curve}
$$

Construct bilinear curve with:

- Elastic branch: $(0, 0) \to (D_{yield}, F_{peak})$
- Plastic plateau: $F = F_{peak}$ from $D_{yield}$ to $D_{peak}$

Adjust $D_{yield}$ until: $E_{bilinear} = E_{actual}$

$$
\mu = \frac{D_{peak}}{D_{yield}}
$$

Where,

$E_{actual}$ — Energy under actual skeleton curve;

$E_{bilinear}$ — Energy under equivalent bilinear curve;

$D_{yield}$ — Yield displacement (adjusted for energy equivalence);

$D_{peak}$ — Peak displacement;

$F_{peak}$ — Peak force;

$\mu$ — Ductility ratio.

**Pros**:

- Energy equivalence (FEMA standard)
- Commonly used in performance-based design
- Accounts for post-yield behavior

**Cons**:
- Requires iteration
- More computationally intensive

**Reference**: FEMA 356, ATC-40

**Typical Range**: 3-6



#### 7. Elastic Yield Method

**Definition**: Intersection of initial stiffness line with peak force

**Calculation**:

$$
K_{initial} = \text{Initial elastic slope}
$$

$$
D_{yield} = \frac{F_{peak}}{K_{initial}}
$$

$$
\mu = \frac{D_{peak}}{D_{yield}}
$$

Where,

$K_{initial}$ — Initial elastic stiffness;

$F_{peak}$ — Peak force;

$D_{yield}$ — Yield displacement;

$D_{peak}$ — Peak displacement;

$\mu$ — Ductility ratio.

**Pros**:

- Simplest method
- Based on elastic assumption
- Clear physical meaning

**Cons**:
- Often underestimates ductility
- Ignores actual yielding behavior
- Very conservative

**Typical Range**: 1.5-4



### Method Comparison Table

| Method | Complexity | Conservatism | Best Application |
|--------|-----------|--------------|------------------|
| Geometric | Low | Medium | General analysis |
| Energy | Medium | Low | Design optimization |
| Park | Medium | High | Damage assessment |
| Farthest | Medium | Medium | Research |
| ASCE | Low | High | Code compliance (US) |
| EEEP | High | Medium | Performance-based design |
| Elastic | Low | Very High | Quick estimates |

---

## 🎨 Smoothing Algorithms

### Algorithm Selection Guide

*Using the peak point connection method to draw curves can achieve better smoothing results.*

```
Need Smoothing?
  ├─ Yes → Primary Goal?
  │         ├─ Exact Data → CubicSpline
  │         ├─ Preserve Shape → PCHIP or Akima
  │         ├─ Max Smooth → Bézier or BSpline
  │         ├─ Reduce Noise → Savitzky-Golay
  │         └─ Flexible → UnivariateSpline
  └─ No → Use Dot-Line
```

### Detailed Algorithm Descriptions

#### 1. PCHIP (Piecewise Cubic Hermite)

**Mathematical Basis**: Piecewise cubic polynomials with continuous first derivative

**Properties**:

- Shape-preserving (monotonicity maintained)
- No overshoot between points
- Local support (changing one point affects only nearby segments)

**When to Use**:

- Data with monotonic segments
- When overshoot is unacceptable
- Structural testing data (physically realistic)

#### 2. Akima Spline

**Mathematical Basis**: Modified cubic spline with local curvature estimation

**Properties**:
- Less oscillation than standard cubic splines
- More natural-looking curves
- Local support

**When to Use**:
- Data with gentle curves
- When you want natural smoothness
- Avoiding oscillations near peaks

#### 3. Bézier Curve

**Mathematical Basis**: Bernstein polynomial parametric curves

**Properties**:
- Extremely smooth
- Doesn't necessarily pass through all points
- Adjustable via control points

**When to Use**:
- Presentation graphics
- Publication-quality figures
- When aesthetic smoothness > accuracy

**Parameters**: 
- Control Point Density (10-100%)
  - 10%: Ultra smooth, may deviate significantly
  - 50%: Balanced
  - 100%: Closer to original data

**Recommended Settings**:
- Presentations: 20-30%
- Technical reports: 40-60%
- Data verification: 80-100%

#### 4. B-spline

**Mathematical Basis**: Basis spline with smoothness parameter

**Properties**:
- Very smooth curves
- Controlled deviation from points
- Adjustable smoothness

**When to Use**:
- Need maximum smoothness
- Acceptable to deviate from exact points
- Artistic rendering

#### 5. Savitzky-Golay Filter

**Mathematical Basis**: Least-squares polynomial fitting in moving window

**Properties**:
- Preserves features (peaks, valleys)
- Reduces high-frequency noise
- Maintains peak positions

**When to Use**:
- Noisy data
- Need to preserve peak locations
- Signal processing applications

#### 6. UnivariateSpline

**Mathematical Basis**: Smoothing spline with adjustable parameter

**Properties**:
- Balance between smoothness and fit
- Widely applicable
- Adjustable trade-off

**When to Use**:
- General-purpose smoothing
- When you want fine control
- Default choice for most cases

#### 7. CubicSpline

**Mathematical Basis**: Cubic polynomials with continuous second derivative

**Properties**:
- Passes exactly through all points
- Smooth transitions
- May oscillate between points

**When to Use**:
- Need exact interpolation
- Trust all data points
- Want smooth derivatives

---

## 📊 Performance Metrics

### Metric Categories and Definitions

#### 1. Displacement-Related Metrics

##### Peak Displacement (D<sub>max</sub>)

**Definition**: Maximum absolute displacement reached during test

$$
D_{max,positive} = max (displacement)
$$

$$
D_{max,negative} = min (displacement)
$$



##### Residual Deformation (D<sub>res</sub>)

**Definition**: Permanent displacement after load removal

$$
D_{res} = displacemnet_{\text{final point}}
$$

#### 2. Mechanical Properties

##### Peak Load (F<sub>max</sub>)

**Definition**: Maximum force during test

$$
F_{max,positive} = max (Force)
$$

$$
F_{max,negative} = min (Force)
$$

##### Initial Stiffness (K<sub>0</sub>)

**Definition**: Slope of initial linear elastic region

$$
K_0 = ΔF / ΔD \text{ (first ~5-10 percent of data)}
$$

**Calculation Method**:

- Take first 5-20 data points (or first 10% of data)
- Exclude points near zero (noise threshold)
- Linear regression to find slope

##### Secant Stiffness (K<sub>sec</sub>)

**Definition**: Slope from origin to peak point

$$
K_{sec} = F_{max} / D_{max}
$$

**Relationship**:

$K_{sec} < K_{0}$ (always, due to damage/yielding)

Ratio $K_{sec}/K_{0}$ indicates degradation

#### 3. Energy Metrics

##### Total Hysteresis Loop Area (E<sub>total</sub>)

**Definition**: Sum of areas enclosed by all hysteresis loops

**Formula**:

$$
E_{total} = \sum_{i=1}^{n} A_i
$$

$$
A_i = \oint F \, dD \text{ (line integral for loop } i\text{)}
$$

$$
A_i = \sum_{j=1}^{m-1} \frac{1}{2}(F_j + F_{j+1})(D_{j+1} - D_j)
$$

Where,

$E_{total}$ — Total hysteresis energy;

$A_i$ — Area of loop $i$;

$n$ — Number of loops;

$F$ — Force;

$D$ — Displacement;

$m$ — Number of data points in loop.

##### Cumulative Energy Dissipation

**Definition**: Same as total hysteresis loop area

$$
E_{cumulative} = E_{total}
$$

##### Average Loop Energy (E<sub>avg</sub>)

**Definition**: Mean energy per loop

$$
E_{avg} = \frac{E_{total}}{n_{loops}}
$$

Where,

$E_{avg}$ — Average loop energy;

$E_{total}$ — Total hysteresis energy;

$n_{loops}$ — Number of loops.

##### Maximum Loop Energy (E<sub>max</sub>)

**Definition**: Largest single loop area

$$
E_{max} = \max(A_i) \text{ for all } i
$$

Where,

$E_{max}$ — Maximum loop energy;

$A_i$ — Area of loop $i$.

##### Equivalent Viscous Damping Coefficient (ξ<sub>eq</sub>)

**Definition**: Ratio of dissipated to elastic strain energy

$$
\xi_{eq} = \frac{E_{dissipated}}{2\pi \times E_{elastic}}
$$

$$
E_{elastic} = \frac{1}{2} D_{max} F_{max}
$$

Where,

$\xi_{eq}$ — Equivalent viscous damping ratio;

$E_{dissipated}$ — Area of hysteresis loop;

$E_{elastic}$ — Elastic strain energy (triangle area);

$D_{max}$ — Maximum displacement;

$F_{max}$ — Maximum force.

**Units**: Dimensionless (often expressed as %)

**Reference**: Often compared to 5% damping (common design assumption)

#### 4. Degradation Metrics

##### Strength Degradation (SD)

**Definition**: Percentage decrease in force capacity

$$
SD_{positive} = \frac{F_{first} - F_{last}}{F_{first}} \times 100\%
$$

$$
SD_{negative} = \frac{F_{first} - F_{last}}{F_{first}} \times 100\%
$$

Where,

$SD_{positive}$ — Strength degradation in positive direction;

$SD_{negative}$ — Strength degradation in negative direction;

$F_{first}$ — Peak force in first loop;

$F_{last}$ — Peak force in last loop.

##### Stiffness Degradation (KD)

**Definition**: Percentage decrease in stiffness

$$
KD = \frac{K_{initial} - K_{secant}}{K_{initial}} \times 100\%
$$

Where,

$KD$ — Stiffness degradation;

$K_{initial}$ — Initial stiffness;

$K_{secant}$ — Secant stiffness.

**Interpretation**:

- Higher = more damage/yielding
- Lower = more elastic behavior

**Note**: High stiffness degradation is EXPECTED and ACCEPTABLE for ductile design

#### 5. Ductility Coefficient (μ)

**Definition**: Ratio of ultimate to yield displacement

**Units**: Dimensionless

**Methods**: See [Ductility Methods](#ductility-coefficient-calculation-methods) section

### Metric Relationships

```
Energy Dissipation ↔ Equivalent Damping
    ↕
Ductility ↔ Force Reduction Factor
    ↕
Degradation ← Cumulative Damage
```

### Quality Indicators

Good Seismic Performance:
- ✓ High ductility
- ✓High energy dissipation
- ✓High equivalent damping 
- ✓ Moderate strength degradation
- ✓ Acceptable residual deformation

Poor Performance:
- ✗ Low ductility
- ✗ Low energy dissipation
- ✗ Severe strength degradation
- ✗ Large residual deformation
- ✗ Sudden failure (no plateau in skeleton curve)

---

## ⌨️ Keyboard Shortcuts

| Shortcut | Action | Context |
|----------|--------|---------|
| **Delete** | Delete selected file | When file is selected in list |
| **Ctrl + Z** | Undo last operation | File management operations |
| **Ctrl + A** | Select all text | In text result panels |
| **Ctrl + C** | Copy text | In text result panels |
| **Ctrl + S** | Save figure | When graph is active (matplotlib) |
| **Ctrl + Home** | Reset graph view | When graph is active |

### Matplotlib Toolbar Shortcuts

| Key | Action |
|-----|--------|
| **Home / H** | Reset original view |
| **Left Arrow** | Previous view |
| **Right Arrow** | Next view |
| **P** | Pan/Zoom mode |
| **O** | Zoom to rectangle |
| **S** | Save figure |
| **G** | Toggle grid |
| **L** | Toggle log/linear Y-axis |
| **K** | Toggle log/linear X-axis |

---

## ❓ Frequently Asked Questions

### General Questions

**Q1: What types of tests is this tool suitable for?**

A: Any cyclic loading test producing force-displacement data:
- Quasi-static cyclic tests
- Pseudodynamic tests
- Slow cyclic tests (not high-rate dynamic)
- Structural components: beams, columns, walls, connections
- Materials: concrete, steel, timber, composites
- Devices: dampers, isolators, energy dissipators

NOT suitable for:
- High-speed impact tests
- True dynamic tests (frequency-dependent)
- Non-mechanical tests

---

**Q2: Can I analyze force-deformation data in different units?**

A: Yes, but:
- Tool assumes displacement in **mm** and force in **N**
- If using different units:
  * Metric values will be in your input units
  * Labels still show "mm" and "N" (cosmetic only)
  * You're responsible for interpreting results
- Recommended: Convert to mm and N before import

---

**Q3: How many data points do I need?**

A: 
- **Minimum**: ~50 points total, ~10 per loop
- **Recommended**: 200+ points total, 30+ per loop
- **Ideal**: 500+ points total, 50+ per loop

More points = smoother curves, more accurate metrics

---

**Q4: Can I analyze monotonic (push-over) tests?**

A: Partially:
- Tool will load data and plot
- Skeleton curve can be extracted
- Peak load and stiffness calculated
- BUT: No hysteresis loops (requires cyclic loading)
- Energy metrics will be zero or inaccurate
- Better to use specialized pushover analysis tools

---

### Technical Questions

**Q5: Why do different smoothing algorithms give different results?**

A: Algorithms have different mathematical properties:
- Some preserve peaks (SG filter, PCHIP)
- Some prioritize smoothness (Bézier, B-spline)
- Some pass exactly through points (Cubic)
- Trade-off: Smoothness ↔ Accuracy

For analysis: Use PCHIP or minimal smoothing
For presentation: Use Bézier with moderate settings

---

**Q6: My ductility values differ from hand calculations. Why?**

A: Common reasons:
1. **Different yield point definition**: Your method vs. software method
2. **Data preprocessing**: Tool auto-filters near-zero values
3. **Skeleton curve extraction**: Manual vs. automatic peak detection
4. **Rounding**: Display rounds to 2-4 decimals

To verify:
- Check intermediate values (yield displacement, ultimate displacement)
- Try different ductility methods

---

**Q7: Can I export numerical data (not just graphs)?**

A: Currently:
- Graphs: Yes (PNG, PDF, SVG via toolbar)
- Text reports: Copy from Tab 2 & 3 (Ctrl+C)
- Numerical data: No direct CSV export

Workaround:
- Copy text report
- Paste into Excel
- Use "Text to Columns" feature

Future feature: Direct CSV/Excel export planned

---

**Q8: Does the tool account for P-Delta effects?**

A: No. Tool analyzes data as-is.
- If your test data includes P-Delta, results reflect total behavior
- If you want pure component response, apply P-Delta correction before import
- Separation of P-Delta from component behavior is user's responsibility

---

**Q9: Can I analyze tests with asymmetric loading?**

A: Yes:
- Tool handles positive and negative directions independently
- Metrics calculated separately when appropriate
- Use "Direction" setting to focus on one direction if needed
- Asymmetry is captured in separate positive/negative metrics

---

**Q10: What if my test started at pre-load (not zero)?**

A: Tool auto-adjusts:
- Detects first "loading" point
- Subtracts offset to shift displacement to zero origin
- Force offset handled if appropriate
- Check starting points in Tab 2 report

If adjustment is incorrect:
- Manually adjust your data before import
- Ensure first point is at or near zero

---

### Data Questions

**Q11: My data file has 3+ columns. Which are used?**

A: Only first two columns:
- Column 1: Displacement
- Column 2: Force
- Columns 3+: Ignored

Ensure correct column order in your file

---

**Q12: Can I import data from ABAQUS/ANSYS/SAP2000?**

A: If you export to CSV/TXT format, yes:

**ABAQUS**:
```
1. Results → Field Output → Create XY Data
2. Select displacement and force
3. Save XY Data → ASCII format
```

**SAP2000**:
```
1. Display → Show Tables
2. Select joint displacement and forces
3. Export → CSV
```

**ANSYS**:
```
1. POST1 → List Results → Nodal Solution
2. Write to file → displacement, force
3. Format as space-delimited text
```

Then import the exported file

---

**Q13: My test was in inches and kips. Do I need to convert?**

A: Recommended: Yes, convert to mm and N

If you don't convert:
- Metrics will be in your units (ips, in)
- Labels will say "N" and "mm" (misleading)
- No calculation errors, just unit label mismatch

Conversion:
```
1 ip = 4.448 N
1 inch = 25.4 mm
```

---

### Error Questions

**Q14: I get "Smoothing interpolation failed". What to do?**

A: This means the algorithm couldn't process your data

Try:
1. **Switch algorithm**: Try PCHIP or Akima (most robust)
2. **Reduce points**: Lower interpolation points to 100
3. **Check data**: Remove duplicate x-values, ensure sorted
4. **Disable smoothing**: Use Dot-Line plot instead

If persists: Your data may have structure incompatible with that algorithm

---

**Q15: Why are there no hysteresis loops detected?**

A: Requirements for loop detection:
1. Data must have "peaks" (local maxima)
2. Displacement must reverse direction
3. At least 3 points per loop
4. Sufficient displacement range (> 0.1% of max)

Check:
- Is test cyclic? (Not monotonic)
- Are there clear peaks?
- Is displacement varying?

View Tab 1 graph to visually inspect

---

### Usage Questions

**Q16: Can I use this tool for my thesis/publication?**

A: Yes! This is open-source software

Please cite as:
```
[S. Xiao]. (2025). HysAnalysis. Force-Displacement Hysteresis Curve Analysis Tool. 
GitHub repository: [https://github.com/GarGarfie/HysAnalysis]
```

Also mention:
- Software version
- Analysis methods used
- Any customizations made

---

**Q17: Can I modify the code?**

A: Yes, it's open-source

Common modifications:
- Add new ductility methods
- Customize metric calculations
- Add export formats
- Integrate with other tools

If you improve it, consider contributing back!

---

## 🤝 Contributing

We welcome contributions!

### Ways to Contribute

1. **Report Bugs**:
   - Open an issue with detailed description
   - Include sample data if possible
   - Specify Python version, OS

2. **Suggest Features**:
   - Open an issue with "Feature Request" tag
   - Explain use case
   - Provide examples

3. **Improve Documentation**:
   - Fix typos
   - Add examples
   - Translate to new languages

4. **Code Contributions**:
   - Fork repository
   - Create feature branch
   - Make changes
   - Submit pull request

---

## 📚 Citation

If you use this tool in your research, please cite:

```bibtex
@software{HysAnalysis,
  author = {[S. Xiao]},
  title = {Force-Displacement Hysteresis Curve Analysis Tool},
  year = {2025},
  publisher = {GitHub},
  url = {[https://github.com/GarGarfie/HysAnalysis]}
}
```

You can also use open source reference managers such as [**Zotero**](https://github.com/zotero/zotero) to directly capture the citation from this page.

---

## 🙏 Acknowledgments

This tool uses the following open-source libraries:
- **NumPy**: Numerical computing
- **Pandas**: Data manipulation
- **PySide6**: GUI framework (Qt for Python)
- **Matplotlib**: Visualization
- **SciPy**: Scientific computing

---

**[⬆ Back to Top](#force-displacement-hysteresis-curve-analysis-tool)**


---

Made with ❤️ for the structural engineering community
