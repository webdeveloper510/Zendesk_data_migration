import pandas as pd
import re

# Create a DataFrame with your data
data = {'column': ['INV 31/10/2019', 'NA', 'DT 02/10/2020', '04/10/22']}
df = pd.DataFrame(data)

# Define a function to remove alpha items before the date using regex
def remove_alpha(text):
    if isinstance(text, str):  # Check if input is a string
        return re.sub(r'^.*?(\d{1,2}/\d{1,2}/\d{2,4}).*', r'\1', text)
    else:
        return str(text)

# Apply the function to the DataFrame
df['column'] = df['column'].apply(remove_alpha)

# Convert the date format to YYYY-MM-DD
df['column'] = pd.to_datetime(df['column'], dayfirst=True).dt.strftime('%Y-%m-%d')

# Output the modified DataFrame
print(df)