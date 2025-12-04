
# 🔬 Force-Displacement Hysteresis Curve Analysis Tool

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![PySide6](https://img.shields.io/badge/GUI-PySide6-orange.svg)](https://pypi.org/project/PySide6/)

### 📖 Multi-language Documentation

[![English](https://img.shields.io/badge/🇺🇸_English-Click-blue?style=for-the-badge)](README.md)
[![简体中文](https://img.shields.io/badge/🇨🇳_简体中文-点击-red?style=for-the-badge)](README.zh-CN.md)
[![Русский](https://img.shields.io/badge/🇷🇺_Русский-Нажмите-Yellow?style=for-the-badge)](README.ru.md)

*A comprehensive desktop application for analyzing force-displacement hysteresis curves from structural cyclic loading tests*

[Features](#-features) • [Installation](#-installation) • [Quick Start](#-quick-start) • [User Guide](#-detailed-user-guide) • [Documentation](#-documentation)

</div>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [System Requirements](#-system-requirements)
- [Installation](#-installation)
- [Quick Start](#-quick-start)
- [Detailed User Guide](#-detailed-user-guide)
- [Data Format Requirements](#-data-format-requirements)
- [Analysis Methods](#-analysis-methods)
- [Smoothing Algorithms](#-smoothing-algorithms)
- [Performance Metrics](#-performance-metrics)
- [Keyboard Shortcuts](#-keyboard-shortcuts)
- [Troubleshooting](#-troubleshooting)
- [Example Workflows](#-example-workflows)
- [FAQ](#-frequently-asked-questions)
- [Contributing](#-contributing)
- [License](#-license)
- [Citation](#-citation)

---

## 🌟 Overview

This application is designed for researchers, engineers, and students working with structural testing data. It provides automated analysis of force-displacement hysteresis curves obtained from cyclic loading tests, commonly used in earthquake engineering, structural dynamics, and material testing.

### Key Capabilities

- **Automated Hysteresis Loop Detection**: Identifies and extracts individual loading cycles
- **Skeleton Curve Extraction**: Derives backbone curves using two different methods
- **Advanced Smoothing**: Seven state-of-the-art interpolation algorithms
- **Comprehensive Metrics**: Calculates 15+ structural performance indicators
- **Ductility Analysis**: Seven different methods for ductility coefficient calculation
- **Multi-language Interface**: Full support for English, Chinese, and Russian
- **Interactive Visualization**: Mouse-driven zoom, pan, and navigation

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

### 🌍 Multi-language Support

- **Interface Language**: Switchable between English, Chinese (Simplified), and Russian
- **Dynamic Translation**: All UI elements, labels, and output reports update instantly
- **Font Optimization**: Automatic font selection based on language for proper character display
- **Number Formatting**: Culturally appropriate number and decimal formatting

### 📑 Comprehensive Reporting

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

## 💻 System Requirements

### Hardware Requirements

- **Minimum**:
  - CPU: 1.5 GHz dual-core processor
  - RAM: 4 GB
  - Display: 1280×720 resolution
  - Storage: 500 MB available space

- **Recommended**:
  - CPU: 2.5 GHz quad-core processor
  - RAM: 8 GB or more
  - Display: 1920×1080 or higher
  - Storage: 1 GB available space

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

### Method 3: Portable Executable (Future Release)

*Standalone executable versions for Windows/Mac will be available in future releases.*

---

## 🎯 Quick Start

### 5-Minute Getting Started

1. **Launch the Application**
   ```bash
   python HysAnalysis_MultiLang.py
   ```

2. **Import Your Data**
   - Click **"Import"** button (top-left panel)
   - Select your data file(s) (`.txt`, `.csv`, or `.xlsx`)
   - File appears in the list

3. **Select a File**
   - Click on the filename in the list
   - Data loads automatically
   - Initial analysis appears

4. **View Results**
   - **Tab 1**: See hysteresis curve and skeleton curves
   - **Tab 2**: Read performance metrics
   - **Tab 3**: Review individual loop details

5. **Customize Analysis** (Optional)
   - Choose skeleton curve method
   - Select ductility calculation method
   - Apply smoothing if desired

### First-time User Workflow

```
Start → Import Data → Select File → View Default Analysis → 
  ↓
Satisfied? 
  Yes → Export Results → End
  No → Adjust Settings → Update Analysis → (loop back to Satisfied?)
```

---

## 📖 Detailed User Guide

### Interface Overview

The application window is divided into two main sections:

```
┌─────────────────────────────────────────────────────────────┐
│  Force-Displacement Curve Analysis Tool                      │
├──────────────────┬────────────────────────────────────────────┤
│  Control Panel   │  Display Area                              │
│                  │                                            │
│  • Language      │  Tab 1: [Graph]                            │
│  • File Mgmt     │  ┌──────────────────────────────────────┐ │
│  • Plot Style    │  │                                      │ │
│  • Skeleton      │  │     Hysteresis Curve                 │ │
│  • Direction     │  │     + Skeleton Curves                │ │
│  • Ductility     │  │                                      │ │
│  • Filtering     │  └──────────────────────────────────────┘ │
│                  │                                            │
│                  │  Tab 2: [Metrics Report]                   │
│                  │  Tab 3: [Loop Details]                     │
└──────────────────┴────────────────────────────────────────────┘
```

### Left Panel: Control Panel

#### 1. Language Selection

```
┌──────────────────────┐
│ Language             │
├──────────────────────┤
│ [English     ▼]      │
└──────────────────────┘
```

- **Options**: English, Русский (Russian), 中文 (Chinese)
- **Effect**: Changes entire interface, labels, and reports
- **Real-time**: Updates immediately without restart

#### 2. File Management

```
┌──────────────────────┐
│ File Management      │
├──────────────────────┤
│ [Import] [Clear]     │
│                      │
│ ┌──────────────────┐ │
│ │ data1.txt        │ │
│ │ data2.csv        │ │
│ │ test_results.xlsx│ │
│ └──────────────────┘ │
│                      │
│ Shortcut: "Delete"   │
└──────────────────────┘
```

**Operations**:
- **Import**: Add one or multiple files
  - Supports multi-selection (Ctrl+Click or Cmd+Click)
  - Filters by supported formats
  - Duplicates are automatically prevented

- **Clear**: Remove all files from list
  - Requires confirmation
  - Clears current analysis

- **Select**: Click filename to load and analyze
  - Automatically triggers analysis
  - Previous analysis is saved for undo

- **Delete**: Select file and press Delete key
  - Removes from list only (original file untouched)
  - Clears analysis if currently displayed file

#### 3. Plot Style

```
┌──────────────────────────────────┐
│ Plot Style                       │
├──────────────────────────────────┤
│ ○ Dot-Line Graph                 │
│ ● Spline Connected Graph         │
│                                  │
│   Smoothing algorithm:           │
│   [PCHIP - Shape-pres...  ▼]     │
│                                  │
│   [Algorithm description box]    │
│                                  │
│   Smoothness parameter:          │
│   Value:    [1.00]               │
│   Slider:   [━━━○━━━━━━]         │
│   Current value: 1.00            │
│                                  │
│   Preset: [None][Low][Med][Hi]   │
│                                  │
│   Points: [300    ▼]             │
│   ☑ Show original data points    │
└──────────────────────────────────┘
```

**Dot-Line Graph**:
- Shows original data as-is
- Points connected by straight lines
- No processing or interpolation
- Fastest rendering

**Spline Connected Graph**:
- Applies smoothing algorithm
- Creates visually appealing curves
- Useful for presentations
- Adjustable parameters

**Smoothing Controls** (only when Spline selected):

a) **Algorithm Dropdown**:
   - Lists all 7 algorithms
   - Hover for brief description
   - Description box updates below

b) **Smoothness Parameter** (visibility depends on algorithm):
   - **Bézier**: Control point density (10-100%)
     - 10% = ultra smooth, 100% = follows data closely
     - Recommended: 20-40%
   - **B-spline**: Smoothness factor s (0.0-10.0)
     - 0 = exact interpolation, higher = smoother
   - **Savitzky-Golay**: Window size (3-51, odd numbers only)
     - Larger = smoother but may lose features
   - **UnivariateSpline**: Smoothness factor s (0.0-10.0)
     - Similar to B-spline
   - **PCHIP, Akima, CubicSpline**: No parameter (auto-hidden)

c) **Preset Buttons**:
   - Quick access to common values
   - None (0.0), Low (2.5), Medium (5.0), High (7.5), Very High (10.0)
   - Only affects algorithms with adjustable parameters

d) **Interpolation Points**:
   - Number of points in smoothed curve
   - Options: 100, 200, 300, 500, 1000
   - More points = smoother appearance, slower rendering
   - Default: 300 (good balance)

e) **Show Original Data Points**:
   - Overlays raw data points on smooth curve
   - Helps verify smoothing accuracy
   - Useful for quality checking

#### 4. Skeleton Curve Extraction Method

```
┌──────────────────────────────────┐
│ Skeleton curve extraction method │
├──────────────────────────────────┤
│ ● Method 1: Outer Envelope       │
│ ○ Method 2: Peak Points          │
└──────────────────────────────────┘
```

**Method 1: Outer Envelope**
- Traces the outermost boundary of all loops
- Incrementally finds maximum displacement points
- Suitable for:
  - Data with consistent loading protocols
  - When you want the absolute maximum response
  - Standard backbone curve generation

**Method 2: Peak Points**
- Connects successive peak points in each loop
- Identifies local maxima/minima
- More sensitive to individual cycle characteristics
- Suitable for:
  - Data with varying displacement levels
  - When each cycle's peak is important
  - Protocols with non-monotonic displacement increase

**Comparison Example**:
```
Force
  │     Method 1          Method 2
  │        *                 *
  │       /│\               /│\
  │      / │ \             / │ \
  │     *  │  *           *  *  *
  │    /   │   \         /   │   \
  │   /    │    \       /    │    \
  └──────────────────────────────── Displacement
```

#### 5. Skeleton Curve Analysis Direction

```
┌──────────────────────────────────┐
│ Skeleton curve analysis direction│
├──────────────────────────────────┤
│ ● All directions                 │
│ ○ Positive direction only        │
│ ○ Negative direction only        │
└──────────────────────────────────┘
```

- **All directions**: Analyzes both positive and negative displacement
  - Default and recommended for symmetric analysis
  - Provides complete picture
  - Calculates metrics for both directions

- **Positive direction only**: Only positive displacement side
  - Useful for asymmetric structures
  - Focuses on push direction
  - Reduces visual clutter

- **Negative direction only**: Only negative displacement side
  - Useful for asymmetric structures
  - Focuses on pull direction
  - Alternative perspective

#### 6. Ductility Coefficient Calculation Method

```
┌──────────────────────────────────┐
│ Ductility coefficient calculation│
├──────────────────────────────────┤
│ ● Geometric Method               │
│ ○ Energy Method                  │
│ ○ Park Method                    │
│ ○ Farthest Point                 │
│ ○ ASCE Method                    │
│ ○ EEEP Method                    │
│ ○ Elastic Yield                  │
└──────────────────────────────────┘
```

See [Ductility Methods](#ductility-coefficient-methods) section for detailed explanations.

#### 7. Data Filtering Options

```
┌──────────────────────────────────┐
│ Data filtering options           │
├──────────────────────────────────┤
│ ☑ Only retain the first loop of  │
│   the same displacement level    │
└──────────────────────────────────┘
```

**Purpose**: Many testing protocols repeat cycles at the same displacement level (e.g., 3 cycles at ±10mm, 3 cycles at ±20mm)

**When enabled**:
- Keeps only the first cycle at each displacement level
- Removes subsequent repetitions
- Reduces data clutter
- Focuses on fresh response (before degradation within same level)

**When disabled**:
- Keeps all cycles
- Shows degradation within same displacement level
- More complete data representation
- May result in overlapping curves

**Example**:
```
Test Protocol: 3 cycles at each level
Without filter: 10mm, 10mm, 10mm, 20mm, 20mm, 20mm, 30mm...
With filter:    10mm, 20mm, 30mm...
```

### Right Panel: Display Area

#### Tab 1: Hysteresis Curve and Backbone Curve

**Toolbar** (Top of graph):
```
[Home] [Back] [Forward] [Pan] [Zoom] [Configure] [Save]
```

- **Home** 🏠: Reset view to original extents
- **Back** ←: Previous view
- **Forward** →: Next view (after using Back)
- **Pan** ✋: Click and drag to move graph
- **Zoom** 🔍: Click and drag to zoom rectangle
- **Configure** ⚙️: Adjust subplot spacing, margins
- **Save** 💾: Export as PNG, PDF, SVG, etc.

**Graph Elements**:
```
Force (kN)
    ↑
    │         Positive Peak *
    │              /\
    │    Skeleton /  \ Hysteresis
    │    Curve  /    \ Loops
    │         /      \
    │        /        \
────┼────────────────────────→ Displacement (mm)
    │         \      /
    │          \    /
    │    Skeleton\  /Hysteresis
    │      Curve  \/  Loops
    │              *
    │         Negative Peak
```

**Legend** (Auto-positioned, movable):
- Hysteresis Curve (blue line)
- Positive Skeleton Curve (red line with circles)
- Negative Skeleton Curve (green line with squares)
- Skeleton Data Points (if smoothing + show points enabled)
- Positive Peak (red star)
- Negative Peak (green star)
- Starting Points (yellow-filled markers)

**Mouse Interactions**:
- **Scroll Wheel**: Zoom in/out centered on cursor
- **Click + Drag**: Pan when Pan mode active
- **Click Legend**: Toggle line visibility (matplotlib feature)

#### Tab 2: Evaluation Metrics and Analysis Results

- 

#### Tab 3: Detailed Hysteresis Loop Information

**Interpretation**:
- **No.**: Sequential loop number
- **Type**: Positive (push) or Negative (pull)
- **Peak Disp.**: Maximum displacement in this loop
- **Peak Force**: Force at peak displacement
- **Loop Area**: Energy dissipated in this cycle (area enclosed by loop)
- **Data Points**: Number of measurement points in this loop

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

#### Optional Columns (Ignored)
- Column 3+: Time, strain, other sensors (not used by this tool)

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
   - Force in kN (or N, but kN is conventional)
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

**Visual Example**:
```
Force
  │        *Peak 3
  │       /│
  │      / │  *Peak 2
  │     /  │ / │
  │    /   │/  │  *Peak 1
  │   /    *   │ /│
  │  /         │/ │
  │ /          *  │
  │/              │
  └────────────────────── Displacement
  Envelope connects: Origin → Peak1 → Peak2 → Peak3
```

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

**Visual Example**:
```
Force
  │     *Peak 2
  │    /│\
  │   / │ \ *Peak 3
  │  /  │  X
  │ /   │ /│
  │/ *──┼/ │ *Peak 1
  │ Peak │  │/
  │  0  /│  *
  │    / │
  └────────────────────── Displacement
  Connects: Start → Peak1 → Peak2 → Peak3
  (May zigzag if peaks vary)
```

### Ductility Coefficient Methods

Ductility (μ) = Ultimate Displacement / Yield Displacement

The key difference is how "yield displacement" is defined:

#### 1. Geometric Method

**Definition**: Yield at 75% of peak force

**Calculation**:
```
F_yield = 0.75 × F_peak
Find displacement where F = F_yield
μ = D_peak / D_yield
```

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
```
Total_Energy = Area under skeleton curve
D_yield = 2 × Total_Energy / F_peak
μ = D_peak / D_yield
```

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
```
K_initial = Initial slope
K_yield = K_initial / 3
Find point where current stiffness = K_yield
μ = D_peak / D_yield
```

**Pros**:
- Based on stiffness degradation
- Commonly used in seismic research
- Park & Ang damage model compatibility

**Cons**:
- Requires clear initial linear region
- May be conservative

**Reference**: Park, Y.J. & Ang, A.H. (1985)

**Typical Range**: 2-5

#### 4. Farthest Point Method

**Definition**: Point farthest from line connecting origin to peak

**Calculation**:
```
Line: Origin to (D_peak, F_peak)
For each point, calculate perpendicular distance to line
D_yield = displacement at maximum distance point
μ = D_peak / D_yield
```

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
```
F_yield = 0.60 × F_peak
Find displacement where F = F_yield
μ = D_peak / D_yield
```

**Pros**:
- Based on US seismic codes
- Standard for ASCE 41 evaluations
- More conservative than geometric

**Cons**:
- Still arbitrary threshold
- Different from other international codes

**Reference**: ASCE 41-17

**Typical Range**: 2-5

#### 6. EEEP (Equivalent Energy Elastic-Plastic)

**Definition**: Bilinear curve with equal energy

**Calculation**:
```
Energy_actual = Area under skeleton curve
Create bilinear curve:
  - Elastic to (D_yield, F_peak)
  - Plastic plateau at F_peak to D_peak
Adjust D_yield until energies match
μ = D_peak / D_yield
```

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
```
K_initial = Initial elastic slope
D_yield = F_peak / K_initial
μ = D_peak / D_yield
```

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

**Parameters**: None (automatic)

**Example Use Case**: Force-displacement data where force shouldn't overshoot between measured points

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

**Parameters**: None (automatic)

**Example Use Case**: Smooth presentation of hysteresis loops without artificial oscillations

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

**Example Use Case**: Creating smooth curves for PowerPoint presentations

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

**Parameters**:
- Smoothness (s): 0.0-10.0
  - 0: Closer to interpolation
  - 5: Moderate smoothing
  - 10: Very smooth, may deviate

**Recommended Settings**:
- Technical: s = 0-2
- General: s = 2-5
- Artistic: s = 5-10

**Example Use Case**: Smoothing noisy sensor data while maintaining overall trend

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

**Parameters**:
- Window Size (odd integer, 3-51)
  - 3-7: Light smoothing
  - 9-15: Moderate smoothing
  - 17+: Heavy smoothing

**Recommended Settings**:
- Low noise: 5-7
- Medium noise: 9-13
- High noise: 15-21

**Caution**: 
- Window must be odd number
- Window should be smaller than feature width
- Very large windows may distort peaks

**Example Use Case**: Filtering electrical noise from load cell data

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

**Parameters**:
- Smoothness (s): 0.0-10.0
  - s=0: Exact interpolation (like CubicSpline)
  - s=1-3: Light smoothing
  - s=4-7: Moderate smoothing
  - s=8-10: Heavy smoothing

**Recommended Settings**:
- Start with s=1.0
- Increase if too jagged
- Decrease if over-smoothed

**Example Use Case**: Standard smoothing for most hysteresis curve presentations

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

**Parameters**: None (automatic)

**Caution**: May show oscillations (Runge's phenomenon) with many points

**Example Use Case**: Interpolating sparse but accurate measurement points

### Visual Comparison

```
Original Data:  ○     ○     ○     ○     ○

PCHIP:         ○─────○─────○─────○─────○
               (follows closely, no overshoot)

Akima:         ○────○────○────○────○
               (smooth, natural curves)

Bézier:        ○──○──○──○──○
(20%)          (very smooth, slight deviation)

B-spline:      ○─○─○─○─○
(s=5)          (smooth, moderate deviation)

SG Filter:     ○ ○ ○ ○ ○
(win=7)        (peaks preserved, noise reduced)

UnivSpline:    ○──○──○──○──○
(s=2)          (balanced smoothness)

CubicSpline:   ○─────○─────○─────○─────○
               (exact through points, possible wiggles)
```

### Parameter Tuning Tips

1. **Start Conservative**:
   - Begin with default/low smoothing
   - Gradually increase until satisfied
   - Compare with original data

2. **Use Preview**:
   - Enable "Show original data points"
   - Visually verify smoothing quality
   - Check peak preservation

3. **Match Purpose**:
   - Research paper: Moderate smoothing (preserve accuracy)
   - Presentation: Higher smoothing (aesthetics)
   - Internal analysis: Minimal smoothing (accuracy)

4. **Check Metrics**:
   - Smoothing shouldn't significantly change calculated metrics
   - If metrics change >5%, reduce smoothing

---

## 📊 Performance Metrics

### Metric Categories and Definitions

#### 1. Displacement-Related Metrics

##### Peak Displacement (D<sub>max</sub>)

**Definition**: Maximum absolute displacement reached during test

**Formula**:
```
D_max_positive = max(displacement)
D_max_negative = min(displacement)
```

**Units**: mm

**Significance**:
- Indicates maximum deformation capacity
- Critical for deformation-based design
- Related to damage level

**Typical Values**:
- Well-confined RC: 50-100 mm (for standard column)
- Steel frames: 100-300 mm
- Base isolators: 200-500 mm

##### Residual Deformation (D<sub>res</sub>)

**Definition**: Permanent displacement after load removal

**Formula**:
```
D_res = displacement[final_point]
```

**Units**: mm

**Significance**:
- Indicates permanent damage
- Important for post-earthquake functionality
- Repair cost indicator

**Typical Values**:
- Excellent: < 1% of peak displacement
- Good: 1-5%
- Moderate: 5-10%
- Poor: > 10%

#### 2. Mechanical Properties

##### Peak Load (F<sub>max</sub>)

**Definition**: Maximum force during test

**Formula**:
```
F_max_positive = max(force)
F_max_negative = min(force)
```

**Units**: kN

**Significance**:
- Ultimate strength capacity
- Design force level
- Safety margin indicator

##### Initial Stiffness (K<sub>0</sub>)

**Definition**: Slope of initial linear elastic region

**Formula**:
```
K_0 = ΔF / ΔD (first ~5-10% of data)
```

**Units**: kN/mm

**Calculation Method**:
- Take first 5-20 data points (or first 10% of data)
- Exclude points near zero (noise threshold)
- Linear regression to find slope

**Significance**:
- Elastic behavior
- Uncracked stiffness
- Theoretical stiffness comparison

**Typical Values**:
- RC beam: 10-100 kN/mm
- RC column: 50-300 kN/mm
- Steel connection: 100-1000 kN/mm

##### Secant Stiffness (K<sub>sec</sub>)

**Definition**: Slope from origin to peak point

**Formula**:
```
K_sec = F_max / D_max
```

**Units**: kN/mm

**Significance**:
- Effective stiffness at peak
- Degraded/cracked stiffness
- Simplified analysis parameter

**Relationship**:
```
K_sec < K_0 (always, due to damage/yielding)
Ratio K_sec/K_0 indicates degradation
```

#### 3. Energy Metrics

##### Total Hysteresis Loop Area (E<sub>total</sub>)

**Definition**: Sum of areas enclosed by all hysteresis loops

**Formula**:
```
E_total = Σ Area_i (for all loops)
Area_i = ∮ F dD (line integral)
```

**Calculation Method**:
```python
for each loop:
    area = 0
    for i in range(len(displacement)-1):
        area += 0.5*(force[i] + force[i+1])*(displacement[i+1] - displacement[i])
    total += abs(area)
```

**Units**: kN·mm (or kN·m = kJ)

**Significance**:
- Total energy dissipated
- Cumulative damage indicator
- Seismic performance parameter

##### Cumulative Energy Dissipation

**Definition**: Same as total hysteresis loop area

**Formula**: E<sub>cumulative</sub> = E<sub>total</sub>

**Units**: kN·mm

**Use**: Progressive energy dissipation analysis (if time-stamped data)

##### Average Loop Energy (E<sub>avg</sub>)

**Definition**: Mean energy per loop

**Formula**:
```
E_avg = E_total / n_loops
```

**Units**: kN·mm

**Significance**:
- Average energy dissipation capacity per cycle
- Comparison between different displacement levels

##### Maximum Loop Energy (E<sub>max</sub>)

**Definition**: Largest single loop area

**Formula**:
```
E_max = max(Area_i) for all i
```

**Units**: kN·mm

**Significance**:
- Peak energy dissipation capacity
- Usually occurs at largest displacement cycle

##### Equivalent Viscous Damping Coefficient (ξ<sub>eq</sub>)

**Definition**: Ratio of dissipated to elastic strain energy

**Formula**:
```
ξ_eq = E_dissipated / (2π × E_elastic)

where:
E_dissipated = Area of hysteresis loop
E_elastic = Area of triangle (0, 0) to (D_max, F_max)
           = 0.5 × D_max × F_max (for each direction)
```

**Units**: Dimensionless (often expressed as %)

**Physical Meaning**:
- Equivalent linear damping ratio
- Higher = better energy dissipation
- Used in equivalent linearization

**Typical Values**:
- Elastic structure: 2-5%
- Lightly damaged RC: 5-10%
- Yielded RC/steel: 10-20%
- Friction devices: 20-40%
- Good seismic design: > 10%

**Reference**: Often compared to 5% damping (common design assumption)

#### 4. Degradation Metrics

##### Strength Degradation (SD)

**Definition**: Percentage decrease in force capacity

**Formula**:
```
SD_positive = (F_first - F_last) / F_first × 100%
SD_negative = (F_first - F_last) / F_first × 100%

where:
F_first = Peak force in first positive/negative loop
F_last = Peak force in last positive/negative loop
```

**Units**: %

**Interpretation**:
- 0%: No degradation (ideal)
- <10%: Excellent performance
- 10-20%: Good performance
- 20-30%: Moderate degradation
- >30%: Significant degradation

**Causes**:

- Concrete crushing
- Reinforcement fracture
- Bond deterioration
- Connection failure

##### Stiffness Degradation (KD)

**Definition**: Percentage decrease in stiffness

**Formula**:
```
KD = (K_initial - K_secant) / K_initial × 100%
```

**Units**: %

**Interpretation**:
- Typical range: 60-95% for ductile elements
- Higher = more damage/yielding
- Lower = more elastic behavior

**Note**: High stiffness degradation is EXPECTED and ACCEPTABLE for ductile design

#### 5. Ductility Coefficient (μ)

**Definition**: Ratio of ultimate to yield displacement

**Formula**:
```
μ = D_ultimate / D_yield
```

**Units**: Dimensionless

**Methods**: See [Ductility Methods](#ductility-coefficient-methods) section

**Significance**:
- Key seismic design parameter
- Indicates deformation capacity
- Force reduction factor (R) related: R ≈ √(2μ - 1)

**Target Values** (Seismic Design):
- Brittle systems: μ < 2
- Limited ductility: μ = 2-4
- Moderate ductility: μ = 4-6
- High ductility: μ > 6

**Code Requirements**:
- ASCE 7: R factors imply μ = 3-6
- Eurocode 8: Ductility classes (DCL: μ=1.5, DCM: μ=3, DCH: μ=4.5)
- Chinese Code: μ ≥ 3 for seismic design

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
- ✓ High ductility (μ > 4)
- ✓ High energy dissipation
- ✓ High equivalent damping (> 10%)
- ✓ Moderate strength degradation (< 20%)
- ✓ Acceptable residual deformation (< 5% of peak)

Poor Performance:
- ✗ Low ductility (μ < 2)
- ✗ Low energy dissipation
- ✗ Severe strength degradation (> 30%)
- ✗ Large residual deformation (> 10% of peak)
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

## 🔧 Troubleshooting

### Common Issues and Solutions

#### Problem 1: Application Won't Start

**Symptoms**:
```
ModuleNotFoundError: No module named 'PySide6'
```

**Solution**:
```bash
pip install PySide6
# Or install all dependencies:
pip install -r requirements.txt
```

---

#### Problem 2: File Import Fails

**Symptoms**:
- Error message: "Data format incorrect"
- No data appears after import

**Possible Causes & Solutions**:

**A) File has headers**:
```
Displacement,Force     ← Header row
0.00,0.00
```
**Solution**: Currently, first row is used as data. Either:
- Remove header row
- Tool will attempt to use it (may cause error)

**B) Non-numeric data**:
```
0.00,0.00
0.12,1.23
N/A,2.45     ← Problem
```
**Solution**: Remove rows with non-numeric values

**C) Insufficient columns**:
```
0.00     ← Only 1 column
0.12
```
**Solution**: Ensure at least 2 columns (displacement, force)

**D) File encoding issues** (Chinese/Russian characters in path):
**Solution**: Move file to path without special characters

---

#### Problem 3: No Hysteresis Loops Detected

**Symptoms**:
- Tab 3 shows "No hysteresis loop information"
- Metrics are incomplete

**Possible Causes & Solutions**:

**A) Data doesn't return to zero**:
```
Monotonic loading (no cycles):
0 → 10 → 20 → 30 ✗
```
**Solution**: Hysteresis requires cyclic loading (back and forth)

**B) Insufficient data points**:
**Solution**: Need at least 20-30 points per cycle

**C) Very small displacement range**:
**Solution**: Check displacement units (should be mm, not m)

**D) All same displacement level**:
**Solution**: Need multiple displacement levels to detect peaks

---

#### Problem 4: Skeleton Curve Looks Wrong

**Symptoms**:
- Curve is jagged or has unexpected jumps
- Missing portions of curve
- Too many or too few points

**Solutions**:

**Try Method 2 if using Method 1**:
- Switch to "Peak Points" method
- May better capture your loading protocol

**Check data filtering**:
- Disable "first loop only" to see all data
- May reveal repeated cycles causing issues

**Verify data quality**:
- Check for outliers in original data
- Look for sensor errors or data transmission issues

**Adjust threshold** (future feature):
- Currently automatic
- Very dense data may need higher thresholds

---

#### Problem 5: Smoothing Creates Artifacts

**Symptoms**:
- Oscillations or waves in smooth curve
- Overshoot beyond original data
- Unnatural-looking curves

**Solutions**:

**A) Switch algorithms**:
```
If using: CubicSpline (oscillations)
Try: PCHIP or Akima (shape-preserving)
```

**B) Adjust parameters**:
```
If too smooth: Decrease s parameter
If too jagged: Increase s parameter
If overshooting: Use PCHIP instead
```

**C) Reduce interpolation points**:
```
Change from 1000 to 300 points
May reduce computational artifacts
```

**D) Use Savitzky-Golay for noisy data**:
```
Window size: Start with 7, adjust up/down
Preserves peaks while smoothing
```

---

#### Problem 6: Metrics Seem Incorrect

**Symptoms**:
- Ductility > 100 or < 1
- Negative stiffness
- Extremely large/small values

**Check These**:

**A) Units**:
```
Displacement should be mm (not m)
Force should be N (not kN)
```

**B) Data quality**:

```
Check for:
- Duplicate points
- Reversed loading (time not sorted)
- Sensor drift or offset
```

**C) Method appropriateness**:
```
Try different ductility calculation method
Results can vary 20-50% between methods
```

**D) Loading protocol**:
```
Some methods require specific loading patterns
Ensure complete cycles to origin
```

---

#### Problem 7: Chinese/Russian Characters Don't Display

**Symptoms**:
- Boxes or question marks instead of characters
- Garbled text

**Solutions**:

**Windows**:
```
Install fonts:
- Microsoft YaHei (Chinese)
- SimHei (Chinese, alternative)
- Arial or Segoe UI (Russian)
```

**Mac**:
```
Install:
- PingFang SC (Chinese)
- Arial or Helvetica (Russian)
```

**Linux**:
```bash
sudo apt install fonts-wqy-microhei  # Chinese
sudo apt install fonts-liberation    # Russian
```

**Matplotlib config** (automatic in code):
```python
plt.rcParams['font.sans-serif'] = ['Arial', 'DejaVu Sans']
```

---

#### Problem 8: Graph is Slow or Laggy

**Symptoms**:
- Delayed response when zooming
- Slow rendering

**Solutions**:

**A) Reduce interpolation points**:
```
Change from 1000 to 300 or even 200
Still looks smooth for most purposes
```

**B) Use simpler algorithm**:
```
PCHIP or Akima are faster than Bézier
```

**C) Disable "Show original points"**:
```
Uncheck option when using smoothing
Reduces number of plotted elements
```

**D) Close other applications**:

```
Matplotlib uses system resources
Free up RAM and CPU
```

---

#### Problem 9: Can't Export Graph

**Symptoms**:

- Save button doesn't work
- Error when saving

**Solutions**:

**A) Check write permissions**:

