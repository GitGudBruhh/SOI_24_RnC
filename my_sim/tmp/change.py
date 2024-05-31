import time

str1 = '''255,0,1
255,1,0
0,0'''

str2 = '''255,0,1
255,0,0
0,0'''

a = True
while(1):
    fobj = open('shared.txt', 'w')
    if(a):
        fobj.write(str1)
        a = False
        fobj.close()
    else:
        fobj.write(str2)
        a = True
        fobj.close()

    time.sleep(0.8014)
