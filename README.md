# Named_Pipe
Asynchronous communication via named pipes in Windows
The server creates a named pipe for asynchronous communication and then listens to the messages on this pipe in an asynchronous way 
(using GetQueuedCompletionStatus and doing some sleep if no data was received on a loop iteration). As soon as the server reads 
a message from the pipe, it writes this message to a text file and terminates. The client connects to the named pipe and sends 
a message via the pipe. The message is encoded in UTF-8 encoding. It contains non-Unicode characters from different Windows code pages 
(e.g. German umlauts and Russian characters in a single string).
