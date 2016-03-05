__author__ = 'tery'
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime

def str_to_date(txt):
    txt = txt.split("/")
    if len(txt) != 3:
        return None
    if len(txt[2]) != 4:
        return None
    date = datetime.date(int(txt[2]),int(txt[1]),int(txt[0]))
    return date

def date_to_str(date):
    txt = "{}/{}/{}".format(date.day,date.month,date.year)
    return txt

def date_expiration(date):
    dexp = datetime.date(date.year+5,date.month,date.day)
    delta = datetime.timedelta(days = 1)
    dexp = dexp - delta
    return dexp

def product(A,B):
    # existe déjà dans itertools en Python 3.x
    return ((x,y) for x in A for y in B)

def sensibilite():
    A = range(245,256,1)
    return [(x,y,z) for x in A for y in A for z in A]

def  recadrage(adresse):
    print("recadrage")
    im = Image.open(adresse)
    pix = im.load()
    width, height = im.size

    liste = ((0,0,width//2,height//2),(width//2,0,width,height//2),(0,height//2,width//2,height),(width//2,height//2,width,height))
    for a,b,c,d in liste:
        print(a,b,c,d)
        r = detect(im,a,b,c,d)
        print(r)
        if r : break

    print(a,b,c,d)
    im = im.crop((a,b,c,d))
    pix = im.load()
    width, height = im.size

    s = sensibilite()
    for (left,y) in product(range(width), range(height)):
        if pix[left,y] not in s: break
    print(left)
    for (right,y) in product(range(width-1,left,-1), range(height)):
        if pix[right,y] not in s: break
    print(right)
    for (top,x) in product(range(height), range(width)):
        if pix[x,top] not in s: break
    print(top)
    for (bottom,x) in product(range(height-1,top,-1), range(width)):
        if pix[x,bottom] not in s: break
    print(bottom)

    im = im.crop((left,top,right+1,bottom+1))
    #im.show()
    return im

def recadrage2(adresse):
    im = Image.open(adresse)
    pix = im.load()
    width, height = im.size
    pixels_fond = [253,254,255]

    for left in xrange(width):
        if any( pix[left,y][:3] != (255,255,255) for y in xrange(height)):  break

    for right in xrange(width-1,left,-1):
        if any( pix[right,y][:3] != (255,255,255) for y in xrange(height)):  break

    for top in xrange(height):
        if any( pix[x,top][:3] != (255,255,255) for x in xrange(width)):  break

    for bottom in xrange(height-1,top,-1):
        if any( pix[x,bottom][:3] != (255,255,255) for x in xrange(width)):  break

    print("\n\nRectangle au-dela duquel il n'y a que des pixels blancs :"\
        +'\n\ttop\tleft ~~~~~~~~~~~~~~~~~'\
        +'\n\t'+str(top).ljust(6)+'\t'+str(left).ljust(6)+'\tbottom\t right'\
        +'\n\t~~~~~~~~~~~~~~~~'+str(bottom).rjust(6)+'\t'+str(right).rjust(6))
    im = im.crop((left+2,top+2,right-2,bottom-2))
    return im

def detect(im,x,y,X,Y):
    im = im.crop((x,y,X,Y))
    pix = im.load()
    width, height = im.size
    s = sensibilite()

    for (x,y) in product(range(0,width,5), range(0,height,5)):
        if pix[x,y] not in s: return 1
    return 0

if __name__ == "__main__":
    print(str_to_date("01/02/1995"))
    print(str_to_date("01/02/95"))
    date = datetime.date(2003,2,1)
    print(date_to_str(date))