# -*- coding: utf-8 -*-

#
#
# Created: Thu Sep 20 2018
#      by: pyside-uic 0.2.15 running on PySide 1.2.4


from PySide import QtCore, QtGui
from PIL import ImageGrab
import sfmApp ,sfmClipEditor,math


#used to add an event system to sampling the same layout could
#be used to add other events to sfm 
class SfmSample(QtCore.QObject):
    

    SamplingDone = QtCore.Signal() #conncent to this signal to know when sampling is done
    Timer=QtCore.QElapsedTimer()  #used to time how long each frame Sampling takes
    def __init__(self):
       
        QtCore.QObject.__init__(self)
        self.StatusBar= self.findtypeinlist(sfmApp.GetMainWindow(),QtGui.QStatusBar) #gets the QStatusBar that holds the current sample
        self.StopChecking=False     
        self.PrevSample=0

	#returns a object of type from the children of a qwidget
    def findtypeinlist(self,widget,typ,flag=False): 
    
	for i in widget.children():
	    if type(i) is typ and i != flag:
		    return i    
	

	#this will start an infinite loop that keeps checking if the sampling is every so millisec
    def BeginChecking(self):
        
        if (self.StopChecking):
            self.StopChecking=False             
            return
	
        currentsample=(int)(self.StatusBar.children()[0].children()[-2].text().split(" ")[0])#gets the current sample number, 1 means done
        
        if(self.PrevSample ==1 and currentsample>1):#this is a new frame, start timer 
            self.Timer.start()
        
        
        if(currentsample==1 and self.PrevSample > 1):#sampling done

            print("Frame #"+(str)(sfmApp.GetHeadTimeInFrames())+" "+str(self.Timer.restart()/1000.0))#prints the frame time in sec
            self.SamplingDone.emit()

        
        
        
        self.PrevSample=currentsample
	
	
        #recalls the function after 200 millisecs lowering the time  will increase accuracy but will cause bottlenecks for the cpu resulting in longer sample times, 1000 millisecs = 1 sec
        QtCore.QTimer.singleShot(200, lambda: self.BeginChecking())








