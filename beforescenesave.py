import hou, re
job = hou.getenv('JOB')
# hip = hou.getenv('HIP')
hip = hou.expandString("$HIP")
pattern = re.compile("/3d/hip$|/3d/hip/")
c_job = pattern.split(hip)[0]
s_job = "S" + c_job[1:]
if job != c_job:
	buttons = ("YES","NO")
	text = "Now $JOB = " + job + "\nAfter $JOB = " + c_job
	choice = hou.ui.displayMessage(text, buttons, hou.severityType.ImportantMessage, 1, 1)
	if(choice==0):
		hou.putenv('JOB', c_job)
		text = "'JOB' set to: " + c_job
		hou.ui.displayMessage(text)
if s_job != hou.getenv('JOB_S'):
	bad_symbols = re.compile("\'")
	s_job = re.sub(bad_symbols, "\\'", s_job)
	hou.hscript('setenv JOB_S = {0}'.format(s_job))
