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
from crackpot.frontend.ui import icon_rc

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
        self.actionCursorColor = QAction(MainWindow)
        self.actionCursorColor.setObjectName(u"actionCursorColor")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.mainLayout = QVBoxLayout(self.centralwidget)
        self.mainLayout.setObjectName(u"mainLayout")
        self.mainLayout.setContentsMargins(-1, 9, -1, -1)
        self.workspaceLayout = QVBoxLayout()
        self.workspaceLayout.setObjectName(u"workspaceLayout")
        self.workspaceLayout.setContentsMargins(-1, 0, -1, 0)
        self.stageBarLayout = QHBoxLayout()
        self.stageBarLayout.setObjectName(u"stageBarLayout")
        self.stageBarLayout.setContentsMargins(-1, 0, -1, 0)
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

        self.stageBarLayout.addWidget(self.calibrationProcessButton)

        self.stageSeparator0 = QFrame(self.centralwidget)
        self.stageSeparator0.setObjectName(u"stageSeparator0")
        self.stageSeparator0.setFrameShape(QFrame.Shape.HLine)
        self.stageSeparator0.setFrameShadow(QFrame.Shadow.Raised)
        self.stageSeparator0.setLineWidth(3)

        self.stageBarLayout.addWidget(self.stageSeparator0)

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

        self.stageBarLayout.addWidget(self.uploadProcessButton)

        self.stageSeparator1 = QFrame(self.centralwidget)
        self.stageSeparator1.setObjectName(u"stageSeparator1")
        self.stageSeparator1.setFrameShape(QFrame.Shape.HLine)
        self.stageSeparator1.setFrameShadow(QFrame.Shadow.Raised)
        self.stageSeparator1.setLineWidth(3)

        self.stageBarLayout.addWidget(self.stageSeparator1)

        self.maskingProcessButton = QPushButton(self.centralwidget)
        self.maskingProcessButton.setObjectName(u"maskingProcessButton")
        sizePolicy.setHeightForWidth(self.maskingProcessButton.sizePolicy().hasHeightForWidth())
        self.maskingProcessButton.setSizePolicy(sizePolicy)
        self.maskingProcessButton.setStyleSheet(u"QPushButton {\n"
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
        self.maskingProcessButton.setIcon(icon2)
        self.maskingProcessButton.setIconSize(QSize(30, 30))

        self.stageBarLayout.addWidget(self.maskingProcessButton)

        self.stageSeparator2 = QFrame(self.centralwidget)
        self.stageSeparator2.setObjectName(u"stageSeparator2")
        self.stageSeparator2.setFrameShape(QFrame.Shape.HLine)
        self.stageSeparator2.setFrameShadow(QFrame.Shadow.Raised)
        self.stageSeparator2.setLineWidth(3)

        self.stageBarLayout.addWidget(self.stageSeparator2)

        self.skeletonProcessButton = QPushButton(self.centralwidget)
        self.skeletonProcessButton.setObjectName(u"skeletonProcessButton")
        sizePolicy.setHeightForWidth(self.skeletonProcessButton.sizePolicy().hasHeightForWidth())
        self.skeletonProcessButton.setSizePolicy(sizePolicy)
        self.skeletonProcessButton.setStyleSheet(u"QPushButton {\n"
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
        self.skeletonProcessButton.setIcon(icon3)
        self.skeletonProcessButton.setIconSize(QSize(30, 30))

        self.stageBarLayout.addWidget(self.skeletonProcessButton)

        self.stageSeparator3 = QFrame(self.centralwidget)
        self.stageSeparator3.setObjectName(u"stageSeparator3")
        self.stageSeparator3.setFrameShape(QFrame.Shape.HLine)
        self.stageSeparator3.setFrameShadow(QFrame.Shadow.Raised)
        self.stageSeparator3.setLineWidth(3)

        self.stageBarLayout.addWidget(self.stageSeparator3)

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

        self.stageBarLayout.addWidget(self.exportProcessButton)


        self.workspaceLayout.addLayout(self.stageBarLayout)

        self.workAreaLayout = QHBoxLayout()
        self.workAreaLayout.setObjectName(u"workAreaLayout")
        self.workAreaLayout.setContentsMargins(0, 0, -1, -1)
        self.imageAreaLayout = QVBoxLayout()
        self.imageAreaLayout.setObjectName(u"imageAreaLayout")
        self.imageAreaLayout.setContentsMargins(-1, -1, -1, 0)
        self.imageScrollArea = QScrollArea(self.centralwidget)
        self.imageScrollArea.setObjectName(u"imageScrollArea")
        self.imageScrollArea.setWidgetResizable(True)
        self.imageScrollContents = QWidget()
        self.imageScrollContents.setObjectName(u"imageScrollContents")
        self.imageScrollContents.setGeometry(QRect(0, 0, 363, 372))
        self.imageLabelLayout = QVBoxLayout(self.imageScrollContents)
        self.imageLabelLayout.setObjectName(u"imageLabelLayout")
        self.imageLabel = QLabel(self.imageScrollContents)
        self.imageLabel.setObjectName(u"imageLabel")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.imageLabel.sizePolicy().hasHeightForWidth())
        self.imageLabel.setSizePolicy(sizePolicy1)
        self.imageLabel.setMinimumSize(QSize(0, 0))
        self.imageLabel.setMaximumSize(QSize(16777215, 16777215))
        self.imageLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.imageLabelLayout.addWidget(self.imageLabel)

        self.imageScrollArea.setWidget(self.imageScrollContents)

        self.imageAreaLayout.addWidget(self.imageScrollArea)

        self.zoomBarLayout = QHBoxLayout()
        self.zoomBarLayout.setObjectName(u"zoomBarLayout")
        self.zoomBarLeftSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.zoomBarLayout.addItem(self.zoomBarLeftSpacer)

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

        self.zoomBarLayout.addWidget(self.zoomInButton)

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

        self.zoomBarLayout.addWidget(self.zoomOutButton)

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

        self.zoomBarLayout.addWidget(self.zoomFitButton)

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

        self.zoomBarLayout.addWidget(self.zoomOneToOneButton)

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

        self.zoomBarLayout.addWidget(self.deleteImageButton)

        self.zoomBarRightSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.zoomBarLayout.addItem(self.zoomBarRightSpacer)


        self.imageAreaLayout.addLayout(self.zoomBarLayout)


        self.workAreaLayout.addLayout(self.imageAreaLayout)

        self.toolLayout = QVBoxLayout()
        self.toolLayout.setObjectName(u"toolLayout")
        self.stageStack = QStackedWidget(self.centralwidget)
        self.stageStack.setObjectName(u"stageStack")
        self.calibrationPage = QWidget()
        self.calibrationPage.setObjectName(u"calibrationPage")
        self.calibrationPageLayout = QVBoxLayout(self.calibrationPage)
        self.calibrationPageLayout.setObjectName(u"calibrationPageLayout")
        self.calibrationOuterLayout = QVBoxLayout()
        self.calibrationOuterLayout.setObjectName(u"calibrationOuterLayout")
        self.calibrationContentLayout = QVBoxLayout()
        self.calibrationContentLayout.setObjectName(u"calibrationContentLayout")
        self.calibrationHeaderLayout = QHBoxLayout()
        self.calibrationHeaderLayout.setObjectName(u"calibrationHeaderLayout")
        self.calibrationHeaderLayout.setContentsMargins(-1, -1, 0, 0)

        self.calibrationContentLayout.addLayout(self.calibrationHeaderLayout)

        self.calibrationGroupBox = QGroupBox(self.calibrationPage)
        self.calibrationGroupBox.setObjectName(u"calibrationGroupBox")
        self.calibrationGroupBox.setMinimumSize(QSize(0, 200))
        self.calibrationGroupBox.setStyleSheet(u"QGroupBox{\n"
"    font-weight: bold;\n"
"}\n"
"")
        self.calibrationGroupLayout = QVBoxLayout(self.calibrationGroupBox)
        self.calibrationGroupLayout.setObjectName(u"calibrationGroupLayout")
        self.calibrationImageLayout = QHBoxLayout()
        self.calibrationImageLayout.setObjectName(u"calibrationImageLayout")
        self.calibrationImageLayout.setContentsMargins(-1, -1, -1, 0)
        self.calibrationImageHintLabel = QLabel(self.calibrationGroupBox)
        self.calibrationImageHintLabel.setObjectName(u"calibrationImageHintLabel")

        self.calibrationImageLayout.addWidget(self.calibrationImageHintLabel)

        self.caliUploadButton = QPushButton(self.calibrationGroupBox)
        self.caliUploadButton.setObjectName(u"caliUploadButton")

        self.calibrationImageLayout.addWidget(self.caliUploadButton)

        self.calibrationImageSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.calibrationImageLayout.addItem(self.calibrationImageSpacer)


        self.calibrationGroupLayout.addLayout(self.calibrationImageLayout)

        self.calibrationPointsLayout = QHBoxLayout()
        self.calibrationPointsLayout.setObjectName(u"calibrationPointsLayout")
        self.calibrationPointsLayout.setContentsMargins(-1, -1, -1, 0)
        self.calibrationPointsLabel = QLabel(self.calibrationGroupBox)
        self.calibrationPointsLabel.setObjectName(u"calibrationPointsLabel")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.calibrationPointsLabel.sizePolicy().hasHeightForWidth())
        self.calibrationPointsLabel.setSizePolicy(sizePolicy2)

        self.calibrationPointsLayout.addWidget(self.calibrationPointsLabel)

        self.clickAddButton = QPushButton(self.calibrationGroupBox)
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

        self.calibrationPointsLayout.addWidget(self.clickAddButton)

        self.clickDeleteButton = QPushButton(self.calibrationGroupBox)
        self.caliButtonGroup.addButton(self.clickDeleteButton)
        self.clickDeleteButton.setObjectName(u"clickDeleteButton")
        sizePolicy.setHeightForWidth(self.clickDeleteButton.sizePolicy().hasHeightForWidth())
        self.clickDeleteButton.setSizePolicy(sizePolicy)
        icon11 = QIcon()
        icon11.addFile(u":/icons/icons/calidelete.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.clickDeleteButton.setIcon(icon11)
        self.clickDeleteButton.setIconSize(QSize(25, 25))
        self.clickDeleteButton.setCheckable(True)

        self.calibrationPointsLayout.addWidget(self.clickDeleteButton)

        self.calibrationPointsSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.calibrationPointsLayout.addItem(self.calibrationPointsSpacer)


        self.calibrationGroupLayout.addLayout(self.calibrationPointsLayout)

        self.calibrationSeparator = QFrame(self.calibrationGroupBox)
        self.calibrationSeparator.setObjectName(u"calibrationSeparator")
        self.calibrationSeparator.setFrameShape(QFrame.Shape.HLine)
        self.calibrationSeparator.setFrameShadow(QFrame.Shadow.Sunken)

        self.calibrationGroupLayout.addWidget(self.calibrationSeparator)

        self.calibrationValuesLayout = QFormLayout()
        self.calibrationValuesLayout.setObjectName(u"calibrationValuesLayout")
        self.calibrationValuesLayout.setContentsMargins(-1, -1, -1, 0)
        self.distanceLabel = QLabel(self.calibrationGroupBox)
        self.distanceLabel.setObjectName(u"distanceLabel")

        self.calibrationValuesLayout.setWidget(1, QFormLayout.ItemRole.LabelRole, self.distanceLabel)

        self.distanceLineEdit = QLineEdit(self.calibrationGroupBox)
        self.distanceLineEdit.setObjectName(u"distanceLineEdit")

        self.calibrationValuesLayout.setWidget(1, QFormLayout.ItemRole.FieldRole, self.distanceLineEdit)

        self.pixelLabel = QLabel(self.calibrationGroupBox)
        self.pixelLabel.setObjectName(u"pixelLabel")

        self.calibrationValuesLayout.setWidget(2, QFormLayout.ItemRole.LabelRole, self.pixelLabel)

        self.pixelLineEdit = QLineEdit(self.calibrationGroupBox)
        self.pixelLineEdit.setObjectName(u"pixelLineEdit")

        self.calibrationValuesLayout.setWidget(2, QFormLayout.ItemRole.FieldRole, self.pixelLineEdit)

        self.resolutionLabel = QLabel(self.calibrationGroupBox)
        self.resolutionLabel.setObjectName(u"resolutionLabel")

        self.calibrationValuesLayout.setWidget(3, QFormLayout.ItemRole.LabelRole, self.resolutionLabel)

        self.resolutionLineEdit = QLineEdit(self.calibrationGroupBox)
        self.resolutionLineEdit.setObjectName(u"resolutionLineEdit")

        self.calibrationValuesLayout.setWidget(3, QFormLayout.ItemRole.FieldRole, self.resolutionLineEdit)


        self.calibrationGroupLayout.addLayout(self.calibrationValuesLayout)

        self.calibrationConfirmLayout = QHBoxLayout()
        self.calibrationConfirmLayout.setObjectName(u"calibrationConfirmLayout")
        self.calibrationConfirmLayout.setContentsMargins(-1, -1, -1, 0)
        self.calibrationConfirmSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.calibrationConfirmLayout.addItem(self.calibrationConfirmSpacer)

        self.confirmButton = QPushButton(self.calibrationGroupBox)
        self.confirmButton.setObjectName(u"confirmButton")

        self.calibrationConfirmLayout.addWidget(self.confirmButton)


        self.calibrationGroupLayout.addLayout(self.calibrationConfirmLayout)


        self.calibrationContentLayout.addWidget(self.calibrationGroupBox)


        self.calibrationOuterLayout.addLayout(self.calibrationContentLayout)

        self.calibrationBottomSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.calibrationOuterLayout.addItem(self.calibrationBottomSpacer)

        self.calibrationNavigationLayout = QHBoxLayout()
        self.calibrationNavigationLayout.setObjectName(u"calibrationNavigationLayout")
        self.calibrationNavigationLayout.setContentsMargins(-1, -1, -1, 0)
        self.nextButton0 = QPushButton(self.calibrationPage)
        self.nextButton0.setObjectName(u"nextButton0")

        self.calibrationNavigationLayout.addWidget(self.nextButton0)


        self.calibrationOuterLayout.addLayout(self.calibrationNavigationLayout)


        self.calibrationPageLayout.addLayout(self.calibrationOuterLayout)

        self.stageStack.addWidget(self.calibrationPage)
        self.uploadPage = QWidget()
        self.uploadPage.setObjectName(u"uploadPage")
        self.uploadPageLayout = QVBoxLayout(self.uploadPage)
        self.uploadPageLayout.setObjectName(u"uploadPageLayout")
        self.uploadContentLayout = QVBoxLayout()
        self.uploadContentLayout.setObjectName(u"uploadContentLayout")
        self.uploadGroupBox = QGroupBox(self.uploadPage)
        self.uploadGroupBox.setObjectName(u"uploadGroupBox")
        self.uploadGroupBox.setMinimumSize(QSize(0, 100))
        self.uploadGroupBox.setStyleSheet(u"QGroupBox{\n"
"    font-weight: bold;\n"
"}\n"
"")
        self.uploadGroupLayout = QVBoxLayout(self.uploadGroupBox)
        self.uploadGroupLayout.setObjectName(u"uploadGroupLayout")
        self.uploadHintLayout = QHBoxLayout()
        self.uploadHintLayout.setObjectName(u"uploadHintLayout")
        self.uploadHintLayout.setContentsMargins(-1, -1, -1, 0)
        self.uploadHintPrefixLabel = QLabel(self.uploadGroupBox)
        self.uploadHintPrefixLabel.setObjectName(u"uploadHintPrefixLabel")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.uploadHintPrefixLabel.sizePolicy().hasHeightForWidth())
        self.uploadHintPrefixLabel.setSizePolicy(sizePolicy3)

        self.uploadHintLayout.addWidget(self.uploadHintPrefixLabel)

        self.plusButton = QPushButton(self.uploadGroupBox)
        self.plusButton.setObjectName(u"plusButton")
        sizePolicy.setHeightForWidth(self.plusButton.sizePolicy().hasHeightForWidth())
        self.plusButton.setSizePolicy(sizePolicy)
        self.plusButton.setMinimumSize(QSize(80, 80))
        icon12 = QIcon()
        icon12.addFile(u":/icons/icons/plus.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.plusButton.setIcon(icon12)
        self.plusButton.setIconSize(QSize(50, 50))

        self.uploadHintLayout.addWidget(self.plusButton)

        self.uploadHintSuffixLabel = QLabel(self.uploadGroupBox)
        self.uploadHintSuffixLabel.setObjectName(u"uploadHintSuffixLabel")

        self.uploadHintLayout.addWidget(self.uploadHintSuffixLabel)


        self.uploadGroupLayout.addLayout(self.uploadHintLayout)


        self.uploadContentLayout.addWidget(self.uploadGroupBox)

        self.uploadBottomSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.uploadContentLayout.addItem(self.uploadBottomSpacer)

        self.uploadNavigationLayout = QHBoxLayout()
        self.uploadNavigationLayout.setObjectName(u"uploadNavigationLayout")
        self.uploadNavigationLayout.setContentsMargins(-1, -1, -1, 0)
        self.previousButton1 = QPushButton(self.uploadPage)
        self.previousButton1.setObjectName(u"previousButton1")

        self.uploadNavigationLayout.addWidget(self.previousButton1)

        self.nextButton1 = QPushButton(self.uploadPage)
        self.nextButton1.setObjectName(u"nextButton1")

        self.uploadNavigationLayout.addWidget(self.nextButton1)


        self.uploadContentLayout.addLayout(self.uploadNavigationLayout)


        self.uploadPageLayout.addLayout(self.uploadContentLayout)

        self.stageStack.addWidget(self.uploadPage)
        self.maskingPage = QWidget()
        self.maskingPage.setObjectName(u"maskingPage")
        self.maskingPageLayout = QVBoxLayout(self.maskingPage)
        self.maskingPageLayout.setObjectName(u"maskingPageLayout")
        self.maskingContentLayout = QVBoxLayout()
        self.maskingContentLayout.setObjectName(u"maskingContentLayout")
        self.maskingContentLayout.setContentsMargins(-1, -1, -1, 0)
        self.maskingGroupBox = QGroupBox(self.maskingPage)
        self.maskingGroupBox.setObjectName(u"maskingGroupBox")
        self.maskingGroupBox.setStyleSheet(u"QGroupBox{\n"
"    font-weight: bold;\n"
"}\n"
"")
        self.maskingGroupLayout = QVBoxLayout(self.maskingGroupBox)
        self.maskingGroupLayout.setObjectName(u"maskingGroupLayout")
        self.modelHintLabel = QLabel(self.maskingGroupBox)
        self.modelHintLabel.setObjectName(u"modelHintLabel")

        self.maskingGroupLayout.addWidget(self.modelHintLabel)

        self.modelSelectionLayout = QHBoxLayout()
        self.modelSelectionLayout.setObjectName(u"modelSelectionLayout")
        self.modelLabel = QLabel(self.maskingGroupBox)
        self.modelLabel.setObjectName(u"modelLabel")

        self.modelSelectionLayout.addWidget(self.modelLabel)

        self.modelComboBox = QComboBox(self.maskingGroupBox)
        self.modelComboBox.addItem("")
        self.modelComboBox.addItem("")
        self.modelComboBox.setObjectName(u"modelComboBox")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.modelComboBox.sizePolicy().hasHeightForWidth())
        self.modelComboBox.setSizePolicy(sizePolicy4)

        self.modelSelectionLayout.addWidget(self.modelComboBox)


        self.maskingGroupLayout.addLayout(self.modelSelectionLayout)

        self.applyModelLabel = QLabel(self.maskingGroupBox)
        self.applyModelLabel.setObjectName(u"applyModelLabel")

        self.maskingGroupLayout.addWidget(self.applyModelLabel)

        self.applyModelButtonLayout = QHBoxLayout()
        self.applyModelButtonLayout.setObjectName(u"applyModelButtonLayout")
        self.applyModelButton = QPushButton(self.maskingGroupBox)
        self.applyModelButton.setObjectName(u"applyModelButton")

        self.applyModelButtonLayout.addWidget(self.applyModelButton)

        self.applyModelAllButton = QPushButton(self.maskingGroupBox)
        self.applyModelAllButton.setObjectName(u"applyModelAllButton")

        self.applyModelButtonLayout.addWidget(self.applyModelAllButton)


        self.maskingGroupLayout.addLayout(self.applyModelButtonLayout)

        self.clearMaskLabel = QLabel(self.maskingGroupBox)
        self.clearMaskLabel.setObjectName(u"clearMaskLabel")

        self.maskingGroupLayout.addWidget(self.clearMaskLabel)

        self.clearMaskButtonLayout = QHBoxLayout()
        self.clearMaskButtonLayout.setObjectName(u"clearMaskButtonLayout")
        self.clearMaskButton = QPushButton(self.maskingGroupBox)
        self.clearMaskButton.setObjectName(u"clearMaskButton")

        self.clearMaskButtonLayout.addWidget(self.clearMaskButton)

        self.clearMaskAllButton = QPushButton(self.maskingGroupBox)
        self.clearMaskAllButton.setObjectName(u"clearMaskAllButton")

        self.clearMaskButtonLayout.addWidget(self.clearMaskAllButton)


        self.maskingGroupLayout.addLayout(self.clearMaskButtonLayout)


        self.maskingContentLayout.addWidget(self.maskingGroupBox)

        self.editingToolsGroupBox = QGroupBox(self.maskingPage)
        self.editingToolsGroupBox.setObjectName(u"editingToolsGroupBox")
        self.editingToolsGroupBox.setMinimumSize(QSize(0, 150))
        self.editingToolsGroupBox.setStyleSheet(u"QGroupBox{\n"
"    font-weight: bold;\n"
"}\n"
"")
        self.editingToolsLayout = QVBoxLayout(self.editingToolsGroupBox)
        self.editingToolsLayout.setObjectName(u"editingToolsLayout")
        self.editModeLayout = QHBoxLayout()
        self.editModeLayout.setObjectName(u"editModeLayout")
        self.addButton = QPushButton(self.editingToolsGroupBox)
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

        self.editModeLayout.addWidget(self.addButton)

        self.deleteButton = QPushButton(self.editingToolsGroupBox)
        self.penButtonGroup.addButton(self.deleteButton)
        self.deleteButton.setObjectName(u"deleteButton")
        icon14 = QIcon()
        icon14.addFile(u":/icons/icons/penminus.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.deleteButton.setIcon(icon14)
        self.deleteButton.setIconSize(QSize(23, 23))
        self.deleteButton.setCheckable(True)

        self.editModeLayout.addWidget(self.deleteButton)


        self.editingToolsLayout.addLayout(self.editModeLayout)

        self.penSizeLayout = QHBoxLayout()
        self.penSizeLayout.setObjectName(u"penSizeLayout")
        self.penSizeLabel = QLabel(self.editingToolsGroupBox)
        self.penSizeLabel.setObjectName(u"penSizeLabel")

        self.penSizeLayout.addWidget(self.penSizeLabel)

        self.penSizeSlider = QSlider(self.editingToolsGroupBox)
        self.penSizeSlider.setObjectName(u"penSizeSlider")
        self.penSizeSlider.setOrientation(Qt.Orientation.Horizontal)

        self.penSizeLayout.addWidget(self.penSizeSlider)


        self.editingToolsLayout.addLayout(self.penSizeLayout)

        self.penShapeLayout = QHBoxLayout()
        self.penShapeLayout.setObjectName(u"penShapeLayout")
        self.penShapeLabel = QLabel(self.editingToolsGroupBox)
        self.penShapeLabel.setObjectName(u"penShapeLabel")

        self.penShapeLayout.addWidget(self.penShapeLabel)

        self.penShapeComboBox = QComboBox(self.editingToolsGroupBox)
        self.penShapeComboBox.addItem("")
        self.penShapeComboBox.addItem("")
        self.penShapeComboBox.setObjectName(u"penShapeComboBox")
        sizePolicy4.setHeightForWidth(self.penShapeComboBox.sizePolicy().hasHeightForWidth())
        self.penShapeComboBox.setSizePolicy(sizePolicy4)

        self.penShapeLayout.addWidget(self.penShapeComboBox)


        self.editingToolsLayout.addLayout(self.penShapeLayout)

        self.opacityLayout = QHBoxLayout()
        self.opacityLayout.setObjectName(u"opacityLayout")
        self.opacityLayout.setContentsMargins(-1, 0, -1, -1)
        self.opacityLabel = QLabel(self.editingToolsGroupBox)
        self.opacityLabel.setObjectName(u"opacityLabel")

        self.opacityLayout.addWidget(self.opacityLabel)

        self.labelOriginal = QLabel(self.editingToolsGroupBox)
        self.labelOriginal.setObjectName(u"labelOriginal")

        self.opacityLayout.addWidget(self.labelOriginal)

        self.opacitySlider = QSlider(self.editingToolsGroupBox)
        self.opacitySlider.setObjectName(u"opacitySlider")
        self.opacitySlider.setOrientation(Qt.Orientation.Horizontal)

        self.opacityLayout.addWidget(self.opacitySlider)

        self.labelMask = QLabel(self.editingToolsGroupBox)
        self.labelMask.setObjectName(u"labelMask")

        self.opacityLayout.addWidget(self.labelMask)


        self.editingToolsLayout.addLayout(self.opacityLayout)

        self.removePatchesLabel = QLabel(self.editingToolsGroupBox)
        self.removePatchesLabel.setObjectName(u"removePatchesLabel")
        self.removePatchesLabel.setWordWrap(True)

        self.editingToolsLayout.addWidget(self.removePatchesLabel)

        self.patchAreaSpinBox = QSpinBox(self.editingToolsGroupBox)
        self.patchAreaSpinBox.setObjectName(u"patchAreaSpinBox")
        self.patchAreaSpinBox.setMinimum(1)
        self.patchAreaSpinBox.setMaximum(999999)
        self.patchAreaSpinBox.setValue(50)

        self.editingToolsLayout.addWidget(self.patchAreaSpinBox)

        self.removePatchesButtonLayout = QHBoxLayout()
        self.removePatchesButtonLayout.setObjectName(u"removePatchesButtonLayout")
        self.removePatchesButton = QPushButton(self.editingToolsGroupBox)
        self.removePatchesButton.setObjectName(u"removePatchesButton")

        self.removePatchesButtonLayout.addWidget(self.removePatchesButton)

        self.removePatchesAllButton = QPushButton(self.editingToolsGroupBox)
        self.removePatchesAllButton.setObjectName(u"removePatchesAllButton")

        self.removePatchesButtonLayout.addWidget(self.removePatchesAllButton)


        self.editingToolsLayout.addLayout(self.removePatchesButtonLayout)


        self.maskingContentLayout.addWidget(self.editingToolsGroupBox)

        self.maskingBottomSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.maskingContentLayout.addItem(self.maskingBottomSpacer)

        self.maskingNavigationLayout = QHBoxLayout()
        self.maskingNavigationLayout.setObjectName(u"maskingNavigationLayout")
        self.previousButton2 = QPushButton(self.maskingPage)
        self.previousButton2.setObjectName(u"previousButton2")

        self.maskingNavigationLayout.addWidget(self.previousButton2)

        self.nextButton2 = QPushButton(self.maskingPage)
        self.nextButton2.setObjectName(u"nextButton2")

        self.maskingNavigationLayout.addWidget(self.nextButton2)


        self.maskingContentLayout.addLayout(self.maskingNavigationLayout)


        self.maskingPageLayout.addLayout(self.maskingContentLayout)

        self.stageStack.addWidget(self.maskingPage)
        self.skeletonPage = QWidget()
        self.skeletonPage.setObjectName(u"skeletonPage")
        self.skeletonPageLayout = QVBoxLayout(self.skeletonPage)
        self.skeletonPageLayout.setObjectName(u"skeletonPageLayout")
        self.skeletonContentLayout = QVBoxLayout()
        self.skeletonContentLayout.setObjectName(u"skeletonContentLayout")
        self.skeletonizationGroupBox = QGroupBox(self.skeletonPage)
        self.skeletonizationGroupBox.setObjectName(u"skeletonizationGroupBox")
        self.skeletonizationGroupBox.setStyleSheet(u"QGroupBox{\n"
"    font-weight: bold;\n"
"}\n"
"")
        self.skeletonizationGroupLayout = QVBoxLayout(self.skeletonizationGroupBox)
        self.skeletonizationGroupLayout.setObjectName(u"skeletonizationGroupLayout")
        self.skeletonHintLabel = QLabel(self.skeletonizationGroupBox)
        self.skeletonHintLabel.setObjectName(u"skeletonHintLabel")

        self.skeletonizationGroupLayout.addWidget(self.skeletonHintLabel)

        self.skeletonizeLabel = QLabel(self.skeletonizationGroupBox)
        self.skeletonizeLabel.setObjectName(u"skeletonizeLabel")

        self.skeletonizationGroupLayout.addWidget(self.skeletonizeLabel)

        self.skeletonizeButtonLayout = QHBoxLayout()
        self.skeletonizeButtonLayout.setObjectName(u"skeletonizeButtonLayout")
        self.skeletonButton = QPushButton(self.skeletonizationGroupBox)
        self.skeletonButton.setObjectName(u"skeletonButton")

        self.skeletonizeButtonLayout.addWidget(self.skeletonButton)

        self.skeletonAllButton = QPushButton(self.skeletonizationGroupBox)
        self.skeletonAllButton.setObjectName(u"skeletonAllButton")

        self.skeletonizeButtonLayout.addWidget(self.skeletonAllButton)


        self.skeletonizationGroupLayout.addLayout(self.skeletonizeButtonLayout)

        self.cleanBranchLabel = QLabel(self.skeletonizationGroupBox)
        self.cleanBranchLabel.setObjectName(u"cleanBranchLabel")
        self.cleanBranchLabel.setWordWrap(True)

        self.skeletonizationGroupLayout.addWidget(self.cleanBranchLabel)

        self.branchLengthSpinBox = QSpinBox(self.skeletonizationGroupBox)
        self.branchLengthSpinBox.setObjectName(u"branchLengthSpinBox")
        self.branchLengthSpinBox.setMinimum(1)
        self.branchLengthSpinBox.setMaximum(9999)
        self.branchLengthSpinBox.setValue(50)

        self.skeletonizationGroupLayout.addWidget(self.branchLengthSpinBox)

        self.cleanBranchButtonLayout = QHBoxLayout()
        self.cleanBranchButtonLayout.setObjectName(u"cleanBranchButtonLayout")
        self.cleanBranchButton = QPushButton(self.skeletonizationGroupBox)
        self.cleanBranchButton.setObjectName(u"cleanBranchButton")

        self.cleanBranchButtonLayout.addWidget(self.cleanBranchButton)

        self.cleanBranchAllButton = QPushButton(self.skeletonizationGroupBox)
        self.cleanBranchAllButton.setObjectName(u"cleanBranchAllButton")

        self.cleanBranchButtonLayout.addWidget(self.cleanBranchAllButton)


        self.skeletonizationGroupLayout.addLayout(self.cleanBranchButtonLayout)

        self.clearSkeletonLabel = QLabel(self.skeletonizationGroupBox)
        self.clearSkeletonLabel.setObjectName(u"clearSkeletonLabel")

        self.skeletonizationGroupLayout.addWidget(self.clearSkeletonLabel)

        self.clearSkeletonButtonLayout = QHBoxLayout()
        self.clearSkeletonButtonLayout.setObjectName(u"clearSkeletonButtonLayout")
        self.clearSkeletonButton = QPushButton(self.skeletonizationGroupBox)
        self.clearSkeletonButton.setObjectName(u"clearSkeletonButton")
        self.clearSkeletonButton.setIcon(icon9)
        self.clearSkeletonButton.setIconSize(QSize(20, 20))

        self.clearSkeletonButtonLayout.addWidget(self.clearSkeletonButton)

        self.clearSkeletonAllButton = QPushButton(self.skeletonizationGroupBox)
        self.clearSkeletonAllButton.setObjectName(u"clearSkeletonAllButton")
        self.clearSkeletonAllButton.setIcon(icon9)
        self.clearSkeletonAllButton.setIconSize(QSize(20, 20))

        self.clearSkeletonButtonLayout.addWidget(self.clearSkeletonAllButton)


        self.skeletonizationGroupLayout.addLayout(self.clearSkeletonButtonLayout)

        self.skeletonEditLayout = QVBoxLayout()
        self.skeletonEditLayout.setObjectName(u"skeletonEditLayout")
        self.skeletonEditSeparator = QFrame(self.skeletonizationGroupBox)
        self.skeletonEditSeparator.setObjectName(u"skeletonEditSeparator")
        self.skeletonEditSeparator.setFrameShape(QFrame.Shape.HLine)
        self.skeletonEditSeparator.setFrameShadow(QFrame.Shadow.Sunken)

        self.skeletonEditLayout.addWidget(self.skeletonEditSeparator)

        self.skeletonEditToolLayout = QHBoxLayout()
        self.skeletonEditToolLayout.setObjectName(u"skeletonEditToolLayout")
        self.skeletonEditLabel = QLabel(self.skeletonizationGroupBox)
        self.skeletonEditLabel.setObjectName(u"skeletonEditLabel")
        sizePolicy5 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.skeletonEditLabel.sizePolicy().hasHeightForWidth())
        self.skeletonEditLabel.setSizePolicy(sizePolicy5)

        self.skeletonEditToolLayout.addWidget(self.skeletonEditLabel)

        self.nodeAddButton = QPushButton(self.skeletonizationGroupBox)
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

        self.skeletonEditToolLayout.addWidget(self.nodeAddButton)

        self.nodeDeleteButton = QPushButton(self.skeletonizationGroupBox)
        self.skeletonButtonGroup.addButton(self.nodeDeleteButton)
        self.nodeDeleteButton.setObjectName(u"nodeDeleteButton")
        sizePolicy.setHeightForWidth(self.nodeDeleteButton.sizePolicy().hasHeightForWidth())
        self.nodeDeleteButton.setSizePolicy(sizePolicy)
        icon16 = QIcon()
        icon16.addFile(u":/icons/icons/routedelete.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.nodeDeleteButton.setIcon(icon16)
        self.nodeDeleteButton.setIconSize(QSize(25, 25))
        self.nodeDeleteButton.setCheckable(True)

        self.skeletonEditToolLayout.addWidget(self.nodeDeleteButton)

        self.skeletonEditSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.skeletonEditToolLayout.addItem(self.skeletonEditSpacer)


        self.skeletonEditLayout.addLayout(self.skeletonEditToolLayout)

        self.hintsButton = QPushButton(self.skeletonizationGroupBox)
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

        self.skeletonEditLayout.addWidget(self.hintsButton)

        self.addNodeHintLabel = QLabel(self.skeletonizationGroupBox)
        self.addNodeHintLabel.setObjectName(u"addNodeHintLabel")
        self.addNodeHintLabel.setStyleSheet(u"color: gray;\n"
"")

        self.skeletonEditLayout.addWidget(self.addNodeHintLabel)

        self.newSegmentHintLabel = QLabel(self.skeletonizationGroupBox)
        self.newSegmentHintLabel.setObjectName(u"newSegmentHintLabel")
        self.newSegmentHintLabel.setStyleSheet(u"color: gray;\n"
"")

        self.skeletonEditLayout.addWidget(self.newSegmentHintLabel)

        self.deleteNodeHintLabel = QLabel(self.skeletonizationGroupBox)
        self.deleteNodeHintLabel.setObjectName(u"deleteNodeHintLabel")
        self.deleteNodeHintLabel.setStyleSheet(u"color: gray;\n"
"")

        self.skeletonEditLayout.addWidget(self.deleteNodeHintLabel)


        self.skeletonizationGroupLayout.addLayout(self.skeletonEditLayout)


        self.skeletonContentLayout.addWidget(self.skeletonizationGroupBox)

        self.skeletonBottomSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.skeletonContentLayout.addItem(self.skeletonBottomSpacer)

        self.skeletonNavigationLayout = QHBoxLayout()
        self.skeletonNavigationLayout.setObjectName(u"skeletonNavigationLayout")
        self.previousButton3 = QPushButton(self.skeletonPage)
        self.previousButton3.setObjectName(u"previousButton3")

        self.skeletonNavigationLayout.addWidget(self.previousButton3)

        self.nextButton3 = QPushButton(self.skeletonPage)
        self.nextButton3.setObjectName(u"nextButton3")

        self.skeletonNavigationLayout.addWidget(self.nextButton3)


        self.skeletonContentLayout.addLayout(self.skeletonNavigationLayout)


        self.skeletonPageLayout.addLayout(self.skeletonContentLayout)

        self.stageStack.addWidget(self.skeletonPage)
        self.exportPage = QWidget()
        self.exportPage.setObjectName(u"exportPage")
        self.exportPageLayout = QVBoxLayout(self.exportPage)
        self.exportPageLayout.setObjectName(u"exportPageLayout")
        self.exportContentLayout = QVBoxLayout()
        self.exportContentLayout.setObjectName(u"exportContentLayout")
        self.resultsGroupBox = QGroupBox(self.exportPage)
        self.resultsGroupBox.setObjectName(u"resultsGroupBox")
        self.resultsGroupBox.setMinimumSize(QSize(0, 100))
        self.resultsGroupBox.setStyleSheet(u"QGroupBox{\n"
"    font-weight: bold;\n"
"}\n"
"")
        self.resultsLayout = QVBoxLayout(self.resultsGroupBox)
        self.resultsLayout.setObjectName(u"resultsLayout")
        self.fileNameRowLayout = QHBoxLayout()
        self.fileNameRowLayout.setObjectName(u"fileNameRowLayout")
        self.fileNameCaptionLabel = QLabel(self.resultsGroupBox)
        self.fileNameCaptionLabel.setObjectName(u"fileNameCaptionLabel")

        self.fileNameRowLayout.addWidget(self.fileNameCaptionLabel)

        self.fileNameLabel = QLabel(self.resultsGroupBox)
        self.fileNameLabel.setObjectName(u"fileNameLabel")

        self.fileNameRowLayout.addWidget(self.fileNameLabel)


        self.resultsLayout.addLayout(self.fileNameRowLayout)

        self.crackAreaRowLayout = QHBoxLayout()
        self.crackAreaRowLayout.setObjectName(u"crackAreaRowLayout")
        self.crackAreaCaptionLabel = QLabel(self.resultsGroupBox)
        self.crackAreaCaptionLabel.setObjectName(u"crackAreaCaptionLabel")

        self.crackAreaRowLayout.addWidget(self.crackAreaCaptionLabel)

        self.crackAreaLabel = QLabel(self.resultsGroupBox)
        self.crackAreaLabel.setObjectName(u"crackAreaLabel")

        self.crackAreaRowLayout.addWidget(self.crackAreaLabel)


        self.resultsLayout.addLayout(self.crackAreaRowLayout)

        self.skeletonLengthRowLayout = QHBoxLayout()
        self.skeletonLengthRowLayout.setObjectName(u"skeletonLengthRowLayout")
        self.skeletonLengthRowLayout.setContentsMargins(-1, -1, -1, 0)
        self.skeletonLengthCaptionLabel = QLabel(self.resultsGroupBox)
        self.skeletonLengthCaptionLabel.setObjectName(u"skeletonLengthCaptionLabel")

        self.skeletonLengthRowLayout.addWidget(self.skeletonLengthCaptionLabel)

        self.skeletonLengthLabel = QLabel(self.resultsGroupBox)
        self.skeletonLengthLabel.setObjectName(u"skeletonLengthLabel")

        self.skeletonLengthRowLayout.addWidget(self.skeletonLengthLabel)


        self.resultsLayout.addLayout(self.skeletonLengthRowLayout)

        self.crackWidthRowLayout = QHBoxLayout()
        self.crackWidthRowLayout.setObjectName(u"crackWidthRowLayout")
        self.crackWidthCaptionLabel = QLabel(self.resultsGroupBox)
        self.crackWidthCaptionLabel.setObjectName(u"crackWidthCaptionLabel")

        self.crackWidthRowLayout.addWidget(self.crackWidthCaptionLabel)

        self.crackWidthLabel = QLabel(self.resultsGroupBox)
        self.crackWidthLabel.setObjectName(u"crackWidthLabel")

        self.crackWidthRowLayout.addWidget(self.crackWidthLabel)


        self.resultsLayout.addLayout(self.crackWidthRowLayout)


        self.exportContentLayout.addWidget(self.resultsGroupBox)

        self.resultsSeparator = QFrame(self.exportPage)
        self.resultsSeparator.setObjectName(u"resultsSeparator")
        sizePolicy.setHeightForWidth(self.resultsSeparator.sizePolicy().hasHeightForWidth())
        self.resultsSeparator.setSizePolicy(sizePolicy)
        self.resultsSeparator.setFrameShape(QFrame.Shape.HLine)
        self.resultsSeparator.setFrameShadow(QFrame.Shadow.Sunken)

        self.exportContentLayout.addWidget(self.resultsSeparator)

        self.exportSettingsGroupBox = QGroupBox(self.exportPage)
        self.exportSettingsGroupBox.setObjectName(u"exportSettingsGroupBox")
        self.exportSettingsGroupBox.setStyleSheet(u"QGroupBox{\n"
"    font-weight: bold;\n"
"}\n"
"")
        self.exportSettingsLayout = QVBoxLayout(self.exportSettingsGroupBox)
        self.exportSettingsLayout.setObjectName(u"exportSettingsLayout")
        self.exportButtonLayout = QHBoxLayout()
        self.exportButtonLayout.setObjectName(u"exportButtonLayout")
        self.exportButton = QPushButton(self.exportSettingsGroupBox)
        self.exportButton.setObjectName(u"exportButton")

        self.exportButtonLayout.addWidget(self.exportButton)

        self.exportButtonSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.exportButtonLayout.addItem(self.exportButtonSpacer)


        self.exportSettingsLayout.addLayout(self.exportButtonLayout)


        self.exportContentLayout.addWidget(self.exportSettingsGroupBox)

        self.exportBottomSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.exportContentLayout.addItem(self.exportBottomSpacer)

        self.exportNavigationLayout = QHBoxLayout()
        self.exportNavigationLayout.setObjectName(u"exportNavigationLayout")
        self.previousButton4 = QPushButton(self.exportPage)
        self.previousButton4.setObjectName(u"previousButton4")

        self.exportNavigationLayout.addWidget(self.previousButton4)

        self.nextButton4 = QPushButton(self.exportPage)
        self.nextButton4.setObjectName(u"nextButton4")

        self.exportNavigationLayout.addWidget(self.nextButton4)


        self.exportContentLayout.addLayout(self.exportNavigationLayout)


        self.exportPageLayout.addLayout(self.exportContentLayout)

        self.stageStack.addWidget(self.exportPage)

        self.toolLayout.addWidget(self.stageStack)

        self.toolPanelSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.toolLayout.addItem(self.toolPanelSpacer)


        self.workAreaLayout.addLayout(self.toolLayout)

        self.workAreaLayout.setStretch(0, 3)
        self.workAreaLayout.setStretch(1, 1)

        self.workspaceLayout.addLayout(self.workAreaLayout)

        self.imageListLayout = QHBoxLayout()
        self.imageListLayout.setObjectName(u"imageListLayout")
        self.previousFigButton = QPushButton(self.centralwidget)
        self.previousFigButton.setObjectName(u"previousFigButton")
        self.previousFigButton.setMaximumSize(QSize(16777215, 80))
        icon18 = QIcon()
        icon18.addFile(u":/icons/icons/arrowleft.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.previousFigButton.setIcon(icon18)
        self.previousFigButton.setIconSize(QSize(20, 20))

        self.imageListLayout.addWidget(self.previousFigButton)

        self.imageListWidget = QListWidget(self.centralwidget)
        self.imageListWidget.setObjectName(u"imageListWidget")
        self.imageListWidget.setMaximumSize(QSize(16777215, 80))
        self.imageListWidget.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.imageListWidget.setIconSize(QSize(70, 70))
        self.imageListWidget.setResizeMode(QListView.ResizeMode.Adjust)
        self.imageListWidget.setGridSize(QSize(80, 80))
        self.imageListWidget.setItemAlignment(Qt.AlignmentFlag.AlignCenter)

        self.imageListLayout.addWidget(self.imageListWidget)

        self.nextFigButton = QPushButton(self.centralwidget)
        self.nextFigButton.setObjectName(u"nextFigButton")
        self.nextFigButton.setMaximumSize(QSize(16777215, 80))
        icon19 = QIcon()
        icon19.addFile(u":/icons/icons/arrowright.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.nextFigButton.setIcon(icon19)
        self.nextFigButton.setIconSize(QSize(20, 20))

        self.imageListLayout.addWidget(self.nextFigButton)


        self.workspaceLayout.addLayout(self.imageListLayout)


        self.mainLayout.addLayout(self.workspaceLayout)

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
        self.menuSetting.addAction(self.actionCursorColor)
        self.menuLanguage.addAction(self.actionEnglish)
        self.menuLanguage.addAction(self.actionGerman)

        self.retranslateUi(MainWindow)

        self.stageStack.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Crackpot", None))
        self.actionDocumentation.setText(QCoreApplication.translate("MainWindow", u"Documentation", None))
        self.actionAbout.setText(QCoreApplication.translate("MainWindow", u"About", None))
        self.actionExit.setText(QCoreApplication.translate("MainWindow", u"Exit", None))
        self.actionImportProject.setText(QCoreApplication.translate("MainWindow", u"Import Project", None))
        self.actionExportProject.setText(QCoreApplication.translate("MainWindow", u"Export Project", None))
        self.actionEnglish.setText(QCoreApplication.translate("MainWindow", u"English", None))
        self.actionGerman.setText(QCoreApplication.translate("MainWindow", u"German", None))
        self.actionCursorColor.setText(QCoreApplication.translate("MainWindow", u"Cursor Color...", None))
        self.calibrationProcessButton.setText("")
        self.uploadProcessButton.setText("")
        self.maskingProcessButton.setText("")
        self.skeletonProcessButton.setText("")
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
        self.calibrationGroupBox.setTitle(QCoreApplication.translate("MainWindow", u"Calibration", None))
        self.calibrationImageHintLabel.setText(QCoreApplication.translate("MainWindow", u"Select an image for calibration.", None))
        self.caliUploadButton.setText(QCoreApplication.translate("MainWindow", u"Browse", None))
        self.calibrationPointsLabel.setText(QCoreApplication.translate("MainWindow", u"Mark Calibration Points:", None))
        self.clickAddButton.setText("")
        self.clickDeleteButton.setText("")
        self.distanceLabel.setText(QCoreApplication.translate("MainWindow", u"Distance(mm)", None))
        self.pixelLabel.setText(QCoreApplication.translate("MainWindow", u"Pixel(px)", None))
        self.resolutionLabel.setText(QCoreApplication.translate("MainWindow", u"Resolution(mm/px)", None))
        self.confirmButton.setText(QCoreApplication.translate("MainWindow", u"Confirm", None))
        self.nextButton0.setText(QCoreApplication.translate("MainWindow", u"Next Stage", None))
        self.uploadGroupBox.setTitle(QCoreApplication.translate("MainWindow", u"Upload Images", None))
        self.uploadHintPrefixLabel.setText(QCoreApplication.translate("MainWindow", u"Click", None))
        self.plusButton.setText("")
        self.uploadHintSuffixLabel.setText(QCoreApplication.translate("MainWindow", u" to upload figures.", None))
        self.previousButton1.setText(QCoreApplication.translate("MainWindow", u"Previous Stage", None))
        self.nextButton1.setText(QCoreApplication.translate("MainWindow", u"Next Stage", None))
        self.maskingGroupBox.setTitle(QCoreApplication.translate("MainWindow", u"Masking", None))
        self.modelHintLabel.setText(QCoreApplication.translate("MainWindow", u"Select a Model to do crack detection.", None))
        self.modelLabel.setText(QCoreApplication.translate("MainWindow", u"Model", None))
        self.modelComboBox.setItemText(0, QCoreApplication.translate("MainWindow", u"Concrete Crack Segmentation", None))
        self.modelComboBox.setItemText(1, QCoreApplication.translate("MainWindow", u"None", None))

        self.applyModelLabel.setText(QCoreApplication.translate("MainWindow", u"Apply model:", None))
        self.applyModelButton.setText(QCoreApplication.translate("MainWindow", u"This Image", None))
        self.applyModelAllButton.setText(QCoreApplication.translate("MainWindow", u"All Images", None))
        self.clearMaskLabel.setText(QCoreApplication.translate("MainWindow", u"Clear mask:", None))
        self.clearMaskButton.setText(QCoreApplication.translate("MainWindow", u"This Image", None))
        self.clearMaskAllButton.setText(QCoreApplication.translate("MainWindow", u"All Images", None))
        self.editingToolsGroupBox.setTitle(QCoreApplication.translate("MainWindow", u"Editing Tools", None))
        self.addButton.setText(QCoreApplication.translate("MainWindow", u"Add", None))
        self.deleteButton.setText(QCoreApplication.translate("MainWindow", u"Delete", None))
        self.penSizeLabel.setText(QCoreApplication.translate("MainWindow", u"Size", None))
        self.penShapeLabel.setText(QCoreApplication.translate("MainWindow", u"Shape", None))
        self.penShapeComboBox.setItemText(0, QCoreApplication.translate("MainWindow", u"Round", None))
        self.penShapeComboBox.setItemText(1, QCoreApplication.translate("MainWindow", u"Square", None))

        self.opacityLabel.setText(QCoreApplication.translate("MainWindow", u"Opacity:", None))
        self.labelOriginal.setText(QCoreApplication.translate("MainWindow", u"Original", None))
        self.labelMask.setText(QCoreApplication.translate("MainWindow", u"Mask", None))
        self.removePatchesLabel.setText(QCoreApplication.translate("MainWindow", u"Remove patches smaller than (px):", None))
#if QT_CONFIG(tooltip)
        self.patchAreaSpinBox.setToolTip(QCoreApplication.translate("MainWindow", u"Disconnected mask regions smaller than this area are removed.", None))
#endif // QT_CONFIG(tooltip)
        self.removePatchesButton.setText(QCoreApplication.translate("MainWindow", u"This Image", None))
        self.removePatchesAllButton.setText(QCoreApplication.translate("MainWindow", u"All Images", None))
        self.previousButton2.setText(QCoreApplication.translate("MainWindow", u"Previous Stage", None))
        self.nextButton2.setText(QCoreApplication.translate("MainWindow", u"Next Stage", None))
        self.skeletonizationGroupBox.setTitle(QCoreApplication.translate("MainWindow", u"Skeletonization", None))
        self.skeletonHintLabel.setText(QCoreApplication.translate("MainWindow", u"Extracting crack skeleton information.", None))
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
        self.skeletonEditLabel.setText(QCoreApplication.translate("MainWindow", u"Skeleton Edit:", None))
        self.nodeAddButton.setText("")
        self.nodeDeleteButton.setText("")
        self.hintsButton.setText(QCoreApplication.translate("MainWindow", u"Hints:", None))
        self.addNodeHintLabel.setText(QCoreApplication.translate("MainWindow", u"Left-click to add and connect nodes.", None))
        self.newSegmentHintLabel.setText(QCoreApplication.translate("MainWindow", u"Right-click to start a new segment.", None))
        self.deleteNodeHintLabel.setText(QCoreApplication.translate("MainWindow", u"Click a node or a line to delete it.", None))
        self.previousButton3.setText(QCoreApplication.translate("MainWindow", u"Previous Stage", None))
        self.nextButton3.setText(QCoreApplication.translate("MainWindow", u"Next Stage", None))
        self.resultsGroupBox.setTitle(QCoreApplication.translate("MainWindow", u"Calculation Results", None))
        self.fileNameCaptionLabel.setText(QCoreApplication.translate("MainWindow", u"File Name:", None))
        self.fileNameLabel.setText("")
        self.crackAreaCaptionLabel.setText(QCoreApplication.translate("MainWindow", u"Crack Area:", None))
        self.crackAreaLabel.setText("")
        self.skeletonLengthCaptionLabel.setText(QCoreApplication.translate("MainWindow", u"Skeleton Length:", None))
        self.skeletonLengthLabel.setText("")
        self.crackWidthCaptionLabel.setText(QCoreApplication.translate("MainWindow", u"Mean Crack Width:", None))
        self.crackWidthLabel.setText("")
        self.exportSettingsGroupBox.setTitle(QCoreApplication.translate("MainWindow", u"Export Settings", None))
        self.exportButton.setText(QCoreApplication.translate("MainWindow", u"Export", None))
        self.previousButton4.setText(QCoreApplication.translate("MainWindow", u"Previous Stage", None))
        self.nextButton4.setText(QCoreApplication.translate("MainWindow", u"Finish", None))
        self.previousFigButton.setText("")
        self.nextFigButton.setText("")
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.menuHelp.setTitle(QCoreApplication.translate("MainWindow", u"Help", None))
        self.menuSetting.setTitle(QCoreApplication.translate("MainWindow", u"Setting", None))
        self.menuLanguage.setTitle(QCoreApplication.translate("MainWindow", u"Language", None))
    # retranslateUi

