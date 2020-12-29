import argparse
import datetime
import subprocess
from copy import deepcopy
from time import sleep

import uiautomation as auto


def mimic_clicks(interval=10.0):
    np = subprocess.Popen('notepad.exe')
    try:
        notepad_window = auto.WindowControl(searchDepth=1, ClassName='Notepad')
        if not notepad_window.Exists(3, 1):
            print('Cannot find notepad window')
            exit(0)
        notepad_window.SetTopmost(True)
        edit = notepad_window.EditControl()
        edit.GetValuePattern().SetValue(f"Notepad opened at {datetime.datetime.now()}")
        edit.SendKeys('{Ctrl}{End}{Enter}')

        count = 0
        start_time = datetime.datetime.now()
        while True:
            try:
                notepad_window.TitleBarControl().ButtonControl(foundIndex=2).Click()
                count += 1
                edit.SendKeys(f"Clicked {count} times\n")
                sleep(interval)
            except KeyboardInterrupt:
                print(f"Run time: {datetime.datetime.now() - start_time}")
                raise Exception("Stop the process")

    except Exception:
        np.terminate()


def _create_dict_from_parser(values: dict) -> dict:
    result = deepcopy(values)
    try:
        tmp_dict = dict()
        for arg in extra_args:
            k, v = arg.split("=")
            tmp_dict[k] = v
        for k, v in tmp_dict.items():
            try:
                result[k] = v
            except ValueError:
                pass
        return result
    except ValueError:
        raise ValueError("Invalid input provided")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    args, extra_args = parser.parse_known_args()
    kwargs = _create_dict_from_parser({
        'interval': 10,
    })
    mimic_clicks(interval=float(kwargs['interval']))
