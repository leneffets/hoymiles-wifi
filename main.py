import asyncio
import logging
from hoymiles_wifi.dtu import DTU

# Configure logging with local timestamp
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

async def main():
    dtu = DTU('192.168.1.184')
    while True:
        response = await dtu.async_get_real_data_new()
        logging.debug(f"response: {response}")

        if response:
            if response.sgs_data:
                sgs_data = response.sgs_data[0]
                voltage = sgs_data.voltage / 10  # Assuming voltage is in tenths of a volt
                current = sgs_data.current / 10  # Assuming current is in tenths of an ampere
                active_power = sgs_data.active_power  # Active power in watts
                apparent_power = voltage * current  # Apparent power in VA
                power_factor = active_power / apparent_power if apparent_power != 0 else 0
                logging.info(f"Power Factor: {power_factor:.2f}")

            # dtu_power = response.dtu_power
            # dtu_power_str = f"{dtu_power // 10}.{dtu_power % 10}"
            # logging.info(f"dtu_power: {dtu_power_str}W")

            dtu_power = response.dtu_power
            logging.info(f"dtu_power: {dtu_power/10}W")

            # Split dtu_daily_energy
            dtu_daily_energy = response.dtu_daily_energy
            #dtu_daily_energy_str = f"{dtu_daily_energy // 10}.{dtu_daily_energy % 10}"
            logging.info(f"dtu_daily_energy: {dtu_daily_energy}Wh")

        await asyncio.sleep(60)

if __name__ == "__main__":
    asyncio.run(main())
