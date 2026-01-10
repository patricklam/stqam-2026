import threading

# In the assignment, you write a mock for this class.
class Model:
    """ Not a semaphore implementation. """
    def __init__(self):
        self.counter = 1
        self.resource = []
        self.lock = threading.Lock()

    def wait(self):
        self.lock.acquire()
        self.counter -= 1
        # if this was actually a semaphore we would block until counter becomes nonnegative
        self.lock.release()

    def signal(self):
        self.lock.acquire()
        self.counter += 1
        # if this was actually a semaphore we would wake threads if appropriate
        self.lock.release()

    def clear_resource(self):
        self.resource = []

    def get_resource(self):
        return self.resource[:]

    def append_to_resource(self, x):
        self.resource.append(x)
