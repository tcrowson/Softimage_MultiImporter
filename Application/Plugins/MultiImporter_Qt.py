"""
APPLICATION:    MultiImporter_Qt
VERSION:        1.15
DATE:           September 7, 2012
AUTHOR:         Tim Crowson
DESCRIPTION:    Scans a directory for various types of 3D file formats, and lets you import selected items.

*** Shout-outs: Steve Caron, Jo Benayoun, Ana Gomez, Luc-Eric Rousseau ***

NOTES:
- The FBX import options here are admittedly sparse. My intention is offer as many options as possible
    but there are discrepancies between the Softimage UI, the commands as described in the SDK, and between Crosswalk versions.
    For now, only the Scale Unit option is supported until I get this all sorted out.
    And in typical FBX fashion, I'm not even sure that's working right! FBX... sheesh...
"""

import os
import sys
import re
from win32com.client import constants
 
import sip
from PyQt4 import uic
from PyQt4 import QtGui
from PyQt4 import QtCore
from PyQt4.QtGui import QDialog
from PyQt4.QtGui import QWidget
from PyQt4.QtGui import QApplication
from PyQt4.QtGui import QFileDialog

__version__ = 1.15



class MultiImporterDialog( QDialog ):
    def __init__( self, uifilepath, parent ):
        QDialog.__init__(self, parent)
        QApplication.setStyle(QtGui.QStyleFactory.create('Plastique'))
        self.ui = uic.loadUi( uifilepath, self)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose) # Ensures that the app is deleted when closed.
        self.setConnections()
        self.init_UI()
        
    def setConnections(self):
        self.ui.fileBrowse_Btn.released.connect(self.launchFileBrowser)
        self.ui.directoryPath.editingFinished.connect(self.scanDirectory)
        self.ui.import_Btn.released.connect(self.importFiles)
        self.ui.lwoScaleFactorSlider.valueChanged.connect(self.setLWOScaleField)
        self.ui.fbxAutoScaleCheck.stateChanged.connect(self.setFBXScaleUnitDisplay)
        self.ui.about_Btn.clicked.connect(self.showAbout)
        
    def init_UI(self):
        self.setFBXScaleUnitDisplay()
        self.lwoScaleFactorField.setValidator(QtGui.QIntValidator(self))
        
    def launchFileBrowser(self):
        # suspend control hooks so our filedialog looks normal
        desktop = Application.Desktop
        desktop.SuspendWin32ControlsHook()

        # call the filedialog
        self.fileDialog = QFileDialog(self)
        sourceDir = self.fileDialog.getExistingDirectory(None,'Choose a directory', Application.ActiveProject2.Path)

        # restore control hooks
        desktop.RestoreWin32ControlsHook()

        # do stuff
        self.fileList.clear()
        self.directoryPath.setText(sourceDir)
        self.scanDirectory()

    def scanDirectory(self):
        self.fileList.clear()
        formatPattern = re.compile('emdl|obj|lwo|fbx', re.IGNORECASE)
        sourceDir = self.directoryPath.text()
        if os.path.exists(sourceDir):
            for item in os.listdir(sourceDir):
                ext = os.path.splitext(item)[1]
                if formatPattern.match(ext[1:]):
                    self.fileList.addItem(item)
                
    def importFiles(self):
        for item in self.fileList.selectedItems():
            importPath = os.path.join(str(self.directoryPath.text()),str(item.text())) # Is there a Qt version of os.path.join()?
    
            if item.text().endsWith('emdl'):
                if self.emdlTypeChoice.currentText() == 'Local':
                    Application.ImportModel(importPath, "", "", "", "", "", "")                     
                elif self.emdlTypeChoice.currentText() == 'Referenced':
                    Application.SICreateRefModel(importPath, "", "", "", "", "", "", "")

            elif item.text().endsWith('obj'):
                Application.ObjImport(importPath,
                                      self.objGroupingChoice.currentIndex(),
                                      self.objHierarchyChoice.currentIndex(),
                                      self.objMaterialsCheck.isChecked(),
                                      self.objUVsCheck.isChecked(),
                                      self.objUserNormalsCheck.isChecked(),
                                      self.objUVwrappingCheck.isChecked())

            elif item.text().endsWith('lwo'):
                Application.PO_XSI_ImportLWO(importPath,
                                             self.lwoMorphsCheck.isChecked(),
                                             self.lwoMorphsToMixerCheck.isChecked(),
                                             self.lwoUVsCheck.isChecked(),
                                             self.lwoSurfacesCheck.isChecked(),
                                             self.lwoWeightsCheck.isChecked(),
                                             int(self.lwoScaleFactorField.text()))

            elif item.text().endsWith('fbx'):
                ''' There are many options that can be set on the FBX importer.
                But there are too many discrepancies between the default FBX import UI
                and the commands described in the SDK to know exactly how to present these to the user.
                Input welcome!'''
                if self.fbxAutoScaleCheck.isChecked():
                    Application.FBXImportAutomaticUnit(True)
                else:
                    Application.FBXImportUnit(str(self.fbxScaleUnitChoice.currentText()))
                Application.FBXImport(importPath,'')

    def setLWOScaleField(self):
        self.lwoScaleFactorField.setText(str(self.lwoScaleFactorSlider.value()))
        
    def setFBXScaleUnitDisplay(self):
        ''' Since I haven't yet learned how to make the disabled state of a QComboBox look less ugly,
            this is a cheap way to make it *look* like it's disabled. It is not technically disabled,
            but the code ignores it unless the Automatic check is off. Sloppy, but it works.
        '''
        if not self.fbxAutoScaleCheck.isChecked():
            self.fbxScaleUnitChoice.setStyleSheet('QComboBox{color: #b2b2b2;}\nQComboBox QAbstractItemView {color: #b2b2b2;}')
        else:
            self.fbxScaleUnitChoice.setStyleSheet('QComboBox{color: #4D4D4D;}\nQComboBox QAbstractItemView {color: #4D4D4D;}')
        
    def showAbout(self):
        box = QtGui.QMessageBox(self)
        box.setWindowTitle('About MultiImporter_Qt')
        box.setText('<html><i> Automates the importing of multiple 3D files of differing file types. Navigate to a directory or paste one into the field to scan its contents. <br/><br/>version: %s<br/>September 7, 2012 <a href="http://www.dynamiclens.com" style="color: #A1BDC7">Tim Crowson</a><br/><br/>Python 2.7.3  |   PyQt 4.9.1  |  QtDesigner  |  PyQtForSoftimage <br/></i><html>'%__version__)
        box.setStyleSheet('QPushButton{height: 20px; width: 50px}')
        box.show()
        
    def log(self, text):
        Application.LogMessage(text)
        
        
def XSILoadPlugin( in_reg ):
    in_reg.Name = 'MultiImporter_Qt'
    in_reg.Author = 'Tim Crowson'
    in_reg.Email = 'tcrowson@gmail.com'
    in_reg.Major = 1
    in_reg.Minor = 15
    in_reg.RegisterCommand('MultiImporter_Qt')
    in_reg.RegisterMenu(constants.siMenuMainFileImportID,"MultiImporter_Qt_Menu",False,False)

def MultiImporter_Qt_Menu_Init( in_ctxt ):
	oMenu = in_ctxt.Source
	oMenu.AddCommandItem("MultiImporter (Qt)","MultiImporter_Qt")
	return True

def MultiImporter_Qt_Execute():  
    uifilepath = os.path.join(Application.Plugins( 'MultiImporter_Qt' ).OriginPath , 'MultiImporter.ui')
    
    sianchor = Application.getQtSoftimageAnchor()
    sianchor = sip.wrapinstance( long(sianchor), QWidget )
    
    for child in sianchor.children(): # Prevent multiple instances.
        if isinstance(child, MultiImporterDialog ):
            return
    dialog = MultiImporterDialog(uifilepath, sianchor)  
    dialog.show()




