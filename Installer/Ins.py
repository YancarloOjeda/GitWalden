import os 

def Lib():
    PList = [
            'serial',
            'pyfirmata', 
            'opencv-python',
            'tk',
            'matplotlib',
            'requests',
            'zipfile'
              ]
    for i in PList:
         installPythonPackage = 'pip install ' + i
         os.system('start cmd /c ' + installPythonPackage)
         
def WaldenPath():
    try:
        os.mkdir('C:\WALDEN')
    except:
        print('000')
    try:
        os.mkdir('C:\WALDEN\Temp')
    except:
        print('001')
        
def Download():
    import requests
    import zipfile
    import shutil
    DList = [
            'http://walden-me.com/Resources/WTS-2.01.zip'
            ]
    PList_0 = [
            'Config',
            'Data',
            'Images',
            'Projects',
            'Schedules',
            'Videos',
            ]
    for i in DList:
        try:
            r = requests.get(i)
            with open('C:/WALDEN/Temp/' + i.split('/')[-1], "wb") as zip:
                zip.write(r.content)
            with zipfile.ZipFile('C:/WALDEN/Temp/' + i.split('/')[-1], 'r') as zip_ref:
                zip_ref.extractall('C:/WALDEN/Temp' )
        except:
            print('003-' + i)
        for i2 in PList_0:
            try:
                shutil.move('C:/WALDEN/Temp/' + i.split('/')[-1].split('.zip')[0] + '/' + i2, 'C:/WALDEN/')
            except:
                print('004-' + i2)
                
def CreateApp():
    #Temp_Path = r'C:/Users/Walden/Anaconda3'
    Temp_Path = os.path.expanduser("~") +'\Anaconda3'
    try:
        Bat = open('C:/WALDEN/' + 'WTS-2.01.bat' ,'w+')
        Bat.write(
                    'set root=' + Temp_Path + '\n'
                    r'call %root%\Scripts\activate.bat %root%' + '\n'
                    r'call python C:\WALDEN\Config\WTS-2.01.py' + '\n'
                   )
        Bat.close()
    except:
        print('005')
    try:
        VB = open('C:/WALDEN/' + 'WTS-2.01.VBS' ,'w+')
        VB.write(
                    r'Set WshShell = CreateObject("WScript.Shell")' + '\n'
                    r'WshShell.Run chr(34) & "C:\WALDEN\WTS-2.01.bat" & Chr(34), 0 ' + '\n'
                    r'Set WshShell = Nothing' + '\n'
                   )
        VB.close()
    except:
        print('006')
        
def CreateIco():
    import win32com.client
    try:
        Temp_Path =  os.path.expanduser("~") + '\Desktop'  
        path = os.path.join(Temp_Path, 'WTS-2.01.lnk')
        target = r'C:\WALDEN\WTS-2.01.VBS'
        icon = r'C:\WALDEN\Images\Icon.ico' 
        
        shell = win32com.client.Dispatch("WScript.Shell")
        shortcut = shell.CreateShortCut(path)
        shortcut.Targetpath = target
        shortcut.IconLocation = icon
        shortcut.WindowStyle = 7 
        shortcut.save()
    except:
        print('007')
    
Lib()
WaldenPath()
Download()
CreateApp() 
CreateIco()