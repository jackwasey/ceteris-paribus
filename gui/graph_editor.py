from functools import partial

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QBrush
from PyQt5.QtWidgets import QMainWindow, QGraphicsView, QDockWidget, QToolBar, QAction, QGridLayout, QLabel, QSlider, \
    QMenuBar, QMenu

from gui.graph_scene import GraphScene
from gui.sidepane import ContextPane


class GraphWindow(QMainWindow):
    """This class represents the MainWindow as a whole."""
    def __init__(self, controller):
        super().__init__()
        self.scene = GraphScene(controller)
        self.controller = controller

        # a grid foreground
        self.grid = True

        # Create upper toolbar with menu options
        menubar = self.menuBar()

        file_menu = menubar.addMenu('File')
        db_action = file_menu.addAction('Open file')
        db_action.setStatusTip('Select a file to use as a database')
        db_action.triggered.connect(self.open_new_db)
        file_menu.addAction(db_action)

        edit_menu = menubar.addMenu('Edit')
        undo_action = edit_menu.addAction('Undo')
        undo_action.setStatusTip('Undo previous action')
        #undo_action.triggered.connect
        edit_menu.addAction(undo_action)

        self.statusBar().showMessage("Ready")

        # Create context pane and link it to the controller
        side_pane = QDockWidget()
        self.context = ContextPane(controller)
        side_pane.setWidget(self.context)
        side_pane.setAllowedAreas(Qt.RightDockWidgetArea)

        # Demonstrate the results from the input.

        self.addDockWidget(Qt.RightDockWidgetArea, side_pane)

        graphics = QGraphicsView(self.scene)
        self.setCentralWidget(graphics)
        self.showFullScreen()

    def get_scene(self):
        return self.scene

    def toggleGrid(self):
        if self.grid:
            self.scene.setBackgroundBrush(QBrush(Qt.white))
            self.grid = False
        else:
            self.scene.setBackgroundBrush(QBrush(Qt.lightGray, Qt.CrossPattern))
            self.grid = True

    def keyPressEvent(self, e):
        # Currently, we respond to a press of the Escape key by closing the program.
        if e.key() == Qt.Key_Escape:
            self.close()

    def open_new_db(self):
        self.controller.open_new_db()
        self.setCentralWidget(QGraphicsView(GraphScene(self.controller)))