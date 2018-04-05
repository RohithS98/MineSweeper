import pygame
from random import randint,choice

x,y,z=15,15,60
x=int(raw_input("Enter side(min-5, max-25)"))
x=max(5,x)
x=min(25,x)
y=x
z=int(raw_input("Enter number of mines"))
z=max(3,z)
z=min(z,x*y-10)

pygame.init()
screen=pygame.display.set_mode((600,600))
done=False
clock=pygame.time.Clock()
image1=pygame.image.load("sprite2.png")
image2=pygame.image.load("sprite3.png")
#13x23
image3=pygame.image.load("sprite4.png")

startx,starty=300-(y*8),145
m_down=0
target=(0,0)
fsp=0
cmn=z

board1=[]
board2=[]

spritelist=[]
for i in range(2):
    for j in range(8):
        spritelist.append((j*17,i*17,16,16))

face1=[]
for i in range(5):
    face1.append((i*27,0,26,26))

num1=[]
for i in range(10):
    num1.append((i*14,0,13,23))


def boardgen(a=9,b=9,c=10,startslot=(0,0)):
    board1=[]
    temp1=[]
    for i in range(a):
        temp=[]
        for j in range(b):
            temp1.append((i,j))
            temp.append(0)
        board1.append(temp)
    startslot=(startslot[1],startslot[0])
    for i in range(startslot[0]-1,startslot[0]+2):
        for j in range(startslot[1]-1,startslot[1]+2):
            if (i,j) in temp1:
                temp1.remove((i,j))

    mines=[]
    for i in range(c):
        mines.append(choice(temp1))
        temp1.remove(mines[-1])
        d,e=mines[-1]
        board1[d][e]=9
        
    tb=[]
    temp=[]
    for i in range(b+2):
        temp.append(0)
    tb.append(temp)
    for i in range(a):
        temp1=[0]+board1[i]+[0]
        tb.append(temp1)
    tb.append(temp)
    for i in range(1,a+1):
        for j in range(1,b+1):
            if tb[i][j]!=9:
                tmine=0
                for k in range(i-1,i+2):
                    for l in range(j-1,j+2):
                        if tb[k][l]==9:
                            tmine+=1
                tb[i][j]=tmine
    tb=tb[1:]
    tb=tb[:a]
    for i in range(a):
        tb[i]=tb[i][1:b+1]
    return tb

def drawboard(b1):
    global fsp
    screen.fill((180,180,180))
    pygame.draw.rect(screen, (220,220,220),pygame.Rect(startx-3*16,starty-4*16,(x+6)*16,2))
    pygame.draw.rect(screen, (220,220,220),pygame.Rect(startx-3*16,starty-4*16,2,(y+6)*16))
    pygame.draw.rect(screen, (120,120,120),pygame.Rect(startx-3*16,starty+2*16+y*16,(x+6)*16,2))
    pygame.draw.rect(screen, (120,120,120),pygame.Rect(startx+3*16+x*16,starty-4*16,2,(y+6)*16))
    if cmn<=0:
        tc='000'
    else:
        tc=str(cmn)
        while len(tc)<3:
            tc='0'+tc
    for i in range(len(tc)):
        screen.blit(image3,(startx-44+i*13,102),num1[int(tc[i])])
    if time>999:
        tc='999'
    else:
        tc=str(time)
        while len(tc)<3:
            tc='0'+tc
    for i in range(len(tc)):
        screen.blit(image3,(startx+x*16+8+i*13,102),num1[int(tc[i])])
    for i in range(len(b1)):
        for j in range(len(b1[i])):
            im=0
            if b1[i][j]==9:
                im=5
            elif b1[i][j]==0:
                im=1
            elif b1[i][j]=='0c':
                im=1
            elif b1[i][j]=='-':
                im=0
            elif b1[i][j]=='F':
                im=2
            elif b1[i][j]=='D':
                im=6
            elif b1[i][j]=='M':
                im=5
            elif b1[i][j]=='W':
                im=7
            else:
                im=b1[i][j]+7
            screen.blit(image1,(startx+j*16,starty+i*16),spritelist[im])
    screen.blit(image2,(287,100),face1[fsp])

