# -*- coding: utf-8 -*-

#
#
# Created: Thu Sep 20 19:35:30 2018
#      by: pyside-uic 0.2.15 running on PySide 1.2.4


from PySide import QtCore, QtGui
from PIL import ImageGrab
import sfmApp ,sfmClipEditor



class SfmSample(QtCore.QObject):
    
    SamplingDone = QtCore.Signal()
    FrameTime=0
    Timer=QtCore.QElapsedTimer()
    def __init__(self):
       
        QtCore.QObject.__init__(self)

    PrevSample=0
    def BeginChecking(self):
        
        if (sfmApp.GetHeadTimeInFrames()==10): return
        currentsample=(int)(bar.children()[0].children()[-2].text().split(" ")[0])
        
        if(self.PrevSample ==1 and currentsample>1):
            self.Timer.start()
        
        
        if(currentsample==1 and self.PrevSample > 1):
            #print(currentsample,self.PrevSample ) 
            print(self.Timer.restart()/1000.0)
            self.SamplingDone.emit()
           # DebugPrint()
            #return
        
        
        
        
        self.PrevSample=currentsample
        
        QtCore.QTimer.singleShot(30, lambda: self.BeginChecking())















class Ui_MainDialog(QtGui.QWidget):
    
    def __init__(self):
        super(Ui_MainDialog, self).__init__()        
       
        self.setupUi(self)
        
        
        
        
        
        
    def RenderImage(self):
        
        im = ImageGrab.grabclipboard()
        
        filename=QtCore.QFileInfo(self.OutputPath_lineEdit.text()).path()+"/"+self.GetBaseFileName()+"_"+str(sfmApp.GetHeadTimeInFrames())+self.Format_comboBox.currentText()
       # print filename
        im.save(filename)          
        
    def closeEvent(self, event):
        # do stuff
        
        if True:            
            event.accept() # let the window close                       
        else:
            event.ignore()    
            
    def GetBaseFileName(self):
        return QtCore.QFileInfo(self.OutputPath_lineEdit.text()).baseName()
        
        
        
    def GetPath(self):
        self.filename ,filt= QtGui.QFileDialog.getSaveFileName(self, "Find Files", self.OutputPath_lineEdit.text())

        if self.filename:
            self.OutputPath_lineEdit.setText(self.filename)
            print(self.RenderImage())
            
    def FrameCheck(self):          
        
        
        if(self.Length_comboBox.currentIndex()==0):
            self.StartFrame_spinBox.setEnabled(False)
            self.StartFrame_spinBox.setValue(sfmApp.GetMovie().GetStartTime().CurrentFrame(vs.DmeFramerate_t(sfmApp.GetFramesPerSecond())))
            self.EndFrame_spinBox.setEnabled(False)
            self.EndFrame_spinBox.setValue(sfmApp.GetMovie().GetEndTime().CurrentFrame(vs.DmeFramerate_t(sfmApp.GetFramesPerSecond())))
            
        elif(self.Length_comboBox.currentIndex()==1):
            self.StartFrame_spinBox.setEnabled(False)
            
            self.StartFrame_spinBox.setValue(sfmClipEditor.GetSelectedShots()[0].GetStartTime().CurrentFrame(vs.DmeFramerate_t(sfmApp.GetFramesPerSecond())))
            
            self.EndFrame_spinBox.setEnabled(False)
            self.EndFrame_spinBox.setValue(sfmClipEditor.GetSelectedShots()[-1].GetEndTime().CurrentFrame(vs.DmeFramerate_t(sfmApp.GetFramesPerSecond())))
        
        elif(self.Length_comboBox.currentIndex()==2):
            self.StartFrame_spinBox.setEnabled(True)
            self.EndFrame_spinBox.setEnabled(True)
        
        
        
        
        
    def setupUi(self, MainDialog):
        MainDialog.setObjectName("MainDialog")
        MainDialog.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        MainDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        MainDialog.setEnabled(True)
        MainDialog.resize(614, 240)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainDialog.sizePolicy().hasHeightForWidth())
        MainDialog.setSizePolicy(sizePolicy)
        MainDialog.setMinimumSize(QtCore.QSize(614, 240))
        MainDialog.setMaximumSize(QtCore.QSize(614, 240))
        self.verticalLayout = QtGui.QVBoxLayout(MainDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setSpacing(5)
        self.horizontalLayout.setSizeConstraint(QtGui.QLayout.SetDefaultConstraint)
        self.horizontalLayout.setContentsMargins(20, -1, 10, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtGui.QLabel(MainDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setMinimumSize(QtCore.QSize(59, 59))
        self.label.setMaximumSize(QtCore.QSize(90, 59))
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.OutputPath_lineEdit = QtGui.QLineEdit(MainDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.OutputPath_lineEdit.sizePolicy().hasHeightForWidth())
        self.OutputPath_lineEdit.setSizePolicy(sizePolicy)
        self.OutputPath_lineEdit.setMinimumSize(QtCore.QSize(440, 20))
        self.OutputPath_lineEdit.setMaximumSize(QtCore.QSize(431, 20))
        self.OutputPath_lineEdit.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.OutputPath_lineEdit.setFrame(True)
        self.OutputPath_lineEdit.setEchoMode(QtGui.QLineEdit.Normal)
        self.OutputPath_lineEdit.setObjectName("OutputPath_lineEdit")
        self.OutputPath_lineEdit.setText(str(sfmApp.GetDocumentRoot().settings.movieSettings.filename))
        
        self.horizontalLayout.addWidget(self.OutputPath_lineEdit)
        self.GetPath_toolButton = QtGui.QToolButton(MainDialog)
        self.GetPath_toolButton.clicked.connect(self.GetPath)
        self.GetPath_toolButton.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.GetPath_toolButton.setObjectName("GetPath_toolButton")
        self.horizontalLayout.addWidget(self.GetPath_toolButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.line_2 = QtGui.QFrame(MainDialog)
        self.line_2.setFrameShape(QtGui.QFrame.HLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.verticalLayout.addWidget(self.line_2)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setSpacing(3)
        self.horizontalLayout_4.setSizeConstraint(QtGui.QLayout.SetDefaultConstraint)
        self.horizontalLayout_4.setContentsMargins(20, -1, 380, -1)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_3 = QtGui.QLabel(MainDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        self.label_3.setMinimumSize(QtCore.QSize(60, 40))
        self.label_3.setMaximumSize(QtCore.QSize(90, 40))
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_4.addWidget(self.label_3)
        self.Format_comboBox = QtGui.QComboBox(MainDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Format_comboBox.sizePolicy().hasHeightForWidth())
        self.Format_comboBox.setSizePolicy(sizePolicy)
        self.Format_comboBox.setMaximumSize(QtCore.QSize(100, 16777215))
        self.Format_comboBox.setInsertPolicy(QtGui.QComboBox.NoInsert)
        self.Format_comboBox.setSizeAdjustPolicy(QtGui.QComboBox.AdjustToContentsOnFirstShow)
        self.Format_comboBox.setMinimumContentsLength(10)
        self.Format_comboBox.setObjectName("Format_comboBox")
        self.Format_comboBox.addItem("")
        self.Format_comboBox.addItem("")
        self.Format_comboBox.addItem("")
        self.horizontalLayout_4.addWidget(self.Format_comboBox)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setSpacing(6)
        self.horizontalLayout_3.setSizeConstraint(QtGui.QLayout.SetDefaultConstraint)
        self.horizontalLayout_3.setContentsMargins(20, 0, 246, 0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_2 = QtGui.QLabel(MainDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setMinimumSize(QtCore.QSize(85, 39))
        self.label_2.setMaximumSize(QtCore.QSize(85, 39))
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_3.addWidget(self.label_2)
        self.Length_comboBox = QtGui.QComboBox(MainDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Length_comboBox.sizePolicy().hasHeightForWidth())
        self.Length_comboBox.setSizePolicy(sizePolicy)
        self.Length_comboBox.setMinimumSize(QtCore.QSize(81, 20))
        self.Length_comboBox.setMaximumSize(QtCore.QSize(100, 20))
        self.Length_comboBox.setInsertPolicy(QtGui.QComboBox.NoInsert)
        self.Length_comboBox.setSizeAdjustPolicy(QtGui.QComboBox.AdjustToMinimumContentsLength)
        self.Length_comboBox.setMinimumContentsLength(10)
        self.Length_comboBox.setObjectName("Length_comboBox")
        self.Length_comboBox.addItem("")
        self.Length_comboBox.addItem("")
        self.Length_comboBox.addItem("")
        
        self.Length_comboBox.currentIndexChanged.connect(lambda:self.FrameCheck())
        
        
        
        self.horizontalLayout_3.addWidget(self.Length_comboBox)
        self.StartFrame_spinBox = QtGui.QSpinBox(MainDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.StartFrame_spinBox.sizePolicy().hasHeightForWidth())
        self.StartFrame_spinBox.setSizePolicy(sizePolicy)
        self.StartFrame_spinBox.setButtonSymbols(QtGui.QAbstractSpinBox.NoButtons)
        self.StartFrame_spinBox.setAccelerated(True)
        self.StartFrame_spinBox.setMaximum(999999999)
        self.StartFrame_spinBox.setMinimum(-9999999)
        
        self.StartFrame_spinBox.setObjectName("StartFrame_spinBox")
        self.horizontalLayout_3.addWidget(self.StartFrame_spinBox)
        self.EndFrame_spinBox = QtGui.QSpinBox(MainDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.EndFrame_spinBox.sizePolicy().hasHeightForWidth())
        self.EndFrame_spinBox.setSizePolicy(sizePolicy)
        self.EndFrame_spinBox.setFrame(True)
        self.EndFrame_spinBox.setButtonSymbols(QtGui.QAbstractSpinBox.NoButtons)
        self.EndFrame_spinBox.setAccelerated(True)
        self.EndFrame_spinBox.setMaximum(999999999)
        self.EndFrame_spinBox.setMinimum(-9999999)
        
        self.EndFrame_spinBox.setObjectName("EndFrame_spinBox")
        self.horizontalLayout_3.addWidget(self.EndFrame_spinBox)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.line = QtGui.QFrame(MainDialog)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout.addWidget(self.line)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setContentsMargins(400, -1, -1, -1)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.Export_Button = QtGui.QPushButton(MainDialog)
        self.Export_Button.clicked.connect(self.RenderImage)
        
        
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Export_Button.sizePolicy().hasHeightForWidth())
        self.Export_Button.setSizePolicy(sizePolicy)
        self.Export_Button.setAutoDefault(False)
        self.Export_Button.setDefault(False)
        self.Export_Button.setFlat(False)
        self.Export_Button.setObjectName("Export_Button")
        self.horizontalLayout_2.addWidget(self.Export_Button)
        self.Exit_Button = QtGui.QPushButton(MainDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Exit_Button.sizePolicy().hasHeightForWidth())
        self.Exit_Button.setSizePolicy(sizePolicy)
        self.Exit_Button.setObjectName("Exit_Button")
        self.horizontalLayout_2.addWidget(self.Exit_Button)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.label.setBuddy(self.OutputPath_lineEdit)
        self.label_3.setBuddy(self.Format_comboBox)
        self.label_2.setBuddy(self.Length_comboBox)
        
        self.FrameCheck()
        self.retranslateUi(MainDialog)
        QtCore.QObject.connect(self.Exit_Button, QtCore.SIGNAL("clicked()"), MainDialog.close)
        QtCore.QMetaObject.connectSlotsByName(MainDialog)
        
        MainDialog.setTabOrder(self.GetPath_toolButton, self.Format_comboBox)
        MainDialog.setTabOrder(self.Format_comboBox, self.StartFrame_spinBox)
        MainDialog.setTabOrder(self.StartFrame_spinBox, self.EndFrame_spinBox)
        MainDialog.setTabOrder(self.EndFrame_spinBox, self.Export_Button)
        MainDialog.setTabOrder(self.Export_Button, self.Exit_Button)

    def retranslateUi(self, MainDialog):
        MainDialog.setWindowTitle(QtGui.QApplication.translate("MainDialog", "Image Render", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("MainDialog", "Output Path", None, QtGui.QApplication.UnicodeUTF8))
        self.GetPath_toolButton.setText(QtGui.QApplication.translate("MainDialog", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("MainDialog", "Format", None, QtGui.QApplication.UnicodeUTF8))
        self.Format_comboBox.setItemText(0, QtGui.QApplication.translate("MainDialog", ".PNG", None, QtGui.QApplication.UnicodeUTF8))
        self.Format_comboBox.setItemText(1, QtGui.QApplication.translate("MainDialog", ".TGA", None, QtGui.QApplication.UnicodeUTF8))
        self.Format_comboBox.setItemText(2, QtGui.QApplication.translate("MainDialog", ".JPG", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("MainDialog", "Duaration", None, QtGui.QApplication.UnicodeUTF8))
        self.Length_comboBox.setItemText(0, QtGui.QApplication.translate("MainDialog", "Sequence", None, QtGui.QApplication.UnicodeUTF8))
        self.Length_comboBox.setItemText(1, QtGui.QApplication.translate("MainDialog", "Selected Shots", None, QtGui.QApplication.UnicodeUTF8))
        self.Length_comboBox.setItemText(2, QtGui.QApplication.translate("MainDialog", "Custom", None, QtGui.QApplication.UnicodeUTF8))
        self.Export_Button.setText(QtGui.QApplication.translate("MainDialog", "Export Movie", None, QtGui.QApplication.UnicodeUTF8))
        self.Exit_Button.setText(QtGui.QApplication.translate("MainDialog", "Cancel", None, QtGui.QApplication.UnicodeUTF8))



    
if __name__ == "__main__":
    import sys




    MainDialog = Ui_MainDialog()
    MainDialog.show()
