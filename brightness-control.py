import os
import sys
import yaml
import subprocess

config_path = f"{os.path.dirname(__file__)}/config.yml"

with open(config_path, 'r') as config_file:
    config = yaml.safe_load(config_file)

brightness = int(sys.argv[1])

for d in config['displays']:
    i2c_bus = d['i2c-bus'].split('-')[1]
    bright = str(int((d['max-brightness'] / 100) * brightness))
    brightness_cmd = str(d['brightness-feature-cmd'])
    # ddcutil --bus 3 setvcp 10 10
    subprocess.run(["ddcutil", "--bus", i2c_bus, "setvcp", brightness_cmd, bright])