```
Try saving to Desktop or Documents
Avoid system protected folders
```

**B) Use toolbar save**:
```
Click toolbar disk icon (💾)
Choose format: PNG, PDF, SVG
```

**C) Alternative - Screenshot**:
```
Windows: Snipping Tool or Win+Shift+S
Mac: Cmd+Shift+4
```

---

#### Problem 10: Undo Doesn't Work

**Note**: Undo only works for file operations (add/remove files)

**Does NOT undo**:
- Settings changes (method selection)
- Graph zoom/pan
- Smoothing parameter adjustments

**To reset analysis**:
- Reselect the file from list
- Close and reopen application

---

### Getting Help

If problems persist:

1. **Check data format**: Use examples in this README
3. **Update packages**: `pip install --upgrade PySide6 matplotlib scipy`
3. **Python version**: Ensure 3.7+

---

## 💼 Example Workflows

### Workflow 1: Standard Cyclic Test Analysis

**Scenario**: You've just completed a cyclic loading test on a reinforced concrete column

**Steps**:

1. **Export test data** to CSV:
   ```
   Time, Displacement_mm, Force_kN
   0.00, 0.00, 0.00
   0.01, 0.12, 1.45
   ...
   ```

2. **Open application**:
   ```bash
   python HysAnalysis_MultiLang.py
   ```

