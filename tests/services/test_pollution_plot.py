"""
Test script to demonstrate pollution plotting functionality.
This script mimics the data structure and plotting functionality
that was added to the API endpoint.
"""

import os
import uuid
from datetime import date, timedelta
import random
import matplotlib.pyplot as plt

# Create plots directory
PLOTS_DIR = "/tmp/outputs/plots"
os.makedirs(PLOTS_DIR, exist_ok=True)


# Mock pollution data
class MockCity:
    def __init__(self, id, name, lat, lon):
        self.id = id
        self.name = name
        self.lat = lat
        self.lon = lon


class MockPollution:
    def __init__(self, city_id, date, co, no, no2, o3, so2, pm2, pm10, nh3):
        self.id = random.randint(1, 1000)
        self.city_id = city_id
        self.date = date
        self.co = co
        self.no = no
        self.no2 = no2
        self.o3 = o3
        self.so2 = so2
        self.pm2 = pm2
        self.pm10 = pm10
        self.nh3 = nh3


# Generate mock data
def generate_mock_pollution_data(city_id, start_date, days=30):
    data = []
    for i in range(days):
        current_date = start_date + timedelta(days=i)

        # Generate random pollution values (some might be None to simulate missing data)
        co = random.uniform(0.5, 3.0) if random.random() > 0.1 else None
        no = random.uniform(1.0, 30.0) if random.random() > 0.1 else None
        no2 = random.uniform(5.0, 50.0) if random.random() > 0.1 else None
        o3 = random.uniform(20.0, 80.0) if random.random() > 0.1 else None
        so2 = random.uniform(0.5, 20.0) if random.random() > 0.1 else None
        pm2 = random.uniform(5.0, 35.0) if random.random() > 0.1 else None
        pm10 = random.uniform(10.0, 70.0) if random.random() > 0.1 else None
        nh3 = random.uniform(0.1, 5.0) if random.random() > 0.1 else None

        pollution = MockPollution(
            city_id=city_id,
            date=current_date,
            co=co,
            no=no,
            no2=no2,
            o3=o3,
            so2=so2,
            pm2=pm2,
            pm10=pm10,
            nh3=nh3,
        )
        data.append(pollution)

    return data


def generate_pollution_plot(pollution_data, city):
    """
    Generate a plot for pollution data and return the file path

    :param pollution_data: List of Pollution instances
    :param city: City instance
    :return: URL to the generated plot or None if no data
    """
    if not pollution_data:
        return None

    # Extract dates and pollutant values
    dates = [p.date for p in pollution_data]
    pollutants = {
        "CO": [p.co for p in pollution_data],
        "NO": [p.no for p in pollution_data],
        "NO2": [p.no2 for p in pollution_data],
        "O3": [p.o3 for p in pollution_data],
        "SO2": [p.so2 for p in pollution_data],
        "PM2.5": [p.pm2 for p in pollution_data],
        "PM10": [p.pm10 for p in pollution_data],
        "NH3": [p.nh3 for p in pollution_data],
    }

    # Create a figure with multiple subplots for each pollutant
    fig, axes = plt.subplots(4, 2, figsize=(14, 16))
    fig.suptitle(
        f"Pollution Data for {city.name} ({dates[0]} to {dates[-1]})", fontsize=16
    )

    # Plot each pollutant on its own subplot
    for i, (pollutant, values) in enumerate(pollutants.items()):
        row, col = divmod(i, 2)
        ax = axes[row, col]

        # Filter out None values
        valid_data = [(d, v) for d, v in zip(dates, values) if v is not None]
        if valid_data:
            plot_dates, plot_values = zip(*valid_data)
            ax.plot(plot_dates, plot_values, marker="o", linestyle="-", markersize=4)
            ax.set_title(pollutant)
            ax.set_ylabel("Concentration")
            ax.grid(True)

            # Set x-axis labels to be readable
            if len(plot_dates) > 10:
                # Show fewer x-ticks if there are many dates
                step = max(1, len(plot_dates) // 10)
                ax.set_xticks(plot_dates[::step])

            ax.tick_params(axis="x", rotation=45)
        else:
            ax.text(
                0.5,
                0.5,
                f"No data for {pollutant}",
                horizontalalignment="center",
                verticalalignment="center",
                transform=ax.transAxes,
            )

    # Adjust layout
    plt.tight_layout(rect=[0, 0, 1, 0.96])  # Leave space for suptitle

    # Generate a unique filename
    plot_filename = f"{city.name.replace(' ', '_')}_{dates[0]}_{dates[-1]}_{uuid.uuid4().hex[:8]}.png"
    plot_path = os.path.join(PLOTS_DIR, plot_filename)

    # Save the plot
    plt.savefig(plot_path)
    plt.close(fig)  # Close the figure to free memory

    print(f"Generated plot: {plot_path}")

    # Return the URL for accessing the plot
    return f"/api/plots/{plot_filename}"


# Create test data for different cities
cities = [
    MockCity(id=1, name="London", lat=51.5074, lon=-0.1278),
    MockCity(id=2, name="New York", lat=40.7128, lon=-74.0060),
    MockCity(id=3, name="Singapore", lat=1.3521, lon=103.8198),
]

# Generate and plot data for each city
for city in cities:
    start_date = date(2023, 1, 1)
    pollution_data = generate_mock_pollution_data(city.id, start_date, days=30)
    plot_url = generate_pollution_plot(pollution_data, city)
    print(f"City: {city.name}, Plot URL: {plot_url}")

print("\nTest complete. Check the plots directory for generated files.")
