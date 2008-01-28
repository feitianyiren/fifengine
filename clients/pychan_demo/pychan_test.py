#!/usr/bin/env python
# coding: utf-8

import sys, os, re

def _jp(path):
	return os.path.sep.join(path.split('/'))

_paths = ('../../engine/swigwrappers/python', '../../engine/extensions')
for p in _paths:
	if p not in sys.path:
		sys.path.append(_jp(p))

import fife
import fifelog
import basicapplication
import pychan

class PyChanExample(object):
	def __init__(self,xmlFile):
		self.xmlFile = xmlFile
		self.widget = None
	
	def start(self):
		self.widget = pychan.loadXML(self.xmlFile)
		eventMap = {
			'closeButton':self.stop,
			'okButton'   :self.stop
		}
		self.widget.mapEvents(eventMap, ignoreMissing = True)
		self.widget.show()

	def stop(self):
		if self.widget:
			self.widget.hide()
		self.widget = None

class DemoApplication(basicapplication.ApplicationBase):
	def __init__(self):
		super(DemoApplication,self).__init__()
		
		pychan.init(self.engine,debug=True)
		pychan.setupModalExecution(self.mainLoop,self.breakFromMainLoop)
		
		self.gui = pychan.loadXML('content/gui/demoapp.xml')
		
		eventMap = {
			'creditsLink'  : self.showCredits,
			'closeButton'  : self.quit,
			'selectButton' : self.selectExample
		}
		self.gui.mapEvents(eventMap)

		from mapwidgets import MapProperties
		from styling import StylingExample
		
		self.examples = {
			'Load Map' : PyChanExample('content/gui/loadmap.xml'),
			'Map Properties' : MapProperties(),
			'Absolute Positioning' : PyChanExample('content/gui/absolute.xml'),
			'Basic Styling' : StylingExample(),
			'All Widgets' : PyChanExample('content/gui/all_widgets.xml')
		}
		self.demoList = self.gui.findChild(name='demoList')
		self.demoList.items += self.examples.keys()
		self.gui.show()
		
		self.currentExample = None
		self.creditsWidget = None

	def selectExample(self):
		if self.demoList.selected_item is None: return
		print "selected",self.demoList.selected_item
		if self.currentExample: self.currentExample.stop()
		self.currentExample = self.examples[self.demoList.selected_item]
		self.gui.findChild(name="xmlSource").text = open(self.currentExample.xmlFile).read()
		self.currentExample.start()

	def showCredits(self):
		print pychan.loadXML('content/gui/credits.xml').execute({ 'okButton' : "Yay!" })

class TestXMLApplication(basicapplication.ApplicationBase):
	"""
	Test Application. Run the pychan_test.py file
	with the XML file you want to load as argument.
	"""
	def __init__(self,xmlfile):
		super(TestXMLApplication,self).__init__()
		pychan.init(self.engine,debug=True)
		self.widget = pychan.loadXML(xmlfile)
		self.widget.show()

if __name__ == '__main__':
	import sys
	if len(sys.argv) == 2:
		app = TestXMLApplication(sys.argv[1])
	else:
		app = DemoApplication()
	app.run()