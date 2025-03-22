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
            "DS:voltage:GAUGE:120:0:U",  # Voltage in volts
            "DS:current:GAUGE:120:0:U",  # Current in amperes
            "DS:active_power:GAUGE:120:0:U",  # Active power in watts
            "DS:apparent_power:GAUGE:120:0:U",  # Apparent power in VA
            "DS:power_factor:GAUGE:120:0:1",  # Power factor (0 to 1)
            "DS:dtu_power:GAUGE:120:0:U",  # DTU power in watts
            "DS:dtu_daily_energy:GAUGE:120:0:U",  # DTU daily energy in watt-hours
            "RRA:AVERAGE:0.5:1:1440",  # Store 1-minute averages for 24 hours
            "RRA:AVERAGE:0.5:60:168"  # Store 1-hour averages for 7 days
        )

def update_rrd(voltage, current, active_power, apparent_power, power_factor, dtu_power, dtu_daily_energy):
    """Update the RRD database with new data."""
    rrdtool.update(
        RRD_FILE,
        f"N:{voltage}:{current}:{active_power}:{apparent_power}:{power_factor}:{dtu_power}:{dtu_daily_energy}"
    )

async def main():
    create_rrd()  # Ensure the RRD database is created
    print(f"{datetime.now()} - INFO: Starting data collection...")
    print(f"{datetime.now()} - INFO: RRD database: {RRD_FILE}")
    print(f"{datetime.now()} - INFO: connecting to DTU...{os.getenv('IPADDR', '')}")
    dtu = DTU(os.getenv('IPADDR', '192.168.1.184'))
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
