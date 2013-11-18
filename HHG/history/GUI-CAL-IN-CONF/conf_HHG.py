#!/usr/bin/python2.7


import sys
from gi.repository import Gtk, GObject
import glob
import time, datetime, os
import subprocess
from math import exp

class configure:

    def getSysTime(self, sysTimeEntry, sysTime, stpTime):
    	sysTime = datetime.datetime.now()
    	sysTimeEntry.set_text(sysTime.strftime("%Y-%m-%d %H:%M:%S"))
	stpTime.insert(0,sysTime.year)
	stpTime.insert(1,sysTime.month)
	stpTime.insert(2,sysTime.day+7)

    def chooseHHG(self, idEntry, rleCombo, rangeCombo, powCombo, freqCombo, modeCombo, sysTimeEntry, sysTime, stpTime, lastStartEntry, lastStpEntry):
	confhhg_path = sys.argv[1] 
	print(confhhg_path)	
        with open (confhhg_path,"r") as confhhg:
               confhhg.seek(0,0)
               idChar = confhhg.read(4)
               idEntry.set_text(idChar)
	       confhhg.seek(8,0)
	       rleCombo.set_active(int(confhhg.read(1)))
	       confhhg.seek(12,0)
	       rangeCombo.set_active(int(confhhg.read(1)))
	       freqCombo.set_active(int(confhhg.read(1)))
	       modeCombo.set_active(int(confhhg.read(1)))
	       powCombo.set_active(int(confhhg.read(1)))			       			
	       self.getSysTime(sysTimeEntry, sysTime, stpTime) 
	       confhhg.seek(59,0)	
	       lastStartTimeChar = confhhg.read(8)
	       lastStartTimeDec = [ord(lastStartTimeChar[0]),ord(lastStartTimeChar[3]),ord(lastStartTimeChar[2]),
                                ord(lastStartTimeChar[4]),ord(lastStartTimeChar[7]),ord(lastStartTimeChar[6])]
	       lastStartEntry.set_text("20%d-%d-%d %d:%d:%d" % (lastStartTimeDec[0],lastStartTimeDec[1],lastStartTimeDec[2],
							       lastStartTimeDec[3],lastStartTimeDec[4],lastStartTimeDec[5]))
	       confhhg.seek(70,0)	
	       lastStpTimeChar = confhhg.read(8)
	       lastStpTimeDec = [ord(lastStpTimeChar[0]),ord(lastStpTimeChar[3]),ord(lastStpTimeChar[2]),
                                ord(lastStpTimeChar[4]),ord(lastStpTimeChar[7]),ord(lastStpTimeChar[6])]
	       lastStpEntry.set_text("20%d-%d-%d %d:%d:%d" % (lastStpTimeDec[0],lastStpTimeDec[1],lastStpTimeDec[2],
							     lastStpTimeDec[3],lastStpTimeDec[4],lastStpTimeDec[5]))
	       confhhg.close()


    def syncSettings(self, idEntry, rleCombo, rangeCombo, powCombo, freqCombo, modeCombo, sysTimeEntry, sysTime, stpTime):
	confhhg_path = sys.argv[1]
	if (stpTime[0]<sysTime.year) or (stpTime[0]==sysTime.year and stpTime[1]<sysTime.month) or (stpTime[0]==sysTime.year and 
						stpTime[1]==sysTime.month and stpTime[2]<sysTime.day):
		self.getSysTime(sysTimeEntry, sysTime, stpTime)
	      	 
	idChar = idEntry.get_text();
	with open (confhhg_path,"r+w") as confhhg:
		confhhg.seek(0,0)   # Write ID
		confhhg.write(idChar[0])
		confhhg.write(idChar[1])
		confhhg.write(idChar[2])
		confhhg.write(idChar[3])
		confhhg.seek(4,0) # Write RLE Delta
 		confhhg.write(str(rleCombo.get_active()))
		confhhg.seek(12,0)  # Write ACC Settings
		confhhg.write(str(rangeCombo.get_active()))
		confhhg.write(str(freqCombo.get_active()))
		confhhg.write(str(modeCombo.get_active()))
		confhhg.write(str(powCombo.get_active()))
		confhhg.seek(59,0)  # Write System Time
		confhhg.write(chr(sysTime.year-2000))
		confhhg.write(chr(0))
		confhhg.write(chr(sysTime.day))
		confhhg.write(chr(sysTime.month))
		confhhg.write(chr(sysTime.hour))
		confhhg.write(chr(0))
		confhhg.write(chr(sysTime.second))
		confhhg.write(chr(sysTime.minute))
		confhhg.seek(70,0)  # Write Stop Time
                confhhg.write(chr(stpTime[0]-2000))
                confhhg.write(chr(0))
                confhhg.write(chr(stpTime[2]))
                confhhg.write(chr(stpTime[1])) # Month
                confhhg.write(chr(sysTime.hour))
                confhhg.write(chr(0))
                confhhg.write(chr(sysTime.second))
                confhhg.write(chr(sysTime.minute))
		confhhg.close()
		sys.exit()

