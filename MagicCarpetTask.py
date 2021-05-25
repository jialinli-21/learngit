from psychopy import visual,core,monitors,event,data
from psychopy.hardware import keyboard
from time import localtime, strftime
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


#定义data的变量
mounDir = [0,1] #0,pink mountain; 1, blue mountain
transDir = [0,1]  #0, common transition; 1, rare transistion
elfDir= [0,1]       #0,A elf; 1,B elf
rewardDir = [0,1]  #0, 无reward；1，有reward
nTrialsPerCon = 3 #how many trials per condition

nTrials = nTrialsPerCon*len(mounDir)*len(transDir)*len(elfDir)*len(rewardDir)
stimList = []
for moun in mounDir:
    for trans in transDir:
        for elf in elfDir:
            for reward in rewardDir:
                stimList.append({'mountain':moun, 'transition':trans, 'elfs':elf, 'rewardDir':reward})
trials = data.TrialHandler(stimList, nTrialsPerCon)


#openwindow
win1 = visual.Window([1000,800], monitor="testMonitor",  units="pix",fullscr = False)

#define welcome instruction interface
instrText=\
    '欢迎参加这个实验！\n\
    您将选择一块魔毯前往魔山\n\
    左键和右键分别代表了粉山和蓝山\n\
    如果您理解了以上内容，请按空格键继续'
tex = visual.TextStim(win=win1, text=instrText, color=(-1,-1,-1),wrapWidth=10)
tex.draw()
win1.flip()
kb.start()
event.waitKeys(keyList=['space'])
kb.stop()

#  =========== exercise loop ========
#呈现魔毯图片刺激（先用文字刺激代替）
isCommon = True #第一次左粉右蓝，下一次实验反转    （偶数次左粉右蓝）
def test()
    for trial in trials:  #练习开始,trialHandler
        #first stage
        tex1 = visual.TextStim(win=win1,text='press left or right to choose moutain',color=(-1,0,1))#选择魔山的文字刺激
        tex1.draw()
        win1.flip()
        r = random.random()
        #开始输入key
        kb.start()
        keys = kb.waitKeys(maxWait=2, keyList=['left','right'])        #被试只有2s选择时间
        kb.stop()
        #拿到key，开始判断
        instrText1 = ''
        if keys:
            if keys[0].name == 'left':      #pink mountain
                if (r>= 0.3) and isCommon:
                    instrText1 = 'pink mountain'
                else:
                    instrText1 = 'blue mountain'
            if keys[0].name == 'right':         #blue mountain
                if (r>= 0.3) and isCommon:
                    instrText1 = 'blue mountain'
                else:
                    instrText1 = 'pink moutain'
        #如果拿不到key,退出             如何退回到上一个循环？
        if not keys:
            core.quit()
    #反馈
        tex2 = visual.TextStim(win=win1, text = instrText1, color = (-1,0,1))
        tex2.draw()
        win1.flip()
        core.wait(1)

    #second stage
    #呈现图片刺激（暂时文字刺激代替)，选择A精灵还是B精灵
        tex3 = visual.TextStim(win=win1, text='press a or b to choose elf',color=(-1,0,1))
        tex3.draw()
        win1.flip()
        instrText2 = 'gold coin' or 'sorry'
        r1 = random.random()      #A精灵给回报的概率
        r2 = random.random()     #B精灵给回报的概率
        r0 = random.random()     #被试此时的概率
    #用户第二次输入
        kb.start()
        kb.waitKeys(maxWait = 2, keyList=['a','b'])
        kb.stop()
    #开始判断
        if keys:
            if (keys[0].name == 'a') and (r0<r1):
                instrText2 = 'gold coin'
            else :
                instrText2 = 'sorry'
            if (keys[0].name == 'b') and (r0<r2):
                instrText2 = 'gold coin'
            else :
                instrText2 = 'sorry'
        #如果拿不到key，退出
        if not keys:
            core.quit()
    #开始反馈
        tex4 = visual.TextStim(win = win1, text=instrText2, color=(-1,0,1))
        tex4.draw()
        win1.flip()
        core.wait(1)       #反馈时间
        isCommon = not isCommon    #reverse
        #save data in this trial
        trials.addData('moun', 0 if instrText1 == 'pink mountain' else 1)
        trials.addData('trans', 0 if r>= 0.3 else 1)
        trials.addData('elf', 0 if keys[0].name == 'a' else 'b')
        trials.addData('reward', 0 if instrText1 == 'sorry' else 1)

    if wantSave:#save data
        #we want to save first choice, transition, second choice, reward
        fileName = strftime('%Y%m%d%H%M%S', localtime())
        fileName = f'{fileName}_{expName}_{subjID}'
        # Save more information into a numpy file 
        dataInfo = '''
            mountain: 0,pink; 1, blue \n
            transition: 0, common transition; 1, rare transistion \n
            second choice: 0,A elf; 1,B elf \n
            reward:0, 无reward；1，有reward
        '''
        # create a result dict
        trials.extraInfo={
            'subjID': subjID,
            'dataInfo': dataInfo,
            'expName': expName,
            'time': strftime('%Y-%m-%d-%H-%M-%S', localtime()),
        }
        #trials.printAsText()
        trials.saveAsExcel(fileName=fileName, sheetName='rawData') # save as excel
        trials.saveAsPickle(fileName=fileName) # # save as pickle

win1.close()
core.quit()