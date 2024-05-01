### How does the DevBoard handle received serial messages? How does this differ from the naïve approach?
The Devboard receives handles serial messages using an event driven approach, which checks to see if the Serial POrt's receive buffer is not empty.The naiive approach would be the be polling the serial port constantly looking for new data, since this is inefficient and could have delays. 
### What does `detached_callback` do? What would happen if it wasn't used?
The detached_callback decorator makes sure that the functions are executed in a separate thread, so if a button isn't responding it doesn't stall the entire GUI. 
### What does `LockedSerial` do? Why is it _necessary_?
LockedSerial is for thread safety to avoid race conditions where two different threads are trying to talk to the same port and have conflicts. LockedSerial makes sure each thread is opened and closed one at a time. 
