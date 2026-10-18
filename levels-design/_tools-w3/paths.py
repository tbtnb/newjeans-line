import os
TOOLS=os.path.dirname(os.path.abspath(__file__))
WORK=os.path.join(TOOLS,'work')
REPO=os.path.abspath(os.path.join(TOOLS,'..','..'))
OUT=os.path.join(REPO,'levels-design')
AUDIO=os.path.join(REPO,'public','audio')
os.makedirs(WORK,exist_ok=True)
