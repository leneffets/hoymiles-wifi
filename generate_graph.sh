#!/bin/bash

# Variables
RRD_FILE="/workspace/data/data.rrd"  # Path to the RRD file
OUTPUT_IMAGE="/workspace/data/$(date +'%Y-%m-%d')"  # Output image file
START_TIME="-1d"  # Start time (e.g., last day)
END_TIME="now"  # End time
TITLE="Hoymiles Data Graph"
VERTICAL_LABEL="Values"
WIDTH=680  # Image width
HEIGHT=400  # Image height

# Generate the graph for all data
rrdtool graph "$OUTPUT_IMAGE-full.png" \
    --start "$START_TIME" \
    --end "$END_TIME" \
    --title "$TITLE" \
    --vertical-label "$VERTICAL_LABEL" \
    --width "$WIDTH" \
    --height "$HEIGHT" \
    DEF:voltage="$RRD_FILE":voltage:AVERAGE \
    DEF:current="$RRD_FILE":current:AVERAGE \
    DEF:active_power="$RRD_FILE":active_power:AVERAGE \
    DEF:apparent_power="$RRD_FILE":apparent_power:AVERAGE \
    DEF:power_factor="$RRD_FILE":power_factor:AVERAGE \
    DEF:dtu_power="$RRD_FILE":dtu_power:AVERAGE \
    DEF:dtu_daily_energy="$RRD_FILE":dtu_daily_energy:AVERAGE \
    LINE1:voltage#FF0000:"Voltage (V)" \
    GPRINT:voltage:LAST:"%20.2lf V\\n" \
    LINE1:current#00FF00:"Current (A)" \
    GPRINT:current:LAST:"%20.2lf A\\n" \
    LINE1:active_power#0000FF:"Active Power (W)" \
    GPRINT:active_power:LAST:"%20.2lf W\\n" \
    LINE1:apparent_power#FFFF00:"Apparent Power (VA)" \
    GPRINT:apparent_power:LAST:"%20.2lf VA\\n" \
    LINE1:power_factor#FF00FF:"Power Factor" \
    GPRINT:power_factor:LAST:"%20.2lf\\n" \
    LINE1:dtu_power#00FFFF:"DTU Power (W)" \
    GPRINT:dtu_power:LAST:"%20.2lf W\\n" \
    LINE1:dtu_daily_energy#FFA500:"DTU Daily Energy (Wh)" \
    GPRINT:dtu_daily_energy:LAST:"%20.2lf Wh\\n"

# Generate the graph for dtu_power for the last 3 hours
OUTPUT_IMAGE_3HRS="$OUTPUT_IMAGE-dtu_power_3hrs.png"
rrdtool graph "$OUTPUT_IMAGE_3HRS" \
    --start "-3h" \
    --end "$END_TIME" \
    --title "DTU Power (Last 3 Hours)" \
    --vertical-label "Power (W)" \
    --width "$WIDTH" \
    --height "$HEIGHT" \
    DEF:dtu_power="$RRD_FILE":dtu_power:AVERAGE \
    LINE2:dtu_power#00FFFF:"DTU Power (W)" \
    GPRINT:dtu_power:LAST:"%20.2lf W\\n"

# Generate the graph for dtu_power for the last 30 mins
OUTPUT_IMAGE_30MINS="$OUTPUT_IMAGE-dtu_power_30mins.png"
rrdtool graph "$OUTPUT_IMAGE_30MINS" \
    --start "-30min" \
    --end "$END_TIME" \
    --title "DTU Power (Last 30 Minutes)" \
    --vertical-label "Power (W)" \
    --width "$WIDTH" \
    --height "$HEIGHT" \
    DEF:dtu_power="$RRD_FILE":dtu_power:AVERAGE \
    LINE2:dtu_power#00FFFF:"DTU Power (W)" \
    GPRINT:dtu_power:LAST:"%20.2lf W\\n"

# Generate the graph for dtu_power for today
OUTPUT_IMAGE_TODAY="$OUTPUT_IMAGE-dtu_power_today.png"
rrdtool graph "$OUTPUT_IMAGE_TODAY" \
    --start "06:00" \
    --end "$END_TIME" \
    --title "DTU Power (Today)" \
    --vertical-label "Power (W)" \
    --width "$WIDTH" \
    --height "$HEIGHT" \
    DEF:dtu_power="$RRD_FILE":dtu_power:AVERAGE \
    DEF:dtu_daily_energy="$RRD_FILE":dtu_daily_energy:MAX \
    AREA:dtu_power#002FAA:"DTU Power (W)" \
    LINE2:dtu_daily_energy#67F200:"Total (Wh)" \
    GPRINT:dtu_power:LAST:"%20.2lf W\\n" \
    GPRINT:dtu_daily_energy:LAST:"Total\: %4.0lf Wh\\n"
