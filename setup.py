import os
import platform
import shutil
import sys
import traceback
import typing as p

term = shutil.get_terminal_size()
sep = "=" * term.columns

venv = False
default = 1

if os.name == "nt":
    print(f"Setup not supported on {platform.system()}")
    exit()


def _opt_selector(options: p.Dict[str, p.Any], default: p.Optional[int] = None, pmt: str = "") -> p.Tuple[int, p.Any]:
    _options = {}
    print("Choose variant")
    print(sep)

    num = 1
    for opt in options:
        if options[opt] is None:
            print()
            continue

        d = "*" if default == num else " "

        print(f"  {d}{num} - {opt}")
        _options[num] = options[opt]
        num += 1
    print(sep)

    while True:
        opt = input(f"{pmt}-> ")
        if opt.isdigit():
            opt = int(opt)
            if opt in _options:
                return opt, _options[opt]
        if opt == "" and default is not None:
            return default, _options[default]

        print("Incorrect answer")
        pmt = ""


def _yes(default: bool = True) -> bool:
    while True:
        if default:
            it = "[Y|n]"
        else:
            it = "[y|N]"

        i = input(f"{it} -> ")
        if i.lower() in ["y", "n"]:
            return i.lower() == "y"
        if i == "":
            return default

        print("Incorrect answer")


def _input(prompt: str, default: str = None, required: bool = True) -> str:
    if default:
        print(f"Default {default}")
    while True:
        result = input(f"{prompt} -> ")
        if not result:
            if default:
                result = default
                break
            elif required:
                print("Parameter required")
        else:
            break

    return result


def _cmd(cmd: str, show_cmd: bool = True) -> bool:
    if show_cmd:
        input(f"Press enter for execute {cmd}")
    result = os.system(cmd)
    return True if result == 0 else False


def _clear():
    print()
    print('\033c', end="")


def _enter():
    input("Press enter, to continue ...")


def create_samples_txt():
    if not os.path.isfile("samples.txt"):
        with open("samples.txt", "w"):
            print("File created")
    else:
        print("File exists")
    _enter()
    return True


def systemd_unit_generator():
    while True:
        username = _input("Your username", os.environ["USER"])
        path = _input("Path to root of project", os.path.dirname(os.path.abspath(__file__)))
        py_path = _input("Path to python 3.9", sys.executable)

        print("Send kill (if SIGTERM Timeout)")
        send_kill = "off"
        if _yes(True):
            send_kill = "on"

        with open("FunnyPineappleBot.sample.service", "r") as file:
            sample = file.read().format(username=username, path=path, py_path=py_path, send_kill=send_kill)

        _clear()
        print(
            f"{sep}",
            f"{sample}",
            f"{sep}",
            f"Your username - {username}",
            f"Path to root of project - {path}",
            f"Path to python 3.9 - {py_path}",
            f"Send kill - {send_kill}",
            f"{sep}",
            "",
            "All correct ?",
            sep="\n"
        )
        if _yes(False):
            with open("FunnyPineappleBot.service", "w") as file:
                file.write(sample)
            _clear()

            print("Link unit from /etc/systemd/system/ ?")
            if _yes():
                _cmd("sudo mv FunnyPineappleBot.service /etc/systemd/system/")
                _cmd("sudo ln /etc/systemd/system/FunnyPineappleBot.service ./ -s")
            break
        else:
            _clear()
    print(sep)
    _enter()
    return True


def config_generator():
    try:
        import config
    except ImportError:
        config = object()
    while True:
        main_token = _input("Main bot token", getattr(config, "main_token", None))
        test_token = _input("Test bot token", getattr(config, "test_token", None))

        with open("shared/config.sample.py", "r") as file:
            sample = file.read().format(main_token=main_token, test_token=test_token)

        print(
            f"{sep}",
            f"{sample}",
            f"{sep}",
            "All correct ?",
            sep="\n"
        )

        if _yes(False):
            with open("shared/config.py", "w") as file:
                file.write(sample)
            break
        else:
            _clear()
    return True


def install_dependencies():
    with open("dependencies", "r") as file:
        dependencies = file.read()
    print(
        "Install this ?",
        f"{sep}",
        f"{dependencies}",
        f"{sep}",
        sep="\n"
    )
    _cmd("pip install -U -r dependencies", False)
    print(f"{sep}\nSuccessfully installed")
    _enter()
    return True


if __name__ == '__main__':
    opts = {
        "Create samples.txt file": create_samples_txt,
        "Setup systemd unit": systemd_unit_generator,
        "Setup config.py": config_generator,
        "Install or Update dependencies": install_dependencies,
        "Exit": exit,
    }
    exit_index = list(opts.keys()).index("Exit") + 1
    default = 1
    pmt = ""

    _clear()
    while True:
        if default >= exit_index:
            default = exit_index
        term = shutil.get_terminal_size()
        sep = "=" * term.columns
        try:
            _clear()
            num, opt = _opt_selector(opts, default, pmt)
            _clear()
            res = opt()
            _clear()

            if num != default:
                default = num + 1
            elif res is True:
                default += 1

            if res is not True:
                pmt = f"{res!r} "
                if num == default:
                    default = num + 1
            else:
                pmt = ""

        except KeyboardInterrupt:
            break
        except Exception as e:
            pmt = f"An error has occurred ({e.__class__.__name__}:{e.args[0]})"
            trc = traceback.format_exc()
            print(trc)
            _enter()
    _clear()
