# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from frontend.ui import icon_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(706, 597)
        self.actionDocumentation = QAction(MainWindow)
        self.actionDocumentation.setObjectName(u"actionDocumentation")
        self.actionAbout = QAction(MainWindow)
        self.actionAbout.setObjectName(u"actionAbout")
        self.actionExit = QAction(MainWindow)
        self.actionExit.setObjectName(u"actionExit")
        self.actionBackward = QAction(MainWindow)
        self.actionBackward.setObjectName(u"actionBackward")
        icon = QIcon()
        icon.addFile(u":/icons/icons/backward.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.actionBackward.setIcon(icon)
        self.actionForward = QAction(MainWindow)
        self.actionForward.setObjectName(u"actionForward")
        icon1 = QIcon()
        icon1.addFile(u":/icons/icons/forward.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.actionForward.setIcon(icon1)
        self.actionExportResults = QAction(MainWindow)
        self.actionExportResults.setObjectName(u"actionExportResults")
        self.actionCrackSeg = QAction(MainWindow)
        self.actionCrackSeg.setObjectName(u"actionCrackSeg")
        self.actionDeepCrack = QAction(MainWindow)
        self.actionDeepCrack.setObjectName(u"actionDeepCrack")
        self.actionEnglish = QAction(MainWindow)
        self.actionEnglish.setObjectName(u"actionEnglish")
        self.actionGerman = QAction(MainWindow)
        self.actionGerman.setObjectName(u"actionGerman")
        self.actionUploadImages = QAction(MainWindow)
        self.actionUploadImages.setObjectName(u"actionUploadImages")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_5 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(-1, 9, -1, -1)
        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(-1, 0, -1, 0)
        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(-1, 0, -1, 0)
        self.uploadProcessButton = QPushButton(self.centralwidget)
        self.uploadProcessButton.setObjectName(u"uploadProcessButton")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.uploadProcessButton.sizePolicy().hasHeightForWidth())
        self.uploadProcessButton.setSizePolicy(sizePolicy)
        self.uploadProcessButton.setStyleSheet(u"QPushButton {\n"
"    border: none; \n"
"    background: transparent;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: lightgray;\n"
"}\n"
"QPushButton:pressed {\n"
"    background-color: lightblue;\n"
"}\n"
"")
        icon2 = QIcon()
        icon2.addFile(u":/icons/icons/imageupload.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.uploadProcessButton.setIcon(icon2)
        self.uploadProcessButton.setIconSize(QSize(50, 50))

        self.horizontalLayout_5.addWidget(self.uploadProcessButton)

        self.line1 = QFrame(self.centralwidget)
        self.line1.setObjectName(u"line1")
        self.line1.setFrameShape(QFrame.HLine)
        self.line1.setFrameShadow(QFrame.Raised)
        self.line1.setLineWidth(3)

        self.horizontalLayout_5.addWidget(self.line1)

        self.detectProcessButton = QPushButton(self.centralwidget)
        self.detectProcessButton.setObjectName(u"detectProcessButton")
        sizePolicy.setHeightForWidth(self.detectProcessButton.sizePolicy().hasHeightForWidth())
        self.detectProcessButton.setSizePolicy(sizePolicy)
        self.detectProcessButton.setStyleSheet(u"QPushButton {\n"
"    border: none; \n"
"    background: transparent;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: lightgray;\n"
"}\n"
"QPushButton:pressed {\n"
"    background-color: lightblue;\n"
"}\n"
"")
        icon3 = QIcon()
        icon3.addFile(u":/icons/icons/imagestar.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.detectProcessButton.setIcon(icon3)
        self.detectProcessButton.setIconSize(QSize(50, 50))

        self.horizontalLayout_5.addWidget(self.detectProcessButton)

        self.line2 = QFrame(self.centralwidget)
        self.line2.setObjectName(u"line2")
        self.line2.setFrameShape(QFrame.HLine)
        self.line2.setFrameShadow(QFrame.Raised)
        self.line2.setLineWidth(3)

        self.horizontalLayout_5.addWidget(self.line2)

        self.editProcessButton = QPushButton(self.centralwidget)
        self.editProcessButton.setObjectName(u"editProcessButton")
        sizePolicy.setHeightForWidth(self.editProcessButton.sizePolicy().hasHeightForWidth())
        self.editProcessButton.setSizePolicy(sizePolicy)
        self.editProcessButton.setStyleSheet(u"QPushButton {\n"
"    border: none; \n"
"    background: transparent;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: lightgray;\n"
"}\n"
"QPushButton:pressed {\n"
"    background-color: lightblue;\n"
"}\n"
"")
        icon4 = QIcon()
        icon4.addFile(u":/icons/icons/edit.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.editProcessButton.setIcon(icon4)
        self.editProcessButton.setIconSize(QSize(50, 50))

        self.horizontalLayout_5.addWidget(self.editProcessButton)

        self.line3 = QFrame(self.centralwidget)
        self.line3.setObjectName(u"line3")
        self.line3.setFrameShape(QFrame.HLine)
        self.line3.setFrameShadow(QFrame.Raised)
        self.line3.setLineWidth(3)

        self.horizontalLayout_5.addWidget(self.line3)

        self.selectProcessButton = QPushButton(self.centralwidget)
        self.selectProcessButton.setObjectName(u"selectProcessButton")
        sizePolicy.setHeightForWidth(self.selectProcessButton.sizePolicy().hasHeightForWidth())
        self.selectProcessButton.setSizePolicy(sizePolicy)
        self.selectProcessButton.setStyleSheet(u"QPushButton {\n"
"    border: none; \n"
"    background: transparent;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: lightgray;\n"
"}\n"
"QPushButton:pressed {\n"
"    background-color: lightblue;\n"
"}\n"
"")
        icon5 = QIcon()
        icon5.addFile(u":/icons/icons/cursoredit.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.selectProcessButton.setIcon(icon5)
        self.selectProcessButton.setIconSize(QSize(50, 50))

        self.horizontalLayout_5.addWidget(self.selectProcessButton)

        self.line4 = QFrame(self.centralwidget)
        self.line4.setObjectName(u"line4")
        self.line4.setFrameShape(QFrame.HLine)
        self.line4.setFrameShadow(QFrame.Raised)
        self.line4.setLineWidth(3)

        self.horizontalLayout_5.addWidget(self.line4)

        self.exportProcessButton = QPushButton(self.centralwidget)
        self.exportProcessButton.setObjectName(u"exportProcessButton")
        sizePolicy.setHeightForWidth(self.exportProcessButton.sizePolicy().hasHeightForWidth())
        self.exportProcessButton.setSizePolicy(sizePolicy)
        self.exportProcessButton.setStyleSheet(u"QPushButton {\n"
"    border: none; \n"
"    background: transparent;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: lightgray;\n"
"}\n"
"QPushButton:pressed {\n"
"    background-color: lightblue;\n"
"}\n"
"")
        icon6 = QIcon()
        icon6.addFile(u":/icons/icons/csv.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.exportProcessButton.setIcon(icon6)
        self.exportProcessButton.setIconSize(QSize(50, 50))

        self.horizontalLayout_5.addWidget(self.exportProcessButton)


        self.verticalLayout_4.addLayout(self.horizontalLayout_5)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, -1, -1)
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(-1, -1, -1, 0)
        self.scrollArea = QScrollArea(self.centralwidget)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 456, 172))
        self.verticalLayout_13 = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_13.setObjectName(u"verticalLayout_13")
        self.imageLabel = QLabel(self.scrollAreaWidgetContents)
        self.imageLabel.setObjectName(u"imageLabel")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.imageLabel.sizePolicy().hasHeightForWidth())
        self.imageLabel.setSizePolicy(sizePolicy1)
        self.imageLabel.setMinimumSize(QSize(0, 0))
        self.imageLabel.setMaximumSize(QSize(16777215, 16777215))
        self.imageLabel.setAlignment(Qt.AlignCenter)

        self.verticalLayout_13.addWidget(self.imageLabel)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout_3.addWidget(self.scrollArea)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_8.addItem(self.horizontalSpacer_3)

        self.zoomInButton = QPushButton(self.centralwidget)
        self.zoomInButton.setObjectName(u"zoomInButton")
        self.zoomInButton.setStyleSheet(u"QPushButton {\n"
"    border: none; \n"
"    background: transparent;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: lightgray;\n"
"}\n"
"QPushButton:pressed {\n"
"    background-color: lightblue;\n"
"}\n"
"")
        icon7 = QIcon()
        icon7.addFile(u":/icons/icons/zoomin.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.zoomInButton.setIcon(icon7)
        self.zoomInButton.setIconSize(QSize(50, 50))

        self.horizontalLayout_8.addWidget(self.zoomInButton)

        self.zoomOutButton = QPushButton(self.centralwidget)
        self.zoomOutButton.setObjectName(u"zoomOutButton")
        self.zoomOutButton.setStyleSheet(u"QPushButton {\n"
"    border: none; \n"
"    background: transparent;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: lightgray;\n"
"}\n"
"QPushButton:pressed {\n"
"    background-color: lightblue;\n"
"}\n"
"")
        icon8 = QIcon()
        icon8.addFile(u":/icons/icons/zoomout.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.zoomOutButton.setIcon(icon8)
        self.zoomOutButton.setIconSize(QSize(50, 50))

        self.horizontalLayout_8.addWidget(self.zoomOutButton)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_8.addItem(self.horizontalSpacer_4)


        self.verticalLayout_3.addLayout(self.horizontalLayout_8)


        self.horizontalLayout_2.addLayout(self.verticalLayout_3)

        self.toolLayout = QVBoxLayout()
        self.toolLayout.setObjectName(u"toolLayout")
        self.stackedWidget = QStackedWidget(self.centralwidget)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.page0 = QWidget()
        self.page0.setObjectName(u"page0")
        self.verticalLayout_2 = QVBoxLayout(self.page0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.plusButton = QPushButton(self.page0)
        self.plusButton.setObjectName(u"plusButton")
        sizePolicy.setHeightForWidth(self.plusButton.sizePolicy().hasHeightForWidth())
        self.plusButton.setSizePolicy(sizePolicy)
        self.plusButton.setMinimumSize(QSize(100, 100))
        icon9 = QIcon()
        icon9.addFile(u":/icons/icons/plus.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.plusButton.setIcon(icon9)
        self.plusButton.setIconSize(QSize(50, 50))

        self.verticalLayout.addWidget(self.plusButton)

        self.label_3 = QLabel(self.page0)
        self.label_3.setObjectName(u"label_3")

        self.verticalLayout.addWidget(self.label_3)

        self.nextButton0 = QPushButton(self.page0)
        self.nextButton0.setObjectName(u"nextButton0")

        self.verticalLayout.addWidget(self.nextButton0)


        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.stackedWidget.addWidget(self.page0)
        self.page1 = QWidget()
        self.page1.setObjectName(u"page1")
        self.horizontalLayout_11 = QHBoxLayout(self.page1)
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.verticalLayout_12 = QVBoxLayout()
        self.verticalLayout_12.setObjectName(u"verticalLayout_12")
        self.horizontalLayout_12 = QHBoxLayout()
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.label_9 = QLabel(self.page1)
        self.label_9.setObjectName(u"label_9")

        self.horizontalLayout_12.addWidget(self.label_9)

        self.modelComboBox = QComboBox(self.page1)
        self.modelComboBox.setObjectName(u"modelComboBox")
        sizePolicy2 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.modelComboBox.sizePolicy().hasHeightForWidth())
        self.modelComboBox.setSizePolicy(sizePolicy2)

        self.horizontalLayout_12.addWidget(self.modelComboBox)


        self.verticalLayout_12.addLayout(self.horizontalLayout_12)

        self.label_7 = QLabel(self.page1)
        self.label_7.setObjectName(u"label_7")

        self.verticalLayout_12.addWidget(self.label_7)

        self.runModelButton = QPushButton(self.page1)
        self.runModelButton.setObjectName(u"runModelButton")

        self.verticalLayout_12.addWidget(self.runModelButton)


        self.horizontalLayout_11.addLayout(self.verticalLayout_12)

        self.stackedWidget.addWidget(self.page1)
        self.page2 = QWidget()
        self.page2.setObjectName(u"page2")
        self.verticalLayout_7 = QVBoxLayout(self.page2)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.verticalLayout_6 = QVBoxLayout()
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_6.setContentsMargins(-1, -1, -1, 0)
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.addButton = QPushButton(self.page2)
        self.penButtonGroup = QButtonGroup(MainWindow)
        self.penButtonGroup.setObjectName(u"penButtonGroup")
        self.penButtonGroup.addButton(self.addButton)
        self.addButton.setObjectName(u"addButton")
        icon10 = QIcon()
        icon10.addFile(u":/icons/icons/penadd.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.addButton.setIcon(icon10)
        self.addButton.setIconSize(QSize(23, 23))
        self.addButton.setCheckable(True)

        self.horizontalLayout_4.addWidget(self.addButton)

        self.deleteButton = QPushButton(self.page2)
        self.penButtonGroup.addButton(self.deleteButton)
        self.deleteButton.setObjectName(u"deleteButton")
        icon11 = QIcon()
        icon11.addFile(u":/icons/icons/penminus.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.deleteButton.setIcon(icon11)
        self.deleteButton.setIconSize(QSize(23, 23))
        self.deleteButton.setCheckable(True)

        self.horizontalLayout_4.addWidget(self.deleteButton)


        self.verticalLayout_6.addLayout(self.horizontalLayout_4)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.label = QLabel(self.page2)
        self.label.setObjectName(u"label")

        self.horizontalLayout_6.addWidget(self.label)

        self.penSizeSlider = QSlider(self.page2)
        self.penSizeSlider.setObjectName(u"penSizeSlider")
        self.penSizeSlider.setOrientation(Qt.Horizontal)

        self.horizontalLayout_6.addWidget(self.penSizeSlider)


        self.verticalLayout_6.addLayout(self.horizontalLayout_6)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.label_2 = QLabel(self.page2)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout_7.addWidget(self.label_2)

        self.penShapeComboBox = QComboBox(self.page2)
        self.penShapeComboBox.addItem("")
        self.penShapeComboBox.addItem("")
        self.penShapeComboBox.setObjectName(u"penShapeComboBox")
        sizePolicy2.setHeightForWidth(self.penShapeComboBox.sizePolicy().hasHeightForWidth())
        self.penShapeComboBox.setSizePolicy(sizePolicy2)

        self.horizontalLayout_7.addWidget(self.penShapeComboBox)


        self.verticalLayout_6.addLayout(self.horizontalLayout_7)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(-1, 0, -1, -1)
        self.label_8 = QLabel(self.page2)
        self.label_8.setObjectName(u"label_8")

        self.horizontalLayout_3.addWidget(self.label_8)

        self.labelOriginal = QLabel(self.page2)
        self.labelOriginal.setObjectName(u"labelOriginal")

        self.horizontalLayout_3.addWidget(self.labelOriginal)

        self.opacitySlider = QSlider(self.page2)
        self.opacitySlider.setObjectName(u"opacitySlider")
        self.opacitySlider.setOrientation(Qt.Horizontal)

        self.horizontalLayout_3.addWidget(self.opacitySlider)

        self.labelMask = QLabel(self.page2)
        self.labelMask.setObjectName(u"labelMask")

        self.horizontalLayout_3.addWidget(self.labelMask)


        self.verticalLayout_6.addLayout(self.horizontalLayout_3)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_6.addItem(self.verticalSpacer)

        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.nextButton2 = QPushButton(self.page2)
        self.nextButton2.setObjectName(u"nextButton2")

        self.horizontalLayout_9.addWidget(self.nextButton2)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_9.addItem(self.horizontalSpacer_2)


        self.verticalLayout_6.addLayout(self.horizontalLayout_9)


        self.verticalLayout_7.addLayout(self.verticalLayout_6)

        self.stackedWidget.addWidget(self.page2)
        self.page3 = QWidget()
        self.page3.setObjectName(u"page3")
        self.verticalLayout_9 = QVBoxLayout(self.page3)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.verticalLayout_8 = QVBoxLayout()
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.skeletonButton = QPushButton(self.page3)
        self.skeletonButton.setObjectName(u"skeletonButton")

        self.verticalLayout_8.addWidget(self.skeletonButton)

        self.cleanBranchButton = QPushButton(self.page3)
        self.cleanBranchButton.setObjectName(u"cleanBranchButton")

        self.verticalLayout_8.addWidget(self.cleanBranchButton)

        self.label_4 = QLabel(self.page3)
        self.label_4.setObjectName(u"label_4")

        self.verticalLayout_8.addWidget(self.label_4)

        self.nextButton3 = QPushButton(self.page3)
        self.nextButton3.setObjectName(u"nextButton3")

        self.verticalLayout_8.addWidget(self.nextButton3)


        self.verticalLayout_9.addLayout(self.verticalLayout_8)

        self.stackedWidget.addWidget(self.page3)
        self.page4 = QWidget()
        self.page4.setObjectName(u"page4")
        self.verticalLayout_11 = QVBoxLayout(self.page4)
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.verticalLayout_10 = QVBoxLayout()
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.label_6 = QLabel(self.page4)
        self.label_6.setObjectName(u"label_6")

        self.horizontalLayout_10.addWidget(self.label_6)

        self.lineEdit = QLineEdit(self.page4)
        self.lineEdit.setObjectName(u"lineEdit")

        self.horizontalLayout_10.addWidget(self.lineEdit)

        self.browseButton = QPushButton(self.page4)
        self.browseButton.setObjectName(u"browseButton")

        self.horizontalLayout_10.addWidget(self.browseButton)


        self.verticalLayout_10.addLayout(self.horizontalLayout_10)

        self.label_5 = QLabel(self.page4)
        self.label_5.setObjectName(u"label_5")

        self.verticalLayout_10.addWidget(self.label_5)

        self.nextButton4 = QPushButton(self.page4)
        self.nextButton4.setObjectName(u"nextButton4")

        self.verticalLayout_10.addWidget(self.nextButton4)


        self.verticalLayout_11.addLayout(self.verticalLayout_10)

        self.stackedWidget.addWidget(self.page4)

        self.toolLayout.addWidget(self.stackedWidget)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.toolLayout.addItem(self.horizontalSpacer)


        self.horizontalLayout_2.addLayout(self.toolLayout)

        self.horizontalLayout_2.setStretch(0, 3)
        self.horizontalLayout_2.setStretch(1, 1)

        self.verticalLayout_4.addLayout(self.horizontalLayout_2)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.previousFigButton = QPushButton(self.centralwidget)
        self.previousFigButton.setObjectName(u"previousFigButton")
        self.previousFigButton.setMaximumSize(QSize(16777215, 100))
        icon12 = QIcon()
        icon12.addFile(u":/icons/icons/arrowleft.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.previousFigButton.setIcon(icon12)
        self.previousFigButton.setIconSize(QSize(20, 20))

        self.horizontalLayout.addWidget(self.previousFigButton)

        self.listWidget = QListWidget(self.centralwidget)
        self.listWidget.setObjectName(u"listWidget")
        self.listWidget.setMaximumSize(QSize(16777215, 100))

        self.horizontalLayout.addWidget(self.listWidget)

        self.nextFigButton = QPushButton(self.centralwidget)
        self.nextFigButton.setObjectName(u"nextFigButton")
        self.nextFigButton.setMaximumSize(QSize(16777215, 100))
        icon13 = QIcon()
        icon13.addFile(u":/icons/icons/arrowright.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.nextFigButton.setIcon(icon13)
        self.nextFigButton.setIconSize(QSize(20, 20))

        self.horizontalLayout.addWidget(self.nextFigButton)


        self.verticalLayout_4.addLayout(self.horizontalLayout)


        self.verticalLayout_5.addLayout(self.verticalLayout_4)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menuBar = QMenuBar(MainWindow)
        self.menuBar.setObjectName(u"menuBar")
        self.menuBar.setGeometry(QRect(0, 0, 706, 22))
        self.menuFile = QMenu(self.menuBar)
        self.menuFile.setObjectName(u"menuFile")
        self.menuHelp = QMenu(self.menuBar)
        self.menuHelp.setObjectName(u"menuHelp")
        self.menuSetting = QMenu(self.menuBar)
        self.menuSetting.setObjectName(u"menuSetting")
        self.menuLanguage = QMenu(self.menuSetting)
        self.menuLanguage.setObjectName(u"menuLanguage")
        self.menuModel = QMenu(self.menuSetting)
        self.menuModel.setObjectName(u"menuModel")
        MainWindow.setMenuBar(self.menuBar)

        self.menuBar.addAction(self.menuFile.menuAction())
        self.menuBar.addAction(self.menuSetting.menuAction())
        self.menuBar.addAction(self.menuHelp.menuAction())
        self.menuFile.addAction(self.actionUploadImages)
        self.menuFile.addAction(self.actionExportResults)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExit)
        self.menuHelp.addAction(self.actionDocumentation)
        self.menuHelp.addAction(self.actionAbout)
        self.menuSetting.addAction(self.menuModel.menuAction())
        self.menuSetting.addAction(self.menuLanguage.menuAction())
        self.menuLanguage.addAction(self.actionEnglish)
        self.menuLanguage.addAction(self.actionGerman)
        self.menuModel.addAction(self.actionCrackSeg)
        self.menuModel.addAction(self.actionDeepCrack)

        self.retranslateUi(MainWindow)

        self.stackedWidget.setCurrentIndex(3)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"CrackCalcu", None))
        self.actionDocumentation.setText(QCoreApplication.translate("MainWindow", u"Documentation", None))
        self.actionAbout.setText(QCoreApplication.translate("MainWindow", u"About", None))
        self.actionExit.setText(QCoreApplication.translate("MainWindow", u"Exit", None))
        self.actionBackward.setText(QCoreApplication.translate("MainWindow", u"Backward", None))
        self.actionForward.setText(QCoreApplication.translate("MainWindow", u"Forward", None))
        self.actionExportResults.setText(QCoreApplication.translate("MainWindow", u"Export Results", None))
        self.actionCrackSeg.setText(QCoreApplication.translate("MainWindow", u"Crack Seg", None))
        self.actionDeepCrack.setText(QCoreApplication.translate("MainWindow", u"Deep Crack", None))
        self.actionEnglish.setText(QCoreApplication.translate("MainWindow", u"English", None))
        self.actionGerman.setText(QCoreApplication.translate("MainWindow", u"German", None))
        self.actionUploadImages.setText(QCoreApplication.translate("MainWindow", u"Upload Images", None))
        self.uploadProcessButton.setText("")
        self.detectProcessButton.setText("")
        self.editProcessButton.setText("")
        self.selectProcessButton.setText("")
        self.exportProcessButton.setText("")
        self.imageLabel.setText("")
        self.zoomInButton.setText("")
        self.zoomOutButton.setText("")
        self.plusButton.setText("")
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Click \"+\" to upload figures.", None))
        self.nextButton0.setText(QCoreApplication.translate("MainWindow", u"Next Stage", None))
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"Model", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"Select a Model to do detection.", None))
        self.runModelButton.setText(QCoreApplication.translate("MainWindow", u"Next Stage", None))
        self.addButton.setText(QCoreApplication.translate("MainWindow", u"Add", None))
        self.deleteButton.setText(QCoreApplication.translate("MainWindow", u"Delete", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Size", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Shape", None))
        self.penShapeComboBox.setItemText(0, QCoreApplication.translate("MainWindow", u"Round", None))
        self.penShapeComboBox.setItemText(1, QCoreApplication.translate("MainWindow", u"Square", None))

        self.label_8.setText(QCoreApplication.translate("MainWindow", u"Opacity:", None))
        self.labelOriginal.setText(QCoreApplication.translate("MainWindow", u"Original", None))
        self.labelMask.setText(QCoreApplication.translate("MainWindow", u"Mask", None))
        self.nextButton2.setText(QCoreApplication.translate("MainWindow", u"Next Stage", None))
        self.skeletonButton.setText(QCoreApplication.translate("MainWindow", u"Skeletonization", None))
        self.cleanBranchButton.setText(QCoreApplication.translate("MainWindow", u"Remove small branches", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Select skeleton to analysis.", None))
        self.nextButton3.setText(QCoreApplication.translate("MainWindow", u"Next Stage", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"Export Path", None))
        self.browseButton.setText(QCoreApplication.translate("MainWindow", u"Browse", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"Select path to export", None))
        self.nextButton4.setText(QCoreApplication.translate("MainWindow", u"Next Stage", None))
        self.previousFigButton.setText("")
        self.nextFigButton.setText("")
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.menuHelp.setTitle(QCoreApplication.translate("MainWindow", u"Help", None))
        self.menuSetting.setTitle(QCoreApplication.translate("MainWindow", u"Setting", None))
        self.menuLanguage.setTitle(QCoreApplication.translate("MainWindow", u"Language", None))
        self.menuModel.setTitle(QCoreApplication.translate("MainWindow", u"Model", None))
    # retranslateUi

