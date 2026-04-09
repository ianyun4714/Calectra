# Calectra CEO Dashboard - Setup Guide

## Project Structure

```
Calectra/
├── data/                           # Raw data files
│   ├── Cambium24_MidCase_annual_gea_version3.xlsx
│   └── Cambium24_Workbook.xlsx
├── dashboard/                      # React frontend application
│   ├── src/
│   │   ├── components/            # React components
│   │   ├── App.tsx
│   │   ├── main.tsx
│   │   ├── index.css
│   │   └── types.ts
│   ├── public/
│   │   └── data/                  # Generated JSON data
│   ├── index.html
│   ├── package.json
│   ├── vite.config.ts
│   └── tsconfig.json
├── process_data.py                # Python data processing script
├── data_analysis.py              # General data analysis tools
└── README.md
```

## Installation & Setup

### Step 1: Install Node.js (if not already installed)
Download from: https://nodejs.org/ (LTS version recommended)

### Step 2: Process the Data
Run the Python data processing script to convert Excel files to JSON:

```bash
cd "c:\Users\dlseh\Desktop\Calectra Github\Calectra"
python.exe -m venv venv  # If not already created
venv\Scripts\activate
pip install pandas openpyxl
python process_data.py
```

Expected output: `dashboard/public/data/dashboard_data.json`

### Step 3: Install Dashboard Dependencies
```bash
cd dashboard
npm install
```

### Step 4: Run the Dashboard
```bash
npm run dev
```

The dashboard will open at `http://localhost:3000`

## Building for Production

```bash
cd dashboard
npm run build
```

Output will be in `dashboard/dist/` ready for deployment.

## Dashboard Features

### 1. Flood View (Top Chart)
**Objective:** Visualize the massive gap between RE generation and battery storage.

- **X-axis:** Years (2025-2050)
- **Left Y-axis:** RE and Total Generation (TWh) - Bar charts
- **Right Y-axis:** Battery Capacity (TWh) - Line chart
- **Dynamic Headline:** "Batteries Cannot Contain the Flood"

**Key Metrics:**
- RE Generation Growth %
- Battery Capacity Growth %
- 2050 Gap Ratio (RE vs Battery)

### 2. Interactive LMP Analysis (Bottom Chart)
**Objective:** Visualize price collapse (Duck Curve) under different conditions.

**Interactive Filters:**
1. **Scenario** - e.g., Mid-case, High Gas Price
2. **Region** - e.g., CAISO, ERCOT, Nation
3. **Month** - January to December

**Chart Type:** 
- Line chart showing 24-hour LMP profile
- X-axis: Hour (1-24)
- Y-axis: $/MWh

**Key Statistics:**
- Min Price (with hour)
- Max Price (with hour)
- Average Price
- Price Range Ratio (Duck Curve intensity)

## Data Sources

### File 1: Cambium24_MidCase_annual_gea_version3.xlsx
- **Sheet:** Raw_Cambium24_MidCase_annual
- **Key Columns:**
  - `Year`: 2025-2050
  - `generation`: Total generation (MWh)
  - `battery_energy_cap_MWh`: Battery storage capacity
  - `distpv_MWh`, `upv_MWh`: Solar generation
  - `wind-ons_MWh`, `wind-ofs_MWh`: Wind generation
  - `curtailment_MWh`: Curtailed energy

### File 2: Cambium24_Workbook.xlsx
- **Sheet:** Data - Month-hour - Costs
- **Content:** Hourly marginal electricity costs by scenario, region, month

## Design Specifications

### Color Scheme (Dark Mode)
- **Primary:** #00D9FF (Cyan - Technical, Energy-forward)
- **Secondary:** #FF6B35 (Orange - Warning, Urgency)
- **Dark Background:** #1a1f2e
- **Darker Background:** #0f1419

### Typography
- Headers: Bold, Gradient text (Primary → Secondary)
- Body: Sans-serif, Professional
- Data: Monospace for precision

### Components
- Dashboard Header with company thesis
- Dual-axis charts using Recharts
- Interactive filter controls
- Dynamic metric cards
- Professional footer

## Technology Stack

- **Frontend:** React 18 + TypeScript
- **Build Tool:** Vite
- **Styling:** Tailwind CSS
- **Charts:** Recharts
- **Data Processing:** Python + Pandas
- **Data Format:** JSON

## Customization

### Modifying Colors
Edit `dashboard/tailwind.config.js`:
```javascript
colors: {
  primary: '#00D9FF',      // Change this
  secondary: '#FF6B35',    // Or this
}
```

### Changing Chart Types
Edit `dashboard/src/components/FloodView.tsx` and `LMPAnalysis.tsx`
Replace chart components from Recharts as needed.

### Adding More Scenarios/Regions
Update `process_data.py` in the `_generate_synthetic_lmp_data()` method.

## Troubleshooting

### "Cannot find module 'recharts'"
```bash
cd dashboard
npm install recharts
```

### Port 3000 already in use
Edit `dashboard/vite.config.ts` and change port to 3001:
```typescript
server: {
  port: 3001,
}
```

### Data not loading
Verify `dashboard/public/data/dashboard_data.json` exists:
```bash
python process_data.py
```

## Performance Tips

- Dashboard is optimized for modern browsers (Chrome, Edge, Firefox)
- Charts render at 60fps using canvas rendering
- Responsive design works on desktop and tablets
- Loading time typically < 2 seconds

## Support & Next Steps

1. **Real Data Integration:** Replace synthetic LMP data with actual parsed values from Excel
2. **Extended Analysis:** Add more metrics (curtailment %, capacity factors, etc.)
3. **Scenario Comparison:** Add side-by-side scenario comparison view
4. **Export Functionality:** Add ability to export charts as PNG/PDF
5. **Real-time Updates:** Connect to live data source for quarterly updates

---

For questions or modifications, contact: strategy@calectra.com
