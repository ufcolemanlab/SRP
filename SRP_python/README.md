# SRP
SRP GUI for Python

Suggested "to do" list  

1) Multi-window layout (JEC)  
2) Make sure "slider" values update appropriately with selected file/session;   
    but I guess this means you need some kind of way to deal with multiple selected files with different parameters (gray out?)  

7/6/16 - The new slider values seem to update appropriately and carryover to the saved MAT file. 
NOTE:  But, there is ‘cross-talk’ when I adjust sliders for grand averages vs individual sessions.  I.e. All adjustments look good when I just go through and select filename(s) (top list) OR individuals/groups of sessions (bottom list). But, if I select file (top list) and adjust sliders for grand average (e.g., ‘A’), the new window applies to ALL sessions for ALL files (but the data saves the correct way, i.e. the grand average changes show up OK, but sessions are “default” values).  By contrast, if I then go back in, select session files, adjust window for selected, then the grand average window selection gets overwritten with new session window.  

I think we need more radio buttons for whether to apply window adjustment to grand average(s) or sessions only.  Basically, need to distinguish whether window adjustments apply to 1) Grand averages all or selected ‘A’ and ‘B’; 2) Grand average of all or selected ‘A’ only; 3) Grand average of all or selected ‘B’ only; 4) ALL session amplitudes; 5) SELECTED session amplitudes only.  

Suggestion:  Label top list box “FILES”, bottom box “SESSIONS”
 
3) Add a way to create unique file name when saving data (prompt?  blank space next to?).
