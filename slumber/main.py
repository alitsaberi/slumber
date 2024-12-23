# your_project/main.py

import sys
from PySide6.QtWidgets import QApplication
from your_project.gui import MainWindow  # Importing from the gui package

def main():
    # Initialize the QApplication
    app = QApplication(sys.argv)
    
    # Optional: Set application properties
    app.setApplicationName("Your Project Name")
    app.setOrganizationName("Your Organization")
    app.setOrganizationDomain("yourdomain.com")
    
    # Initialize the main window
    window = MainWindow()
    
    # Show the main window
    window.show()
    
    # Execute the application's main loop
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
