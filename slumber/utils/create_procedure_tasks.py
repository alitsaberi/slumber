import os
import subprocess

from ruamel.yaml import YAML


def select_task_type():
    options = {"1": "pre_processing", "2": "post_processing", "3": "action"}
    print("Select task type:")
    for key, value in options.items():
        print(f"{key}. {value}")
    while True:
        choice = input("Enter the number corresponding to the task type: ")
        if choice in options:
            return options[choice]
        else:
            print("Invalid selection. Please try again.")


def load_yaml(settings_path):
    yaml = YAML()
    yaml.preserve_quotes = True
    if not os.path.exists(settings_path):
        print(f"Settings file not found at {settings_path}.")
        return yaml.load("")
    try:
        with open(settings_path) as f:
            return yaml.load(f) or {}
    except Exception as e:
        print(f"Error reading YAML file: {e}")
        return {}


def save_yaml(data, settings_path):
    yaml = YAML()
    yaml.preserve_quotes = True
    yaml.indent(mapping=2, sequence=4, offset=2)
    try:
        with open(settings_path, "w") as f:
            yaml.dump(data, f)
    except Exception as e:
        print(f"Error writing YAML file: {e}")


def create_widget_ui(file_path, header, name):
    template = f"""<?xml version="1.0" encoding="UTF-8"?>
<ui version="4.0">
 <class>Widget</class>
 <widget class="QWidget" name="Widget">
  <property name="geometry">
   <rect>
    <x>0</x>
    <y>0</y>
    <width>800</width>
    <height>600</height>
   </rect>
  </property>
  <property name="sizePolicy">
   <sizepolicy hsizetype="Expanding" vsizetype="Expanding">
    <horstretch>0</horstretch>
    <verstretch>0</verstretch>
   </sizepolicy>
  </property>
  <property name="maximumSize">
   <size>
    <width>3840</width>
    <height>2160</height>
   </size>
  </property>
  <property name="windowTitle">
   <string>{header}</string>
  </property>
  <layout class="QVBoxLayout" name="verticalLayout">
   <item>
    <layout class="QHBoxLayout" name="horizontalLayout_4">
     <property name="sizeConstraint">
      <enum>QLayout::SizeConstraint::SetMaximumSize</enum>
     </property>
     <item>
      <widget class="QLabel" name="widget_title">
       <property name="maximumSize">
        <size>
         <width>16777215</width>
         <height>100</height>
        </size>
       </property>
       <property name="font">
        <font>
         <family>Arial</family>
         <pointsize>36</pointsize>
        </font>
       </property>
       <property name="text">
        <string>{header}</string>
       </property>
      </widget>
     </item>
     <item>
      <spacer name="horizontalSpacer">
       <property name="orientation">
        <enum>Qt::Orientation::Horizontal</enum>
       </property>
       <property name="sizeHint" stdset="0">
        <size>
         <width>40</width>
         <height>20</height>
        </size>
       </property>
      </spacer>
     </item>
     <item>
      <widget class="QPushButton" name="button_info">
       <property name="minimumSize">
        <size>
         <width>50</width>
         <height>50</height>
        </size>
       </property>
       <property name="maximumSize">
        <size>
         <width>50</width>
         <height>50</height>
        </size>
       </property>
       <property name="styleSheet">
        <string notr="true">QPushButton {{
    color: rgb(255, 255, 255);
    background-color: rgb(1, 92, 187);
    border: 1px;
    border-radius: 10px;
}}

QPushButton:hover {{
    color: rgb(220,221,229);
    background-color: rgb(37, 150, 190);
}}

QPushButton:pressed {{
    color: rgb(220,221,229);
    background-color: rgb(37, 150, 190);
}}</string>
       </property>
       <property name="text">
        <string/>
       </property>
       <property name="icon">
        <iconset theme="QIcon::ThemeIcon::DialogInformation"/>
       </property>
       <property name="iconSize">
        <size>
         <width>40</width>
         <height>40</height>
        </size>
       </property>
      </widget>
     </item>
    </layout>
   </item>
   <item>
    <widget class="QWidget" name="widget_body" native="true">
     <property name="sizePolicy">
      <sizepolicy hsizetype="Expanding" vsizetype="Expanding">
       <horstretch>0</horstretch>
       <verstretch>0</verstretch>
      </sizepolicy>
     </property>
     <property name="maximumSize">
      <size>
       <width>3840</width>
       <height>2160</height>
      </size>
     </property>
     <widget class="QLabel" name="label_body">
      <property name="geometry">
       <rect>
        <x>200</x>
        <y>160</y>
        <width>391</width>
        <height>211</height>
       </rect>
      </property>
      <property name="font">
       <font>
        <bold>false</bold>
       </font>
      </property>
      <property name="text">
       <string>{name} works correctly.</string>
      </property>
     </widget>
    </widget>
   </item>
  </layout>
 </widget>
 <resources/>
 <connections/>
</ui>
"""
    try:
        with open(file_path, "w") as f:
            f.write(template)
        print(f"Created {file_path}")
    except Exception as e:
        print(f"Error writing widget.ui: {e}")


