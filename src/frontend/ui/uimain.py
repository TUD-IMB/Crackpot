# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main.ui'
##
## Created by: Qt User Interface Compiler version 6.11.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QButtonGroup, QComboBox, QFormLayout,
    QFrame, QGroupBox, QHBoxLayout, QLabel,
    QLineEdit, QListView, QListWidget, QListWidgetItem,
    QMainWindow, QMenu, QMenuBar, QPushButton,
    QScrollArea, QSizePolicy, QSlider, QSpacerItem,
    QSpinBox, QStackedWidget, QStatusBar, QVBoxLayout,
    QWidget)
from frontend.ui import icon_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(706, 656)
        self.actionDocumentation = QAction(MainWindow)
        self.actionDocumentation.setObjectName(u"actionDocumentation")
        self.actionAbout = QAction(MainWindow)
        self.actionAbout.setObjectName(u"actionAbout")
        self.actionExit = QAction(MainWindow)
        self.actionExit.setObjectName(u"actionExit")
        self.actionImportProject = QAction(MainWindow)
        self.actionImportProject.setObjectName(u"actionImportProject")
        self.actionExportProject = QAction(MainWindow)
        self.actionExportProject.setObjectName(u"actionExportProject")
        self.actionEnglish = QAction(MainWindow)
        self.actionEnglish.setObjectName(u"actionEnglish")
        self.actionGerman = QAction(MainWindow)
        self.actionGerman.setObjectName(u"actionGerman")
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
        self.calibrationProcessButton = QPushButton(self.centralwidget)
        self.calibrationProcessButton.setObjectName(u"calibrationProcessButton")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.calibrationProcessButton.sizePolicy().hasHeightForWidth())
        self.calibrationProcessButton.setSizePolicy(sizePolicy)
        self.calibrationProcessButton.setStyleSheet(u"QPushButton {\n"
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
        icon = QIcon()
        icon.addFile(u":/icons/icons/ruler.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.calibrationProcessButton.setIcon(icon)
        self.calibrationProcessButton.setIconSize(QSize(30, 30))

        self.horizontalLayout_5.addWidget(self.calibrationProcessButton)

        self.line0 = QFrame(self.centralwidget)
        self.line0.setObjectName(u"line0")
        self.line0.setFrameShape(QFrame.Shape.HLine)
        self.line0.setFrameShadow(QFrame.Shadow.Raised)
        self.line0.setLineWidth(3)

        self.horizontalLayout_5.addWidget(self.line0)

        self.uploadProcessButton = QPushButton(self.centralwidget)
        self.uploadProcessButton.setObjectName(u"uploadProcessButton")
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
        icon1 = QIcon()
        icon1.addFile(u":/icons/icons/imageupload.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.uploadProcessButton.setIcon(icon1)
        self.uploadProcessButton.setIconSize(QSize(30, 30))

        self.horizontalLayout_5.addWidget(self.uploadProcessButton)

        self.line1 = QFrame(self.centralwidget)
        self.line1.setObjectName(u"line1")
        self.line1.setFrameShape(QFrame.Shape.HLine)
        self.line1.setFrameShadow(QFrame.Shadow.Raised)
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
        icon2 = QIcon()
        icon2.addFile(u":/icons/icons/edit.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.detectProcessButton.setIcon(icon2)
        self.detectProcessButton.setIconSize(QSize(30, 30))

        self.horizontalLayout_5.addWidget(self.detectProcessButton)

        self.line2 = QFrame(self.centralwidget)
        self.line2.setObjectName(u"line2")
        self.line2.setFrameShape(QFrame.Shape.HLine)
        self.line2.setFrameShadow(QFrame.Shadow.Raised)
        self.line2.setLineWidth(3)

        self.horizontalLayout_5.addWidget(self.line2)

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
        icon3 = QIcon()
        icon3.addFile(u":/icons/icons/cursoredit.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.selectProcessButton.setIcon(icon3)
        self.selectProcessButton.setIconSize(QSize(30, 30))

        self.horizontalLayout_5.addWidget(self.selectProcessButton)

        self.line4 = QFrame(self.centralwidget)
        self.line4.setObjectName(u"line4")
        self.line4.setFrameShape(QFrame.Shape.HLine)
        self.line4.setFrameShadow(QFrame.Shadow.Raised)
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
        icon4 = QIcon()
        icon4.addFile(u":/icons/icons/csv.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.exportProcessButton.setIcon(icon4)
        self.exportProcessButton.setIconSize(QSize(30, 30))

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
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 363, 372))
        self.verticalLayout_13 = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_13.setObjectName(u"verticalLayout_13")
        self.imageLabel = QLabel(self.scrollAreaWidgetContents)
        self.imageLabel.setObjectName(u"imageLabel")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.imageLabel.sizePolicy().hasHeightForWidth())
        self.imageLabel.setSizePolicy(sizePolicy1)
        self.imageLabel.setMinimumSize(QSize(0, 0))
        self.imageLabel.setMaximumSize(QSize(16777215, 16777215))
        self.imageLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_13.addWidget(self.imageLabel)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout_3.addWidget(self.scrollArea)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

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
        icon5 = QIcon()
        icon5.addFile(u":/icons/icons/zoomin.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.zoomInButton.setIcon(icon5)
        self.zoomInButton.setIconSize(QSize(30, 30))

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
        icon6 = QIcon()
        icon6.addFile(u":/icons/icons/zoomout.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.zoomOutButton.setIcon(icon6)
        self.zoomOutButton.setIconSize(QSize(30, 30))

        self.horizontalLayout_8.addWidget(self.zoomOutButton)

        self.zoomFitButton = QPushButton(self.centralwidget)
        self.zoomFitButton.setObjectName(u"zoomFitButton")
        self.zoomFitButton.setStyleSheet(u"QPushButton {\n"
"    border: none;\n"
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
        icon7.addFile(u":/icons/icons/zoomfit.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.zoomFitButton.setIcon(icon7)
        self.zoomFitButton.setIconSize(QSize(30, 30))

        self.horizontalLayout_8.addWidget(self.zoomFitButton)

        self.zoomOneToOneButton = QPushButton(self.centralwidget)
        self.zoomOneToOneButton.setObjectName(u"zoomOneToOneButton")
        self.zoomOneToOneButton.setStyleSheet(u"QPushButton {\n"
"    border: none;\n"
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
        icon8.addFile(u":/icons/icons/zoom1to1.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.zoomOneToOneButton.setIcon(icon8)
        self.zoomOneToOneButton.setIconSize(QSize(30, 30))

        self.horizontalLayout_8.addWidget(self.zoomOneToOneButton)

        self.deleteImageButton = QPushButton(self.centralwidget)
        self.deleteImageButton.setObjectName(u"deleteImageButton")
        self.deleteImageButton.setStyleSheet(u"QPushButton {\n"
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
        icon9 = QIcon()
        icon9.addFile(u":/icons/icons/delete.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.deleteImageButton.setIcon(icon9)
        self.deleteImageButton.setIconSize(QSize(30, 30))

        self.horizontalLayout_8.addWidget(self.deleteImageButton)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_8.addItem(self.horizontalSpacer_4)


        self.verticalLayout_3.addLayout(self.horizontalLayout_8)


        self.horizontalLayout_2.addLayout(self.verticalLayout_3)

        self.toolLayout = QVBoxLayout()
        self.toolLayout.setObjectName(u"toolLayout")
        self.stackedWidget = QStackedWidget(self.centralwidget)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.page0 = QWidget()
        self.page0.setObjectName(u"page0")
        self.verticalLayout_24 = QVBoxLayout(self.page0)
        self.verticalLayout_24.setObjectName(u"verticalLayout_24")
        self.verticalLayout_20 = QVBoxLayout()
        self.verticalLayout_20.setObjectName(u"verticalLayout_20")
        self.verticalLayout_21 = QVBoxLayout()
        self.verticalLayout_21.setObjectName(u"verticalLayout_21")
        self.horizontalLayout_21 = QHBoxLayout()
        self.horizontalLayout_21.setObjectName(u"horizontalLayout_21")
        self.horizontalLayout_21.setContentsMargins(-1, -1, 0, 0)

        self.verticalLayout_21.addLayout(self.horizontalLayout_21)

        self.groupBox_6 = QGroupBox(self.page0)
        self.groupBox_6.setObjectName(u"groupBox_6")
        self.groupBox_6.setMinimumSize(QSize(0, 200))
        self.groupBox_6.setStyleSheet(u"QGroupBox{\n"
"    font-weight: bold;\n"
"}\n"
"")
        self.verticalLayout_22 = QVBoxLayout(self.groupBox_6)
        self.verticalLayout_22.setObjectName(u"verticalLayout_22")
        self.horizontalLayout_22 = QHBoxLayout()
        self.horizontalLayout_22.setObjectName(u"horizontalLayout_22")
        self.horizontalLayout_22.setContentsMargins(-1, -1, -1, 0)
        self.label_14 = QLabel(self.groupBox_6)
        self.label_14.setObjectName(u"label_14")

        self.horizontalLayout_22.addWidget(self.label_14)

        self.caliUploadButton = QPushButton(self.groupBox_6)
        self.caliUploadButton.setObjectName(u"caliUploadButton")

        self.horizontalLayout_22.addWidget(self.caliUploadButton)

        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_22.addItem(self.horizontalSpacer_7)


        self.verticalLayout_22.addLayout(self.horizontalLayout_22)

        self.horizontalLayout_13 = QHBoxLayout()
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.horizontalLayout_13.setContentsMargins(-1, -1, -1, 0)
        self.label_10 = QLabel(self.groupBox_6)
        self.label_10.setObjectName(u"label_10")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.label_10.sizePolicy().hasHeightForWidth())
        self.label_10.setSizePolicy(sizePolicy2)

        self.horizontalLayout_13.addWidget(self.label_10)

        self.clickAddButton = QPushButton(self.groupBox_6)
        self.caliButtonGroup = QButtonGroup(MainWindow)
        self.caliButtonGroup.setObjectName(u"caliButtonGroup")
        self.caliButtonGroup.addButton(self.clickAddButton)
        self.clickAddButton.setObjectName(u"clickAddButton")
        sizePolicy.setHeightForWidth(self.clickAddButton.sizePolicy().hasHeightForWidth())
        self.clickAddButton.setSizePolicy(sizePolicy)
        icon10 = QIcon()
        icon10.addFile(u":/icons/icons/caliadd.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.clickAddButton.setIcon(icon10)
        self.clickAddButton.setIconSize(QSize(25, 25))
        self.clickAddButton.setCheckable(True)

        self.horizontalLayout_13.addWidget(self.clickAddButton)

        self.clickDeleteButton = QPushButton(self.groupBox_6)
        self.caliButtonGroup.addButton(self.clickDeleteButton)
        self.clickDeleteButton.setObjectName(u"clickDeleteButton")
        sizePolicy.setHeightForWidth(self.clickDeleteButton.sizePolicy().hasHeightForWidth())
        self.clickDeleteButton.setSizePolicy(sizePolicy)
        icon11 = QIcon()
        icon11.addFile(u":/icons/icons/calidelete.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.clickDeleteButton.setIcon(icon11)
        self.clickDeleteButton.setIconSize(QSize(25, 25))
        self.clickDeleteButton.setCheckable(True)

        self.horizontalLayout_13.addWidget(self.clickDeleteButton)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_13.addItem(self.horizontalSpacer_5)


        self.verticalLayout_22.addLayout(self.horizontalLayout_13)

        self.line = QFrame(self.groupBox_6)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout_22.addWidget(self.line)

        self.formLayout_2 = QFormLayout()
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.formLayout_2.setContentsMargins(-1, -1, -1, 0)
        self.distanceLabel = QLabel(self.groupBox_6)
        self.distanceLabel.setObjectName(u"distanceLabel")

        self.formLayout_2.setWidget(1, QFormLayout.ItemRole.LabelRole, self.distanceLabel)

        self.distanceLineEdit = QLineEdit(self.groupBox_6)
        self.distanceLineEdit.setObjectName(u"distanceLineEdit")

        self.formLayout_2.setWidget(1, QFormLayout.ItemRole.FieldRole, self.distanceLineEdit)

        self.pixelLabel = QLabel(self.groupBox_6)
        self.pixelLabel.setObjectName(u"pixelLabel")

        self.formLayout_2.setWidget(2, QFormLayout.ItemRole.LabelRole, self.pixelLabel)

        self.pixelLineEdit = QLineEdit(self.groupBox_6)
        self.pixelLineEdit.setObjectName(u"pixelLineEdit")

        self.formLayout_2.setWidget(2, QFormLayout.ItemRole.FieldRole, self.pixelLineEdit)

        self.resolutionLabel = QLabel(self.groupBox_6)
        self.resolutionLabel.setObjectName(u"resolutionLabel")

        self.formLayout_2.setWidget(3, QFormLayout.ItemRole.LabelRole, self.resolutionLabel)

        self.resolutionLineEdit = QLineEdit(self.groupBox_6)
        self.resolutionLineEdit.setObjectName(u"resolutionLineEdit")

        self.formLayout_2.setWidget(3, QFormLayout.ItemRole.FieldRole, self.resolutionLineEdit)


        self.verticalLayout_22.addLayout(self.formLayout_2)

        self.horizontalLayout_23 = QHBoxLayout()
        self.horizontalLayout_23.setObjectName(u"horizontalLayout_23")
        self.horizontalLayout_23.setContentsMargins(-1, -1, -1, 0)
        self.horizontalSpacer_9 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_23.addItem(self.horizontalSpacer_9)

        self.confirmButton = QPushButton(self.groupBox_6)
        self.confirmButton.setObjectName(u"confirmButton")

        self.horizontalLayout_23.addWidget(self.confirmButton)


        self.verticalLayout_22.addLayout(self.horizontalLayout_23)


        self.verticalLayout_21.addWidget(self.groupBox_6)


        self.verticalLayout_20.addLayout(self.verticalLayout_21)

        self.verticalSpacer_6 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_20.addItem(self.verticalSpacer_6)

        self.horizontalLayout_25 = QHBoxLayout()
        self.horizontalLayout_25.setObjectName(u"horizontalLayout_25")
        self.horizontalLayout_25.setContentsMargins(-1, -1, -1, 0)
        self.nextButton0 = QPushButton(self.page0)
        self.nextButton0.setObjectName(u"nextButton0")

        self.horizontalLayout_25.addWidget(self.nextButton0)


        self.verticalLayout_20.addLayout(self.horizontalLayout_25)


        self.verticalLayout_24.addLayout(self.verticalLayout_20)

        self.stackedWidget.addWidget(self.page0)
        self.page1 = QWidget()
        self.page1.setObjectName(u"page1")
        self.verticalLayout_2 = QVBoxLayout(self.page1)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.groupBox_3 = QGroupBox(self.page1)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.groupBox_3.setMinimumSize(QSize(0, 100))
        self.groupBox_3.setStyleSheet(u"QGroupBox{\n"
"    font-weight: bold;\n"
"}\n"
"")
        self.verticalLayout_17 = QVBoxLayout(self.groupBox_3)
        self.verticalLayout_17.setObjectName(u"verticalLayout_17")
        self.horizontalLayout_19 = QHBoxLayout()
        self.horizontalLayout_19.setObjectName(u"horizontalLayout_19")
        self.horizontalLayout_19.setContentsMargins(-1, -1, -1, 0)
        self.label_13 = QLabel(self.groupBox_3)
        self.label_13.setObjectName(u"label_13")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.label_13.sizePolicy().hasHeightForWidth())
        self.label_13.setSizePolicy(sizePolicy3)

        self.horizontalLayout_19.addWidget(self.label_13)

        self.plusButton = QPushButton(self.groupBox_3)
        self.plusButton.setObjectName(u"plusButton")
        sizePolicy.setHeightForWidth(self.plusButton.sizePolicy().hasHeightForWidth())
        self.plusButton.setSizePolicy(sizePolicy)
        self.plusButton.setMinimumSize(QSize(80, 80))
        icon12 = QIcon()
        icon12.addFile(u":/icons/icons/plus.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.plusButton.setIcon(icon12)
        self.plusButton.setIconSize(QSize(50, 50))

        self.horizontalLayout_19.addWidget(self.plusButton)

        self.label_3 = QLabel(self.groupBox_3)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout_19.addWidget(self.label_3)


        self.verticalLayout_17.addLayout(self.horizontalLayout_19)


        self.verticalLayout.addWidget(self.groupBox_3)

        self.verticalSpacer_4 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer_4)

        self.horizontalLayout_17 = QHBoxLayout()
        self.horizontalLayout_17.setObjectName(u"horizontalLayout_17")
        self.horizontalLayout_17.setContentsMargins(-1, -1, -1, 0)
        self.previousButton1 = QPushButton(self.page1)
        self.previousButton1.setObjectName(u"previousButton1")

        self.horizontalLayout_17.addWidget(self.previousButton1)

        self.nextButton1 = QPushButton(self.page1)
        self.nextButton1.setObjectName(u"nextButton1")

        self.horizontalLayout_17.addWidget(self.nextButton1)


        self.verticalLayout.addLayout(self.horizontalLayout_17)


        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.stackedWidget.addWidget(self.page1)
        self.page3 = QWidget()
        self.page3.setObjectName(u"page3")
        self.verticalLayout_7 = QVBoxLayout(self.page3)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.verticalLayout_6 = QVBoxLayout()
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_6.setContentsMargins(-1, -1, -1, 0)
        self.maskingGroupBox = QGroupBox(self.page3)
        self.maskingGroupBox.setObjectName(u"maskingGroupBox")
        self.maskingGroupBox.setStyleSheet(u"QGroupBox{\n"
"    font-weight: bold;\n"
"}\n"
"")
        self.verticalLayout_171 = QVBoxLayout(self.maskingGroupBox)
        self.verticalLayout_171.setObjectName(u"verticalLayout_171")
        self.label_7 = QLabel(self.maskingGroupBox)
        self.label_7.setObjectName(u"label_7")

        self.verticalLayout_171.addWidget(self.label_7)

        self.horizontalLayout_12 = QHBoxLayout()
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.label_9 = QLabel(self.maskingGroupBox)
        self.label_9.setObjectName(u"label_9")

        self.horizontalLayout_12.addWidget(self.label_9)

        self.modelComboBox = QComboBox(self.maskingGroupBox)
        self.modelComboBox.addItem("")
        self.modelComboBox.addItem("")
        self.modelComboBox.setObjectName(u"modelComboBox")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.modelComboBox.sizePolicy().hasHeightForWidth())
        self.modelComboBox.setSizePolicy(sizePolicy4)

        self.horizontalLayout_12.addWidget(self.modelComboBox)


        self.verticalLayout_171.addLayout(self.horizontalLayout_12)

        self.applyModelLabel = QLabel(self.maskingGroupBox)
        self.applyModelLabel.setObjectName(u"applyModelLabel")

        self.verticalLayout_171.addWidget(self.applyModelLabel)

        self.applyModelButtonLayout = QHBoxLayout()
        self.applyModelButtonLayout.setObjectName(u"applyModelButtonLayout")
        self.applyModelButton = QPushButton(self.maskingGroupBox)
        self.applyModelButton.setObjectName(u"applyModelButton")

        self.applyModelButtonLayout.addWidget(self.applyModelButton)

        self.applyModelAllButton = QPushButton(self.maskingGroupBox)
        self.applyModelAllButton.setObjectName(u"applyModelAllButton")

        self.applyModelButtonLayout.addWidget(self.applyModelAllButton)


        self.verticalLayout_171.addLayout(self.applyModelButtonLayout)

        self.clearMaskLabel = QLabel(self.maskingGroupBox)
        self.clearMaskLabel.setObjectName(u"clearMaskLabel")

        self.verticalLayout_171.addWidget(self.clearMaskLabel)

        self.clearMaskButtonLayout = QHBoxLayout()
        self.clearMaskButtonLayout.setObjectName(u"clearMaskButtonLayout")
        self.clearMaskButton = QPushButton(self.maskingGroupBox)
        self.clearMaskButton.setObjectName(u"clearMaskButton")

        self.clearMaskButtonLayout.addWidget(self.clearMaskButton)

        self.clearMaskAllButton = QPushButton(self.maskingGroupBox)
        self.clearMaskAllButton.setObjectName(u"clearMaskAllButton")

        self.clearMaskButtonLayout.addWidget(self.clearMaskAllButton)


        self.verticalLayout_171.addLayout(self.clearMaskButtonLayout)


        self.verticalLayout_6.addWidget(self.maskingGroupBox)

        self.groupBox = QGroupBox(self.page3)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setMinimumSize(QSize(0, 150))
        self.groupBox.setStyleSheet(u"QGroupBox{\n"
"    font-weight: bold;\n"
"}\n"
"")
        self.verticalLayout_15 = QVBoxLayout(self.groupBox)
        self.verticalLayout_15.setObjectName(u"verticalLayout_15")
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.addButton = QPushButton(self.groupBox)
        self.penButtonGroup = QButtonGroup(MainWindow)
        self.penButtonGroup.setObjectName(u"penButtonGroup")
        self.penButtonGroup.addButton(self.addButton)
        self.addButton.setObjectName(u"addButton")
        icon13 = QIcon()
        icon13.addFile(u":/icons/icons/penadd.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.addButton.setIcon(icon13)
        self.addButton.setIconSize(QSize(23, 23))
        self.addButton.setCheckable(True)
        self.addButton.setChecked(True)

        self.horizontalLayout_4.addWidget(self.addButton)

        self.deleteButton = QPushButton(self.groupBox)
        self.penButtonGroup.addButton(self.deleteButton)
        self.deleteButton.setObjectName(u"deleteButton")
        icon14 = QIcon()
        icon14.addFile(u":/icons/icons/penminus.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.deleteButton.setIcon(icon14)
        self.deleteButton.setIconSize(QSize(23, 23))
        self.deleteButton.setCheckable(True)

        self.horizontalLayout_4.addWidget(self.deleteButton)


        self.verticalLayout_15.addLayout(self.horizontalLayout_4)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.label = QLabel(self.groupBox)
        self.label.setObjectName(u"label")

        self.horizontalLayout_6.addWidget(self.label)

        self.penSizeSlider = QSlider(self.groupBox)
        self.penSizeSlider.setObjectName(u"penSizeSlider")
        self.penSizeSlider.setOrientation(Qt.Orientation.Horizontal)

        self.horizontalLayout_6.addWidget(self.penSizeSlider)


        self.verticalLayout_15.addLayout(self.horizontalLayout_6)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.label_2 = QLabel(self.groupBox)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout_7.addWidget(self.label_2)

        self.penShapeComboBox = QComboBox(self.groupBox)
        self.penShapeComboBox.addItem("")
        self.penShapeComboBox.addItem("")
        self.penShapeComboBox.setObjectName(u"penShapeComboBox")
        sizePolicy4.setHeightForWidth(self.penShapeComboBox.sizePolicy().hasHeightForWidth())
        self.penShapeComboBox.setSizePolicy(sizePolicy4)

        self.horizontalLayout_7.addWidget(self.penShapeComboBox)


        self.verticalLayout_15.addLayout(self.horizontalLayout_7)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(-1, 0, -1, -1)
        self.label_8 = QLabel(self.groupBox)
        self.label_8.setObjectName(u"label_8")

        self.horizontalLayout_3.addWidget(self.label_8)

        self.labelOriginal = QLabel(self.groupBox)
        self.labelOriginal.setObjectName(u"labelOriginal")

        self.horizontalLayout_3.addWidget(self.labelOriginal)

        self.opacitySlider = QSlider(self.groupBox)
        self.opacitySlider.setObjectName(u"opacitySlider")
        self.opacitySlider.setOrientation(Qt.Orientation.Horizontal)

        self.horizontalLayout_3.addWidget(self.opacitySlider)

        self.labelMask = QLabel(self.groupBox)
        self.labelMask.setObjectName(u"labelMask")

        self.horizontalLayout_3.addWidget(self.labelMask)


        self.verticalLayout_15.addLayout(self.horizontalLayout_3)

        self.removePatchesLabel = QLabel(self.groupBox)
        self.removePatchesLabel.setObjectName(u"removePatchesLabel")
        self.removePatchesLabel.setWordWrap(True)

        self.verticalLayout_15.addWidget(self.removePatchesLabel)

        self.patchAreaSpinBox = QSpinBox(self.groupBox)
        self.patchAreaSpinBox.setObjectName(u"patchAreaSpinBox")
        self.patchAreaSpinBox.setMinimum(1)
        self.patchAreaSpinBox.setMaximum(999999)
        self.patchAreaSpinBox.setValue(50)

        self.verticalLayout_15.addWidget(self.patchAreaSpinBox)

        self.removePatchesButtonLayout = QHBoxLayout()
        self.removePatchesButtonLayout.setObjectName(u"removePatchesButtonLayout")
        self.removePatchesButton = QPushButton(self.groupBox)
        self.removePatchesButton.setObjectName(u"removePatchesButton")

        self.removePatchesButtonLayout.addWidget(self.removePatchesButton)

        self.removePatchesAllButton = QPushButton(self.groupBox)
        self.removePatchesAllButton.setObjectName(u"removePatchesAllButton")

        self.removePatchesButtonLayout.addWidget(self.removePatchesAllButton)


        self.verticalLayout_15.addLayout(self.removePatchesButtonLayout)


        self.verticalLayout_6.addWidget(self.groupBox)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_6.addItem(self.verticalSpacer)

        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.previousButton3 = QPushButton(self.page3)
        self.previousButton3.setObjectName(u"previousButton3")

        self.horizontalLayout_9.addWidget(self.previousButton3)

        self.nextButton3 = QPushButton(self.page3)
        self.nextButton3.setObjectName(u"nextButton3")

        self.horizontalLayout_9.addWidget(self.nextButton3)


        self.verticalLayout_6.addLayout(self.horizontalLayout_9)


        self.verticalLayout_7.addLayout(self.verticalLayout_6)

        self.stackedWidget.addWidget(self.page3)
        self.page4 = QWidget()
        self.page4.setObjectName(u"page4")
        self.verticalLayout_9 = QVBoxLayout(self.page4)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.verticalLayout_8 = QVBoxLayout()
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.groupBox_2 = QGroupBox(self.page4)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.groupBox_2.setStyleSheet(u"QGroupBox{\n"
"    font-weight: bold;\n"
"}\n"
"")
        self.verticalLayout_16 = QVBoxLayout(self.groupBox_2)
        self.verticalLayout_16.setObjectName(u"verticalLayout_16")
        self.label_16 = QLabel(self.groupBox_2)
        self.label_16.setObjectName(u"label_16")

        self.verticalLayout_16.addWidget(self.label_16)

        self.skeletonizeLabel = QLabel(self.groupBox_2)
        self.skeletonizeLabel.setObjectName(u"skeletonizeLabel")

        self.verticalLayout_16.addWidget(self.skeletonizeLabel)

        self.skeletonizeButtonLayout = QHBoxLayout()
        self.skeletonizeButtonLayout.setObjectName(u"skeletonizeButtonLayout")
        self.skeletonButton = QPushButton(self.groupBox_2)
        self.skeletonButton.setObjectName(u"skeletonButton")

        self.skeletonizeButtonLayout.addWidget(self.skeletonButton)

        self.skeletonAllButton = QPushButton(self.groupBox_2)
        self.skeletonAllButton.setObjectName(u"skeletonAllButton")

        self.skeletonizeButtonLayout.addWidget(self.skeletonAllButton)


        self.verticalLayout_16.addLayout(self.skeletonizeButtonLayout)

        self.cleanBranchLabel = QLabel(self.groupBox_2)
        self.cleanBranchLabel.setObjectName(u"cleanBranchLabel")
        self.cleanBranchLabel.setWordWrap(True)

        self.verticalLayout_16.addWidget(self.cleanBranchLabel)

        self.branchLengthSpinBox = QSpinBox(self.groupBox_2)
        self.branchLengthSpinBox.setObjectName(u"branchLengthSpinBox")
        self.branchLengthSpinBox.setMinimum(1)
        self.branchLengthSpinBox.setMaximum(9999)
        self.branchLengthSpinBox.setValue(50)

        self.verticalLayout_16.addWidget(self.branchLengthSpinBox)

        self.cleanBranchButtonLayout = QHBoxLayout()
        self.cleanBranchButtonLayout.setObjectName(u"cleanBranchButtonLayout")
        self.cleanBranchButton = QPushButton(self.groupBox_2)
        self.cleanBranchButton.setObjectName(u"cleanBranchButton")

        self.cleanBranchButtonLayout.addWidget(self.cleanBranchButton)

        self.cleanBranchAllButton = QPushButton(self.groupBox_2)
        self.cleanBranchAllButton.setObjectName(u"cleanBranchAllButton")

        self.cleanBranchButtonLayout.addWidget(self.cleanBranchAllButton)


        self.verticalLayout_16.addLayout(self.cleanBranchButtonLayout)

        self.clearSkeletonLabel = QLabel(self.groupBox_2)
        self.clearSkeletonLabel.setObjectName(u"clearSkeletonLabel")

        self.verticalLayout_16.addWidget(self.clearSkeletonLabel)

        self.clearSkeletonButtonLayout = QHBoxLayout()
        self.clearSkeletonButtonLayout.setObjectName(u"clearSkeletonButtonLayout")
        self.clearSkeletonButton = QPushButton(self.groupBox_2)
        self.clearSkeletonButton.setObjectName(u"clearSkeletonButton")
        self.clearSkeletonButton.setIcon(icon9)
        self.clearSkeletonButton.setIconSize(QSize(20, 20))

        self.clearSkeletonButtonLayout.addWidget(self.clearSkeletonButton)

        self.clearSkeletonAllButton = QPushButton(self.groupBox_2)
        self.clearSkeletonAllButton.setObjectName(u"clearSkeletonAllButton")
        self.clearSkeletonAllButton.setIcon(icon9)
        self.clearSkeletonAllButton.setIconSize(QSize(20, 20))

        self.clearSkeletonButtonLayout.addWidget(self.clearSkeletonAllButton)


        self.verticalLayout_16.addLayout(self.clearSkeletonButtonLayout)

        self.verticalLayout_14 = QVBoxLayout()
        self.verticalLayout_14.setObjectName(u"verticalLayout_14")
        self.line_3 = QFrame(self.groupBox_2)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setFrameShape(QFrame.Shape.HLine)
        self.line_3.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout_14.addWidget(self.line_3)

        self.horizontalLayout_14 = QHBoxLayout()
        self.horizontalLayout_14.setObjectName(u"horizontalLayout_14")
        self.label_15 = QLabel(self.groupBox_2)
        self.label_15.setObjectName(u"label_15")
        sizePolicy5 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.label_15.sizePolicy().hasHeightForWidth())
        self.label_15.setSizePolicy(sizePolicy5)

        self.horizontalLayout_14.addWidget(self.label_15)

        self.nodeAddButton = QPushButton(self.groupBox_2)
        self.skeletonButtonGroup = QButtonGroup(MainWindow)
        self.skeletonButtonGroup.setObjectName(u"skeletonButtonGroup")
        self.skeletonButtonGroup.addButton(self.nodeAddButton)
        self.nodeAddButton.setObjectName(u"nodeAddButton")
        sizePolicy.setHeightForWidth(self.nodeAddButton.sizePolicy().hasHeightForWidth())
        self.nodeAddButton.setSizePolicy(sizePolicy)
        icon15 = QIcon()
        icon15.addFile(u":/icons/icons/routeadd.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.nodeAddButton.setIcon(icon15)
        self.nodeAddButton.setIconSize(QSize(25, 25))
        self.nodeAddButton.setCheckable(True)

        self.horizontalLayout_14.addWidget(self.nodeAddButton)

        self.nodeDeleteButton = QPushButton(self.groupBox_2)
        self.skeletonButtonGroup.addButton(self.nodeDeleteButton)
        self.nodeDeleteButton.setObjectName(u"nodeDeleteButton")
        sizePolicy.setHeightForWidth(self.nodeDeleteButton.sizePolicy().hasHeightForWidth())
        self.nodeDeleteButton.setSizePolicy(sizePolicy)
        icon16 = QIcon()
        icon16.addFile(u":/icons/icons/routedelete.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.nodeDeleteButton.setIcon(icon16)
        self.nodeDeleteButton.setIconSize(QSize(25, 25))
        self.nodeDeleteButton.setCheckable(True)

        self.horizontalLayout_14.addWidget(self.nodeDeleteButton)

        self.horizontalSpacer_8 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_14.addItem(self.horizontalSpacer_8)


        self.verticalLayout_14.addLayout(self.horizontalLayout_14)

        self.hintsButton = QPushButton(self.groupBox_2)
        self.hintsButton.setObjectName(u"hintsButton")
        self.hintsButton.setEnabled(False)
        sizePolicy.setHeightForWidth(self.hintsButton.sizePolicy().hasHeightForWidth())
        self.hintsButton.setSizePolicy(sizePolicy)
        self.hintsButton.setStyleSheet(u"QPushButton {\n"
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
        icon17 = QIcon()
        icon17.addFile(u":/icons/icons/hints.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.hintsButton.setIcon(icon17)
        self.hintsButton.setIconSize(QSize(18, 18))

        self.verticalLayout_14.addWidget(self.hintsButton)

        self.hintsLabel1 = QLabel(self.groupBox_2)
        self.hintsLabel1.setObjectName(u"hintsLabel1")
        self.hintsLabel1.setStyleSheet(u"color: gray;\n"
"")

        self.verticalLayout_14.addWidget(self.hintsLabel1)

        self.hintsLabel2 = QLabel(self.groupBox_2)
        self.hintsLabel2.setObjectName(u"hintsLabel2")
        self.hintsLabel2.setStyleSheet(u"color: gray;\n"
"")

        self.verticalLayout_14.addWidget(self.hintsLabel2)

        self.hintsLabel3 = QLabel(self.groupBox_2)
        self.hintsLabel3.setObjectName(u"hintsLabel3")
        self.hintsLabel3.setStyleSheet(u"color: gray;\n"
"")

        self.verticalLayout_14.addWidget(self.hintsLabel3)


        self.verticalLayout_16.addLayout(self.verticalLayout_14)


        self.verticalLayout_8.addWidget(self.groupBox_2)

        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_8.addItem(self.verticalSpacer_3)

        self.horizontalLayout_26 = QHBoxLayout()
        self.horizontalLayout_26.setObjectName(u"horizontalLayout_26")
        self.previousButton4 = QPushButton(self.page4)
        self.previousButton4.setObjectName(u"previousButton4")

        self.horizontalLayout_26.addWidget(self.previousButton4)

        self.nextButton4 = QPushButton(self.page4)
        self.nextButton4.setObjectName(u"nextButton4")

        self.horizontalLayout_26.addWidget(self.nextButton4)


        self.verticalLayout_8.addLayout(self.horizontalLayout_26)


        self.verticalLayout_9.addLayout(self.verticalLayout_8)

        self.stackedWidget.addWidget(self.page4)
        self.page5 = QWidget()
        self.page5.setObjectName(u"page5")
        self.verticalLayout_11 = QVBoxLayout(self.page5)
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.verticalLayout_10 = QVBoxLayout()
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.groupBox_4 = QGroupBox(self.page5)
        self.groupBox_4.setObjectName(u"groupBox_4")
        self.groupBox_4.setMinimumSize(QSize(0, 100))
        self.groupBox_4.setStyleSheet(u"QGroupBox{\n"
"    font-weight: bold;\n"
"}\n"
"")
        self.verticalLayout_18 = QVBoxLayout(self.groupBox_4)
        self.verticalLayout_18.setObjectName(u"verticalLayout_18")
        self.horizontalLayout_16 = QHBoxLayout()
        self.horizontalLayout_16.setObjectName(u"horizontalLayout_16")
        self.label_12 = QLabel(self.groupBox_4)
        self.label_12.setObjectName(u"label_12")

        self.horizontalLayout_16.addWidget(self.label_12)

        self.fileNameLabel = QLabel(self.groupBox_4)
        self.fileNameLabel.setObjectName(u"fileNameLabel")

        self.horizontalLayout_16.addWidget(self.fileNameLabel)


        self.verticalLayout_18.addLayout(self.horizontalLayout_16)

        self.horizontalLayout_20 = QHBoxLayout()
        self.horizontalLayout_20.setObjectName(u"horizontalLayout_20")
        self.label_4 = QLabel(self.groupBox_4)
        self.label_4.setObjectName(u"label_4")

        self.horizontalLayout_20.addWidget(self.label_4)

        self.crackAreaLabel = QLabel(self.groupBox_4)
        self.crackAreaLabel.setObjectName(u"crackAreaLabel")

        self.horizontalLayout_20.addWidget(self.crackAreaLabel)


        self.verticalLayout_18.addLayout(self.horizontalLayout_20)

        self.horizontalLayout_24 = QHBoxLayout()
        self.horizontalLayout_24.setObjectName(u"horizontalLayout_24")
        self.horizontalLayout_24.setContentsMargins(-1, -1, -1, 0)
        self.label_17 = QLabel(self.groupBox_4)
        self.label_17.setObjectName(u"label_17")

        self.horizontalLayout_24.addWidget(self.label_17)

        self.skeletonLengthLabel = QLabel(self.groupBox_4)
        self.skeletonLengthLabel.setObjectName(u"skeletonLengthLabel")

        self.horizontalLayout_24.addWidget(self.skeletonLengthLabel)


        self.verticalLayout_18.addLayout(self.horizontalLayout_24)

        self.horizontalLayout_15 = QHBoxLayout()
        self.horizontalLayout_15.setObjectName(u"horizontalLayout_15")
        self.label_11 = QLabel(self.groupBox_4)
        self.label_11.setObjectName(u"label_11")

        self.horizontalLayout_15.addWidget(self.label_11)

        self.crackWidthLabel = QLabel(self.groupBox_4)
        self.crackWidthLabel.setObjectName(u"crackWidthLabel")

        self.horizontalLayout_15.addWidget(self.crackWidthLabel)


        self.verticalLayout_18.addLayout(self.horizontalLayout_15)


        self.verticalLayout_10.addWidget(self.groupBox_4)

        self.line_2 = QFrame(self.page5)
        self.line_2.setObjectName(u"line_2")
        sizePolicy.setHeightForWidth(self.line_2.sizePolicy().hasHeightForWidth())
        self.line_2.setSizePolicy(sizePolicy)
        self.line_2.setFrameShape(QFrame.Shape.HLine)
        self.line_2.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout_10.addWidget(self.line_2)

        self.groupBox_5 = QGroupBox(self.page5)
        self.groupBox_5.setObjectName(u"groupBox_5")
        self.groupBox_5.setStyleSheet(u"QGroupBox{\n"
"    font-weight: bold;\n"
"}\n"
"")
        self.verticalLayout_19 = QVBoxLayout(self.groupBox_5)
        self.verticalLayout_19.setObjectName(u"verticalLayout_19")
        self.horizontalLayout_18 = QHBoxLayout()
        self.horizontalLayout_18.setObjectName(u"horizontalLayout_18")
        self.exportButton = QPushButton(self.groupBox_5)
        self.exportButton.setObjectName(u"exportButton")

        self.horizontalLayout_18.addWidget(self.exportButton)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_18.addItem(self.horizontalSpacer_6)


        self.verticalLayout_19.addLayout(self.horizontalLayout_18)


        self.verticalLayout_10.addWidget(self.groupBox_5)

        self.verticalSpacer_5 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_10.addItem(self.verticalSpacer_5)

        self.horizontalLayout_27 = QHBoxLayout()
        self.horizontalLayout_27.setObjectName(u"horizontalLayout_27")
        self.previousButton5 = QPushButton(self.page5)
        self.previousButton5.setObjectName(u"previousButton5")

        self.horizontalLayout_27.addWidget(self.previousButton5)

        self.nextButton5 = QPushButton(self.page5)
        self.nextButton5.setObjectName(u"nextButton5")

        self.horizontalLayout_27.addWidget(self.nextButton5)


        self.verticalLayout_10.addLayout(self.horizontalLayout_27)


        self.verticalLayout_11.addLayout(self.verticalLayout_10)

        self.stackedWidget.addWidget(self.page5)

        self.toolLayout.addWidget(self.stackedWidget)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.toolLayout.addItem(self.horizontalSpacer)


        self.horizontalLayout_2.addLayout(self.toolLayout)

        self.horizontalLayout_2.setStretch(0, 3)
        self.horizontalLayout_2.setStretch(1, 1)

        self.verticalLayout_4.addLayout(self.horizontalLayout_2)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.previousFigButton = QPushButton(self.centralwidget)
        self.previousFigButton.setObjectName(u"previousFigButton")
        self.previousFigButton.setMaximumSize(QSize(16777215, 80))
        icon18 = QIcon()
        icon18.addFile(u":/icons/icons/arrowleft.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.previousFigButton.setIcon(icon18)
        self.previousFigButton.setIconSize(QSize(20, 20))

        self.horizontalLayout.addWidget(self.previousFigButton)

        self.listWidget = QListWidget(self.centralwidget)
        self.listWidget.setObjectName(u"listWidget")
        self.listWidget.setMaximumSize(QSize(16777215, 80))
        self.listWidget.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.listWidget.setIconSize(QSize(70, 70))
        self.listWidget.setResizeMode(QListView.ResizeMode.Adjust)
        self.listWidget.setGridSize(QSize(80, 80))
        self.listWidget.setItemAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout.addWidget(self.listWidget)

        self.nextFigButton = QPushButton(self.centralwidget)
        self.nextFigButton.setObjectName(u"nextFigButton")
        self.nextFigButton.setMaximumSize(QSize(16777215, 80))
        icon19 = QIcon()
        icon19.addFile(u":/icons/icons/arrowright.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.nextFigButton.setIcon(icon19)
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
        self.menuBar.setGeometry(QRect(0, 0, 706, 33))
        self.menuFile = QMenu(self.menuBar)
        self.menuFile.setObjectName(u"menuFile")
        self.menuHelp = QMenu(self.menuBar)
        self.menuHelp.setObjectName(u"menuHelp")
        self.menuSetting = QMenu(self.menuBar)
        self.menuSetting.setObjectName(u"menuSetting")
        self.menuLanguage = QMenu(self.menuSetting)
        self.menuLanguage.setObjectName(u"menuLanguage")
        MainWindow.setMenuBar(self.menuBar)

        self.menuBar.addAction(self.menuFile.menuAction())
        self.menuBar.addAction(self.menuSetting.menuAction())
        self.menuBar.addAction(self.menuHelp.menuAction())
        self.menuFile.addAction(self.actionImportProject)
        self.menuFile.addAction(self.actionExportProject)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExit)
        self.menuHelp.addAction(self.actionDocumentation)
        self.menuHelp.addAction(self.actionAbout)
        self.menuSetting.addAction(self.menuLanguage.menuAction())
        self.menuLanguage.addAction(self.actionEnglish)
        self.menuLanguage.addAction(self.actionGerman)

        self.retranslateUi(MainWindow)

        self.stackedWidget.setCurrentIndex(5)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Crackpot", None))
        self.actionDocumentation.setText(QCoreApplication.translate("MainWindow", u"Documentation", None))
        self.actionAbout.setText(QCoreApplication.translate("MainWindow", u"About", None))
        self.actionExit.setText(QCoreApplication.translate("MainWindow", u"Exit", None))
        self.actionImportProject.setText(QCoreApplication.translate("MainWindow", u"Import Project...", None))
        self.actionExportProject.setText(QCoreApplication.translate("MainWindow", u"Export Project...", None))
        self.actionEnglish.setText(QCoreApplication.translate("MainWindow", u"English", None))
        self.actionGerman.setText(QCoreApplication.translate("MainWindow", u"German", None))
        self.calibrationProcessButton.setText("")
        self.uploadProcessButton.setText("")
        self.detectProcessButton.setText("")
        self.selectProcessButton.setText("")
        self.exportProcessButton.setText("")
        self.imageLabel.setText("")
        self.zoomInButton.setText("")
        self.zoomOutButton.setText("")
#if QT_CONFIG(tooltip)
        self.zoomFitButton.setToolTip(QCoreApplication.translate("MainWindow", u"Fit to Window", None))
#endif // QT_CONFIG(tooltip)
        self.zoomFitButton.setText("")
#if QT_CONFIG(tooltip)
        self.zoomOneToOneButton.setToolTip(QCoreApplication.translate("MainWindow", u"1:1 (Native Resolution)", None))
#endif // QT_CONFIG(tooltip)
        self.zoomOneToOneButton.setText("")
        self.deleteImageButton.setText("")
        self.groupBox_6.setTitle(QCoreApplication.translate("MainWindow", u"Calibration", None))
        self.label_14.setText(QCoreApplication.translate("MainWindow", u"Select an image for calibration.", None))
        self.caliUploadButton.setText(QCoreApplication.translate("MainWindow", u"Browse", None))
        self.label_10.setText(QCoreApplication.translate("MainWindow", u"Mark Calibration Points:", None))
        self.clickAddButton.setText("")
        self.clickDeleteButton.setText("")
        self.distanceLabel.setText(QCoreApplication.translate("MainWindow", u"Distance(mm)", None))
        self.pixelLabel.setText(QCoreApplication.translate("MainWindow", u"Pixel(px)", None))
        self.resolutionLabel.setText(QCoreApplication.translate("MainWindow", u"Resolution(mm/px)", None))
        self.confirmButton.setText(QCoreApplication.translate("MainWindow", u"Confirm", None))
        self.nextButton0.setText(QCoreApplication.translate("MainWindow", u"Next Stage", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("MainWindow", u"Upload Images", None))
        self.label_13.setText(QCoreApplication.translate("MainWindow", u"Click", None))
        self.plusButton.setText("")
        self.label_3.setText(QCoreApplication.translate("MainWindow", u" to upload figures.", None))
        self.previousButton1.setText(QCoreApplication.translate("MainWindow", u"Previous Stage", None))
        self.nextButton1.setText(QCoreApplication.translate("MainWindow", u"Next Stage", None))
        self.maskingGroupBox.setTitle(QCoreApplication.translate("MainWindow", u"Masking", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"Select a Model to do crack detection.", None))
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"Model", None))
        self.modelComboBox.setItemText(0, QCoreApplication.translate("MainWindow", u"Concrete Crack Segmentation", None))
        self.modelComboBox.setItemText(1, QCoreApplication.translate("MainWindow", u"None", None))

        self.applyModelLabel.setText(QCoreApplication.translate("MainWindow", u"Apply model:", None))
        self.applyModelButton.setText(QCoreApplication.translate("MainWindow", u"This Image", None))
        self.applyModelAllButton.setText(QCoreApplication.translate("MainWindow", u"All Images", None))
        self.clearMaskLabel.setText(QCoreApplication.translate("MainWindow", u"Clear mask:", None))
        self.clearMaskButton.setText(QCoreApplication.translate("MainWindow", u"This Image", None))
        self.clearMaskAllButton.setText(QCoreApplication.translate("MainWindow", u"All Images", None))
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"Editing Tools", None))
        self.addButton.setText(QCoreApplication.translate("MainWindow", u"Add", None))
        self.deleteButton.setText(QCoreApplication.translate("MainWindow", u"Delete", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Size", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Shape", None))
        self.penShapeComboBox.setItemText(0, QCoreApplication.translate("MainWindow", u"Round", None))
        self.penShapeComboBox.setItemText(1, QCoreApplication.translate("MainWindow", u"Square", None))

        self.label_8.setText(QCoreApplication.translate("MainWindow", u"Opacity:", None))
        self.labelOriginal.setText(QCoreApplication.translate("MainWindow", u"Original", None))
        self.labelMask.setText(QCoreApplication.translate("MainWindow", u"Mask", None))
        self.removePatchesLabel.setText(QCoreApplication.translate("MainWindow", u"Remove patches smaller than (px):", None))
#if QT_CONFIG(tooltip)
        self.patchAreaSpinBox.setToolTip(QCoreApplication.translate("MainWindow", u"Disconnected mask regions smaller than this area are removed.", None))
#endif // QT_CONFIG(tooltip)
        self.removePatchesButton.setText(QCoreApplication.translate("MainWindow", u"This Image", None))
        self.removePatchesAllButton.setText(QCoreApplication.translate("MainWindow", u"All Images", None))
        self.previousButton3.setText(QCoreApplication.translate("MainWindow", u"Previous Stage", None))
        self.nextButton3.setText(QCoreApplication.translate("MainWindow", u"Next Stage", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("MainWindow", u"Skeletonization", None))
        self.label_16.setText(QCoreApplication.translate("MainWindow", u"Extracting crack skeleton information.", None))
        self.skeletonizeLabel.setText(QCoreApplication.translate("MainWindow", u"Skeletonization", None))
        self.skeletonButton.setText(QCoreApplication.translate("MainWindow", u"This Image", None))
        self.skeletonAllButton.setText(QCoreApplication.translate("MainWindow", u"All Images", None))
        self.cleanBranchLabel.setText(QCoreApplication.translate("MainWindow", u"Remove branches shorter than (px):", None))
#if QT_CONFIG(tooltip)
        self.branchLengthSpinBox.setToolTip(QCoreApplication.translate("MainWindow", u"Branches shorter than this length are removed from the skeleton.", None))
#endif // QT_CONFIG(tooltip)
        self.cleanBranchButton.setText(QCoreApplication.translate("MainWindow", u"This Image", None))
        self.cleanBranchAllButton.setText(QCoreApplication.translate("MainWindow", u"All Images", None))
        self.clearSkeletonLabel.setText(QCoreApplication.translate("MainWindow", u"Clear skeleton", None))
        self.clearSkeletonButton.setText(QCoreApplication.translate("MainWindow", u"This Image", None))
        self.clearSkeletonAllButton.setText(QCoreApplication.translate("MainWindow", u"All Images", None))
        self.label_15.setText(QCoreApplication.translate("MainWindow", u"Skeleton Edit:", None))
        self.nodeAddButton.setText("")
        self.nodeDeleteButton.setText("")
        self.hintsButton.setText(QCoreApplication.translate("MainWindow", u"Hints:", None))
        self.hintsLabel1.setText(QCoreApplication.translate("MainWindow", u"Left-click to add and connect nodes.", None))
        self.hintsLabel2.setText(QCoreApplication.translate("MainWindow", u"Right-click to start a new segment.", None))
        self.hintsLabel3.setText(QCoreApplication.translate("MainWindow", u"Click a node to delete it and its lines.", None))
        self.previousButton4.setText(QCoreApplication.translate("MainWindow", u"Previous Stage", None))
        self.nextButton4.setText(QCoreApplication.translate("MainWindow", u"Next Stage", None))
        self.groupBox_4.setTitle(QCoreApplication.translate("MainWindow", u"Calculation Results", None))
        self.label_12.setText(QCoreApplication.translate("MainWindow", u"File Name:", None))
        self.fileNameLabel.setText("")
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Crack Area:", None))
        self.crackAreaLabel.setText("")
        self.label_17.setText(QCoreApplication.translate("MainWindow", u"Skeleton Length:", None))
        self.skeletonLengthLabel.setText("")
        self.label_11.setText(QCoreApplication.translate("MainWindow", u"Mean Crack Width:", None))
        self.crackWidthLabel.setText("")
        self.groupBox_5.setTitle(QCoreApplication.translate("MainWindow", u"Export Settings", None))
        self.exportButton.setText(QCoreApplication.translate("MainWindow", u"Export", None))
        self.previousButton5.setText(QCoreApplication.translate("MainWindow", u"Previous Stage", None))
        self.nextButton5.setText(QCoreApplication.translate("MainWindow", u"Finish", None))
        self.previousFigButton.setText("")
        self.nextFigButton.setText("")
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.menuHelp.setTitle(QCoreApplication.translate("MainWindow", u"Help", None))
        self.menuSetting.setTitle(QCoreApplication.translate("MainWindow", u"Setting", None))
        self.menuLanguage.setTitle(QCoreApplication.translate("MainWindow", u"Language", None))
    # retranslateUi

