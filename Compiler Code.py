#library imports

from re import A
from tkinter import *
from PIL import Image
import math

'''
Script required to load a pop-out window (not recommended; no zoom)

win = Tk()
win.geometry("500x500")
canvas= Canvas(win, width= 5000, height= 5000)
canvas.pack()

'''


def turnandplaceinto(im1, dis1xy, rot1, im2, dis2xy, rot2): #fits together and pastes collage/image with largest cavity and image with best-matching convexity

    img1 = Image.open(im1 +".png")      #loads individual images
    img2 = Image.open(im2 +".png")
    
    b = Image.open("background.png").resize((7000,7000),Image.ANTIALIAS)        #background image

    img2 = img2.rotate(rot2)
    img1 = img1.rotate(rot1+180)
    img1 = img1.convert("RGBA")
    img2 = img2.convert("RGBA")
    img1 = img1.transpose(Image.FLIP_LEFT_RIGHT)  #flips concavity-image to a) undo mirroring of convexity-concavity match and b) preserve ultimate mirroring of final collage (eventually reversed)
    
    w1 = int(((b.width - img1.width) // 2) - (dis1xy[0]))           #calculations used to paste images in the middle of background image with respective offsets
    w2 = int(((b.width - img2.width) // 2) - (dis2xy[0]))
    
    
    h1 = int(((b.height - img1.height) // 2) + (dis1xy[1]))
    h2 = int(((b.height - img2.height) // 2) - (dis2xy[1]))

    
    b.paste(img1, (w1, h1), img1)
    b.paste(img2, (w2, h2), img2)
    
    b.save("new.png", format="png")

    return (im2, " has been used as a concave. ", im1, " has been added as a convex.")

def findMiddle(image):                      #finds middle position of the image (Edit: NOT necessarily the middle of the shape)
    return [(image.width//2),(image.height//2)] #this function is used primarily for pasting a shape in the middle of a larger image

def largestCave(image):                     #finds the coordinates, area, and point relationships of the largest cavity of a given shape (orientation given)

    points=[] #list of heights of the pixels on bottom of the shape (upside down orientation)
    for x in range (0,image.width,5): #interates through the x-vals of an image
        j=0     #alpha val
        h=0     #height
        while j==0 and h<image.height:      #interates through the y-vals (h) of an image and stops at ground
            j=(image.getpixel((x,h)))[3]    #255 means transparent, 0 means black
            #test checkpoint: img.putpixel((x,h),(255, 0, 0, 255))
            h+=1
        points.append((image.height)-h)
    mem = [[]] #record of the points that compose the biggest cavity
    f = 0 #first peak
    b = 0 #back peak
    templist = [] #immediate list of points
    templist2 = [] #level cavities
    s = -1 #number of concavities (minus 1)
    z = True #boolean used to distinct first peak from others
    t = True #boolean used to distinct direction of cavity (True: Decreasing, False: Increasing)
    v = 0 #cavity score (resettable)
    loc = [] #the deepest values of every cavity
    loc2 = [] #all the accepted loc values (based on whether cavity is level and cavity score)
    g = []
    leonard = []
    tolerance = 3 #you can set this to any number >=0 but I recommend 3
    for y in range (len(points)-1):                 #finding the large cavity interval
        if (z and points[y] > points[y+1]):
            f = y
            z = False
        if ((not z) and points[y] < points[y+1]):
            b = y+1
    if (f != 0 and b != 0):
        templist.append([])
        s += 1
        templist[s].insert(0,points[f])
        for n in range (f+1,b):
            if (points[n+1] <= points[n]+tolerance):
                templist[s].append(points[n])
                if (not t and points[n+1] < points[n]+tolerance):     #this is only true when a new curve is started (exclusive of first goaround)
                    templist.append([])     #starts the new curve
                    s += 1
                    templist[s].append(points[n])
                    g = [5*(points.index(min(templist[s-1]))),((-1)*(min(templist[s-1])))+image.height]
                    loc.append(g)
                    t = True
            else:              
                if (t):
                    t = False
                templist[s].append(points[n])
        templist[s].append(points[b])
    if (len(templist) != 0):
        g = [5*(points.index(max(templist[s]))),((-1)*(max(templist[s])))+image.height]         #test 2 (inactive)
        loc.append(g)
    for j in range(s+1):
        v=0
        if ((len(templist[j]) != 0) and ((templist[j][0]+2) >= (templist[j][len(templist[j])-1])) and ((templist[j][0]-2) <= templist[j][len(templist[j])-1])):
            for q in range(len(templist[j])):
                v += max(templist[j][0],templist[j][len(templist[j])-1])-templist[j][q]
            templist2.append(v)
            mem.append(templist[j])
            #print(loc, s, templist, j)
            loc2.append(loc[j])
        #test checkpoint: print("templist:", templist)
        #test checkpoint: print("f:", f)
        #test checkpoint: print("b:", b)
        #test checkpoint: print("s:", s)
        #test checkpoint: print("templist2:", templist2)
    if (len(templist2) != 0):
        leonard = loc2[templist2.index(max(templist2))]
        '''
        test checkpoint (9 point placement):

        image.putpixel((leonard[0],leonard[1]-1),(255, 0, 0, 255))
        image.putpixel((leonard[0]+1,leonard[1]-1),(255, 0, 0, 255))
        image.putpixel((leonard[0]-1,leonard[1]-1),(255, 0, 0, 255))
        image.putpixel((leonard[0],leonard[1]),(255, 0, 0, 255))
        image.putpixel((leonard[0]+1,leonard[1]),(255, 0, 0, 255))
        image.putpixel((leonard[0]-1,leonard[1]),(255, 0, 0, 255))
        image.putpixel((leonard[0],leonard[1]+1),(255, 0, 0, 255))
        image.putpixel((leonard[0]+1,leonard[1]+1),(255, 0, 0, 255))
        image.putpixel((leonard[0]-1,leonard[1]+1),(255, 0, 0, 255))
        image.save("shitcave.png", format="png")

        '''
        return max(templist2), mem[1+templist2.index(max(templist2))], leonard,
    else:
        return [0,0,[0,0]]

def convexMatch(cavecoords, image):         #finds the series of points on top of a shape that best match the cavity

    position = []                   #all points on the top of a shape (normal orientation)
    tempcoords = []                 #Immediate coordinates of a concavity
    basevaluetempcoords = 0         #smallest value of tempcoords (to simplify the matching process)
    basevaluecavecoords = 0         #smallest value of cavecoords (to simplify the matching process)
    score = []                      #how well a concavity matches a given cavity (the smaller the better)
    g = 0                           #the location of the highest point of the concavity
    extrascore = 0                  #the amount added to score if a shape is smaller than the cavity of a shape


    basevaluecavecoords = min(cavecoords)       #simplifying cavecoords
    for x in range(len(cavecoords)):
        cavecoords[x] = cavecoords[x]-basevaluecavecoords
    
    points=[]
    for x in range (0,image.width,5): #interates through the x-vals of an image
        j = 0 #alpha val
        h = 0  #height
        while j==0 and h<image.height: #interates through the y-vals (h) of an image and stops at ground
            j=(image.getpixel((x,h)))[3]  #255 means transparent, 0 means black
            #img.putpixel((x,h),(255, 0, 0, 255))
            h += 1
        points.append(h)
    
    if (len(cavecoords)>len(points)):
        extrascore = 100*(len(cavecoords)-len(points))         #applying extrascore and making cavecoord corrections
        cavecoordslong = cavecoords
        cavecoords = []
        for x in range(len(points)):
            cavecoords.append(cavecoordslong[x])
    
    for x in range (len(points)-len(cavecoords)+1):     
        v = 0
        tempcoords = []
        if (points[x] != image.height):             #every series on top of the shape is considered for 'tempcoords'
            for q in range (len(cavecoords)):
                tempcoords.append(points[x+q])      #tempcoords created in opposite orientation as cavcoords so the cavity and concavity can match
            basevaluetempcoords = min(tempcoords)
            for z in range (len(cavecoords)):
                tempcoords[z] = tempcoords[z]-basevaluetempcoords           
            for y in range (len(cavecoords)-1):                                 #score/matching calculations determined by the space between the curves (overlapping and empty space are both included)
                if (cavecoords[y]+tempcoords[y+1]!=tempcoords[y]+cavecoords[y+1]):
                    if (tempcoords[y]>cavecoords[y] and tempcoords[y+1]<cavecoords[y+1]):
                        v += (abs(((tempcoords[y]-cavecoords[y])/2)*((tempcoords[y]-cavecoords[y])/(cavecoords[y+1]-cavecoords[y]-tempcoords[y+1]+tempcoords[y]))) + abs(((cavecoords[y+1]-tempcoords[y+1])/2)*(1-((tempcoords[y]-cavecoords[y])/(cavecoords[y+1]-cavecoords[y]-tempcoords[y+1]+tempcoords[y])))))
                    else: 
                        if (tempcoords[y]<cavecoords[y] and tempcoords[y+1]>cavecoords[y+1]):
                            v += (abs(((cavecoords[y]-tempcoords[y])/2)*((cavecoords[y]-tempcoords[y])/(tempcoords[y+1]-tempcoords[y]-cavecoords[y+1]+cavecoords[y]))) + abs(((tempcoords[y+1]-cavecoords[y+1])/2)*(1-((cavecoords[y]-tempcoords[y])/(tempcoords[y+1]-tempcoords[y]-cavecoords[y+1]+cavecoords[y])))))
                        else:
                            v += ((abs(cavecoords[y+1]-tempcoords[y+1]) + abs(cavecoords[y]-tempcoords[y]))/2)
                else:
                    v += abs(cavecoords[y]-tempcoords[y])
                
            score.append(v+extrascore)
            g = [5*(x+tempcoords.index(0)), basevaluetempcoords] 
            
            position.append(g)
    if (len(score) == 0):
        score = [999999]
        position = [[0,0]]
        leonard = [0,0]
    else:
        leonard = position[score.index(min(score))]         #location of the highest point of the best-matching concavity
        #test checkpoint: image.putpixel((leonard[0],leonard[1]),(255, 0, 0, 255))
        #test checkpoint: image.save("shitconvex.png", format="png")
    return [min(score),leonard]

def convexRunner(imnum, usedconvexities):   #finds the image that best fits the given image's largest level cavity and return information about the match

    cfai = []       #cavities from all images
    cffai = []      #cavity facts from all images
    cavrot = []     #rotations of shapes when their biggest caves are facing upwards
    cavim = 0       #selected image
    cavloc = []     #the location of the cavity         
    runner = []     #constantly updated information received from largestCave
    cav = []        #the area inside the largest level cavity of an image (updated with rotations)
    cavfax = []     #facts about the cavities
    cavfax2 = []    #location of the deepest point in the cavity
    cavreset2 = []  #location of the middle of the image
    xvar = 0
    yvar = 0
    for rot in range(0,360,2):  #information gathered about the largest cavity of a given image

        print(str(len(usedconvexities))+".2.0."+str(rot+2)) #rotation ticker
        img = Image.open(imnum + ".png")
        img = img.rotate(rot)
        runner.append((largestCave(img)))
        cav.append(runner[len(runner)-1][0])
        cavfax.append(runner[len(runner)-1][1])
        cavfax2.append(runner[len(runner)-1][2])
    
    cavrot.append(2*cav.index(max(cav)))                #saving information about the image with the largest cavity
    img = img.rotate(cavrot[0])
    cavreset2.append(findMiddle(img))
    cfai.append(max(cav))
    cffai.append(cavfax[cav.index(max(cav))])
    xvar = cavfax2[cav.index(max(cav))][0]-cavreset2[len(cavreset2)-1][0]
    yvar = cavfax2[cav.index(max(cav))][1]-cavreset2[len(cavreset2)-1][1]
    print(xvar,yvar)
    cavloc.append([int(xvar),int(yvar)])
    
    #test checkpoint: print(cffai, cfai, cfai.index(max(cfai)))

    if (len(cffai)==1 and cffai[0]==0):
        cffai = [[0]]
    
    cavim = imnum   #either the collage or the image found by largestCave
    confai = []     #convexities from all images
    conrot = []     #rotations of shapes that "fit" the cave best
    conim = 0       #selected image
    conloc = []     #the location of the convexity
    conreset2 = []  #the location of the middle of the image
    xvar = 0        #horizontal distance between the convexity point and the middle of the image
    yvar = 0        #vertical distance between the convexity point and the middle of the image

    for im in range (1,23):           
        if (im not in usedconvexities):
            runner = [] #constantly updated information received from convexMatch
            con = []    #how well a shape matches the cave found above
            confax = [] #facts about the cavities

            for rot in range(0,360,2):      #information gathered about the convexities of an image
                
                print(str(len(usedconvexities))+".2."+str(im)+"."+str(2+rot)) #rotation ticker
                img = Image.open(str(im) +".png")
                img = img.rotate(rot)
                runner.append(convexMatch(cffai[cfai.index(max(cfai))],img))
                con.append(runner[len(runner)-1][0])
                confax.append(runner[len(runner)-1][1])
            
            conrot.append(2*con.index(min(con)))            #storing convexities and comparing how well they match the cavity (see convexMatch for more information on matching)
            confai.append(min(con))
            img = Image.open(str(im) +".png")
            img = img.rotate(conrot[len(conrot)-1])
            conreset2.append(findMiddle(img))
            xvar = confax[con.index(min(con))][0]-conreset2[len(conreset2)-1][0]
            yvar = confax[con.index(min(con))][1]-conreset2[len(conreset2)-1][1]
            conloc.append([int(xvar), int(yvar)])
        else:
            confai.append(1000000)
            conrot.append(0)
            conreset2.append([0,0])
            conloc.append([0,0])
            
            
    conim = confai.index(min(confai))+1

    #test checkpoint (enabling strongly recommended): print("FOR CONVEXITY: The best (lowest) score: ", confai, " The rotation: ", conrot[confai.index(min(confai))], " The distance: ", conloc[confai.index(min(confai))], " The shape: ", conim)
    #test checkpoint (enabling strongly recommended): print("FOR CONCAVITY: The highest score: ", cfai, " The actual points: ", cffai, " The rotation: ", cavrot[cfai.index(max(cfai))], " The distance: ", cavloc[cfai.index(max(cfai))], " The shape: ", cavim)
    #order: (image1, image1position, image1rotation, image1midpoint(x), image1midpoint(y), image2, image2position, image2rotation, image2midpoint(x), image2midpoint(y))
    turnandplaceinto(str(conim), conloc[confai.index(min(confai))], conrot[confai.index(min(confai))], cavim, cavloc[cfai.index(max(cfai))], cavrot[cfai.index(max(cfai))])
    return conim

def caveRunner():                           #finds the shape with the largest cavity

    cfai = [] #cavities from all images
    cavim = 0 #selected image
    for im in range (1,23):           
        runner = []     #constantly updated information received from largestCave
        cav = []        #score (used to compare cavities)
        for rot in range(0,360,2):
            print("1.1."+str(im)+"."+str(2+rot))
            img = Image.open(str(im) + ".png")
            img = img.rotate(rot)
            runner.append((largestCave(img)))
            #print(runner[len(runner)-1][2])
            cav.append(runner[len(runner)-1][0])
        cfai.append(max(cav))
    cavim = cfai.index(max(cfai))+1
    flip = Image.open(str(cavim)+".png")        #shape with largest cavity is flipped (all other shapes are flipped too, then reflipped at end)
    flip = flip.transpose(Image.FLIP_LEFT_RIGHT)    #the flips are necessary because the comparisons between cavity and concavity are reversed
    flip.save((str(cavim)+".png"), format="png")
    return cavim       #image with the largest cavity (at any rotation)

def crop(imname):                           #crops images to minimize the number of pixels the code will have to iterate through

    im = Image.open(str(imname) +".png")
    points=[] #list of heights of the pixels on bottom of the shape (varying orientation)
    points2 = []
    dw = True
    pos = [10000,0,0,0] #edge case so code won't crash during edit process

    im = im.convert('RGBA')
    image = Image.open("background.png").resize(((im.width*2),(im.height*2)),Image.ANTIALIAS) #background image for pasting
    
    w1 = int((image.width - im.width) // 2)     #width and height are used to paste image in the middle of a larger background image
    h1 = int((image.height - im.height) // 2)

    image.paste(im, (w1, h1), im)
    a = ((image.width)//150)+1 #horizontal step determination, independent of image width
    b = ((image.height)//150)+1 #vertical step determination, independent of image height
    for x in range (0,image.width,a): #interates through the x-vals of an image to find the 
        j = 0 #alpha val
        h = 0  #height
        
        while j == 0 and h < image.height: #interates through the y-vals (h) of an image and stops at ground to find LEFT and UPPER bounds
            j = image.getpixel((x,h))[3]  #255 means transparent, 0 means black
            #test checkpoint: image.putpixel((x,h),(0, 255, 0, 255)) #green
            h += b
        points.append(h-b)
    
    while j == 0 and h < image.height: #interates through the y-vals (h) of an image and stops at ground to find LEFT and UPPER bounds
        j=image.getpixel((image.width-1,h))[3]  #255 means transparent, 0 means black
        #test checkpoint: image.putpixel((image.width-1,h),(0, 255, 0, 255)) #green
        h += b
    points.append(h-b)

    for x in range (0,image.width,a): #interates through the x-vals of an image
        j = 0 #alpha val
        h = image.height - 1

        while j == 0 and h > 0: #interates through the y-vals (h) of an image and stops at ground to find RIGHT and LOWER bounds
            j = (image.getpixel((x,h)))[3]  #255 means transparent, 0 means black
            #test checkpoint: image.putpixel((x,h),(255, 0, 0, 255)) #red
            h -= b
        points2.append(h+b)
    
    while j == 0 and h > 0: #interates through the y-vals (h) of an image and stops at ground to find RIGHT and LOWER bounds
        j = (image.getpixel((image.width,h)))[3]  #255 means transparent, 0 means black
        #test checkpoint: image.putpixel((image.width,h),(255, 0, 0, 255)) #red
        h -= b
    points2.append(h+b)

    for n in range (len(points)):   #calculations used to transform extrema points found above into image bounds
        if (points[n]+b < image.height):
            if (dw):
                pos[2] = (n-1)*a
                dw = False
            if ((points2[n]+b) > pos[1]):
                pos[1] = (points2[n]+b)
            pos[3] = (n+1)*a
            if (points[n]-b < pos[0]):
                pos[0] = points[n]-b

    print("Image #", str(imname), ": ", pos[0],pos[1],pos[2],pos[3])
    eh = (((math.sqrt(2))-1)*(abs(pos[0]-pos[1])))//1 #extra space needed for horizonal extrema to rotate
    ew = (((math.sqrt(2))-1)*(abs(pos[0]-pos[1])))//1 #extra space needed for vertical extrema to rotate
    e = max(eh,ew) #extra space so images can fully rotate without going off screen
    #test checkpoint: print(points)
    #test checkpoint: print(points2)
    #report order: left, upper, right, lower
    image = image.crop((pos[2]-e, pos[0]-e, pos[3]+e, pos[1]+e)) #bounds

    image.save(str(imname)+ ".png", format = "png")

#main loop:

for im in range (1,23):           
    crop(im)            #cropping images saves time, do not remove
u = []                  #all used convexities

print("******************************************* CURRENT ROUND: 1/22 *******************************************")

originalcaveshape = caveRunner()
u.append(originalcaveshape)
u.append(convexRunner(str(originalcaveshape), u))   #first two images added to collage
#test checkpoint: print(u)
while (len(u)!=22): #all other shapes added to collage

    print("******************************************* CURRENT ROUND: ", len(u), "/22 *******************************************")

    u.append(convexRunner("new", u))
    print(u)
new = Image.open("new.png")                                 #entire collage flipped horizontally (all shapes within are already flipped horizontally)
new = new.transpose(Image.FLIP_LEFT_RIGHT)
new.save("new.png", format="png")
flip = Image.open(str(originalcaveshape)+".png")            #originalcaveshape returned to initial state
flip = flip.transpose(Image.FLIP_LEFT_RIGHT)
flip.save(str(originalcaveshape)+".png", format="png")
print("Program Complete.")
#Check new.png for results

'''
Terminal Information:

prints (1-21).(1-2,2).(1-22),(1-360 step:2)

22*22*180 = 87K seconds ~ 24.2 hours 24.2/2 = 12.1 hours (assuming each iteration averages at a second for every shape)

'''