def create_help_ui(file_path, header, name):
    template = f"""<?xml version="1.0" encoding="UTF-8"?>
<ui version="4.0">
 <class>HelpDialog</class>
 <widget class="QDialog" name="HelpDialog">
  <property name="windowTitle">
   <string>Slumber - {header}</string>
  </property>
  <property name="sizePolicy">
   <sizepolicy hsizetype="Expanding" vsizetype="Expanding">
    <horstretch>0</horstretch>
    <verstretch>0</verstretch>
   </sizepolicy>
  </property>
  <property name="minimumSize">
   <size>
    <width>400</width>
    <height>300</height>
   </size>
  </property>
  <layout class="QVBoxLayout" name="verticalLayout">
   <item>
    <widget class="QWidget" name="widget_body" native="true">
     <property name="sizePolicy">
      <sizepolicy hsizetype="Expanding" vsizetype="Expanding">
       <horstretch>0</horstretch>
       <verstretch>0</verstretch>
      </sizepolicy>
     </property>
     <property name="maximumSize">
      <size>
       <width>3840</width>
       <height>2160</height>
      </size>
     </property>
     <widget class="QLabel" name="label_body">
      <property name="text">
       <string>{name} - dialog window works.</string>
      </property>
      <property name="font">
       <font>
        <pointsize>12</pointsize>
        <bold>false</bold>
       </font>
      </property>
     </widget>
    </widget>
   </item>
   <item>
    <layout class="QHBoxLayout" name="buttonLayout">
     <item>
      <spacer name="horizontalSpacer">
       <property name="orientation">
        <enum>Qt::Orientation::Horizontal</enum>
       </property>
       <property name="sizeHint" stdset="0">
        <size>
         <width>40</width>
         <height>20</height>
        </size>
       </property>
      </spacer>
     </item>
     <item>
      <widget class="QPushButton" name="button_ok">
       <property name="text">
        <string>OK</string>
       </property>
      </widget>
     </item>
     <item>
      <widget class="QPushButton" name="button_cancel">
       <property name="text">
        <string>Cancel</string>
       </property>
      </widget>
     </item>
    </layout>
   </item>
  </layout>
 </widget>
 <resources/>
 <connections/>
</ui>
"""
    try:
        with open(file_path, "w") as f:
            f.write(template)
        print(f"Created {file_path}")
    except Exception as e:
        print(f"Error writing help.ui: {e}")


def create_widget_py(file_path, header, name):
    template = """from PySide6.QtWidgets import QWidget, QDialog, QPushButton
from PySide6.QtCore import Signal, QSize
from .help_ui import Ui_HelpDialog
from .widget_ui import Ui_Widget
import os

class WidgetPage(QWidget, Ui_Widget):
    is_done_signal = Signal(int)

    # Getting a index as well as status parameter to set the status of the task
    # 1: Task is not done
    # 2: Task is done
    def __init__(self, index, status=1, parent=None):
        super().__init__(parent)
        self.index = index
        self.status = status
        self.setupUi(self)  # Setup the UI from the generated class

        # Connect the info button to open the help dialog
        self.button_info.clicked.connect(self.open_help_dialog)

        # TODO: DELETE THIS BUTTON
        self.button_done = QPushButton("Done", self)
        self.button_done.setObjectName("button_done")
        self.button_done.setMinimumSize(QSize(100, 40))
        self.verticalLayout.addWidget(self.button_done)
        self.button_done.clicked.connect(self.emit_done_signal)

        
    def start(self):
        # TODO: Implement your functionality here, which will be called 
        # when the task opens.
        # Make sure to use the status as well, to make sure to not call this 
        # function several times
        if self.status == 1:
            print("Task started")
        else:
            print("Task already done")
        

    def open_help_dialog(self):
        # Create a QDialog instance
        dialog = QDialog(self)
        dialog.setWindowTitle("Help")  # Optional: Set window title

        # Set up the UI for the dialog using Ui_HelpDialog
        ui = Ui_HelpDialog()
        ui.setupUi(dialog)

        # Connect dialog buttons to methods
        # Assuming your help.ui has buttons named 'button_ok' and 'button_cancel'
        ui.button_ok.clicked.connect(
            lambda: self.handle_help_response(dialog, accepted=True)
        )
        ui.button_cancel.clicked.connect(
            lambda: self.handle_help_response(dialog, accepted=False)
        )

        # Execute the dialog modally
        dialog.exec()

    def handle_help_response(self, dialog, accepted):
        if accepted:
            print("OK button pressed in Help Dialog")
        else:
            print("Cancel button pressed in Help Dialog")
        # Close the dialog
        dialog.close()

    # DELETE THIS FUNCTION
    def emit_done_signal(self):
        if self.status == 1:
            self.is_done_signal.emit(self.index)
        self.status = 2
"""
    try:
        with open(file_path, "w") as f:
            f.write(template)
        print(f"Created {file_path}")
    except Exception as e:
        print(f"Error writing widget.py: {e}")


