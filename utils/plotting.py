import os
from datetime import date
from pathlib import Path
from typing import List, Dict, Any, Optional
import uuid

import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import pandas as pd

from city_pollution.entities import Pollution, City


def generate_pollution_plot(
    pollution_data: List[Pollution], 
    city: City,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    plot_dir: str = "/tmp/outputs",
) -> Dict[str, Any]:
    """
    Generate a plot for pollution data and save it to a file
    
    Args:
        pollution_data: List of Pollution instances
        city: City instance
        start_date: Optional start date for the plot title
        end_date: Optional end date for the plot title
        plot_dir: Directory where to save the plot
        
    Returns:
        Dict with plot information including the file path
    """
    if not pollution_data:
        return {"error": "No pollution data available for plotting"}
    
    # Create a pandas DataFrame from the pollution data
    df = pd.DataFrame([{
        'date': p.date,
        'co': p.co,
        'no': p.no,
        'no2': p.no2,
        'o3': p.o3,
        'so2': p.so2,
        'pm2_5': p.pm2_5,
        'pm10': p.pm10,
        'nh3': p.nh3
    } for p in pollution_data])
    
    # Sort by date
    df = df.sort_values('date')
    
    # Create the plot
    fig = plt.figure(figsize=(12, 8))
    
    # Plot each pollutant
    plt.subplot(2, 1, 1)
    for col in ['co', 'no', 'no2', 'o3']:
        if col in df.columns and df[col].notna().any():  # Check if column exists and has data
            plt.plot(df['date'], df[col], label=col.upper())
    
    plt.title(f"Pollution Data for {city.name}, {city.country}"
              f"{f' ({start_date} to {end_date})' if start_date and end_date else ''}")
    plt.ylabel("Concentration")
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend()
    
    plt.subplot(2, 1, 2)
    for col in ['so2', 'pm2_5', 'pm10', 'nh3']:
        if col in df.columns and df[col].notna().any():  # Check if column exists and has data
            plt.plot(df['date'], df[col], label=col if col != 'pm2_5' else 'PM2.5')
    
    plt.xlabel("Date")
    plt.ylabel("Concentration")
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend()
    
    plt.tight_layout()
    
    # Ensure the output directory exists
    os.makedirs(plot_dir, exist_ok=True)
    
    # Generate unique filename
    filename = f"pollution_{city.name.lower().replace(' ', '_')}_{uuid.uuid4().hex[:8]}.png"
    filepath = os.path.join(plot_dir, filename)
    
    # Save the plot
    plt.savefig(filepath)
    plt.close(fig)  # Close the figure to free memory
    
    return {
        "filename": filename,
        "filepath": filepath,
        "city": city.name,
        "start_date": start_date.isoformat() if start_date else None,
        "end_date": end_date.isoformat() if end_date else None
    }
