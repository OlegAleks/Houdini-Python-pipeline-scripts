import hou, os, sys, glob, re
from sys import platform as _platform
import webbrowser

def openCurFolder():
	buttons = ("HIP", "geo", "3d-out","out","Materials","cancel")
	choice = hou.ui.displayMessage("OPEN FOLDER:", buttons, hou.severityType.Message, 0, len(buttons)-1)
	if(choice!=len(buttons)-1):
		st = hou.expandString("$HIP")
		pattern = re.compile("/3d/hip")
		dirname = ''
		if pattern.search(st):
			if(choice==1):
				st = pattern.split(st)[0] + "/3d/hip/geo"
				dirname = 'geo'
			if(choice==2): 
				st = pattern.split(st)[0] + "/3d-out"
				dirname = '3d-out'
			if(choice==3): 
				st = pattern.split(st)[0] + "/out"
				dirname = 'out'
			if(choice==4): 
				st = pattern.split(st)[0] + "/Materials"
				dirname = 'Materials'
			nSt = os.path.normpath(st)
			if os.path.isdir(nSt):
				if _platform == "linux" or _platform == "linux2":
					os.chdir(nSt)
					webbrowser.open(nSt)
				else:
					os.system("start "+ nSt)
			else:
				hou.ui.displayMessage('"' + dirname + '"' + " directory does not exist")
		else: hou.ui.displayMessage(" Scene is not saved")

def removeFiles():
	nodes = hou.selectedNodes()
	for node in nodes:
		tname = node.type().name()
		if(tname=="file" or tname=="filecache" or tname=="dopnet" or tname=="rop_geometry"):
			if(tname=="dopnet"):
				sf = re.compile("((?<=[._])\$SF(?=[1-9]?[._]))")
				path = node.parm("explicitcachename").unexpandedString()
				path = sf.sub("$F", path)
			else:
				if(tname=="rop_geometry"):
					path = node.parm("sopoutput").unexpandedString()
				else:
					path = node.parm("file").unexpandedString()
			test_path = os.sep.join([hou.expandString(os.path.dirname(path)), os.path.basename(path)])
			if os.path.isfile(test_path):
				os.remove(test_path)
			else:
			# test for expressions
				p = re.compile("`(.*?)`")
			# test if expression is inside of the path
				p2 = re.compile("(?<=.)?`.*?`(?=.?)")
			# list of expressions in the path
				ex_list = p.findall(path)
			# list of parts inbetween expressions
				parts = p2.split(path)
				# print "parts: ", parts
			# insure ex_list have at least one element
				ex_list.append('')
			# some parameter expressions like '$OS' depends on the node it evaluates on. For that reason we set current node
				hou.setPwd(node)
			# list with raw expressons
				eval_list = []
			# list with expanded expressions
				eval_list2 = []
				# print "ex_list: ", ex_list
				for i in ex_list:
					try: eval_list.append(hou.hscriptExpression(i))
					except: eval_list.append(i)
				# print "eval_list: ", eval_list
				path = ''.join(["{0}{1}".format(a_,b_) for a_, b_ in zip(parts, ex_list)])
				# print "path: "+path
				spl = os.path.split(path)
				# print "spl: ", spl
			# override 'path' with expanded expression from 'eval_list'
				path = ''.join(["{0}{1}".format(a_,b_) for a_, b_ in zip(parts, eval_list)])
				spl2 = os.path.split(path)
				# print "spl2: ", spl2
			# test for $F in path
				pattern = re.compile("((?<=[a-z0-9A-Z])[._](?=\$F))")
			# test for expanded frame number in path
				pattern2 = re.compile("((?<=[a-z0-9A-Z])[._](?=[0-9]))")
			# test for "padzero" expression in a sequence name
				pattern3 = re.compile("(?<=[a-z0-9A-Z])[._](?=padzero\()")
				padzero = pattern3.findall(spl[1])
			# extract base name of sequence
				# print "spl[1]: ",spl[1]
				if len(padzero)>0:
					name = pattern3.split(spl[1])[0]
				else:
					name = pattern.split(spl[1])[0]
				name = hou.expandString(name)
				# print "base name: "+name
			# expand directory and expanded name of sequence
				spl_0 = hou.expandString(spl[0])
				# print "folder: "+spl_0
				spl_1 = hou.expandString(spl[1])
				# print "file name: "+spl_1
				fileList = []
				for f in os.listdir(spl_0):
					v0 = pattern2.split(f)[0]
					v1 = pattern3.split(spl[1])[0]
					v2 = hou.expandString(pattern.split(spl[1])[0])
					# print "file", f, "\n\t", v0, " == ", name, " : ", v0==name
					# print "\t", v1, " == ", v0, " : ", v1 == v0
					# print "\t", v2, " == ", v0, " : ", v2 == v0
					if os.path.isfile(os.path.join(spl_0, f)) and v0==name and (v1==v0 or v2==v0):
						fileList.append(os.path.join(spl_0, f))
				for file in fileList:
					os.remove(file)
				# print "*****************\n"