3. **Import file**:
   - Click "Import"
   - Select your CSV file
   - Appears in file list

4. **Initial analysis** (automatic):
   - Click filename
   - Default settings applied:
     * Method 1 (Outer Envelope)
     * Both directions
     * Geometric ductility
     * Dot-line plot

5. **Review results**:
   - **Tab 1**: Check curve shape
   - **Tab 2**: Note peak load, ductility
   - **Tab 3**: Count loops, check energy

6. **Apply filtering** (if needed):
   - Enable "first loop only" if repeated cycles
   - Analysis updates automatically

7. **Create presentation graph**:
   - Select "Spline Connected Graph"
   - Choose "PCHIP" algorithm
   - Uncheck "Show original points"
   - Adjust interpolation to 500 points

8. **Export**:
   - Click toolbar save icon
   - Save as PNG (presentation) or PDF (publication)

9. **Copy metrics**:
   - Go to Tab 2
   - Ctrl+A, Ctrl+C
   - Paste into report document

**Estimated Time**: 5 minutes

---

### Workflow 2: Comparing Multiple Specimens

**Scenario**: You tested 3 identical specimens and want to compare

**Steps**:

1. **Import all files**:
   ```
   - Specimen_A.txt
   - Specimen_B.txt
   - Specimen_C.txt
   ```