class Ui_RenderWindow(QtGui.QWidget):
    def __init__(self,obj,ref):
        super(Ui_RenderWindow, self).__init__()        
        self.Renderwin=obj
        self.MainDialogRef=ref
        self.setupUi(self.Renderwin)   
        self.Renderwin.show()
        self.Renderwin.move(100,100)
        self.Renderwin.closeEvent = self.closeEvent
	
        self.Sample=SfmSample()        
        self.Sample.SamplingDone.connect(self.StartRendering)
        self.Sample.BeginChecking() 
    
    def closeEvent(self, event):
        # do stuff        
        if True:
            self.Sample.StopChecking=True            
            event.accept() # let the window close   
	    self.MainDialogRef.deleteLater()
            self.Renderwin.deleteLater()

        else:
            event.ignore()    
        
    
    #this gets called each time sampling is done
    def StartRendering(self):
        
        

	
        self.MainDialogRef.ExportImage()
        self.RenderPreview.setPixmap(QtGui.QPixmap(self.MainDialogRef.filename))     

	
	precent= math.ceil((float(sfmApp.GetHeadTimeInFrames()- self.MainDialogRef.StartFrame_spinBox.value())  /  (self.MainDialogRef.EndFrame_spinBox.value()-self.MainDialogRef.StartFrame_spinBox.value()))*100)
	
        self.progressBar.setValue ( precent)
        sfmApp.SetHeadTimeInFrames(sfmApp.GetHeadTimeInFrames()+1)
        
	if (sfmApp.GetHeadTimeInFrames()>=self.MainDialogRef.EndFrame_spinBox.value()): #did we reach the last frame
	    self.Sample.StopChecking=True
	    self.Renderwin.close()
	    self.close()
	    return
	
    
    
    
    
    
    
    
    
    def setupUi(self, RenderWindow):
        RenderWindow.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        RenderWindow.setWindowModality(QtCore.Qt.ApplicationModal)
        RenderWindow.resize(640, 480)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(RenderWindow.sizePolicy().hasHeightForWidth())
        RenderWindow.setSizePolicy(sizePolicy)
        RenderWindow.setMinimumSize(QtCore.QSize(640, 480))
        RenderWindow.setMaximumSize(QtCore.QSize(1298, 823))
        self.verticalLayout = QtGui.QVBoxLayout(RenderWindow)
        self.verticalLayout.setSizeConstraint(QtGui.QLayout.SetFixedSize)
        self.verticalLayout.setObjectName("verticalLayout")
        self.RenderPreview = QtGui.QLabel(RenderWindow)
        self.RenderPreview.setFrameShape(QtGui.QFrame.Panel)
        self.RenderPreview.setFrameShadow(QtGui.QFrame.Plain)
        self.RenderPreview.setLineWidth(2)
        self.RenderPreview.setText("")
        self.RenderPreview.setPixmap(QtGui.QPixmap( QtCore.QDir.currentPath()+"/platform/tools/images/sfm/sfm_screencast_default.png"))
        self.RenderPreview.setScaledContents(True)
        self.RenderPreview.setWordWrap(False)
        self.RenderPreview.setObjectName("RenderPreview")
        self.verticalLayout.addWidget(self.RenderPreview)
        self.progressBar = QtGui.QProgressBar(RenderWindow)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setTextVisible(True)
        self.progressBar.setOrientation(QtCore.Qt.Horizontal)
        self.progressBar.setInvertedAppearance(False)
        self.progressBar.setTextDirection(QtGui.QProgressBar.TopToBottom)
        self.progressBar.setObjectName("progressBar")
        self.verticalLayout.addWidget(self.progressBar)
        self.Pause_Button = QtGui.QPushButton(RenderWindow)
        self.Pause_Button.setObjectName("Pause_Button")
        self.verticalLayout.addWidget(self.Pause_Button)
        self.Cancel_Button = QtGui.QPushButton(RenderWindow)
        self.Cancel_Button.setObjectName("Cancel_Button")
        self.verticalLayout.addWidget(self.Cancel_Button)

        self.retranslateUi(RenderWindow)
        QtCore.QObject.connect(self.Cancel_Button, QtCore.SIGNAL("clicked()"), RenderWindow.close)
        QtCore.QMetaObject.connectSlotsByName(RenderWindow)

    def retranslateUi(self, RenderWindow):
        RenderWindow.setWindowTitle(QtGui.QApplication.translate("RenderWindow", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.Pause_Button.setText(QtGui.QApplication.translate("RenderWindow", "Pause", None, QtGui.QApplication.UnicodeUTF8))
        self.Cancel_Button.setText(QtGui.QApplication.translate("RenderWindow", "Cancel", None, QtGui.QApplication.UnicodeUTF8))








class Ui_MainDialog(QtGui.QWidget):
    
    def __init__(self):
        super(Ui_MainDialog, self).__init__()        
       
        self.setupUi(self)
        self.show()
        
        self.filename=""
        
        
     #sets up the render window
    def RenderMovie(self):
        
        sfmApp.SetHeadTimeInFrames(self.StartFrame_spinBox.value())
        self.RenderWindow = QtGui.QWidget()
        Ui_RenderWindow(self.RenderWindow,self)
        self.close()
        
        
        
        
        
 
     
        
        
    def ExportImage(self):
        
        sfm.console("sfm_export_image_to_clipboard")
        
        im = ImageGrab.grabclipboard()#grab the img from clipboard
        
        self.filename=QtCore.QFileInfo(self.OutputPath_lineEdit.text()).path()+"/"+self.GetBaseFileName()+"_"+str(sfmApp.GetHeadTimeInFrames())+self.Format_comboBox.currentText()
    
        im.save(self.filename) #saves file with frame#         
        
    def closeEvent(self, event):
        # do stuff
        
        if True:            
            event.accept() # let the window close     
           # self.deleteLater()
        else:
            event.ignore()    
            
    def GetBaseFileName(self):
        return QtCore.QFileInfo(self.OutputPath_lineEdit.text()).baseName()
        
        
        
    def GetPath(self):
        self.filename ,filt= QtGui.QFileDialog.getSaveFileName(self, "Find Files", self.OutputPath_lineEdit.text())

        if self.filename:
            self.OutputPath_lineEdit.setText(self.filename)
           
            
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
        self.Export_Button.clicked.connect(self.RenderMovie)
        
        
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



    





Ui_MainDialog()

