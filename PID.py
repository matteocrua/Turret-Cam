#PID controller class
# i have made this a class as the PID controller is 
# used for both servos, therefore needing two instances
class PID:
    def __init__(self, P = 0.1, I = 0.0, D = 0, Prev_error = 0, Integrator = 0, Integrator_max = 200, Integrator_min = -200):
        # PID constants and variables
        self.Kp = P # proportional gain
        self.Ki = I # integral gain
        self.Kd = D # derivative gain
        self.Prev_error = Prev_error # previous error
        self.Integrator = Integrator # integral of error
        self.Integrator_max = Integrator_max # maximum value of integrator
        self.Integrator_min = Integrator_min # minimum value of integrator
        self.set_point = 0.0 # set point
        self.error = 0.0 # error

    # calculate PID output value for given reference input and feedback
    def update(self,current_value):
        # calculate error
        self.error = self.set_point - current_value
        # proportional term 
        self.P_value = self.Kp * self.error
        # derivative term
        self.D_value = self.Kd * ( self.error - self.Prev_error)
        self.Prev_error = self.error
        # integral term
        self.Integrator = self.Integrator + self.error
        # limit the integral term as to reduce windup effect 
        if (self.Integrator > self.Integrator_max):
            self.Integrator = self.Integrator_max
        elif (self.Integrator < self.Integrator_min):
            self.Integrator = self.Integrator_min
        # calculate the integral value
        self.I_value = self.Integrator * self.Ki
        # calculate total value 
        PID = self.P_value + self.I_value + self.D_value

        return PID

    # # set PID setpoint
    # def setPoint(self,set_point):
    #     self.set_point = set_point
    #     self.Integrator=0
    #     self.Prev_error=0

    # def setIntegrator(self, Integrator):
    #     self.Integrator = Integrator

    # def setPrev_error(self, Prev_error):
    #     self.Prev_error = Prev_error


    # def setKp(self,P):
    #     self.Kp=P

    # def setKi(self,I):
    #     self.Ki=I

    # def setKd(self,D):
    #     self.Kd=D

    # def getPoint(self):
    #     return self.set_point

    # def getError(self):
    #     return self.error

    # def getIntegrator(self):
    #     return self.Integrator

    # def getPrev_error(self):
    #     return self.Prev_error