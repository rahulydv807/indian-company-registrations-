import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Set Seaborn style
sns.set_style("whitegrid")

# Load the dataset
try:
    df = pd.read_csv('indian-company-registrations.csv')
    print("Dataset loaded successfully!")
except FileNotFoundError:
    print("Error: File 'indian-company-registrations.csv' not found. Please check the file path.")
    exit()
except Exception as e:
    print(f"Error loading dataset: {str(e)}")
    exit()

# Display dataset info for debugging
print("\nDataset Preview (first 5 rows):")
print(df.head())
print("\nColumns in the dataset:")
print(df.columns.tolist())
print("\nDataset Info (data types and non-null counts):")
print(df.info())

# Define column names (UPDATE THESE based on df.columns output)
# Check the printed columns above and replace with the correct names
COL_REGISTRATION_DATE = 'registration_date'  # e.g., 'DATE_OF_REGISTRATION'
COL_DISTRICT = 'district'  # e.g., 'DISTRICT' (optional)
COL_COMPANY_CLASS = 'company_class'  # e.g., 'COMPANY_CLASS'

# Verify column existence
print("\nChecking required columns:")
required_columns = [COL_REGISTRATION_DATE, COL_COMPANY_CLASS]
for col in required_columns:
    if col not in df.columns:
        print(f"Warning: Column '{col}' not found. Please update to the correct column name from: {df.columns.tolist()}")
if COL_DISTRICT not in df.columns:
    print(f"Note: Column '{COL_DISTRICT}' not found. District analysis will be skipped if not updated.")

# Data preprocessing: Convert registration_date to datetime
if COL_REGISTRATION_DATE in df.columns:
    try:
        df[COL_REGISTRATION_DATE] = pd.to_datetime(df[COL_REGISTRATION_DATE], errors='coerce')
        df['year'] = df[COL_REGISTRATION_DATE].dt.year
        df['month'] = df[COL_REGISTRATION_DATE].dt.month
        print("\nDate preprocessing successful.")
        print(f"Unique years: {df['year'].unique()}")
        print(f"Missing dates: {df[COL_REGISTRATION_DATE].isna().sum()}")
    except Exception as e:
        print(f"Error processing '{COL_REGISTRATION_DATE}': {str(e)}")
        exit()
else:
    print(f"Error: Column '{COL_REGISTRATION_DATE}' not found. Skipping date-related analyses.")
    exit()

# Track number of charts
chart_count = 0




# 3. Month-wise registration trends (Heatmap)
try:
    monthly_registrations = df.groupby(['year', 'month']).size()
    monthly_registrations_unstacked = monthly_registrations.unstack()
    plt.figure(figsize=(14, 8))
    sns.heatmap(monthly_registrations_unstacked, cmap='YlGnBu', annot=True, fmt='.0f')
    plt.title('Heatmap of Company Registrations by Month and Year')
    plt.xlabel('Month')
    plt.ylabel('Year')
    plt.show()
    chart_count += 1
    print(f"Chart {chart_count}: Heatmap (Month-wise registrations) generated.")
except Exception as e:
    print(f"Error in month-wise analysis: {str(e)}")

# 4. Top districts by registrations (Bar Chart, if available)
if COL_DISTRICT in df.columns:
    try:
        top_districts = df[COL_DISTRICT].value_counts().head(10)
        plt.figure(figsize=(12, 6))
        top_districts.plot(kind='bar', color='lightgreen')
        plt.title('Top 10 Districts by Company Registrations')
        plt.xlabel('District')
        plt.ylabel('Number of Registrations')
        plt.xticks(rotation=45)
        plt.show()
        chart_count += 1
        print(f"Chart {chart_count}: Bar Chart (Top districts) generated.")
    except Exception as e:
        print(f"Error in district analysis: {str(e)}")
else:
    print("\nDistrict data not available in the dataset.")

# 5. Distribution of company classes (Pie Chart)
if COL_COMPANY_CLASS in df.columns:
    try:
        company_classes = df[COL_COMPANY_CLASS].value_counts()
        plt.figure(figsize=(8, 8))
        company_classes.plot(kind='pie', autopct='%1.1f%%', startangle=90)
        plt.title('Distribution of Company Classes')
        plt.ylabel('')
        plt.show()
        chart_count += 1
        print(f"Chart {chart_count}: Pie Chart (Company classes) generated.")
    except Exception as e:
        print(f"Error in company class analysis: {str(e)}")
else:
    print(f"\nError: Column '{COL_COMPANY_CLASS}' not found. Skipping company class analysis.")

# 6. Daily registrations per year (Box Plot)
try:
    daily_registrations = df.groupby(COL_REGISTRATION_DATE).size().reset_index(name='registrations')
    daily_registrations['year'] = daily_registrations[COL_REGISTRATION_DATE].dt.year
    plt.figure(figsize=(12, 6))
    sns.boxplot(x='year', y='registrations', hue='year', data=daily_registrations, palette='coolwarm', legend=False)
    plt.title('Box Plot of Daily Company Registrations per Year')
    plt.xlabel('Year')
    plt.ylabel('Number of Registrations per Day')
    plt.show()
    chart_count += 1
    print(f"Chart {chart_count}: Box Plot (Daily registrations per year) generated.")
except Exception as e:
    print(f"Error in daily registrations analysis: {str(e)}")

# 7. Registrations by month across all years (Bar Chart)
try:
    monthly_totals = df.groupby('month').size()
    plt.figure(figsize=(12, 6))
    monthly_totals.plot(kind='bar', color='teal')
    plt.title('Company Registrations by Month (All Years)')
    plt.xlabel('Month')
    plt.ylabel('Number of Registrations')
    plt.xticks(ticks=range(12), labels=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'], rotation=0)
    plt.show()
    chart_count += 1
    print(f"Chart {chart_count}: Bar Chart (Registrations by month) generated.")
except Exception as e:
    print(f"Error in monthly totals analysis: {str(e)}")



# 8. Registrations by year (Bar Chart)
try:
    yearly_totals = df.groupby('year').size()
    plt.figure(figsize=(10, 6))
    yearly_totals.plot(kind='bar', color='coral')
    plt.title('Total Company Registrations by Year')
    plt.xlabel('Year')
    plt.ylabel('Number of Registrations')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
    chart_count += 1
    print(f"Chart {chart_count}: Bar Chart (Registrations by year) generated.")
except Exception as e:
    print(f"Error in yearly totals bar chart: {str(e)}")



# Summary of charts generated
print(f"\nTotal charts generated: {chart_count}")
if chart_count < 7:
    print("Warning: Fewer than 7 charts generated. Check for missing columns or data issues.")
else:
    print("Success: Minimum 7 charts requirement met.")