def walk_and_set(rootNode, searchStr, replString, recursive):
	try:
		locked = rootNode.parent().isLocked()==1
	except:
		locked = 0
	# print "rootNode = ", rootNode.path()
	if(rootNode.path()=='/' or locked==0):
		for parm in rootNode.parms():
			not_lock_dis_hidden = parm.isLocked()==0 and parm.isDisabled()==0 and parm.isHidden()==0
			isExp = 1
			eX = ""
			# check for expressions
			try:
				eX = parm.expression()
			except:
				isExp = 0
			if isExp and not_lock_dis_hidden:
				newStr = eX.replace(searchStr, replString)
				print parm.path(), " isExp = 1", " newStr="+newStr
				if(newStr!=eX):
						parm.setExpression(newStr)			
						# print parm.path(), ': expression: ', newStr
			else:
				if isinstance(parm.parmTemplate(), hou.StringParmTemplate):
					# print "parm ", parm.path(), " keyframes=", len(parm.keyframes()), " not_lock_dis_hidden: ", not_lock_dis_hidden==True
					if len(parm.keyframes())==0 and not_lock_dis_hidden==True:
						realStr = parm.unexpandedString()
						newStr = realStr.replace(searchStr, replString)
						if(newStr!=realStr):
							parm.set(newStr)
							# print parm.path(), ': string: ', newStr
		if len(rootNode.children())>0 and recursive:
			for child in rootNode.children():
				walk_and_set(child, searchStr, replString, True)

def search_replace_str():
	nodes = hou.selectedNodes()	
	menu = hou.ui.readMultiInput("In Parameters", ("search for", "replace on"), buttons=('OK', "Cancel"), initial_contents = ('\\', '/'), close_choice = 1)
	if(menu[0]!=1):
		if len(nodes)==0:
			buttons = ("Ok","Cancel")
			choice = hou.ui.displayMessage("Apply for ALL nodes in scene:", buttons, hou.severityType.Message, 0, 1)
			if choice!=1:
				root = hou.node("/")
				# print "send walk_and_set("+menu[1][0]+","+menu[1][1]+")"
				walk_and_set(root, menu[1][0], menu[1][1], True)
		else:
			for root in nodes:
				# print "send walk_and_set("+menu[1][0]+","+menu[1][1]+") for node "+root.path()
				walk_and_set(root, menu[1][0], menu[1][1], False)

def points_from_objects():
	node = hou.selectedNodes()[0]
	obj = hou.node('/obj')
	pts = obj.createNode('geo', node_name = 'pts', run_init_scripts=False)
	w = pts.createNode('attribwrangle')
	w.parm('class').set(0)
	number = len(node.children())
	s = "int i = 0;\nwhile(i<" +str(number) +")\n{\n\tint pt = addpoint(geoself(), {0,0,0});\n\tsetpointattrib(geoself(), 'rotate', pt, {0,0,0}, 'set');\n\tsetpointattrib(geoself(), 'scale', pt, {1,1,1}, 'set');\n\ti++;\n}"
	w.parm('snippet').set(s)
	p = w.createOutputNode('python')
	r = "node = hou.pwd()\n"
	r += "geo = node.geometry()\n"
	r += "fbx = hou.node('" + node.path() + "')\n"
	r += "nodes = fbx.children()\n"
	r += "i = 0\n"
	r += "for point in geo.points():\n"
	r += "\tnode = nodes[i]\n"
	r += "\ttr = hou.Vector3(node.parm('tx').eval(), node.parm('ty').eval(), node.parm('tz').eval())\n"
	r += "\tpoint.setPosition(tr)\n"
	r += "\trot = hou.Vector3(node.parm('rx').eval(), node.parm('ry').eval(), node.parm('rz').eval())\n"
	r += "\tpoint.setAttribValue('rotate', rot)\n"
	r += "\tsc = hou.Vector3(node.parm('sx').eval(), node.parm('sy').eval(), node.parm('sz').eval())\n"
	r += "\tpoint.setAttribValue('scale', rot)\n"
	r += "\ti += 1\n"
	p.parm('python').set(r)
	p.setDisplayFlag(True)
	p.setRenderFlag(True)

def change_str(path, mode):
	pattern1 = re.compile("\A\$JOB/|\A\$JOB$|\A\$JOB_S/|\A\$JOB_S$")
	new_str = path
	c = 0
	if pattern1.search(path) == None:
		hip = hou.getenv('HIP')
		pattern = re.compile("/3d/hip$|/3d/hip/")
		if pattern.search(hip):
			pat_hip = re.compile("\A\$HIP/|\A\$HIP$")
			if pat_hip.search(path):
				re_subn = re.subn(pat_hip, '$'+mode+'/3d/hip/', path)
				if re_subn[1]:
					new_str = re_subn[0]
					c = 1
			else:
				c_job = pattern.split(hip)[0]
				parm_job = pattern.split(path)[0]
				if c_job==parm_job:
					pattern = re.compile(c_job)
					re_subn = re.subn(pattern, "$"+mode, path)
					if re_subn[1]:
						new_str = re_subn[0]
						c = 1
	else:
		re_subn = re.subn(pattern1, "$"+mode+"/", path)
		if re_subn[1]:
			new_str = re_subn[0]
			c = 1
	return [new_str, c]

