import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter, date2num
import matplotlib.dates as mdates
import mplcursors  # Import mplcursors for interactive tooltips

# Load the Excel dataset
file_path = 'GanttChartDataSet.xlsx'  # Adjust this path if necessary
file_data = pd.read_excel(file_path)

# Convert date columns to datetime format
file_data['Maintenance Start Date'] = pd.to_datetime(file_data['Maintenance Start Date'])
file_data['Maintenance End Date'] = pd.to_datetime(file_data['Maintenance End Date'])
file_data['Docking Start Date'] = pd.to_datetime(file_data['Docking Start Date'])
file_data['Docking End Date'] = pd.to_datetime(file_data['Docking End Date'])

# Initialize the figure and axis
fig, axis = plt.subplots(figsize=(15, 8))


# Loop through each ship to plot Maintenance and Docking periods
for i, row in file_data.iterrows():
    # Calculate durations in days for tooltips
    maintenance_duration = (row['Maintenance End Date'] - row['Maintenance Start Date']).days
    docking_duration = (row['Docking End Date'] - row['Docking Start Date']).days

    # Plot Maintenance period
    maintenance_bar = axis.barh(
        i,
        maintenance_duration,
        left=date2num(row['Maintenance Start Date']),
        height=0.4,
        color="blue",
        label="Maintenance" if i == 0 else ""
    )

    # Plot Docking period directly below the Maintenance bar
    docking_bar = axis.barh(
        i - 0.4,
        docking_duration,
        left=date2num(row['Docking Start Date']),
        height=0.4,
        color="red",
        label="Docking" if i == 0 else ""
    )

    # Attach hover tooltips for Maintenance with type, start, end, ship name, and duration
    mplcursors.cursor(maintenance_bar).connect(
        "add", lambda sel, row=row, duration=maintenance_duration:
        sel.annotation.set_text(
            f"Type=Maintenance\nStart_Date={row['Maintenance Start Date'].strftime('%b %d, %Y')}\n"
            f"End_Date={row['Maintenance End Date'].strftime('%b %d, %Y')}\n"
            f"Ship_Name={row['Ship Name']}\nDuration={duration} days"
        )
    )
    
    # Attach hover tooltips for Docking with type, start, end, ship name, and duration
    mplcursors.cursor(docking_bar).connect(
        "add", lambda sel, row=row, duration=docking_duration:
        sel.annotation.set_text(
            f"Type=Docking\nStart_Date={row['Docking Start Date'].strftime('%b %d, %Y')}\n"
            f"End_Date={row['Docking End Date'].strftime('%b %d, %Y')}\n"
            f"Ship_Name={row['Ship Name']}\nDuration={duration} days"
        )
    )

# Define y positions for each ship
y_positions = range(len(file_data))

# Set labels and titles
axis.set_yticks([pos for pos in y_positions])
axis.set_yticklabels(file_data['Ship Name'])
axis.set_ylabel("Ship Name")
axis.set_xlabel("Dates")
axis.set_title("Ship Maintenance and Docking Schedule")

# Format the x-axis to show dates
axis.xaxis.set_major_formatter(DateFormatter("%Y-%m-%d"))
axis.xaxis.set_major_locator(mdates.MonthLocator(interval=4))

# Add a legend to differentiate Maintenance and Docking periods
axis.legend()

plt.tight_layout()
plt.show()