def generate_ui_py(ui_path, output_path):
    try:
        subprocess.run(["pyside6-uic", ui_path, "-o", output_path], check=True)
        print(f"Generated {output_path} from {ui_path}")
    except subprocess.CalledProcessError as e:
        print(f"Error generating {output_path}: {e}")
    except FileNotFoundError:
        print(
            "pyside6-uic command not found. Please ensure PySide6 is installed "
            "and pyside6-uic is in your PATH."
        )


def ensure_init_files(full_path):
    """
    Ensures that __init__.py exists in all directories along the given path.
    Creates an empty __init__.py if it does not exist.
    """
    full_path = os.path.abspath(full_path)
    dirs = []
    while True:
        full_path, folder = os.path.split(full_path)
        if folder:
            dirs.insert(0, folder)
        else:
            if full_path:
                dirs.insert(0, full_path)
            break

    current = ""
    for folder in dirs:
        current = os.path.join(current, folder)
        init_path = os.path.join(current, "__init__.py")
        if not os.path.exists(init_path):
            try:
                open(init_path, "w").close()
                print(f"Created {init_path}")
            except Exception as e:
                print(f"Error creating {init_path}: {e}")


def main():
    # 1. Collect inputs
    raw_name = input("Enter name: ")
    header = input("Enter header: ")
    task_type = select_task_type()
    adjusted_name = raw_name.lower().replace(" ", "_").replace("-", "_")

    # 2. Load YAML
    settings_path = "./configs/settings.yaml"
    data = load_yaml(settings_path)

    # Navigate to 'procedure_tasks'
    procedure_tasks = data.get("procedure_tasks")
    if procedure_tasks is None:
        procedure_tasks = data.setdefault("procedure_tasks", [])

    # 3. Check duplicates
    for task in procedure_tasks:
        if task.get("name", "").lower() == raw_name.lower():
            print("Duplicate name found. Please run again with a different name.")
            return

    # 4. Add task entry
    entry = {
        "name": raw_name,
        "header": header,
        "module": f"slumber.gui.pages.procedure.tasks.{adjusted_name}",
        "type": task_type,
        "enabled": True,
    }
    procedure_tasks.append(entry)

    # 5. Write updated YAML
    save_yaml(data, settings_path)

    # 6. Create folder and files
    base_path = os.path.join(
        "slumber", "gui", "pages", "procedure", "tasks", adjusted_name
    )
    os.makedirs(base_path, exist_ok=True)
    print(f"Created directory: {base_path}")

    # Ensure __init__.py files in all parent directories
    ensure_init_files(base_path)

    for filename in ["widget_ui.py", "widget.py", "widget.ui", "help_ui.py", "help.ui"]:
        file_path = os.path.join(base_path, filename)
        if not os.path.exists(file_path):
            if filename == "widget.ui":
                create_widget_ui(file_path, header, raw_name)
                # Generate widget_ui.py from widget.ui
                ui_path = file_path
                output_path = os.path.join(base_path, "widget_ui.py")
                generate_ui_py(ui_path, output_path)
            elif filename == "help.ui":
                create_help_ui(file_path, header, raw_name)
                # Generate help_ui.py from help.ui
                ui_path = file_path
                output_path = os.path.join(base_path, "help_ui.py")
                generate_ui_py(ui_path, output_path)
            elif filename == "widget.py":
                create_widget_py(file_path, header, raw_name)
            elif filename.endswith("_ui.py"):
                # These are handled above
                continue
            else:
                try:
                    open(file_path, "w").close()
                    print(f"Created empty {file_path}")
                except Exception as e:
                    print(f"Error creating {filename}: {e}")

    # 7. Optional HTML support
    html_support = input("Need HTML support? (y/n): ").lower()
    if html_support == "y":
        assets_path = os.path.join(base_path, "assets")
        for sub in ["html", "css", "js"]:
            os.makedirs(os.path.join(assets_path, sub), exist_ok=True)
            print(f"Created directory: {os.path.join(assets_path, sub)}")
        html_files = {"html/index.html": "", "css/styles.css": "", "js/script.js": ""}
        for path, content in html_files.items():
            file_path = os.path.join(assets_path, path)
            if not os.path.exists(file_path):
                try:
                    with open(file_path, "w") as f:
                        f.write(content)
                    print(f"Created {file_path}")
                except Exception as e:
                    print(f"Error creating {path}: {e}")

    print("Procedure task added successfully.")


if __name__ == "__main__":
    main()