2. **Analyze each**:
   - Click Specimen_A
   - Copy metrics from Tab 2 → Spreadsheet row 1
   - Save graph → "Specimen_A_curve.png"
   - Repeat for B and C

3. **Consistency check**:
   - Use same settings for all (important!)
   - Same ductility method
   - Same skeleton extraction method

4. **Create comparison table**:
   ```
   Metric          | Specimen A | Specimen B | Specimen C | Average
   ----------------|------------|------------|------------|--------
   Peak Load (kN)  |    67.5    |    65.2    |    69.1    |  67.3
   Ductility       |     4.2    |     3.9    |     4.5    |   4.2
   Energy (kN·mm)  |   4521     |   4102     |   4788     | 4470
   ...
   ```

5. **Statistical analysis** (external):
   - Export metrics to Excel
   - Calculate mean, std dev, COV
   - Check for outliers

**Estimated Time**: 15 minutes for 3 specimens

---

### Workflow 3: Parametric Study of Ductility Methods

**Scenario**: Research on how different ductility definitions affect results

**Steps**:

1. **Load test data**

2. **Create result matrix**:
   ```
   Method          | μ_positive | μ_negative | Notes
   ----------------|------------|------------|-------
   Geometric       |            |            |
   Energy          |            |            |
   Park            |            |            |
   Farthest        |            |            |
   ASCE            |            |            |
   EEEP            |            |            |
   Elastic Yield   |            |            |
   ```

