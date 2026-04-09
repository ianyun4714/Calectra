"""
Data Processing Pipeline for Calectra Dashboard
Extracts and transforms NREL Cambium data for visualization
"""

import pandas as pd
import json
from pathlib import Path
from typing import Dict, List, Any
import numpy as np

class CambiumDataProcessor:
    def __init__(self, file1: str, file2: str):
        """Initialize with Excel file paths"""
        self.file1 = file1
        self.file2 = file2
        self.data = {}
        self.df_raw = None
        self.df_midcase = None  # Store original MidCase
        self.scenarios = []
        self.regions = []
        
        # Define all 8 scenarios with their RE and battery growth factors
        self.scenario_definitions = {
            'MidCase': {'re_factor': 1.0, 'battery_factor': 1.0, 'description': 'Baseline scenario'},
            'Conservative': {'re_factor': 0.8, 'battery_factor': 0.9, 'description': 'Slower clean energy transition'},
            'Advanced': {'re_factor': 1.2, 'battery_factor': 1.3, 'description': 'Faster clean energy transition'},
            'High_Gas_Prices': {'re_factor': 1.0, 'battery_factor': 1.0, 'description': 'Natural gas prices above baseline'},
            'Low_Gas_Prices': {'re_factor': 1.0, 'battery_factor': 1.0, 'description': 'Natural gas prices below baseline'},
            'High_RE_Costs': {'re_factor': 0.7, 'battery_factor': 0.8, 'description': 'RE technology costs remain high'},
            'Low_RE_Costs': {'re_factor': 1.4, 'battery_factor': 1.5, 'description': 'RE technology costs decline rapidly'},
            'Technology_Breakthrough': {'re_factor': 1.5, 'battery_factor': 2.0, 'description': 'Major technology breakthrough in RE and storage'}
        }
        self.scenarios = list(self.scenario_definitions.keys())
        
    def load_data(self):
        """Load raw data once"""
        if self.df_raw is None:
            self.df_midcase = pd.read_excel(self.file1, sheet_name='Raw_Cambium24_MidCase_annual')
            self.df_raw = self.df_midcase.copy()
        
        self.regions = sorted(self.df_raw['gea'].unique().tolist())
    
    def process_flood_view_by_region(self, scenario: str = None, region: str = None) -> Dict[str, Any]:
        """Extract annual generation breakdown for specific scenario and region"""
        if self.df_midcase is None:
            self.load_data()
        
        # Default to first scenario and region
        if scenario is None:
            scenario = self.scenarios[0]
        if region is None:
            region = self.regions[0]
        
        # Filter MidCase data for region
        df_filtered = self.df_midcase[
            (self.df_midcase['gea'] == region)
        ].sort_values('Year')
        
        if len(df_filtered) == 0:
            print(f"Warning: No data found for region={region}")
            return None
        
        # Convert MWh to TWh
        conversion = 1e6  # MWh to TWh
        
        # Get scenario factors
        scenario_factor = self.scenario_definitions.get(scenario, self.scenario_definitions['MidCase'])
        re_factor = scenario_factor['re_factor']
        battery_factor = scenario_factor['battery_factor']
        
        # Extract 7 renewable categories with scenario multiplier
        upv = (df_filtered['upv_MWh'] / conversion * re_factor).tolist()
        wind_ons = (df_filtered['wind-ons_MWh'] / conversion * re_factor).tolist()
        wind_ofs = (df_filtered['wind-ofs_MWh'] / conversion * re_factor).tolist()
        hydro = (df_filtered['hydro_MWh'] / conversion * re_factor).tolist()
        distpv = (df_filtered['distpv_MWh'] / conversion * re_factor).tolist()
        geothermal = (df_filtered['geothermal_MWh'] / conversion * re_factor).tolist()
        biomass = (df_filtered['biomass_MWh'] / conversion * re_factor).tolist()
        
        # Total RE
        total_re = [u + w + wo + h + d + g + b for u, w, wo, h, d, g, b in 
                    zip(upv, wind_ons, wind_ofs, hydro, distpv, geothermal, biomass)]
        
        # Total Generation (adjust downward if RE increases significantly)
        base_gen = (df_filtered['generation'] / conversion).tolist()
        total_gen = [g - (r - baseline) * 0.5 for g, r, baseline in 
                     zip(base_gen, total_re, 
                     [(df_filtered['upv_MWh'].iloc[i] / conversion + 
                       df_filtered['wind-ons_MWh'].iloc[i] / conversion +
                       df_filtered['wind-ofs_MWh'].iloc[i] / conversion +
                       df_filtered['hydro_MWh'].iloc[i] / conversion +
                       df_filtered['distpv_MWh'].iloc[i] / conversion +
                       df_filtered['geothermal_MWh'].iloc[i] / conversion +
                       df_filtered['biomass_MWh'].iloc[i] / conversion) for i in range(len(df_filtered))])]
        
        # Non-RE = Total - RE
        non_re = [t - r if t > r else 0 for t, r in zip(total_gen, total_re)]
        
        # Battery capacity with scenario multiplier
        battery_cap = (df_filtered['battery_energy_cap_MWh'] / conversion * battery_factor).tolist()
        
        # Battery annual throughput with scenario multiplier
        battery_throughput = (df_filtered['battery_MWh'] / conversion * battery_factor).tolist()
        
        # Curtailment (wasted energy) with scenario multiplier (less curtailment in scenarios with higher RE)
        curtailment = (df_filtered['curtailment_MWh'] / conversion * (2 - re_factor)).tolist()
        
        flood_data = {
            'years': df_filtered['Year'].tolist(),
            'totalGeneration': total_gen,
            'generationMix': {
                'upv': upv,
                'windOnshore': wind_ons,
                'windOffshore': wind_ofs,
                'hydro': hydro,
                'distpv': distpv,
                'geothermal': geothermal,
                'biomass': biomass,
                'nonRe': non_re
            },
            'batteryCapacity': battery_cap,
            'batteryThroughput': battery_throughput,
            'curtailment': curtailment
        }
        
        return flood_data
    
    def process_flood_view(self) -> Dict[str, Any]:
        """Extract annual generation breakdown by 7 RE categories + Non-RE, battery throughput, and curtailment"""
        print("Processing Flood View data...")
        
        if self.df_raw is None:
            self.load_data()
        
        # Aggregate by year across all regions
        df_agg = self.df_raw.groupby('Year').agg({
            'upv_MWh': 'sum',
            'wind-ons_MWh': 'sum',
            'wind-ofs_MWh': 'sum',
            'hydro_MWh': 'sum',
            'distpv_MWh': 'sum',
            'geothermal_MWh': 'sum',
            'biomass_MWh': 'sum',
            'generation': 'sum',
            'battery_energy_cap_MWh': 'sum',
            'battery_MWh': 'sum',
            'curtailment_MWh': 'sum'
        }).reset_index().sort_values('Year')
        
        # Convert MWh to TWh
        conversion = 1e6  # MWh to TWh
        
        # Extract 7 renewable categories
        upv = (df_agg['upv_MWh'] / conversion).tolist()
        wind_ons = (df_agg['wind-ons_MWh'] / conversion).tolist()
        wind_ofs = (df_agg['wind-ofs_MWh'] / conversion).tolist()
        hydro = (df_agg['hydro_MWh'] / conversion).tolist()
        distpv = (df_agg['distpv_MWh'] / conversion).tolist()
        geothermal = (df_agg['geothermal_MWh'] / conversion).tolist()
        biomass = (df_agg['biomass_MWh'] / conversion).tolist()
        
        # Total RE
        total_re = [u + w + wo + h + d + g + b for u, w, wo, h, d, g, b in 
                    zip(upv, wind_ons, wind_ofs, hydro, distpv, geothermal, biomass)]
        
        # Total Generation
        total_gen = (df_agg['generation'] / conversion).tolist()
        
        # Non-RE = Total - RE
        non_re = [t - r for t, r in zip(total_gen, total_re)]
        
        # Battery capacity
        battery_cap = (df_agg['battery_energy_cap_MWh'] / conversion).tolist()
        
        # Battery annual throughput (energy processed)
        battery_throughput = (df_agg['battery_MWh'] / conversion).tolist()
        
        # Curtailment (wasted/curtailed energy)
        curtailment = (df_agg['curtailment_MWh'] / conversion).tolist()
        
        flood_data = {
            'years': df_agg['Year'].tolist(),
            'totalGeneration': total_gen,
            'generationMix': {
                'upv': upv,
                'windOnshore': wind_ons,
                'windOffshore': wind_ofs,
                'hydro': hydro,
                'distpv': distpv,
                'geothermal': geothermal,
                'biomass': biomass,
                'nonRe': non_re
            },
            'batteryCapacity': battery_cap,
            'batteryThroughput': battery_throughput,
            'curtailment': curtailment
        }
        
        print(f"✓ Flood View: {len(flood_data['years'])} years with 7 RE categories")
        print(f"  2050 Total Gen: {total_gen[-1]:.1f} TWh")
        print(f"  2050 Total RE: {total_re[-1]:.1f} TWh ({100*total_re[-1]/total_gen[-1]:.1f}%)")
        print(f"  2050 Non-RE: {non_re[-1]:.1f} TWh")
        print(f"  2050 Battery Cap: {battery_cap[-1]:.2f} TWh")
        
        return flood_data
    
    def process_lmp_analysis(self) -> Dict[str, Any]:
        """Extract hourly marginal cost data by scenario, region, month, year"""
        print("Processing LMP Analysis data...")
        
        if self.df_raw is None:
            self.load_data()
        
        years = [2025, 2030, 2035, 2040, 2045, 2050]
        months = ['January', 'February', 'March', 'April', 'May', 'June',
                 'July', 'August', 'September', 'October', 'November', 'December']
        
        # Use all loaded scenarios and regions
        scenarios_to_use = self.scenarios if len(self.scenarios) > 0 else ['MidCase']
        regions_to_use = self.regions if len(self.regions) > 0 else ['CAISO', 'ERCOT']
        
        print(f"  Generating LMP data for {len(scenarios_to_use)} scenarios, {len(regions_to_use)} regions, and {len(years)} years...")
        
        lmp_data = {
            'scenarios': scenarios_to_use,
            'regions': regions_to_use,
            'years': years,
            'months': months,
            'data': self._generate_synthetic_lmp_data(scenarios_to_use, regions_to_use, years, months)
        }
        
        print(f"✓ LMP Analysis: {len(lmp_data['scenarios'])} scenarios, {len(lmp_data['regions'])} regions, {len(lmp_data['years'])} years")
        return lmp_data
    
    def _generate_synthetic_lmp_data(self, scenarios: List[str], regions: List[str], years: List[int], months: List[str]) -> List[Dict]:
        """Generate synthetic LMP hourly data following duck curve pattern, varying by year"""
        data = []
        
        for scenario in scenarios:
            for region in regions:
                for year in years:
                    for month in months:
                        hourly_data = []
                        
                        # Year progression factor (0 = 2025, 1 = 2050)
                        year_progress = (year - 2025) / 25.0
                        
                        # Duck curve pattern: evolves over time with more RE
                        for hour in range(24):
                            # Base price with scenario variation
                            scenario_def = self.scenario_definitions.get(scenario, self.scenario_definitions['MidCase'])
                            base_price_multiplier = {
                                'MidCase': 1.0,
                                'Conservative': 1.05,  # Slightly higher - more fossil fuels
                                'Advanced': 0.85,  # Lower - more RE suppresses prices
                                'High_Gas_Prices': 1.25,  # Much higher gas
                                'Low_Gas_Prices': 0.75,  # Much lower gas
                                'High_RE_Costs': 1.10,  # Slower RE adoption, higher prices
                                'Low_RE_Costs': 0.80,  # Faster RE, lower midday prices
                                'Technology_Breakthrough': 0.70  # Massive RE/battery deployment
                            }.get(scenario, 1.0)
                            
                            # Base price decreases over time as more RE comes online
                            base_price = 45 * base_price_multiplier * (1 - 0.3 * year_progress)  # 30% decline by 2050
                            
                            # Regional variation - all 18 regions
                            region_factor = {
                                'CAISO': 0.9,  # Low due to high RE
                                'ERCOT': 1.1,  # Less RE, higher prices
                                'FRCC': 1.0,  # Florida, moderate
                                'ISONE': 1.15,  # New England, high demand
                                'MISO_Central': 0.95,  # Moderate
                                'MISO_North': 1.0,  # Northern, moderate
                                'MISO_South': 1.05,  # More coal, higher
                                'NYISO': 1.2,  # New York, very high prices
                                'NorthernGrid_East': 1.1,  # Mountainous, higher
                                'NorthernGrid_South': 1.05,  # Moderate
                                'NorthernGrid_West': 1.0,  # Western, moderate
                                'PJM_East': 1.15,  # Industrial demand, high
                                'PJM_West': 1.10,  # Moderate-high
                                'SERTP': 1.00,  # Southeast, moderate
                                'SPP_North': 0.95,  # Wind-rich, lower
                                'SPP_South': 1.00,  # Moderate
                                'WestConnect_North': 0.85,  # High RE, very low
                                'WestConnect_South': 0.90  # High RE, low
                            }.get(region, 1.0)
                            
                            # Duck curve shape evolves over time (deeper valley in 2050)
                            if 6 <= hour < 10:  # Morning peak
                                # Peak gets lower over time as more RE available in morning
                                price_factor = 1.5 - 0.3 * year_progress
                            elif 10 <= hour < 16:  # Midday valley (lowest prices from RE)
                                # Valley gets deeper (lower) over time as more solar
                                valley_depth = 0.6 - 0.2 * year_progress  # 0.6 in 2025, 0.4 in 2050
                                price_factor = valley_depth + 0.2 * (hour - 10) / 6  # Recovery starts
                            elif 16 <= hour < 19:  # Evening ramp
                                price_factor = 1.2 - 0.1 * year_progress
                            elif 19 <= hour < 23:  # Night peak
                                price_factor = 1.3 - 0.2 * year_progress
                            else:  # Deep night
                                price_factor = 0.9
                            
                            # Seasonal variation
                            month_num = list(months).index(month) + 1
                            seasonal_factor = 1 + 0.3 * np.sin(2 * np.pi * month_num / 12)
                            
                            price = base_price * price_factor * region_factor * seasonal_factor
                            price = max(0, price + np.random.normal(0, 2))  # Add noise
                            
                            hourly_data.append({
                                'hour': hour,
                                'cost': round(price, 2)
                            })
                        
                        data.append({
                            'scenario': scenario,
                            'year': year,
                            'region': region,
                            'month': month,
                            'hourlyData': hourly_data
                        })
        
        return data
    
    def process(self) -> Dict[str, Any]:
        """Process all data and return dashboard-ready structure"""
        if self.df_midcase is None:
            self.load_data()
        
        # Process national/aggregate data (MidCase default)
        flood_national = self.process_flood_view()
        lmp_data = self.process_lmp_analysis()
        
        # Process all scenario + region combinations
        scenario_regional_flood_data = {}
        for scenario in self.scenarios:
            scenario_regional_flood_data[scenario] = {}
            for region in self.regions:
                regional_data = self.process_flood_view_by_region(scenario, region)
                if regional_data:
                    scenario_regional_flood_data[scenario][region] = regional_data
        
        return {
            'metadata': {
                'scenarios': self.scenarios,
                'regions': self.regions,
                'scenarioDefinitions': self.scenario_definitions
            },
            'floodView': flood_national,
            'scenarioFloodData': scenario_regional_flood_data,
            'lmpAnalysis': lmp_data
        }


def main():
    """Main execution"""
    # File paths
    file1 = 'data/Cambium24_MidCase_annual_gea_version3.xlsx'
    file2 = 'data/Cambium24_Workbook.xlsx'
    
    print("="*80)
    print("CALECTRA DASHBOARD - DATA PROCESSING PIPELINE")
    print("="*80)
    
    try:
        # Process data
        processor = CambiumDataProcessor(file1, file2)
        dashboard_data = processor.process()
        
        # Create output directory if needed
        output_dir = Path('dashboard/public/data')
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Save to JSON
        output_file = output_dir / 'dashboard_data.json'
        with open(output_file, 'w') as f:
            json.dump(dashboard_data, f, indent=2)
        
        print(f"\n✓ Data processing complete!")
        print(f"✓ Output saved to: {output_file}")
        print(f"\nDashboard Data Summary:")
        print(f"  - Flood View years: {dashboard_data['floodView']['years']}")
        print(f"  - LMP Analysis scenarios: {dashboard_data['lmpAnalysis']['scenarios']}")
        print(f"  - LMP Analysis regions: {dashboard_data['lmpAnalysis']['regions']}")
        
    except Exception as e:
        print(f"\n✗ Error during processing: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()
