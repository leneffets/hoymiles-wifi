import asyncio
import os
from datetime import datetime
import rrdtool  # Import rrdtool for database handling
from hoymiles_wifi.dtu import DTU

RRD_FILE = "/workspace/data/data.rrd"  # Define the RRD file path

def create_rrd():
    """Create an RRD database if it doesn't exist."""
    if not os.path.exists(RRD_FILE):
        rrdtool.create(
            RRD_FILE,
            "--step", "60",  # 60-second intervals
            "--start", "-86400",  # Start 24 hours ago
            "DS:voltage:GAUGE:120:0:U",  # Voltage in volts, heartbeat increased to 24 hours
            "DS:current:GAUGE:120:0:U",  # Current in amperes, heartbeat increased to 24 hours
            "DS:active_power:GAUGE:120:0:U",  # Active power in watts, heartbeat increased to 24 hours
            "DS:apparent_power:GAUGE:120:0:U",  # Apparent power in VA, heartbeat increased to 24 hours
            "DS:power_factor:GAUGE:120:0:1",  # Power factor (0 to 1), heartbeat increased to 24 hours
            "DS:dtu_power:GAUGE:86400:0:U",  # DTU power in watts, heartbeat increased to 24 hours
            "DS:dtu_daily_energy:GAUGE:120:0:U",  # DTU daily energy in watt-hours, heartbeat increased to 24 hours
            "RRA:AVERAGE:0.5:1:4320",  # Store 1-minute averages for 72 hours
            "RRA:AVERAGE:0.5:60:168"  # Store 1-hour averages for 7 days
        )

def update_rrd(voltage, current, active_power, apparent_power, power_factor, dtu_power, dtu_daily_energy):
    """Update the RRD database with new data."""
    # Get the last update time from the RRD database
    #last_update_time = int(rrdtool.last(RRD_FILE))
    current_time = int(datetime.now().timestamp())

    rrdtool.update(
        RRD_FILE,
        f"{current_time}:{voltage}:{current}:{active_power}:{apparent_power}:{power_factor}:{dtu_power}:{dtu_daily_energy}"
    )

async def fetch_and_fill_history(dtu):
    """Fetch historical data and fill the RRD database."""
    print(f"{datetime.now()} - INFO: Fetching historical data...")

    history_response = await dtu.async_app_get_hist_power()

    start_time = history_response.absolute_start
    step_time = history_response.step_time

    for i, power in enumerate(history_response.power_array):
        timestamp = start_time + (i * step_time)

        try:
            print(f"{timestamp}:U:U:U:U:U:{power/10}:U")
            rrdtool.update(
                RRD_FILE,
                f"{timestamp}:U:U:U:U:U:{power/10}:U"  # Only power is available, others are unknown
            )
        except rrdtool.OperationalError as e:
            NotImplementedError
            #print(f"ERROR Update: {timestamp}:U:U:U:U:U:{power/10}:U")

    print(f"{datetime.now()} - INFO: Historical data filled successfully.")

async def main():
    create_rrd()  # Ensure the RRD database is created
    print(f"{datetime.now()} - INFO: Starting data collection...")
    print(f"{datetime.now()} - INFO: RRD database: {RRD_FILE}")
    print(f"{datetime.now()} - INFO: Connecting to DTU...{os.getenv('IPADDR', '192.168.1.184')}")
    dtu = DTU(os.getenv('IPADDR', '192.168.1.184'))

    # Fetch and fill historical data if needed
    await fetch_and_fill_history(dtu)

    while True:
        response = await dtu.async_get_real_data_new()
        # print(f"{datetime.now()}: response: {response}")

        if response:
            if response.sgs_data:
                sgs_data = response.sgs_data[0]
                voltage = sgs_data.voltage / 10  # Assuming voltage is in tenths of a volt
                current = sgs_data.current / 10  # Assuming current is in tenths of an ampere
                active_power = sgs_data.active_power  # Active power in watts
                apparent_power = voltage * current  # Apparent power in VA
                power_factor = active_power / apparent_power if apparent_power != 0 else 0
                dtu_power = response.dtu_power / 10  # Convert to watts
                dtu_daily_energy = response.dtu_daily_energy  # Daily energy in watt-hours

                # Update the RRD database
                update_rrd(voltage, current, active_power, apparent_power, power_factor, dtu_power, dtu_daily_energy)

                print(f"{datetime.now()} - INFO: dtu_power: {dtu_power:4.1f} W | dtu_daily_energy: {dtu_daily_energy:4d} Wh")

        await asyncio.sleep(60)

if __name__ == "__main__":
    asyncio.run(main())
