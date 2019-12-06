# -*- coding: utf-8 -*-
"""
---------- Server ----------

Created on Wed Dec  4 22:27:34 2019
@author: Virab
"""

import time
import win32pipe, win32file, pywintypes
import codecs



def pipe_server():
    pipe = win32pipe.CreateNamedPipe(
        r'\\.\pipe\my_pipe',
        win32pipe.PIPE_ACCESS_INBOUND | win32file.FILE_FLAG_OVERLAPPED,
        win32pipe.PIPE_TYPE_MESSAGE | win32pipe.PIPE_READMODE_MESSAGE | win32pipe.PIPE_WAIT,
        1, 65536, 65536,
        0,
        None)
    quit = False
    overlapped_obj1 = pywintypes.OVERLAPPED()
    
    completion_port = win32file.CreateIoCompletionPort(pipe, None, 0, 0)
    
    while not quit:
        try:
            win32pipe.ConnectNamedPipe(pipe, overlapped_obj1)
        
            while True:    # Doing some sleep (2 seconds): Actually, other things could be done in this time          
                for i  in range(10):    
                    time.sleep(0.2)
                
                # If the function succeeds, rc will be set to 0, otherwise it will be set to the win32 error code (258).
                (rc, byte_num, key, ovrlpd) = win32file.GetQueuedCompletionStatus(completion_port, 50)#1000)

                if rc == 0: # The message can be retrieved 
                    msg = ''  # Will contain the whole message at the end
                    """
                    in order to read the characters we need to distinguish two cases:
                        -the character is a normal (unicode) character, which takes 1 byte
                        -the character is non_unicode (German, Russian...), which takes 2 bytes
                    as we are reading 1 byte at a time, the above-mentioned discussion is essential.
                    When a 1 byte character is coming, its decoding is done without problems.
                    Let's see what happens, when a 2-byte character is coming. In this case, we read
                    1 byte, try to decode, get an error. Now we know that the character takes 2-bytes.
                    Then, we read 1 byte again, combine them and decode.
                    """
                    # 1-byte character case
                    try:    
                        rtnvalue, data = win32file.ReadFile(pipe, 1, overlapped_obj1)
                        msg = msg + bytes(data).decode("utf-8")                  
                    # 2-bytes character case
                    except:
                        rtnvalue, data1 = win32file.ReadFile(pipe, 1, overlapped_obj1)
                        non_unicode = data.tobytes() + data1.tobytes()
                        msg = msg + non_unicode.decode("utf-8")

                    while rtnvalue == 234: # more data is available
                        
                        try: # 1-byte character case
                            rtnvalue, data = win32file.ReadFile(pipe, 1, overlapped_obj1)
                            msg = msg + bytes(data).decode("utf-8")

                        except: # 2-bytes character case
                            rtnvalue, data1 = win32file.ReadFile(pipe, 1, overlapped_obj1)
                            non_unicode = data.tobytes() + data1.tobytes()                          
                            msg = msg + non_unicode.decode("utf-8")

                            
                    # the next line helps with writing Russian and Armenian characters into a text file
                    with codecs.open('test.txt', 'w', encoding='utf-8') as f:  
                        f.write(msg)
                    f.close()
                    print("Successfully received and written")
                    print("Closing Handle") 
                    exit (0)
                    

        except pywintypes.error as e:
            if e.args[0] == 109:
                print("broken pipe")
                quit = True
            else:
                print(e)
                quit = True          
    win32file.CloseHandle(pipe)
    
pipe_server()