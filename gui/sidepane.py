""" Contains the definition of the side panel on the right hand side of the UI. This panel displays the relevant
    information for the model."""
from functools import partial

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QGridLayout, QGroupBox, QLabel, QSlider, QSpacerItem, QHBoxLayout, QVBoxLayout, \
    QPushButton, QDialog


class ContextPane(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller

        self.context = QGridLayout()

        # Find the available screen geometry
        available_height = self.height()
        print(available_height)

        self.input_group = QGroupBox("Inputs")
        self.input_group.setFixedSize(300, (available_height / 2))
        self.set_input()

        self.context_group = QGroupBox("Context")
        self.context_group.setFixedSize(300, (available_height / 2))
        self.set_context(list(controller.get_model().organs.values())[0])

        self.output_group = QGroupBox("Outputs")
        self.output_group.setFixedSize(300, (available_height / 2))
        self.set_output()

        layout = QGridLayout()
        self.context_group.setLayout(self.context)
        layout.addWidget(self.input_group)
        layout.addWidget(self.context_group)
        layout.addWidget(self.output_group)

        self.setLayout(layout)

    def set_input(self):
        layout = QGridLayout()
        global_params = self.controller.get_global_params()
        for index, param_name in enumerate(global_params):
            layout.addWidget(QLabel(param_name), index, 0)
            slider = QSlider(Qt.Horizontal)
            slider.setMinimum(global_params[param_name][0])
            slider.setMaximum(global_params[param_name][1])
            slider.setValue(global_params[param_name][2])
            slider.valueChanged.connect(partial(self.controller.param_changed, param_name, slider))
            layout.addWidget(slider, index, 1)
        layout.setRowStretch(2, 500)
        self.input_group.setLayout(layout)

    def set_context(self, organ):
        self.current_organ = organ

        layout = QVBoxLayout()

        name_label = QLabel(organ.get_name())
        layout.addWidget(name_label)

        var_button = QPushButton("Local values")
        var_button.clicked.connect(self.show_locals)
        layout.addWidget(var_button)

        glob_button = QPushButton("Global values")
        glob_button.clicked.connect(self.show_globals)
        layout.addWidget(glob_button)

        func_button = QPushButton("Functions")
        func_button.clicked.connect(self.show_funcs)
        layout.addWidget(func_button)

        out_button = QPushButton("Outputs")
        out_button.clicked.connect(self.show_outs)
        layout.addWidget(out_button)

        del_button = QPushButton("Delete")
        del_button.clicked.connect(self.delete_organ)
        layout.addWidget(del_button)

        self.context_group.setLayout(layout)

    def show_locals(self):
        dialog = QDialog()
        dialog.setWindowTitle("Local values")
        layout = QGridLayout()

        for index, val in enumerate(self.current_organ.get_locals()):
            # TODO make into sliders with values
            assert '__builtins__' not in self.current_organ.get_locals()
            if val != '__builtins__':
                print("val is " + str(val))
                layout.addWidget(QLabel(val), index, 0)
                layout.addWidget(QLabel(str(self.current_organ.get_locals()[val])), index, 1)
        dialog.setLayout(layout)
        dialog.exec_()

    def show_globals(self):
        dialog = QDialog()
        dialog.setWindowTitle("Globals")
        layout = QGridLayout()
        for index, val in enumerate(self.current_organ.get_globals()):
            layout.addWidget(QLabel(val), index, 0)
            layout.addWidget(QLabel(str(self.current_organ.get_globals()[val])), index, 1)
        dialog.setLayout(layout)
        dialog.exec_()

    def show_funcs(self):
        dialog = QDialog()
        layout = QGridLayout()
        dialog.setWindowTitle("Functions")
        for index, func in enumerate(self.current_organ.get_funcs()):
            layout.addWidget(QLabel(func + ":"), index, 0)
            layout.addWidget(QLabel(str(self.current_organ.get_funcs()[func])), index, 1)
        dialog.setLayout(layout)
        dialog.exec_()

    def show_outs(self):
        dialog = QDialog()
        layout = QGridLayout()
        dialog.setWindowTitle("Outputs")
        for index, func in enumerate(self.current_organ.get_funcs()):
            layout.addWidget(QLabel(func + ":"), index, 0)
            layout.addWidget(QLabel(str(self.current_organ.defined_variables[func])), index, 1)
        dialog.setLayout(layout)
        dialog.exec_()


    def delete_organ(self):
        dialog = QDialog()
        dialog.setWindowTitle("Delete " + self.current_organ.get_name() + "?")

        msg = QLabel("Are you sure you want to delete this organ?")
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        y_button = QPushButton("Yes")
        y_button.clicked.connect(dialog.accept)
        button_layout.addWidget(y_button)
        n_button = QPushButton("No")
        n_button.clicked.connect(dialog.reject)
        button_layout.addWidget(n_button)

        layout = QGridLayout()
        layout.addWidget(msg, 0, 0)
        layout.addLayout(button_layout, 1, 0)

        dialog.setLayout(layout)
        if dialog.exec_():
            self.controller.remove_organ(self.current_organ)

    def set_output(self):
        outputs = self.controller.model.get_outputs()
        layout = QGridLayout()
        for index, out_name in enumerate(outputs):
            labels = QHBoxLayout()
            labels.addWidget(QLabel(out_name))
            labels.addWidget(QLabel(str(outputs[out_name])))
            layout.addLayout(labels, index, 0)
        self.output_group.setLayout(layout)