3. **For each method**:
   - Select ductility method radio button
   - Wait for analysis update
   - Copy ductility values from Tab 2
   - Paste into matrix

4. **Analysis**:
   - Calculate range: (max - min)
   - Calculate coefficient of variation
   - Identify most conservative method
   - Identify method closest to code intent

5. **Visualization** (external):
   - Create bar chart comparing methods
   - Show ±1 std dev error bars if multiple specimens

**Estimated Time**: 10 minutes

---

### Workflow 4: Performance-Based Design Verification

**Scenario**: Checking if design meets ASCE 41 requirements

**Steps**:

1. **Load test data**

2. **Configure for ASCE compliance**:
   - Skeleton: Method 1 (Outer Envelope)
   - Ductility: ASCE Method
   - Direction: Both

3. **Extract target values** from Tab 2:
   ```
   ✓ Ductility coefficient: μ = 4.2
   ✓ Equivalent damping: ξ = 0.18 (18%)
   ✓ Residual drift: 2.3 mm (3% of peak)
   ```

4. **Compare to ASCE 41 criteria**:
   ```
   Criteria           | Required | Achieved | Status
   -------------------|----------|----------|--------
   Ductility          |   ≥ 3.0  |   4.2    |   ✓
   Equivalent damping |   ≥ 10%  |   18%    |   ✓
   Residual drift     |   < 5%   |    3%    |   ✓
   Strength degradation| < 20%   |   12%    |   ✓
   ```

