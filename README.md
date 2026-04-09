# Data Analysis Setup

This project provides a complete environment for analyzing Excel datasets with exploratory data analysis (EDA), statistical analysis, and visualization.

## Setup Instructions

### 1. Create Virtual Environment
```bash
python -m venv venv
venv\Scripts\activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Prepare Your Data
Create a `data` folder and place your Excel files:
```
Calectra/
├── data/
│   ├── dataset1.xlsx
│   └── dataset2.xlsx
├── data_analysis.py
└── README.md
```

### 4. Update File Paths
Edit `data_analysis.py` and update these lines with your actual file paths:
```python
file1_path = "data/dataset1.xlsx"  # Change this path
file2_path = "data/dataset2.xlsx"  # Change this path
```

### 5. Run the Analysis
```bash
python data_analysis.py
```

## What This Script Does

✓ **Loads Excel Files** - Reads your Excel datasets into pandas DataFrames

✓ **Exploratory Data Analysis**
- Dataset shape and structure
- Column names and data types
- Missing values detection
- Descriptive statistics
- Data preview

✓ **Statistical Analysis**
- Correlation matrices
- Summary statistics
- Distribution analysis

✓ **Data Visualization**
- Distribution histograms for each dataset
- Comparison visualizations
- Saves visualizations as PNG files

## Output Files
The script generates:
- `dataset1_distributions.png` - Distribution plots for Dataset 1
- `dataset2_distributions.png` - Distribution plots for Dataset 2
- `dataset_comparison.png` - Comparison visualization between datasets
- Console output with detailed analysis

## Customization

You can modify `data_analysis.py` to:
- Add more statistical tests
- Create custom visualizations
- Filter or transform data
- Export results to CSV/Excel

## Libraries Used
- **pandas** - Data manipulation
- **numpy** - Numerical operations
- **matplotlib** - Visualization
- **seaborn** - Statistical visualization
- **scipy** - Statistical functions
- **openpyxl** - Excel file handling

---

For questions or modifications, edit the Python script as needed!
