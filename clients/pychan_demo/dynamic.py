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
import settings

import pychan

from pychan_test import PyChanExample

class DynamicExample(PyChanExample):
	def __init__(self):
		super(DynamicExample,self).__init__('content/gui/dynamic.xml')
		
	def start(self):
		self.widget = pychan.loadXML(self.xmlFile)
		self.widget.mapEvents({
			'okButton'   :self.stop,
			'addButton'  :self.addLabel,
		})
		self.labelBox = self.widget.findChild(name="labelBox")
		self.widget.show()

	def addLabel(self):
		label = pychan.widgets.ClickLabel()
		label.text = self.widget.collectData('labelText')
		label.capture(self.removeLabel)
		self.labelBox.addChild( label )
		self.widget.adaptLayout()
		
	def removeLabel(self,widget=None):
		widget._parent.removeChild(widget)
		self.widget.adaptLayout()
