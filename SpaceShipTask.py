from psychopy import visual,core,event,data,monitors
from psychopy.hardware import keyboard
import random
import numpy as np

subjID = 'JLL'
expName = 'magic carpet task'
wantSave = True #Save data or not

mon = monitors.Monitor('testMonitor')
mon.setDistance(57)#view distance
mon.setSizePix([1440,900])

event.globalKeys.clear()
event.globalKeys.add(key='q', func=core.quit)
kb = keyboard.Keyboard()   #creat kb object

#定义data变量
spDir = [-1,1]      #-1,x;1,y
ptDir = [-2,2]  #-2,red planet;2,black planet,
clDir = [0,1]   #0,left;1,right
reDir = [0,1]  #0, nothing;1, reward 
nTrialsPerCon = 2   #how many trials per condition

nTrials = nTrialsPerCon*len(spDir)*len(ptDir)*len(clDir)
stimList = []
for sp in spDir:
    for pt in ptDir:
        for cl in clDir:
            stimList.append({'ship':sp,'planet':pt,'crystal':cl})
trials = data.TrialHandler(stimList, nTrialsPerCon)

#openwindow
win1 = visual.Window([1000,800], monitor="testMonitor",  units="pix",fullscr = False)

#define welcome instruction interface
instrText=\
    '欢迎参加这个实验！\n\
    您将选择一艘宇宙飞船前往未知的星球\n\
    左键和右键分别代表了X船和Y船\n\
    如果您理解了以上内容，请按空格键继续'
tex = visual.TextStim(win=win1, text=instrText, color=(-1,-1,-1),wrapWidth=10)
tex.draw()
win1.flip()
kb.start()
event.waitKeys(keyList=['space'])
kb.stop()

#  =========== main experiment loop ========

for trial in trials:#use trialHandler
#=============first stage=============
    spr = random.random()
    plr = random.random()
    spText = ''    #显示飞船刺激
    plText = ''    #显示星球刺激
    xc = 0      #xcounter
    yc = 0      #ycounter
    rc = 0       #redcounter
    bc = 0      #blackcounter
    if spr < 0.5 and  xc<8 :
        spText = 'x'
        xc += 1
        if plr < 0.5:
            plText = 'x,red planet'     #x,red
            rc += 1
        else: 
            plText = 'x,black planet' #x,black
            bc +=1
    else :
        spText = 'y'
        yc += 1
        if plr < 0.5:
            plText = 'y,red planet'# y,red
            rc += 1
        else: 
            plText = 'y,black planet'#y,black
            bc +=1
    sptex = visual.TextStim(win =win1, text = spText, color=(-1,0,1))
    sptex.draw()
    win1.flip()
    core.wait(2)
    pltex = visual.TextStim(win = win1, text = plText, color=(-1,0,1))
    pltex.draw()
    win1.flip()
    core.wait(2)
    #此时呈现x或y的选择刺激
    tex1 = visual.TextStim(win = win1, 'press left or right to choose spaceship',color = (-1,0,1))
    tex1.draw()
    win1.flip()
    core.wait(2)
    
    #收集key
    kb.start()
    keys = kb.waitKeys(maxWait=2, keyList=['left','right'])        #被试只有2s选择时间
    kb.stop()
    
    #反馈
    r = random.random()
    fcText = ''       #first choice text
    clstimText = ''               #second choice stimulus text
    if keys:
        if keys[0].name == 'left' :     #choose x
            if (spr < 0.5) and (plr <0.5) :# x,red
                if r>0.3:                                     #common transition
                    fcText = 'red planet'
                    clstimText = 'This is the red planet, left or right'
                else :                                         #rare transition
                    fcText = 'black planet'
                    clstimText = 'This is the black planet, left or right'
            if (spr < 0.5) and (plr >=0.5): #x,black
                if r> 0.3:
                    fcText = 'black planet'
                    clstimText = 'This is the black planet, left or right'
                else :
                    fcText = 'red planet'
                    clstimText = 'This is the red planet, left or right'
            if (spr >= 0.5) and (plr >=0.5): # y,red
                if r>0.3:
                    fcText = 'red planet'
                    clstimText = 'This is the red planet, left or right'
                else :
                    fcText = 'black planet'
                    clstimText = 'This is the black planet, left or right'
            if (spr >= 0.5)  and (plr <0.5) :#y,black
                if r>0.3:
                    fcText = 'red planet'
                    clstimText = 'This is the red planet, left or right'
                else :
                    fcText = 'black planet'
                    clstimText = 'This is the black planet, left or right'
        if keys[0].name == 'right':             #choose y
            if (spr >= 0.5) and (plr >=0.5):# y,red
                if r>0.3:
                    fcText = 'red planet'
                    clstimText = 'This is the red planet, left or right'
                else :
                    fcText = 'black planet'
                    clstimText = 'This is the black planet, left or right'
            if (spr >= 0.5)  and (plr <0.5) :#y,black
                if r>0.3:
                    fcText = 'black planet'
                    clstimText = 'This is the black planet, left or right'
                else :
                    fcText = 'red planet'
                    clstimText = 'This is the red planet, left or right'
            if (spr < 0.5) and (plr <0.5) :#x,red
                if r>0.3:
                    fcText = 'black planet'
                    clstimText = 'This is the black planet, left or right'
                else :
                    fcText = 'red planet'
                    clstimText = 'This is the red planet, left or right'
            if (spr < 0.5) and (plr >=0.5):#x,black
                if r>0.3:
                    fcText = 'red planet'
                    clstimText = 'This is the red planet, left or right'
                else :
                    fcText = 'black planet'
                    clstimText = 'This is the black planet, left or right'
    if not keys:
        core.quit()
    fcTex = visual.TextStim(win = win1, text = fcText, color= (-1,0,1))      #transition screen
    fcTex.draw()
    win1.flip()
    core.wait(1)
#=============second stage=============
#呈现图片刺激,第二次选择界面
    clstimTex = visual.TextStim(win =win1, text = clstimText, color=(-1,0,1))
    clstimTex.draw()
    win1.flip()
    core.wait(2)
    
#collect second choice
    kb.start()
    kb.waitKeys(maxWait = 2, keyList=['left','right'])
    kb.stop()
    
#给回报
    rwText = ''
    lPro = random.random()       #left side reward probability
    rPro = random.random()      #right side reward probability
    gPro = random.random()#gain reward probability
    if keys:
        if keys[0].name == 'left':
            if gPro < lPro:
                rwText = 'crystal'         #left side, reward
            else :
                rwText = 'sorry'
        if keys[0].name == 'right':    #right side, reward
            if gPro < rPro:
                rwText = 'crystal'
            else :
                rwText = 'sorry'
    if not keys:
        core.quit()
    rwTex = visual.TextStim(win = win1, text = rwText, color= (-1,0,1))
    rwTex.draw()
    win1.flip()
    core.wait(2)
    
#save data to csv
    
    
    