5. **Generate compliance report**:
   - Export graph showing skeleton curve
   - Copy metrics table
   - Document test setup
   - Include in design documentation

6. **Acceptance**:
   - All criteria met → Design validated
   - If any fail → Redesign required

**Estimated Time**: 20 minutes (including documentation)

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

**Q5: Which ductility method should I use?**

A: Depends on context:

| Context | Recommended Method | Reason |
|---------|-------------------|--------|
| General research | Geometric | Simple, widely used |
| Seismic design (US) | ASCE | Code compliance |
| Energy dissipation study | Energy or EEEP | Physically meaningful |
| Damage assessment | Park | Stiffness-based |
| Conservative estimate | Elastic Yield | Lowest values |

When in doubt: Report **Geometric** AND **EEEP** methods

---

### Technical Questions

**Q6: Why do different smoothing algorithms give different results?**

A: Algorithms have different mathematical properties:
- Some preserve peaks (SG filter, PCHIP)
- Some prioritize smoothness (Bézier, B-spline)
- Some pass exactly through points (Cubic)
- Trade-off: Smoothness ↔ Accuracy

For analysis: Use PCHIP or minimal smoothing
For presentation: Use Bézier with moderate settings

---

**Q7: My ductility values differ from hand calculations. Why?**

A: Common reasons:
1. **Different yield point definition**: Your method vs. software method
2. **Data preprocessing**: Tool auto-filters near-zero values
3. **Skeleton curve extraction**: Manual vs. automatic peak detection
4. **Rounding**: Display rounds to 2-4 decimals