class conf_HHG_dialog:
          	
    def __init__( self ):
	self.confer = configure()
        self.builder = Gtk.Builder()
        self.builder.add_from_file("/home/hany/HedgeHog/nocdc/HHG/Conf.ui")
        self.window = self.builder.get_object("HedgeHog")
        self.window.set_title("HedgeHog Configuration")
        self.window.show_all()
	
        self.cal = self.builder.get_object("Cal")
        self.idEntry = self.builder.get_object("IDEntry")
        self.sysTimeEntry = self.builder.get_object("SysTimeEntry")
	self.lastStartEntry = self.builder.get_object("LastStart")
	self.lastStpEntry = self.builder.get_object("LastStop")
	self.rangeCombo = self.builder.get_object("RangeCombo")
	self.powCombo = self.builder.get_object("PowCombo")
	self.freqCombo = self.builder.get_object("FreqCombo")
	self.compCombo = self.builder.get_object("CompCombo")
	self.rleCombo = self.builder.get_object("RLECombo")
	self.modeCombo = self.builder.get_object("ModeCombo")

	self.stpTime = []
    	self.sysTime = datetime.datetime.now()
	self.ranges = ["-2 to +2 g","-4 to +4 g","-8 to +8 g","-16 to +16 g"]    
	self.freqs =  ["0.1Hz","5Hz","10Hz","25Hz","50Hz","100Hz","0.2kHz","0.4kHz",
			"0.8kHz","1.5kHz"]
	self.pows = ["normal","low-power","auto-sleep","low / auto"]
	self.comps = ["none (raw data)", "mean/variance","emSWAB","tap features"]	
	self.mods = ["mirco-controller sampling", "on-chio FIFO, raw sampling"] 
	self.deltas = ["0","1","2","3","4","5","6","7"]

        dic = { 
           "on_HedgeHog_destroy" : self.Quit,
           "on_SysTimeButton_clicked": self.SysTimeButtonClick,
           "on_SyncButton_clicked": self.SyncButtonClick,
	   "on_Cal_day_selected_double_click": self.CalDayClick,
        }
        self.builder.connect_signals(dic)

	for rang in self.ranges:
	    self.rangeCombo.append_text(rang)

	for freq in self.freqs:
	    self.freqCombo.append_text(freq)	
		
	for power in self.pows:
	    self.powCombo.append_text(power)		
				
	for comp in self.comps:
	    self.compCombo.append_text(comp)	
			
	for delta in self.deltas:
	    self.rleCombo.append_text(delta)
			
	for mod in self.mods:
	    self.modeCombo.append_text(mod)

	self.confer.chooseHHG(self.idEntry, self.rleCombo, self.rangeCombo, self.powCombo, self.freqCombo, self.modeCombo, self.sysTimeEntry, self.sysTime, self.stpTime, 			   					self.lastStartEntry,self.lastStpEntry)					   		
	
	self.cal.clear_marks()
   	self.cal.select_month(self.stpTime[1]-1, self.stpTime[0])	
	self.cal.mark_day(self.stpTime[2])

    	

    def HHGReadSettings(self, widget):
	self.confer.chooseHHG(self.idEntry, self.rleCombo, self.rangeCombo, self.powCombo, self.freqCombo, self.modeCombo, self.sysTimeEntry, self.sysTime, self.stpTime, 			   					self.lastStartEntry,self.lastStpEntry)

    def SysTimeButtonClick(self, widget):
	self.confer.getSysTime(self.sysTimeEntry, self.sysTime, self.stpTime)
	
    def CalDayClick(self, widget): 
	self.cal.clear_marks()
	self.stpTime = list(self.cal.get_date())
	self.stpTime[1] = self.stpTime[1]+1	
	self.cal.mark_day(self.stpTime[2])

    def SyncButtonClick(self, widget):
   	self.confer.syncSettings(self.idEntry, self.rleCombo, self.rangeCombo, self.powCombo, self.freqCombo, self.modeCombo, self.sysTimeEntry, self.sysTime, self.stpTime)
    		    		
    def Quit(self, widget):
        sys.exit(0)

	
hhg_dialog = conf_HHG_dialog()
Gtk.main()

