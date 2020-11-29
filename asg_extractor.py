import re
import numpy as np
import shutil 
import os
import getopt
import pathlib
import sys
import time

def CopyFiles(details, dst_path):
    count = 0
    for k in details.keys():
        outputfile = '{0}_{1}'.format(details[k]["name"],details[k]["file"])
        src = details[k]["source"]
        if dst_path:
            ofile = os.path.join(dst_path,outputfile)
        else:
            ofile = outputfile
        try:
            #batch_text.append(f'copy "{src}" "{ofile}"')
            print("copying {0} to {1}".format(src,ofile))
            shutil.copy2(src,ofile)
            count += 1
        except Exception as e:
            print(e)
    return(count)

def GetDetails(all_files, root,asg_name):
    root = root.replace('\\','\\\\')
    qry_sname = fr'{root}\\(.*?)\\{asg_name}.*Version.(\d+?)\\(.*\..*?)$'
    
    output = {}
    for i in range(len(all_files)):
        x = all_files[i]
        grp_res = re.search(qry_sname, x)
        
        if grp_res:
            stname = grp_res.group(1).replace(" ","")
            ver = grp_res.group(2)
            filename = grp_res.group(3).replace(" ","")

            if not stname in output:
                output[stname] = {"name":stname, "ver":int(ver), "file":filename, "source":x}
            elif output[stname]["ver"] < int(ver):
                output[stname] = {"name":stname, "ver":int(ver), "file":filename, "source":x}
        else:
            print("not found at",x,root)
            pass
    return(output)

def FilterAssignments(all_lines, asg_name):
    qry = f'^.*{asg_name}.*\.[a-zA-Z]+'
    r = re.compile(qry)
    result = list(filter(r.match, all_lines))
    return(result)


def AllFiles(root):
    f = []
    #root = os.path.join("e:\\","test","allfiles")
    root = os.path.join(os.getcwd(),root)
    print(root)
    for path, subdirs, files in os.walk(root):
        for name in files:
            print(os.path.join(path, name))
            f.append(os.path.join(path, name))
    return(f)

def main(argv):

    if len(argv)==0:
        print("argument error")
        return
        
    try:
        opts, args = getopt.getopt(argv,"hi:o:a:")
    except getopt.GetoptError:
        print("error in arguments")
    
    inputfile = ''
    outputfile = os.getcwd()
    resultfile = 'result.txt'
    asg_title = ''
    for opt, arg in opts:
        if opt == '-h':
            print("help")
            sys.exit()
        elif opt in ("-i"):
            if arg:
                if arg == ".":
                    inputfile = os.path.join(os.getcwd(), os.getcwd())
                else:
                    inputfile = os.path.join(os.getcwd(), pathlib.Path(arg))
            else:
                print("no argument provide for -i")
        elif opt in ("-o"):
            if arg == ".":
                outputfile = os.getcwd()
            else:
                outputfile = pathlib.Path(arg)
        elif opt in ("-r"):
            resultfile = pathlib.Path(arg)
        elif opt in ("-a"):
            asg_title = arg

##    print("input file",inputfile)
##    print("output file",outputfile)
##    print("result file",resultfile)
##    #RunTest(inputfile, resultfile)

    print("scanning files ... ")
    time.sleep(1)
    all_files = AllFiles(inputfile)
    print("Total files found:",len(all_files))
    print(f"Filtering files for '{asg_title}'")
    result = FilterAssignments(all_files, asg_title)
    print("Filtered files:",len(result))
    details = GetDetails(result, inputfile, asg_title)
    print("after removing duplicate versions",len(details))
    print("copying files...")
    copied = CopyFiles(details, outputfile)
    print("{0} files copied".format(copied))

if __name__ == "__main__":
   main(sys.argv[1:])




##qry_sname = fr'Submitted files\\(.*?)\\{asg_name}.*Version.(\d+?)\\(.*\..*?)$'
##
##output = {}
##dst_path = 'files'
##for i in range(len(result)):
##    x = result[i]
##    grp_res = re.search(qry_sname, x)
##    if grp_res:
##        stname = grp_res.group(1).replace(" ","")
##        ver = grp_res.group(2)
##        filename = grp_res.group(3).replace(" ","")
##        if not stname in output:
##            output[stname] = {"name":stname, "ver":int(ver), "file":filename, "source":x}
##        elif output[stname]["ver"] < int(ver):
##            output[stname] = {"name":stname, "ver":int(ver), "file":filename, "source":x}
##
##batch_text = []
##print("total assignments:",len(output))
##for k in output.keys():
##    outputfile = '{0}_{1}'.format(output[k]["name"],output[k]["file"])
##    src = output[k]["source"]
##    if dst_path:
##        ofile = os.path.join(dst_path,outputfile)
##    else:
##        ofile = outputfile
##    try:
##        #batch_text.append(f'copy "{src}" "{ofile}"')
##        shutil.copy2(src,ofile)
##    except Exception as e:
##        print(e)
##
####f = open("copyall.bat","w")
####f.write('\n'.join(batch_text))
####f.close()
####        
####
