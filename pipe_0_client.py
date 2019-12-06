# -*- coding: utf-8 -*-
"""
---------- Client ----------

Created on Wed Dec  4 22:37:00 2019
@author: Virab
"""
import win32file, win32pipe, pywintypes

def pipe_client():
    try:
        print("trying to connect to the pipe...")
        handle = win32file.CreateFile(
            r'\\.\pipe\my_pipe',
            win32file.GENERIC_WRITE, #win32file.GENERIC_READ |
            0,
            None,
            win32file.OPEN_EXISTING,
            win32file.FILE_FLAG_OVERLAPPED,
            None
        )
        win32pipe.SetNamedPipeHandleState(handle, win32pipe.PIPE_READMODE_MESSAGE, None, None)


        # convert to bytes
        some_data = str.encode(f"English Text:\nThat's life, and as funny as it may seem\n\nGerman Text:\nNicht alles, was zählt, ist zählbar, und nicht alles, was zählbar ist, zählt\n\nRussian Text:\nЖить, как говорится, хорошо! -А хорошо жить - еще лучше! \n\nArmenian Text:\nԾերանալը ձանձրալի է, բայց դա երկար ապրելու միակ միջոցն է:", encoding="utf-8")#f"{count}")
        overlapped_obj = pywintypes.OVERLAPPED()
        print("sending the string...")
        win32file.WriteFile(handle, some_data, overlapped_obj)

    
    except pywintypes.error as e:
        if e.args[0] == 109:
            print("broken pipe")
    finally:
        print("closing handle")
        handle.Close()
               
pipe_client()