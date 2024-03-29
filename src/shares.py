'''!    @file       shares.py
        @brief      Task sharing library implementing both shares and queues.
        @details    Implements a very simple interface for sharing data between
                    multiple tasks.

        @author     Juan Luna
        @date       2022-01-31 Original file
        @date       2022-12-30 Modified for portfolio update
'''

class Share:
    '''! @brief      A standard shared variable.
         @details    Values can be accessed with read() or changed with write()
    '''
    def __init__(self, initial_value=None):
        '''! @brief      Constructs a shared variable
             @param      initial_value An optional initial value for the 
                                      shared variable.
        '''
        self._buffer = initial_value
    
    def write(self, item):
        '''! @brief      Updates the value of the shared variable
             @param item The new value for the shared variable
        '''
        self._buffer = item
        
    def read(self):
        '''! @brief      Access the value of the shared variable
             @return    The value of the shared variable
        '''
        return self._buffer

class Queue:
    '''! @brief      A queue of shared data.
         @details    Values can be accessed with placed into queue with put() or
                     removed from the queue with get(). Check if there are
                     items in the queue with num_in() before using get().
    '''
    def __init__(self):
        '''! @brief              Constructs an empty queue of shared values
        '''
        self._buffer = []
    
    def put(self, item):
        '''! @brief      Adds an item to the end of the queue.
             @param item The new item to append to the queue.
        '''
        self._buffer.append(item)
        
    def get(self):
        '''! @brief      Remove the first item from the front of the queue
             @return     The value of the item removed
        '''
        return self._buffer.pop(0)
    
    def num_in(self):
        '''! @brief      Find the number of items in the queue. Call before get().
             @return     The number of items in the queue
        '''
        return len(self._buffer)