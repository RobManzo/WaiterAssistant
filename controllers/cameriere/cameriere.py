from controller import Robot

robot = Robot()

left_motor = robot.getDevice("left wheel motor")
right_motor = robot.getDevice("right wheel motor")
left_motor.setPosition(float('inf'))
right_motor.setPosition(float('inf'))
left_motor.setVelocity(0.0)
right_motor.setVelocity(0.0)
ps = []
psNames = [
    'ps0', 'ps1', 'ps2', 'ps3',
    'ps4', 'ps5', 'ps6', 'ps7'
]

for i in range(8):
    ps.append(robot.getDevice(psNames[i]))
    ps[i].enable(32)

while robot.step(32) != -1:
    left_motor.setVelocity(5.0)
    right_motor.setVelocity(5.0)
    
    psValues = []
    for i in range(8):
        psValues.append(ps[i].getValue())
        print(psValues[i])