def all_JOB(mode, chx):
	sel_nodes = hou.selectedNodes()
	if len(sel_nodes)!=0:
		all_nodes = sel_nodes
	else:
		all_sop = hou.node("/").recursiveGlob("*", filter = hou.nodeTypeFilter.Sop)
		all_rop = hou.node("/").recursiveGlob("*", filter = hou.nodeTypeFilter.Rop)
		all_vops = hou.node("/").recursiveGlob("*", filter = hou.nodeTypeFilter.Vop)
		all_nodes = all_sop + all_rop + all_vops
	processed = {}
	for node in all_nodes:
		n_type = node.type().name()
		parm_name = None
		new_str = ['', 0]
		if n_type == 'file':
			parm_name = 'file'
		if n_type == 'alembic':
			parm_name = 'fileName'
		if n_type == 'rop_geometry':
			parm_name = 'sopoutput'
		if n_type == 'rop_alembic':
			parm_name = 'filename'
		if n_type == 'Redshift_Proxy_Output':
			parm_name = 'RS_archive_file'
		if n_type == 'Redshift_ROP':
			parm_name = 'RS_outputFileNamePrefix'
		if n_type == 'ifd':
			parm_name = 'vm_picture'
		if 'redshift' in n_type:
			for parm in node.parms():
				not_lock_dis_hidden = parm.isLocked()==0 and parm.isDisabled()==0 and parm.isHidden()==0
				if parm.parmTemplate().type()==hou.parmTemplateType.String and not_lock_dis_hidden:
					if parm.eval() != '' and len(parm.keyframes())==0:
						parm_str = parm.unexpandedString()
						new_str = change_str(parm_str, mode)
						if new_str[1] == 1 and parm_str!=new_str[0]:
							if chx:
								processed[parm.path()] = new_str[0]
								print parm.path() + " is set to: " + new_str[0]
							else:
								parm.set(new_str[0])
			continue
		if parm_name:
			parm = node.parm(parm_name)
			not_lock_dis_hidden = parm.isLocked()==0 and parm.isDisabled()==0 and parm.isHidden()==0
			if  len(parm.keyframes())==0 and not_lock_dis_hidden:
				parm_str = parm.unexpandedString()
				new_str = change_str(parm_str, mode)
		if new_str[1]==1 and parm_str!=new_str[0]:
			if chx:
				processed[parm.path()] = new_str[0]
				print parm.path() + " is set to: " + new_str[0]
			else:
				node.parm(parm_name).set(new_str[0])

###   PySide   Windows ########
from PySide2.QtWidgets import *
from PySide2.QtCore import *
class allJOB_window(QWidget):
	def __init__(self, parent=None):
		#initial window
		super(allJOB_window, self).__init__()
		self.setGeometry(500, 200, 300, 100)
		self.setFixedSize(300, 100)
		self.setWindowTitle('Change Path')

		self.text = QLabel('Change all paths to:')
		self.text.setMargin(20)

		self.button1 = QPushButton('JOB')
		self.button1.setContentsMargins(0,0,0,0)
		@self.button1.clicked.connect
		def paulwinex1():
			all_JOB('JOB', self.check_state)
			self.close()

		self.button2 = QPushButton('JOB_S')
		self.button2.setContentsMargins(0,0,0,0)
		@self.button2.clicked.connect
		def paulwinex2():
			all_JOB('JOB_S', self.check_state)
			self.close()

		self.chx_label = QLabel('TEST:')
		self.chx_label.setMargin(10)
		self.chx = QCheckBox()
		self.chx.setChecked(True)
		self.chx.stateChanged.connect(self.trig)
		self.check_state = self.chx.isChecked()
		self.chx.setFixedHeight(37)
		style = \
			".QCheckBox {\n" \
			+ "padding: 11px" \
			+ "}"\
			+ ".QPushButton {\n"\
			+ "padding: 9px" \
			+ "}"\

		self.chx.setStyleSheet(style)
		self.button1.setStyleSheet(style)
		self.button2.setStyleSheet(style)

		Vbox = QVBoxLayout()
		Vbox.setContentsMargins(0,0,0,0)
		Vbox.setSpacing(1)
		Hbox = QHBoxLayout()
		Hbox.setSpacing(0)

		Vbox.addWidget(self.text)
		Vbox.addLayout(Hbox)

		Hbox.addWidget(self.chx_label)
		Hbox.addWidget(self.chx, Qt.AlignRight)
		Hbox.addWidget(self.button1, Qt.AlignCenter)
		Hbox.addWidget(self.button2, Qt.AlignCenter)

		self.setLayout(Vbox)
	def trig(self):
		self.check_state = self.chx.isChecked()
	def closeEvent(self, event):
		self.setParent(None)

def makeJOB():
	w = allJOB_window()
	w.setParent(hou.qt.mainWindow(), Qt.Window)
	w.show()
