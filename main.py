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
                current_value = response.sgs_data[0].current
                logging.info(f"sgs_data.current: {current_value}")
        
        await asyncio.sleep(60)

if __name__ == "__main__":
    asyncio.run(main())