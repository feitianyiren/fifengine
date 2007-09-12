# coding: utf-8
import fife, re

__doc__ = """\
Pythonize FIFE

Import this extension to get a more
pythonic interface to FIFE.

Currently it implements the following
conveniences:

* FIFE Exceptions print their message.
* Automatic property generation for:
  * fife.Engine
  * fife.Instance
  * fife.Image
  * fife.Animation
  * fife.Point
  * fife.Rect

"""

__all__ = ()

fife.Exception.__str__ = fife.Exception.getMessage
def _Color2Str(c):
	return 'Color(%s)' % ','.join(map(str,(c.r,c.g,c.b,c.a)))
fife.Color.__str__ = _Color2Str

classes = [ fife.Engine, fife.Instance, fife.Point, fife.Rect, fife.Image, fife.Animation,
 fife.RenderBackend, fife.IEvent, fife.Command, fife.Container ]

def createProperties():
	""" Autocreate properties for getXYZ/setXYZ functions.
	"""
	try:
		import inspect
		getargspec = inspect.getargspec
	except ImportError:
		print "Pythonize: inspect not available - properties are generated with dummy argspec."
		getargspec = lambda func : ([],'args',None,None)

	def isSimpleGetter(func):
		if not callable(func):
			return False
		try:
			argspec = getargspec(func)
			return not (argspec[0] or any(argspec[2:]))
		except TypeError, e:
			#print func, e
			return False
	
	def createNames(name):
		for prefix in ('get', 'is', 'are'):
			if name.startswith(prefix):
				new_name = name[len(prefix):]
				break
		settername   = 'set' + new_name
		propertyname = new_name[0].lower() + new_name[1:]
		return settername, propertyname
		
	getter = re.compile(r"^(get|are|is)[A-Z]")
	for class_ in classes:
		methods = [(name,attr) for name,attr in class_.__dict__.items()
		                       if isSimpleGetter(attr) ]
		setmethods = [(name,attr) for name,attr in class_.__dict__.items() if callable(attr)]
		getters = []
		for name,method in methods:
			if getter.match(name):
				getters.append((name,method))
				settername, propertyname = createNames(name)
				setter = dict(setmethods).get(settername,None)
				#print name, settername, "--->",propertyname,'(',method,',',setter,')'
				setattr(class_,propertyname,property(method,setter))
		if not getters: continue
		
		# We need to override the swig setattr function
		# to get properties to work.
		class_._property_names = set([name for name,method in getters])
		def _setattr_wrapper_(self,*args):
			if name in class_._property_names:
				object.__setattr__(self,*args)
			else:
				class_.__setattr__(self,*args)
		class_.__setattr__ = _setattr_wrapper_

createProperties()