To verify:
- Check intermediate values (yield displacement, ultimate displacement)
- Try different ductility methods

---

**Q8: Can I export numerical data (not just graphs)?**

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

**Q9: Does the tool account for P-Delta effects?**

A: No. Tool analyzes data as-is.
- If your test data includes P-Delta, results reflect total behavior
- If you want pure component response, apply P-Delta correction before import
- Separation of P-Delta from component behavior is user's responsibility

---

**Q10: How is equivalent viscous damping calculated?**

A: Formula:
```
ξ_eq = E_dissipated / (4π × E_elastic)

where:
E_dissipated = Area of largest hysteresis loop
E_elastic = 0.5 × D_max × F_max × 2 (both directions)
```

Matches ASCE 7 and most seismic codes

Note: Some references use 2π instead of 4π (convention difference)

---

**Q11: Can I analyze tests with asymmetric loading?**

A: Yes:
- Tool handles positive and negative directions independently
- Metrics calculated separately when appropriate
- Use "Direction" setting to focus on one direction if needed
- Asymmetry is captured in separate positive/negative metrics

---

**Q12: What if my test started at pre-load (not zero)?**

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

**Q13: My data file has 3+ columns. Which are used?**

A: Only first two columns:
- Column 1: Displacement
- Column 2: Force
- Columns 3+: Ignored

