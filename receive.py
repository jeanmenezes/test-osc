""" receiving OSC with pyOSC
https://trac.v2.nl/wiki/pyOSC
example by www.ixi-audio.net based on pyOSC documentation

this is a very basic example, for detailed info on pyOSC functionality check the OSC.py file
or run pydoc pyOSC.py. you can also get the docs by opening a python shell and doing
>>> import OSC
>>> help(OSC)
"""


import pygame, pygame.gfxdraw
import OSC
import time, threading
import random

screen = pygame.display.set_mode((1000, 300))


# tupple with ip, port. i dont use the () but maybe you want -> send_address = ('127.0.0.1', 9000)
receive_address = 'localhost', 6449


# OSC Server. there are three different types of server.
s = OSC.OSCServer(receive_address) # basic
##s = OSC.ThreadingOSCServer(receive_address) # threading
##s = OSC.ForkingOSCServer(receive_address) # forking


# this registers a 'default' handler (for unmatched messages),
# an /'error' handler, an '/info' handler.
# And, if the client supports it, a '/subscribe' & '/unsubscribe' handler
s.addDefaultHandlers()


# define a message-handler function for the server to call.
def printing_handler(addr, tags, stuff, source):
    rgb = (int(stuff[1]) * 2)
    if rgb < 255:
        cinza = [rgb, rgb, rgb]
        thick = False
    else:
        cinza = [random.randint(1, 255), random.randint(1, 255), \
            random.randint(1, 255), 111]
        thick = True
    if thick:
        pygame.gfxdraw.filled_circle(screen, int(stuff[0] + 64), \
            (278 - int(stuff[1])), int(random.randint(80, 120) - \
            (stuff[2] * 128)), tuple(cinza))
    else:
        pygame.gfxdraw.aacircle(screen, int(stuff[0] + 64), \
            (278 - int(stuff[1])), int(149 - (stuff[2] * 128)), \
            tuple(cinza))
    pygame.display.flip()

s.addMsgHandler("/print", printing_handler) # adding our function


# just checking which handlers we have added
print "Registered Callback-functions are :"
for addr in s.getOSCAddressSpace():
    print addr


# Start OSCServer
print "\nStarting OSCServer. Use ctrl-C to quit."
st = threading.Thread( target = s.serve_forever )
st.start()


try :
    while 1 :
        time.sleep(5)
except KeyboardInterrupt :
    print "\nClosing OSCServer."
    s.close()
    print "Waiting for Server-thread to finish"
    st.join() ##!!!
    print "Done"
