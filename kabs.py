import wx
import speech_recognition as sr
import pyttsx3
import wolframalpha
import wikipedia
import webbrowser
import os
import sys
import warnings

if not sys.warnoptions:
    warnings.simplefilter("ignore")

BRING_KEY = 'enter your api'

def speak(value):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[4].id)
    rate = engine.getProperty('rate')
    engine.setProperty('rate', rate-30)
    engine.say(value)
    engine.runAndWait()

#main class
class MyFrame(wx.Frame):
    def __init__(self):        
        #basic gui info 
        wx.Frame.__init__(self, None,
            pos=wx.DefaultPosition, size=wx.Size(550, 150),
            style=wx.MINIMIZE_BOX | wx.SYSTEM_MENU | wx.CAPTION |
            wx.CLOSE_BOX | wx.CLIP_CHILDREN,
            title="HeloBot")
        panel = wx.Panel(self)
        my_sizer = wx.BoxSizer(wx.VERTICAL)
        lbl = wx.StaticText(panel, 
        label="Hi! I am HeloBot your Digital Assistance. How can I help you?")
        my_sizer.Add(lbl, 0, wx.ALL, 5)
        #text box
        self.txt = wx.TextCtrl(panel, style=wx.TE_PROCESS_ENTER,size=(400,30))
        self.txt.SetFocus()
        self.txt.Bind(wx.EVT_TEXT_ENTER, self.OnEnter)
        my_sizer.Add(self.txt, 0, wx.ALL, 5)
        panel.SetSizer(my_sizer)
        self.Show()
        speak('Hi! I am Helo Bot your Digital Assistance. How can I help you?')
        
    def OnEnter(self, event):
            inputx = str(self.txt.GetValue())
            inputx = inputx.lower()
            if inputx == '':
                r = sr.Recognizer()
                with sr.Microphone() as source:
                    audio = r.listen(source)
                    
                try:
                    inputx = r.recognize_google(audio)
                    inputx = inputx.lower()
                    self.txt.SetValue(inputx)

                except sr.UnknownValueError:
                    print("Bring Speech Recognition could not understand audio")
                except sr.RequestError as e:
                    print("Could not request results from Bring Recognition service; {0}"
                      .format(e))
                    
            #elif inputx.startswith('search '):
             #   try:
              #      inputx = '+'.join(inputx[1:])
               #     say = inputx.replace('+', ' ')
                # print(link)
                #    speak("searching on google for " + say)
                 #   webbrowser.open('https://www.google.co.in/search?q=' + inputx)
               # except Exception as e:
                #    print (str(e))
            
            else:
                try:
                    #wolframalpha
                    app_id = "Enter your API"
                    client = wolframalpha.Client(app_id)
                    res = client.query(inputx)
                    #res.replace("Wolfram|Alpha","Chipo")
                    answer = (next(res.results).text).replace("My name is Wolfram|Alpha","Hi! My name is HeloBot. Designed and developed by Kabs. I can do what a normal bot does and help you in the world of Internet.")
                    if(answer.find('I was created by Stephen Wolfram')!=-1):
                        answer = 'I was made by Kabs.'
                    print (answer)
                    speak (answer)
                except:
                    try:
                        # wikipedia
                        #inputx = inputx.split(' ')
                        #inputx = ' '.join(inputx[2:])
                        #inputz = wikipedia.search(inputx)
                        res = wikipedia.summary(inputx, sentences=2)
                        speak ('Searched wikipedia for '+inputx)
                        print (res)
                        speak(str(res))
                        
                        
                    except:
                        #inputx = '+'.join(inputx[1:])
                        speak("searching on google for " + inputx)
                        say = inputx.replace(' ', '+')
                        webbrowser.open('https://www.google.co.in/search?q=' + inputx)
                        
# Trigger GUI
if __name__ == '__main__':
    app = wx.App(True)
    frame = MyFrame()
    app.MainLoop()
    
