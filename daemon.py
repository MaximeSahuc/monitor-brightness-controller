import os

BRIGHTNESS_VALUE_FILE_PATH = os.path.join(
    os.path.expanduser("~"),
    ".brightness"
)

CONFIG_FILE_PATH = os.path.join(
    os.path.expanduser("~/.config"),
    "brightness-controller.yml"
)

config = None


def get_brightness():
    with open(BRIGHTNESS_VALUE_FILE_PATH, "r") as br_value_file:
        value = br_value_file.read()
        br_value_file.close()
        return value


def set_brightness(monitor, brightness):
    import subprocess

    global config

    for display in config['displays']:
        i2c_bus = display['i2c-bus'].split('-')[1]

        if display['i2c-bus'] != monitor:
            continue

        bright = str(int((display['max-brightness'] / 100) * int(brightness)))
        brightness_cmd = str(display['brightness-feature-cmd'])

        subprocess.run([
            "ddcutil",
            "--bus",
            i2c_bus,
            "setvcp",
            brightness_cmd,
            bright
        ])


def get_monitor_brightness(i2c_bus):
    import subprocess

    for display in config["displays"]:
        i2c_bus = display["i2c-bus"].split('-')[1]
        br_cmd = display["brightness-feature-cmd"]

        p = subprocess.Popen(
            f"ddcutil --bus {i2c_bus} getvcp {br_cmd}",
            stdout=subprocess.PIPE,
            shell=True
        )

        output, err = p.communicate()
        p_status = p.wait()

        if p_status != 0:
            print(f"error: {err}")
        
        current_brightness = output.decode().split("current value =    ")[1].split(",")[0]
        return current_brightness


def read_config(path):
    import yaml

    with open(path, 'r') as config_file:
        return yaml.safe_load(config_file)


def init():
    import os

    # read config
    global config
    config = read_config(CONFIG_FILE_PATH)

    # check brightness value file
    if not os.path.isfile(BRIGHTNESS_VALUE_FILE_PATH):
        with open(BRIGHTNESS_VALUE_FILE_PATH, "w") as br_value_file:
            br_value_file.write("50")
            br_value_file.close()


def main():
    from time import sleep
    
    global config

    init()

    while True:
        target_brightness = get_brightness()

        for display in config["displays"]:
            monitor_br =  get_monitor_brightness(display["i2c-bus"])

            if monitor_br != target_brightness:
                set_brightness(display["i2c-bus"], target_brightness)


if __name__ == '__main__':
    main()