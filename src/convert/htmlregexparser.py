import re
import pandas as pd
import subprocess

def htmlregexparser(toolpath, filepath):
    #converts the file from pdf to html (use delimiter as period for file extension)

    subprocess.call([toolpath, '--zoom', '1.3', filepath+'.pdf', '--dest-dir', 'media/documents'], shell=True)

    #file location of html
    filename = filepath+'.html'

    #opens html file
    f = open(filename, 'r', encoding="utf8")
    html_string = f.read()

    #first regex for finding names
    rname= re.findall(r"""<div class="t m0 x0 h.*? y1 ff.*? fs0 fc0 sc0 ls0 ws0">(.*?)\s(.*?)[,|<].*?<\/div>""", html_string)

    #removing doubles of names
    names=rname[::2]

    #separating names
    firstname=[]
    lastname=[]
    for i in range(len(names)):
        firstname.append(names[i][0])
        lastname.append(names[i][1])

    #second regex for finding jobs
    #rjob = re.findall(r"""Experience</div><div class="t m0 x0 h5 y.. f.. fs3 fc2 sc0 ls0 ws0">(.*?)\sat\s(.*?)</div>""", html_string)
    rjob = re.findall(r"""Experience</div><div class=.*?>(.*?)at\s(.*?)</div>""", html_string)

    #separating positions and companies
    position=[]
    company=[]
    for i in range(len(rjob)):
        position.append(rjob[i][0])
        company.append(rjob[i][1])

    #create new df 
    df = pd.DataFrame({'Last Name':lastname, 'First Name':firstname, 'Position':position, 'Company':company})
    df.to_excel(filepath+'.xlsx', index=False)


