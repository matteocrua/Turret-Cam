#PID controller class
# i have made this a class as the PID controller is 
# used for both servos, therefore needing two instances
class PID:
    # setup is called when the class is instantiated
    def setup(self, P, I, D, Prev_error=0, Integrator=0, Integrator_max=200, Integrator_min=-200):
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

    # calculate PID output value, 
    # steps is the number of steps to move the servo
    def update(self,servo_steps): 
        # calculate error, the difference between the set point and the current position
        self.error = self.set_point - servo_steps

        # proportional term 
        self.P_value = self.Kp * self.error

        # derivative term
        self.D_value = self.Kd * ( self.error - self.Prev_error)
        # store the error for the next iteration
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