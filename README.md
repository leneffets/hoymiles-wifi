# hoymiles-wifi

This tool collects and visualizes solar production data from a Hoymiles DTU.

## Usage

```
IPADDR=192.168.1.183 python main.py
```

```
docker run -it -v $PWD:/workspace/data/ -e IPADDR=192.168.1.183 ghcr.io/leneffets/hoymiles-wifi:latest
```

- The script fetches historical and live data from your DTU.
- It generates a PNG graph for today's DTU power using matplotlib.
- The graph is saved as `/workspace/data/YYYY-MM-DD-dtu_power_today.png`.
- Data for today is also saved as `/workspace/data/YYYY-MM-DD-dtu_power_today.csv`.

## Example Output

- Graph:  
  `/workspace/data/2025-09-28-dtu_power_today.png`
- CSV:  
  `/workspace/data/2025-09-28-dtu_power_today.csv`

## Requirements

- Python 3.12+
- matplotlib

Install requirements:
```
pip install -r requirements.txt
```

## License

See [LICENSE](LICENSE).