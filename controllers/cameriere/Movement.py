class Movement:
    def __init__(self,positioning,lmotor,rmotor,collisionAvoidance):
        self.positioning=positioning
        self.lmotor=lmotor
        self.rmotor=rmotor
        self.positioning.update()
        self.collisionAvoidance=collisionAvoidance
        self.collisionAvoidance.update()
        self.isRotating=0

    def rotate(self):
        self.rmotor.setVelocity(-1.00)
        self.lmotor.setVelocity(1.00)
    
    def movement(self):
        self.rmotor.setVelocity(3.00)
        self.lmotor.setVelocity(3.00)
    
    def update(self):
        print(self.positioning.getOrientation())
        self.collisionAvoidance.update()
        if(self.collisionAvoidance.getCollision() and not self.isRotating):
            self.isRotating=1
            self.rotate()
            print(self.isRotating,"ciao")
        elif(self.isRotating and self.positioning.getOrientation()>180.0 ): #aggiungere orientazione della collisione e quindi controllare l'orientazione finale
            self.isRotating=0
        elif(not self.isRotating):
            print(self.isRotating,"movement")
            self.movement()
        