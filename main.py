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

def generate_graphs():
    """Generate RRD graphs similar to generate_graph.sh."""
    now = datetime.now()
    output_image_base = f"/workspace/data/{now.strftime('%Y-%m-%d')}"
    end_time = "now"
    width = "680"
    height = "400"

    # 1. Full graph (all data)
    rrdtool.graph(
        f"{output_image_base}-full.png",
        "--start", "00:00",
        "--end", end_time,
        "--title", f"Hoymiles Data Graph ({now.strftime('%Y-%m-%d')})",
        "--vertical-label", "Values",
        "--width", width,
        "--height", height,
        f"DEF:voltage={RRD_FILE}:voltage:AVERAGE",
        f"DEF:current={RRD_FILE}:current:AVERAGE",
        f"DEF:active_power={RRD_FILE}:active_power:AVERAGE",
        f"DEF:apparent_power={RRD_FILE}:apparent_power:AVERAGE",
        f"DEF:power_factor={RRD_FILE}:power_factor:AVERAGE",
        f"DEF:dtu_power={RRD_FILE}:dtu_power:AVERAGE",
        f"DEF:dtu_daily_energy={RRD_FILE}:dtu_daily_energy:AVERAGE",
        "LINE1:voltage#FF0000:Voltage (V)",
        "GPRINT:voltage:LAST:%20.2lf V\\n",
        "LINE1:current#00FF00:Current (A)",
        "GPRINT:current:LAST:%20.2lf A\\n",
        "LINE1:active_power#0000FF:Active Power (W)",
        "GPRINT:active_power:LAST:%20.2lf W\\n",
        "LINE1:apparent_power#FFFF00:Apparent Power (VA)",
        "GPRINT:apparent_power:LAST:%20.2lf VA\\n",
        "LINE1:power_factor#FF00FF:Power Factor",
        "GPRINT:power_factor:LAST:%20.2lf\\n",
        "LINE1:dtu_power#00FFFF:DTU Power (W)",
        "GPRINT:dtu_power:LAST:%20.2lf W\\n",
        "LINE1:dtu_daily_energy#FFA500:DTU Daily Energy (Wh)",
        "GPRINT:dtu_daily_energy:LAST:%20.2lf Wh\\n"
    )

    # 2. dtu_power last 3 hours
    rrdtool.graph(
        f"{output_image_base}-dtu_power_3hrs.png",
        "--start", "-3h",
        "--end", end_time,
        "--title", f"DTU Power ({now.strftime('%Y-%m-%d')} Last 3 Hours)",
        "--vertical-label", "Power (W)",
        "--width", width,
        "--height", height,
        f"DEF:dtu_power={RRD_FILE}:dtu_power:AVERAGE",
        "AREA:dtu_power#00222F:DTU Power (W)",
        "GPRINT:dtu_power:LAST:%20.2lf W\\n"
    )

    # 3. dtu_power last 30 minutes
    rrdtool.graph(
        f"{output_image_base}-dtu_power_30mins.png",
        "--start", "-30min",
        "--end", end_time,
        "--title", f"DTU Power ({now.strftime('%Y-%m-%d')} Last 30 Minutes)",
        "--vertical-label", "Power (W)",
        "--width", width,
        "--height", height,
        f"DEF:dtu_power={RRD_FILE}:dtu_power:AVERAGE",
        "LINE2:dtu_power#00FFFF:DTU Power (W)",
        "GPRINT:dtu_power:LAST:%20.2lf W\\n"
    )

    # 4. dtu_power today (from 06:00)
    rrdtool.graph(
        f"{output_image_base}-dtu_power_today.png",
        "--start", "06:00",
        "--end", end_time,
        "--title", f"DTU Power ({now.strftime('%Y-%m-%d')})",
        "--vertical-label", "Power (W)",
        "--width", width,
        "--height", height,
        f"DEF:dtu_power={RRD_FILE}:dtu_power:AVERAGE",
        f"DEF:dtu_daily_energy={RRD_FILE}:dtu_daily_energy:MAX",
        "AREA:dtu_power#002FAA:DTU Power (W)",
        "GPRINT:dtu_power:LAST:%20.2lf W\\n",
        "GPRINT:dtu_daily_energy:LAST:Total\\: %4.0lf Wh\\n"
    )

async def fetch_and_fill_history(dtu):
    """Fetch historical data and fill the RRD database."""
    print(f"{datetime.now()} - INFO: Fetching historical data...")

    history_response = await dtu.async_app_get_hist_power()
    print(f"history_response: {history_response}")
    start_time = history_response.absolute_start
    step_time = history_response.step_time

    for i, power in enumerate(history_response.power_array):
        # TODO: Fix the timestamp calculation
        # When returned in combined array, not the first request time is taken
        # timestamp = start_time + (i * step_time)
        timestamp = history_response.request_time - (len(history_response.power_array) * step_time) + (i * step_time)

        try:
            print(f"{datetime.fromtimestamp(timestamp)} - {timestamp}:U:U:U:U:U:{power/10}:U")
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
    print(f"{datetime.now()} - INFO: connecting to DTU...{os.getenv('IPADDR', '')}")
    dtu = DTU(os.getenv('IPADDR', '192.168.1.183'))
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

                # Generate graphs after updating RRD
                generate_graphs()

                print(f"{datetime.now()} - INFO: dtu_power: {dtu_power:4.1f} W | dtu_daily_energy: {dtu_daily_energy:4d} Wh")

        await asyncio.sleep(60)

if __name__ == "__main__":
    asyncio.run(main())
