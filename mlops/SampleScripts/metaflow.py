from metaflow import FlowSpec,step, resources, kubernetes,environment, timeout
import os

class LinearFlow(FlowSpec):
    
    @resources(memory=600, cpu=1)
    @kubernetes(namespace="default")
    @timeout(seconds=60)
    @step
    def start(self):
        self.my_var = 'hello world'
        self.next(self.a)
        
    @resources(memory=600, cpu=1)
    @kubernetes(namespace="default")
    @timeout(seconds=60)
    @step
    def a(self):
        print('the data artifact is: %s' % self.my_var)
        self.next(self.end)
        
    @resources(memory=600, cpu=1)
    @kubernetes( namespace="default")
    @timeout(seconds=60)
    @step
    def end(self):
        print('the data artifact is still: %s' % self.my_var)

if __name__ == '__main__':
    LinearFlow()