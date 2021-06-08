# -*- coding: utf-8 -*-
"""
Created on Wed Jun  2 08:52:09 2021

@author: MkZee
"""

import tkinter as tk
import tkinter.ttk as ttk
import tkinter.filedialog as fdl
    


class M2eFrame(tk.LabelFrame):
    """
    Gui to configure and run a M2E Latency Test
    
    strvars : StringVarDict
    loads and stores the values in the controls
    
    """
       
    
    def __init__(self, btnvars, text='Mouth-to-Ear Latency Test',
                 *args, **kwargs):
        #sets what controls will be in this frame
        controls = (
            test,
            audio_file,
            trials,
            bgnoise_file,
            bgnoise_volume,
            ptt_wait,
            overplay,
            outdir,
            advanced
            )
        
        
        
        super().__init__(*args, text=text, **kwargs)
        #option functions will get and store their values in here
        self.btnvars = btnvars
        
        
        #initializes controls
        for row in range(len(controls)):
            controls[row](master=self, row=row)
        
           
   
            
class M2EAdvancedConfigGUI(tk.Toplevel):
    """Advanced options for the M2E test
    

    """    
    
    def __init__(self, master, btnvars, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.master = master
        
        self.title('Advanced')
        #sets the controls in this window
        controls = (
            radioport,
            blocksize,
            buffersize,
            _advanced_submit
            )
        
        self.btnvars = btnvars
        
        #Sets window on top of other windows
        self.attributes('-topmost', True)
        
        #initializes controls
        for row in range(len(controls)):
            controls[row](master=self, row=row)
        
        
        # return key closes window
        self.bind('<Return>', lambda *args : self.destroy())
        
        #sets focus on the window
        self.focus_force()
        
            
        
        
        
        
        #------------------ Controls ----------------------
class LabeledControl():
    """A one-row grid consisting of a label, control, and optional 2nd control
    
    row : int
        the row that the controls should be gridded in
    
    """
    text = ''
    
    
    MCtrl = ttk.Entry
    MCtrlargs = []
    MCtrlkwargs = {}
    
    variable_arg = 'textvariable'
    
    #usually the browse button
    RCtrl = None
    RCtrlkwargs = {}
    
    padx = 5
    pady = 10
    
    def __init__(self, master, row):
        self.master = master
        
    
        ttk.Label(master, text=self.text).grid(
            column=0, row=row, sticky='E')
        
        MCtrlkwargs = self.MCtrlkwargs.copy()
        MCtrlargs = self.MCtrlargs.copy()
        RCtrlkwargs = self.RCtrlkwargs.copy()
        
        try:
            self.btnvar = master.btnvars[self.__class__.__name__]
        except KeyError:
            self.btnvar = None
            
            
        # some controls require the textvariable=... to be positional
        
        #some controls require more flexibility, so they don't use self.MCtrl
        if self.MCtrl:
            if self.variable_arg:
                MCtrlkwargs[self.variable_arg] = self.btnvar
            
            else:
                MCtrlargs.insert(0, self.btnvar)
                
            
            # initialize the control
            self.MCtrl(master, *MCtrlargs, **MCtrlkwargs).grid(
                column=1, row=row, padx=self.padx, pady=self.pady, sticky='WE')
        
        
        if self.RCtrl:
            #add command to button
            if self.RCtrl in (ttk.Button, tk.Button):
                RCtrlkwargs['command'] = self.on_button
            
            self.RCtrl(master, **RCtrlkwargs).grid(
                column=2, row=row, sticky='WE')
            
            
            
    def on_button(self):
        pass
            


class test(LabeledControl):
    text = 'Test Type:'
    
    variable_arg = None # indicates the argument is positional
    MCtrl = ttk.OptionMenu
    MCtrlargs = ['', 'm2e_1loc', 'm2e_2loc_rx', 'm2e_2loc_tx']
    
    
class audio_file(LabeledControl):
    
    def on_button(self):
        fp = fdl.askopenfilename(parent=self.master,
                initialfile=self.btnvar.get(),
                filetypes=[('WAV files', '*.wav')])
        if fp:
            self.btnvar.set(fp)
    
    
    text='Audio File:'
    RCtrl = ttk.Button
    RCtrlkwargs = {
        'text'   : 'Browse...'
        }
    
    
class trials(LabeledControl):
    text = 'Number of Trials:'
    MCtrl = ttk.Spinbox
    MCtrlkwargs = {'from_' : 1, 'to' : 2**15 - 1}
    

class radioport(LabeledControl):
    text = 'Radio Port:'
    
    
    
class bgnoise_file(LabeledControl):
    text = 'Background Noise File:'
    
    RCtrl = ttk.Button
    RCtrlkwargs = {'text' : 'Browse...'}
    
    def on_button(self):
        fp = fdl.askopenfilename(parent=self.master,
            initialfile=self.btnvar.get(),
            filetypes=[('WAV files', '*.wav')])
        if fp:
            self.btnvar.set(fp)


class bgnoise_volume(LabeledControl):
    text = 'Background Noise Volume:'
    RCtrl = None
    MCtrl = None
    
    def __init__(self, master, row, *args, **kwargs):
        super().__init__(master, row, *args, **kwargs)
        self.txtvar = _bgnoise_volume_percentage()
        self.on_change()
        
        self.btnvar.trace_add('write', self.on_change)
    
        ttk.Label(master, textvariable=self.txtvar).grid(
            column=2, row=row, sticky='W')
    
        ttk.Scale(master, variable=self.btnvar,
            from_=0, to=1).grid(
            column=1, row=row, padx=self.padx, pady=self.pady, sticky='WE')
    
    def on_change(self, *args, **kwargs):
        #updates the percentage to match the value of the slider
        self.txtvar.set(self.btnvar.get())

class _bgnoise_volume_percentage(tk.StringVar):
    """Displays a percentage instead of a float
    
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    def set(self, value):
        v = float(value) * 100
        s = ''
        
        for char in str(v):
            if char == '.':
                break
            s = f'{s}{char}'
        
                    
        super().set(f'{s}%')
            
        
class ptt_wait(LabeledControl):
    text = 'PTT Wait Time (sec):'
    
    MCtrl = ttk.Spinbox
    MCtrlkwargs = {'increment' : 0.01, 'from_' : 0, 'to' : 2**15 - 1}

              
                                  
class blocksize(LabeledControl):
    text = 'Block Size:'
    

class buffersize(LabeledControl):
    text='Buffer Size:'
    
class overplay(LabeledControl):
    text='Overplay Time (sec):'
    MCtrl = ttk.Spinbox
    MCtrlkwargs = {'increment':0.01, 'from_':0, 'to':2**15 -1}

class outdir(LabeledControl):
    text='Output Folder:'
    
    RCtrl = ttk.Button
    RCtrlkwargs = {'text': 'Browse...'}
    
    def on_button(self):
        dirp = fdl.askdirectory(parent=self.master)
        if dirp:
            self.btnvar.set(dirp)

class advanced(LabeledControl):
    text = ''
    
    MCtrl = None
    RCtrl = ttk.Button       
    RCtrlkwargs = {'text': 'Advanced...'}
    
    def on_button(self):
        M2EAdvancedConfigGUI(btnvars=self.master.btnvars)

    

class _advanced_submit(LabeledControl):
    
    #closes the advanced window
    MCtrl = None
    RCtrl = ttk.Button
    RCtrlkwargs = {'text': 'OK'}
    
    def on_button(self):
        self.master.destroy()
    
    
    
    
    
