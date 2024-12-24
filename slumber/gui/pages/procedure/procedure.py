# your_project/gui/pages/procedure/procedure.py

from PySide6.QtWidgets import QWidget, QStackedWidget, QPushButton, QVBoxLayout, QHBoxLayout
from .procedure_ui import Ui_Procedure  # Generated from procedure.ui
from .steps import Step1, Step2  # Importing steps

class Procedure(QWidget, Ui_Procedure):
    def __init__(self, parent=None):
        super(Procedure, self).__init__(parent)
        self.setupUi(self)
        self.setup_ui()
        self.data = {}  # Centralized data storage
    
    def setup_ui(self):
        # Initialize layout
        main_layout = QVBoxLayout(self)
        
        # Navigation buttons for steps
        nav_layout = QHBoxLayout()
        self.btn_step1 = QPushButton("Step 1", self)
        self.btn_step2 = QPushButton("Step 2", self)
        # Add additional buttons as needed for more steps
        nav_layout.addWidget(self.btn_step1)
        nav_layout.addWidget(self.btn_step2)
        main_layout.addLayout(nav_layout)
        
        # Initialize stacked widget for steps
        self.steps_stacked_widget = QStackedWidget(self)
        main_layout.addWidget(self.steps_stacked_widget)
        
        # Initialize steps
        self.step1 = Step1()
        self.step2 = Step2()
        
        # Add steps to the stacked widget
        self.steps_stacked_widget.addWidget(self.step1)
        self.steps_stacked_widget.addWidget(self.step2)
        
        # Connect navigation buttons to switch steps
        self.btn_step1.clicked.connect(lambda: self.steps_stacked_widget.setCurrentWidget(self.step1))
        self.btn_step2.clicked.connect(lambda: self.steps_stacked_widget.setCurrentWidget(self.step2))
        
        # Connect step completion signals
        self.step1.step_completed.connect(self.on_step1_completed)
        self.step2.step_completed.connect(self.on_step2_completed)
    
    def on_step1_completed(self, data):
        # Store data from Step1
        self.data.update(data)
        print("Step1 completed with data:", self.data)
        # Navigate to Step2
        self.steps_stacked_widget.setCurrentWidget(self.step2)
    
    def on_step2_completed(self, data):
        # Store data from Step2
        self.data.update(data)
        print("Step2 completed with data:", self.data)
        # Continue as needed
