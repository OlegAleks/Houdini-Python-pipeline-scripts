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
