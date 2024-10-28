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

def check_brightness():
    pass


def set_brightness(monitor):
    pass


def set_brightness_all():
    pass


def create_br_value_file(path):
    # for monitor
    # write br
    pass


def read_br_from_file(path):
    pass


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
    # if not os.path.isfile(BRIGHTNESS_VALUE_FILE_PATH):
    if True:
        import subprocess

        with open(BRIGHTNESS_VALUE_FILE_PATH, "w") as br_value_file:
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
                
                current_brightness = output.decode().split("current value =     ")[1].split(",")[0]
                print(current_brightness)

                exit()

            br_value_file.close()


def main():
    from time import sleep
    
    global config

    init()

    print(config)

    while True:
        print("a")
        sleep(1)
        break

if __name__ == '__main__':
    main()