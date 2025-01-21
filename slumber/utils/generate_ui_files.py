import os
import subprocess


def generate_ui_files(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".ui"):
                ui_file = os.path.join(root, file)
                py_file = os.path.join(root, file.replace(".ui", "_ui.py"))
                command = f"pyside6-uic {ui_file} -o {py_file}"
                try:
                    subprocess.run(command, check=True, shell=True)
                    print(f"Generated {py_file} from {ui_file}")
                except subprocess.CalledProcessError as e:
                    print(f"Error generating {py_file} from {ui_file}: {e}")

def main():
    ui_directory = os.path.join(os.path.dirname(__file__), '../gui')
    generate_ui_files(ui_directory)

if __name__ == "__main__":
    main()