# hoymiles-wifi

```
hoymiles-wifi --host 192.168.1.184 get-version-info
Get-version-info Response: 
dtu_hw_version: "H00.01.00"
dtu_sw_version: "V00.03.02"
inverter_hw_version: "H00.04.00"
inverter_sw_version: "V01.00.08"
```

```
hoymiles-wifi --host 192.168.1.184 get-real-data-new
Get-real-data-new Response: 
device_serial_number: "414393132164"
timestamp: 1742542601
ap: 1
firmware_version: 1
sgs_data {
  serial_number: 22070009471332
  firmware_version: 1
  voltage: 2389
  frequency: 4999
  active_power: 741
  current: 31
  power_factor: 1000
  temperature: 112
  warning_number: 3
  link_status: 1
  modulation_index_signal: 16580771
}
pv_data {
  serial_number: 22070009471332
  port_number: 1
  voltage: 367
  current: 124
  power: 457
  energy_total: 244094
  energy_daily: 46
}
pv_data {
  serial_number: 22070009471332
  port_number: 2
  voltage: 356
  current: 91
  power: 326
  energy_total: 236847
  energy_daily: 39
}
dtu_power: 741
dtu_daily_energy: 85
```

```
python main.py
```