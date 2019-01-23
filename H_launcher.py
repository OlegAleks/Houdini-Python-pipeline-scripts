import os, sys, subprocess
HRELEASE = "16.5.496"
HINSTALL = ("C:/Program Files/Side Effects Software/Houdini ")
HFS = HINSTALL+HRELEASE
HBIN = HFS+"/bin"
RBIN = "$PATH;C:/ProgramData/Redshift/bin"
RPLUGIN = "C:/ProgramData/Redshift/Plugins/Houdini/"+HRELEASE+";&"
JOB = "C:/Users/" + os.environ['USERNAME']
path = JOB + "/Documents/" + "houdini" + HRELEASE.split('.')[0] + "." + HRELEASE.split('.')[1] + "/houdini.env"
file = open(path, "w")
text = "#\n"
text+="# Houdini Environment Settings\n"
text+="#\n"
text+="# The contents of this file are read into the environment\n"
text+="# at startup.  They will override any existing entries in\n"
text+="# the environment.\n"
text+="#\n"
text+="# The syntax is one entry per line as follows:\n"
text+="#    VAR = VALUE\n"
text+="#\n"
text+="# Values may be quoted\n"
text+='#    VAR = "VALUE"\n'
text+="#\n"
text+="# Values may be empty\n"
text+="#    VAR = \n"
text+="#\n"
text+="\n"
text+="# Example:\n"
text+="#\n"
text+="# HOUDINI_NO_SPLASH = 1\n"
text+="\n\n"
text+='PATH = "' + RBIN + '"\n'
text+='HOUDINI_DISABLE_FILE_LOAD_WARNINGS = 1\n'
text+="#HOUDINI_DSO_ERROR = 2\n"
text+='HOUDINI_MENU_PATH = "N:/3D-Project Blank/PIPELINE/3d/Houdini/UNIFY_PREFERENCES/houdini;&"\n'
text+='HOUDINI_PATH = "' + RPLUGIN + '"\n'
text+='#HOUDINI_USER_PREF_DIR = "N:/3D-Project Blank/PIPELINE/3d/Houdini/UNIFY_PREFERENCES/houdini"\n'
text+='HOUDINI_GALLERY_PATH = "N:/3D-Project Blank/PIPELINE/3d/Houdini/Gallery"\n'
text+='HOUDINI_ASSET_STORE_PATH = "N:/3D-Project Blank/PIPELINE/3d/Houdini/Assets"\n'
text+='HOUDINI_OTLSCAN_PATH = "' + os.path.pathsep.join(["N:/3D-Project Blank/PIPELINE/3d/Houdini/Assets","N:/3D-Project Blank/PIPELINE/3d/Houdini/Assets/otls", HFS+"/houdini/otls", RPLUGIN.split(os.path.pathsep)[0]+"/otls"]) + '"\n'
text+='HOUDINI_SCRIPT_PATH = "N:/3D-Project Blank/PIPELINE/3d/Houdini/UNIFY_PREFERENCES/houdini/scripts;@/scripts;&"\n'
text+='HOUDINI_TOOLBAR_PATH = "N:/3D-Project Blank/PIPELINE/3d/Houdini/UNIFY_PREFERENCES/houdini/toolbar;@/toolbar;&"\n'
# text+="HOUDINI_MAXTHREADS = 1\n"
file.write(text)
file.close()
if __name__== "__main__":
	os.chdir(JOB)
	startpath = HBIN+"/houdinifx.exe"
	subprocess.call([startpath])
