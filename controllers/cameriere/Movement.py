class Movement:
    def __init__(self,positioning,lmotor,rmotor):
        self.positioning=positioning
        self.lmotor=lmotor
        self.rmotor=rmotor
        self.positioning.update()
        self.status=2

    def rotate(self):
        self.rmotor.setVelocity(-1.00)
        self.lmotor.setVelocity(1.00)
    
    def movement(self):
        self.rmotor.setVelocity(5.00)
        self.lmotor.setVelocity(5.00)
    
    def update(self):
        print(self.positioning.getOrientation())
        if(self.status==2 and not (179.0 <self.positioning.getOrientation()<181.0 )):
            self.rotate()
        else:
            self.movement()