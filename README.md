# SLUMBER - Sleep Logging and Unsupervised Monitoring through BioElectrical Recordings

## Description

<!--
Provide a concise description of your project here.
Describe what it does, the problem it solves, and why it’s useful.
-->

## Table of Contents

- [SLUMBER - Sleep Logging and Unsupervised Monitoring through BioElectrical Recordings](#slumber---sleep-logging-and-unsupervised-monitoring-through-bioelectrical-recordings)
  - [Description](#description)
  - [Table of Contents](#table-of-contents)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Usage](#usage)
  - [Add a Procedure Task](#add-a-procedure-task)
    - [Running the Script](#running-the-script)
      - [Files Created](#files-created)
      - [YAML Configuration Update](#yaml-configuration-update)
    - [How is the added task work?](#how-is-the-added-task-work)
    - [How to adjust the UI](#how-to-adjust-the-ui)
  - [Configuration](#configuration)
  - [Testing](#testing)
  - [Deployment](#deployment)
  - [Contributing](#contributing)
  - [License](#license)
  - [Contact](#contact)

## Prerequisites

<!--
List any prerequisites for your project such as Python version or system requirements.
For example:
- Python >= 3.9
- Poetry >= 1.0
-->

## Installation

<!--
Describe how to set up your development environment.
Include steps to install Poetry and any other dependencies required for the project.
-->

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/yourproject.git
   ```
2. **Navigate to the project directory**
   ```bash
   cd yourproject
   ```
3. **Install dependencies with Poetry**
   ```bash
   poetry install
   ```

## Usage

<!--
Explain how to run or use your application. Provide examples and common use cases.
-->

After installing dependencies, you can start the application with:

```bash
poetry run slumber
```

## Add a Procedure Task

The `create_task` script allows you to add a new procedure task to the SLUMBER application. This script performs the following actions:

1. **Collects Inputs:** Prompts the user to enter the task name, header, and select the task type.
2. **Loads YAML Configuration:** Reads the existing configuration from `configs/settings.yaml`.
3. **Checks for Duplicates:** Ensures that the task name does not already exist in the configuration.
4. **Adds Task Entry:** Appends the new task entry to the `procedure_tasks` section in the YAML configuration.
5. **Creates Necessary Files:** Generates the required UI and Python files for the new task.
6. **Optional HTML Support:** If requested, creates directories and files for HTML, CSS, and JavaScript support.

### Running the Script

To add a new procedure task, run the following command:

```bash
poetry run create_task
```

Follow the prompts to enter the task details. The script will handle the rest, ensuring that the new task is properly configured and integrated into the SLUMBER application.

#### Files Created

The script generates the following files in the slumber/gui/pages/procedure/<task_name>/ directory:

1. **UI Files:**
   - widget.ui - Main UI Window, which is editable with QT Creator
   - help.ui - Help Window, which opens when pressing the question mark button.
2. **Python Files:**

   - widget.py - Main Python file to add all functionalities.
   - widget_ui.py - Auto-Generated file from the widget.ui
   - help_ui.py - Auto-Generated file from the help.ui

3. **Optional HTML Support:**
   - index.html adds an empty file into the assets folder.
   - style.css adds an empty file into the assets folder.
   - script.js adds an empty file into the assets folder.

#### YAML Configuration Update

The script updates the configs/settings.yaml file by appending the new task entry to the procedure_tasks section. The entry includes the task name, header, module, and type. Changing the order in the yaml file, changes the order of the procedure task order.

Example YAML Update:

```bash
procedure_tasks:
  - name: <task_name>
    header: <task_header>
    module: <task_module>
    type: <task_type>
```

### How is the added task work?

All tasks are provided to slumber/gui/pages/procedure/procedure.py, which adds during initialization all tasks into a stacked widget in PySide6.
Additionally this module has a list view of all tasks, as well as functionalities to go to previous/next task page, as well as receiving a signal of each task, if it is finished.

Each created widget.py, already has the functionality to build the UI, as well as additional functionalities which the contributor needs to add

```bash
class WidgetPage(QWidget, Ui_Widget):
   is_done_signal = Signal(int)
   ...

   def start(self):
      # This method is being called when the page (stacked widget) is being opened.

   def emit_done_signal(self):
      if self.status == 1:
         self.is_done_signal.emit(self.index)
         self.status = 2
```

- is_done_signal: The signal should be emitted with emit_done_signal as soon as the task is over.
- start: This function can be adjusted and is being called whenever the page is opened / selected.

### How to adjust the UI

To adjust the UI files, you can use Qt Designer, which is part of the Qt Creator suite. Follow these steps to edit and update your `.ui` files:

1. **Using Qt Designer from the Command Line:**

   - Navigate to the directory containing the `.ui` file you want to edit:

     ```bash
     cd path/to/your/ui/file
     ```

   - Open the `.ui` file with Qt Designer:

     ```bash
     designer yourfile.ui
     ```

   This command will open the Qt Designer editor, allowing you to adjust the UI with drag-and-drop functionality.

2. **Using Qt Creator:**

   - Download and install Qt Creator from the [official Qt website](https://www.qt.io/download-qt-installer).

   - Open Qt Creator and use the "Open File or Project" option to open the `.ui` file you want to edit.

   - Adjust the UI using the drag-and-drop interface provided by Qt Creator.

3. **Saving and Updating UI Files:**

   - After making your changes in Qt Designer or Qt Creator, save the `.ui` file.

   - Run the following command to update all the `_ui.py` files in the gui directory:

     ```bash
     poetry run generate_ui
     ```

   This command will regenerate the corresponding `_ui.py` files for all the `.ui` files that have been changed, ensuring that your Python code reflects the updated UI.

By following these steps, you can easily adjust the UI of your application using Qt Designer or Qt Creator and keep your Python code up to date with the latest UI changes.

## Configuration

<!--
Detail any configuration options, environment variables, or settings that need to be set up.
-->

## Testing

<!--
Explain how to run tests. Provide instructions for running unit tests, integration tests, or any other tests included.
-->

## Deployment

<!--
If applicable, describe the process for deploying the application to various environments (e.g., staging, production).
-->

## Contributing

<!--
Outline guidelines for how other developers can contribute to the project.
Include a link to a CONTRIBUTING.md if you have one.
-->

## License

<!--
Specify the license under which your project is distributed, e.g., MIT, Apache, GPL.
Include a link to the LICENSE file if you have one.
-->

## Contact

<!--
Provide ways for others to reach out: email, Twitter handle, etc.
-->
