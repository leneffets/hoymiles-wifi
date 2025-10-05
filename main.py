import asyncio
import os
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import csv
from hoymiles_wifi.dtu import DTU

# Store data in memory
dtu_power_data = []

def save_dtu_power_csv():
    """Save today's dtu_power data as a CSV file."""
    today = datetime.now().date()
    outpath = f"/workspace/data/{today.strftime('%Y-%m-%d')}-dtu_power_today.csv"
    with open(outpath, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["datetime", "dtu_power_w"])
        for dt, power in dtu_power_data:
            if dt.date() == today:
                writer.writerow([dt.isoformat(), power])

def plot_dtu_power_today():
    """Plot dtu_power for today and save as PNG."""
    if not dtu_power_data:
        return
    # Filter today's data
    today = datetime.now().date()
    times = [dt for dt, _ in dtu_power_data if dt.date() == today]
    powers = [p for dt, p in dtu_power_data if dt.date() == today]
    if not times:
        return
    plt.figure(figsize=(12, 6))
    plt.plot(times, powers, label="DTU Power (W)", color="tab:blue")
    plt.title(f"DTU Power for {today}")
    plt.xlabel("Time")
    plt.ylabel("Power (W)")
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.legend()
    plt.tight_layout()
    # Format x-axis as HH:MM
    ax = plt.gca()
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    ax.xaxis.set_major_locator(mdates.HourLocator(interval=1))
    plt.xticks(rotation=45)
    # Output file with date in name
    outpath = f"/workspace/data/{today.strftime('%Y-%m-%d')}-dtu_power_today.png"
    plt.savefig(outpath)
    plt.close()

async def fetch_and_fill_history(dtu):
    """Fetch historical data and fill the in-memory data."""
    print(f"{datetime.now()} - INFO: Fetching historical data...")
    history_response = await dtu.async_app_get_hist_power()
    start_time = history_response.absolute_start
    step_time = history_response.step_time
    for i, power in enumerate(history_response.power_array):
        timestamp = start_time + (i * step_time)
        # timestamp = history_response.request_time - (len(history_response.power_array) * step_time) + (i * step_time)
        dt = datetime.fromtimestamp(timestamp)
        dtu_power_data.append((dt, power / 10))
    print(f"{datetime.now()} - INFO: Historical data filled successfully.")

async def main():
    print(f"{datetime.now()} - INFO: Starting data collection...")
    print(f"{datetime.now()} - INFO: connecting to DTU...{os.getenv('IPADDR', '')}")
    dtu = DTU(os.getenv('IPADDR', '192.168.1.183'))
    await fetch_and_fill_history(dtu)
    while True:
        response = await dtu.async_get_real_data_new()
        if response and response.sgs_data:
            sgs_data = response.sgs_data[0]
            dtu_power = response.dtu_power / 10  # Convert to watts
            dtu_daily_energy = response.dtu_daily_energy  # Daily energy in watt-hours
            now = datetime.now()
            dtu_power_data.append((now, dtu_power))
            # Keep only today's data in memory
            today = now.date()
            dtu_power_data[:] = [(dt, p) for dt, p in dtu_power_data if dt.date() == today]
            plot_dtu_power_today()
            save_dtu_power_csv()
            print(f"{now} - INFO: dtu_power: {dtu_power:4.1f} W | dtu_daily_energy: {dtu_daily_energy:.0f} Wh")
        await asyncio.sleep(60)

if __name__ == "__main__":
    asyncio.run(main())