def finish(b1,b2):
    for i in range(len(b1)):
        for j in range(len(b1[i])):
            if b1[i][j]==9:
                if b2[i][j]=='-':
                    b2[i][j]='M'
            elif b2[i][j]=='F':
                b2[i][j]='W'
    return b2

def checkwin(b1,b2):
    global win
    c=1
    for i in range(len(b1)):
        for j in range(len(b1[i])):
            if b1[i][j]!=9 and (b2[i][j]=='-' or b2[i][j]=='F'):
                c=0
    if c==1:
        win=True
    
def checkmove(b1,b2,t):
    global loss
    global win

    if loss==False and win==False:
        if b1[t[1]][t[0]]==9:
            b2[t[1]][t[0]]='D'
            loss=True
            b2=finish(b1,b2)
        elif b2[t[1]][t[0]]!='0c':
            b2[t[1]][t[0]]=b1[t[1]][t[0]]
            #print t,'a'
            checkwin(b1,b2)
            if win==False and b2[t[1]][t[0]]==0:
                for i in range(t[0]-1,t[0]+2):
                    for j in range(t[1]-1,t[1]+2):
                        if -1<i<x and -1<j<y:
                            if b2[j][i]!='0c':
                                b2[j][i]=b1[j][i]
            checkwin(b1,b2)
    return b2

def convert0(b1,b2):
    for i in range(len(b2)):
        for j in range(len(b2[i])):
            if b2[j][i]==0:
                b2=checkmove(b1,b2,(i,j))
                b2[j][i]=='0c'
    return b2
    
board2=[]
for i in range(x):
    temp=[]
    for j in range(y):
        temp.append('-')
    board2.append(temp)

firstmove=True
loss=False
win=False
timex=0
time=0
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done=True
        if event.type==pygame.KEYDOWN and event.key==pygame.K_SPACE:
            if loss==True or win==True:
                loss=False
                win=False
                cmn=z
                board2=[]
                for i in range(x):
                    temp=[]
                    for j in range(y):
                        temp.append('-')
                    board2.append(temp)
                firstmove=True
                fsp=0
                
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button==1:
                m_down=1
            elif event.button==3:
                m_down=3
            else:
                break
            tm=list(pygame.mouse.get_pos())
            if startx<tm[0]<startx+x*16 and starty<tm[1]<starty+y*16:
                tm[0]-=startx
                tm[1]-=starty
                tm[0]/=16
                tm[1]/=16
                target=tm
                fsp=2
            elif 286<tm[0]<313 and 99<tm[1]<126:
                fsp=1
        if  event.type==pygame.MOUSEBUTTONUP:
            tm=list(pygame.mouse.get_pos())
            if startx<tm[0]<startx+x*16 and starty<tm[1]<starty+y*16:
                tm[0]-=startx
                tm[1]-=starty
                tm[0]/=16
                tm[1]/=16
            else:
                m_down=0
                fsp=0
                break
            if target==tm:
                if event.button==1:
                    if board2[target[1]][target[0]]=='-':
                        if firstmove:
                            board1=boardgen(x,y,z,target)
                            firstmove=False
                            for i in range(target[0]-1,target[0]+2):
                                for j in range(target[1]-1,target[1]+2):
                                    if -1<i<x and -1<j<y:
                                        board2=checkmove(board1,board2,(i,j))
                        else:
                            board2=checkmove(board1,board2,target)
                    
                elif event.button==3:
                    if loss==False and win==False:
                        if board2[target[1]][target[0]]=='-':
                            board2[target[1]][target[0]]='F'
                            cmn-=1
                        elif board2[target[1]][target[0]]=='F':
                            board2[target[1]][target[0]]='-'
                            cmn+=1
            m_down=0
            fsp=0
            
    if win:
        fsp=3
    elif loss:
        fsp=4
    if firstmove:
        timex=0
        time=0
    elif not(win) and not(loss):
        timex+=1
        if timex==29:
            time+=1
            timex=0
    pressed=pygame.key.get_pressed()
    board2=convert0(board1,board2)
    drawboard(board2)

    pygame.display.flip()
    clock.tick(30)
pygame.quit()
