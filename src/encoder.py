'''!    @file       encoder.py
        
        @brief      A driver for working with a quadrature incremental encoder.
        @details    Encapsulates functionality of encoder attached to the motor.
                    This class sets up pins to control the encoder and methods
                    to read and zero (reset) the angular position of the motor
                    in units of "ticks". Position reading is based on an 
                    algorithm that accounts for overflow and underflow.
        
        @author   Juan Luna
        @date     2022-02-03 Original file
        @date     2022-12-30 Modified for portfolio update
'''

import pyb
#import utime

class Encoder_Driver:
    '''! @brief      Driver class for the quadrature incremental encoder.
         @details    Objects of this class can be used to instantiate encoder
                     objects to control two encoders, each attach to one motor.
    '''
    def __init__ (self, enc1_pin, enc2_pin, timer):
        '''! @brief      Initializes objects of the EncoderDriver class.
             @param  enc1_pin    Encoder pin object for first timer channel.
             @param  enc2_pin    Encoder pin object for second timer channel.
             @param  timer       Timer object for program timing.
             @param  tim_ch1     Channel object "1" for motor timer.
             @param  tim_ch2     Channel object "2" for motor timer.
             @param  period      Timer period, defined as largest 16-bit number.
             @param  delta_val      Difference between consecutive tick counts.
             @param  last_tick      Previous recorded encoder tick value.
             @param  new_tick       Latest recorded encoder tick value.
             @param  true_position  Encoder position that accounts for overflow/underflow.
        '''     
        # Encoder pin objects for two channels
        self.enc1_pin = enc1_pin
        self.enc2_pin = enc2_pin

        # Encoder timer object
        self.timer = timer

        # Encoder timer channel setup     
        self.tim_ch1 = timer.channel(1, mode = pyb.Timer.ENC_AB,
                                            pin = self.enc1_pin)
        self.tim_ch2 = timer.channel(2, mode = pyb.Timer.ENC_AB,
                                             pin = self.enc2_pin)

        # Timer period   
        self.period = 2**16 - 1

        #  Timing variables
        self.delta_val      = 0         
        self.last_tick      = 0         
        self.new_tick       = 0         
        self.true_position  = 0
        
    def read(self):
        '''! @brief      Reads current position of encoder.
             @details    Algorithm accounting for overflow and underflow is
                         implemented to return current encoder position.
             @return     Position read by encoder, in units of "ticks".
        '''
        # Save last encoder reading
        self.last_tick = self.new_tick
        # Take a new encoder reading
        self.new_tick = self.timer.counter()
        # Calculate difference between last two readings
        self.delta_val = self.new_tick - self.last_tick
        
        # Accounting for overflow or underflow
        if (self.delta_val > 0.5*self.period):
            self.delta_val -= self.period
        elif (self.delta_val < -0.5*self.period):
            self.delta_val += self.period
        
        #self.rev_per_s = self.delta_var/(16384)
        self.true_position += self.delta_val
        return self.true_position

    def zero(self):
        '''! @brief      Resets (zeroes) the position of the encoder.
        '''
        self.true_position = 0
