#!/bin/bash

# Variables
RRD_FILE="/workspace/data/data.rrd"  # Path to the RRD file
OUTPUT_IMAGE="/workspace/data/graph.png"  # Output image file
START_TIME="-1d"  # Start time (e.g., last day)
END_TIME="now"  # End time
TITLE="Hoymiles Data Graph"
VERTICAL_LABEL="Values"

# Generate the graph for all data
rrdtool graph "$OUTPUT_IMAGE" \
    --start "$START_TIME" \
    --end "$END_TIME" \
    --title "$TITLE" \
    --vertical-label "$VERTICAL_LABEL" \
    DEF:voltage="$RRD_FILE":voltage:AVERAGE \
    DEF:current="$RRD_FILE":current:AVERAGE \
    DEF:active_power="$RRD_FILE":active_power:AVERAGE \
    DEF:apparent_power="$RRD_FILE":apparent_power:AVERAGE \
    DEF:power_factor="$RRD_FILE":power_factor:AVERAGE \
    DEF:dtu_power="$RRD_FILE":dtu_power:AVERAGE \
    DEF:dtu_daily_energy="$RRD_FILE":dtu_daily_energy:AVERAGE \
    LINE1:voltage#FF0000:"Voltage (V)" \
    GPRINT:voltage:LAST:"Current\\: %6.2lf V" \
    LINE1:current#00FF00:"Current (A)" \
    GPRINT:current:LAST:"Current\\: %6.2lf A" \
    LINE1:active_power#0000FF:"Active Power (W)" \
    GPRINT:active_power:LAST:"Current\\: %6.2lf W" \
    LINE1:apparent_power#FFFF00:"Apparent Power (VA)" \
    GPRINT:apparent_power:LAST:"Current\\: %6.2lf VA" \
    LINE1:power_factor#FF00FF:"Power Factor" \
    GPRINT:power_factor:LAST:"Current\\: %6.2lf" \
    LINE1:dtu_power#00FFFF:"DTU Power (W)" \
    GPRINT:dtu_power:LAST:"Current\\: %6.2lf W" \
    LINE1:dtu_daily_energy#FFA500:"DTU Daily Energy (Wh)" \
    GPRINT:dtu_daily_energy:LAST:"Current\\: %6.2lf Wh"

# Generate the graph for dtu_power for the last 3 hours
OUTPUT_IMAGE_3HRS="/workspace/data/dtu_power_3hrs.png"
rrdtool graph "$OUTPUT_IMAGE_3HRS" \
    --start "00:00" \
    --end "$END_TIME" \
    --title "DTU Power (Last 3 Hours)" \
    --vertical-label "Power (W)" \
    DEF:dtu_power="$RRD_FILE":dtu_power:AVERAGE \
    LINE2:dtu_power#00FFFF:"DTU Power (W)" \
    GPRINT:dtu_power:LAST:"Current\\: %6.2lf W"

# Generate the graph for dtu_power for today
OUTPUT_IMAGE_TODAY="/workspace/data/dtu_power_today.png"
rrdtool graph "$OUTPUT_IMAGE_TODAY" \
    --start "00:00" \
    --end "$END_TIME" \
    --title "DTU Power (Today)" \
    --vertical-label "Power (W)" \
    DEF:dtu_power="$RRD_FILE":dtu_power:AVERAGE \
    LINE2:dtu_power#00FFFF:"DTU Power (W)" \
    GPRINT:dtu_power:LAST:"Current\\: %6.2lf W"