Ensure correct column order in your file

---

**Q14: Can I import data from ABAQUS/ANSYS/SAP2000?**

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

**Q15: My test was in inches and kips. Do I need to convert?**

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

**Q16: I get "Smoothing interpolation failed". What to do?**

A: This means the algorithm couldn't process your data

Try:
1. **Switch algorithm**: Try PCHIP or Akima (most robust)
2. **Reduce points**: Lower interpolation points to 100
3. **Check data**: Remove duplicate x-values, ensure sorted
4. **Disable smoothing**: Use Dot-Line plot instead

If persists: Your data may have structure incompatible with that algorithm

---

**Q17: Why are there no hysteresis loops detected?**

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

**Q18: Can I use this tool for my thesis/publication?**

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

**Q19: Can I modify the code?**

A: Yes, it's open-source

Common modifications:
- Add new ductility methods
- Customize metric calculations
- Add export formats
- Integrate with other tools

If you improve it, consider contributing back!

---

**Q20: Is there a video tutorial?**

A: Not yet, but planned

Meanwhile:
- This README is comprehensive
- Follow Quick Start for basics
- Try Example Workflows
- Experiment with sample data

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

### Development Setup

```bash
# Clone repository
git clone [https://github.com/GarGarfie/HysAnalysis]
cd HysAnalysis

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run tests (if available)
python -m pytest

# Run application
python HysAnalysis.py
```



---

## 📄 License

This project is licensed under the MIT License.

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



---

## 🙏 Acknowledgments

This tool uses the following open-source libraries:
- **NumPy**: Numerical computing
- **Pandas**: Data manipulation
- **PySide6**: GUI framework (Qt for Python)
- **Matplotlib**: Visualization
- **SciPy**: Scientific computing

---

## 📅 Version History

**Version 1.0.0** (December 2025)
- Initial release
- Multi-language support (EN, ZH, RU)
- 7 smoothing algorithms
- 7 ductility methods
- Comprehensive metric calculations
- Interactive plotting

**Planned Features**:
- Data export to CSV/Excel
- Batch processing mode
- Customizable metric formulas
- Additional smoothing algorithms
- Video tutorials

---

<div align="center">
**[⬆ Back to Top](#-force-displacement-hysteresis-curve-analysis-tool)**

---

Made with ❤️ for the structural engineering community



</div>
