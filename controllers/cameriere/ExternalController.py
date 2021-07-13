import time

class ExternalController:

    def __init__(self, keyboard):
        self.keyboard = keyboard
        self.status = False
        self.motionStatus = None
        self.orderlist = []
        self.table=None

    def update(self):
        self.currentkey = None
        return self.updateCommands()

    def getMotionStatus(self):
        return self.motionStatus
    
    def setMotionStatus(self, motionstatus):
        self.motionStatus = motionstatus
    
    def emptyorderlist(self):
        self.orderlist = []

    def getTable(self):
        print("TAVOLO: "+ str(self.table))
        return self.table

    def updateCommands(self):
        self.keyboard.update()
        
        # get current key
        self.currentkey = self.keyboard.getKey()

        # Start
        if self.keyboard.isKeyPressed(self.currentkey, '1'):
            print(chr(27) + "[2J")
            if(len(self.orderlist) < 2):
                self.orderlist.append(chr(self.currentkey))
                print(str(''.join(self.orderlist)))
                time.sleep(1)
            else:
                print('Table number must be between 1 and 11!')
        
        elif self.keyboard.isKeyPressed(self.currentkey, '2'):
            print(chr(27) + "[2J")
            if(len(self.orderlist) < 2):
                self.orderlist.append(chr(self.currentkey))
                print(str(''.join(self.orderlist)))
                time.sleep(1)
            else:
                print('Table number must be between 1 and 11!')
        
        elif self.keyboard.isKeyPressed(self.currentkey, '3'):
            print(chr(27) + "[2J")
            if(len(self.orderlist) < 2):
                self.orderlist.append(chr(self.currentkey))
                print(str(''.join(self.orderlist)))
                time.sleep(1)
            else:
                print('Table number must be between 1 and 11!')
        
        elif self.keyboard.isKeyPressed(self.currentkey, '4'):
            print(chr(27) + "[2J")
            if(len(self.orderlist) < 2):
                self.orderlist.append(chr(self.currentkey))
                print(str(''.join(self.orderlist)))
                time.sleep(1)
            else:
                print('Table number must be between 1 and 11!')
        
        elif self.keyboard.isKeyPressed(self.currentkey, '5'):
            print(chr(27) + "[2J")
            if(len(self.orderlist) < 2):
                self.orderlist.append(chr(self.currentkey))
                print(str(''.join(self.orderlist)))
                time.sleep(1)
            else:
                print('Table number must be between 1 and 11!')
        
        elif self.keyboard.isKeyPressed(self.currentkey, '6'):
            print(chr(27) + "[2J")
            if(len(self.orderlist) < 2):
                self.orderlist.append(chr(self.currentkey))
                print(str(''.join(self.orderlist)))
                time.sleep(1)
            else:
                print('Table number must be between 1 and 11!')
        
        elif self.keyboard.isKeyPressed(self.currentkey, '7'):
            print(chr(27) + "[2J")
            if(len(self.orderlist) < 2):
                self.orderlist.append(chr(self.currentkey))
                print(str(''.join(self.orderlist)))
                time.sleep(1)
            else:
                print('Table number must be between 1 and 11!')
        
        elif self.keyboard.isKeyPressed(self.currentkey, '8'):
            print(chr(27) + "[2J")
            if(len(self.orderlist) < 2):
                self.orderlist.append(chr(self.currentkey))
                print(str(''.join(self.orderlist)))
                time.sleep(1)
            else:
                print('Table number must be between 1 and 11!')
        
        elif self.keyboard.isKeyPressed(self.currentkey, '9'):
            print(chr(27) + "[2J")
            if(len(self.orderlist) < 2):
                self.orderlist.append(chr(self.currentkey))
                print(str(''.join(self.orderlist)))
                time.sleep(1)
            else:
                print('Table number must be between 1 and 11!')
        
        elif self.keyboard.isKeyPressed(self.currentkey, '0'):
            print(chr(27) + "[2J")
            if(len(self.orderlist) < 2):
                self.orderlist.append(chr(self.currentkey))
                print(str(''.join(self.orderlist)))
                time.sleep(1)
            else:
                print('Table number must be between 1 and 11!')
                
        elif self.keyboard.isKeyPressed(self.currentkey, '\4'):
            print(chr(27) + "[2J")
            if(1 <= len(self.orderlist) <= 2):
                table = int(''.join(self.orderlist))
                self.emptyorderlist()
                if( 0 < table < 12):
                    self.motionStatus = 99
                    self.table=table                
                else:
                    print('Tavolo inesistente.')
                    
            else:
                self.emptyorderlist()
                print('Per favore, inserire un numero compreso tra 1-11.')

    
    def isEnabled(self):
            return self.status != 0

    def enable(self):
        self.status = True

    def disable(self):
        self.status = False
