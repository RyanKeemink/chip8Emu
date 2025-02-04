import RAM
import time
import random

class CPU:
    ram = RAM.RAM()
    stack = []
    delayTimer = 0
    soundTimer = 0
    currtime = time.time_ns()
    I = 0
    var = [0 for i in range(16)]

    def timerHandler(self):
        hz = (1000000000/60)
        diffrence = time.time_ns() - self.currtime
        cycles = diffrence // hz
        self.delayTimer = max(0, self.delayTimer -cycles)
        self.soundTimer = max(0, self.soundTimer -cycles)
        self.currtime += (cycles*hz)

    def CPUcycle(self):
        self.timerHandler()

        fetch = (self.ram.readMem(), self.ram.readMem())
        return self.execute(fetch)

    def overflow(self,register,flag =True):
        if self.var[register] > 255:
            self.var[register] - 255
            return self.setFlag()
        return self.setFlag(False)

        
    
    def underflow(self,register,flag =True):
        if self.var[register] < 0 :
            self.var[register] + 255
            return self.setFlag(False)
        self.setFlag()

    def setFlag(self, state = True):
        self.var[0x0F] = state
        



    def execute(self, data):

        nibbles = (int(data[0]) & 0xF0,int(data[0]) & 0x0F, (int(data[1]) & 0xF0)>>4,int(data[1]) & 0x0F)

        if  nibbles[0] == 0x00:
            if nibbles[2] == 0x0e:
                if nibbles[3] == 0x0e:
                    self.ram.setPC(self.stack.pop())
                return "clean"
            
        elif nibbles[0] == 0x10:
            loc = (nibbles[1] << 8) + data[1]
            self.ram.setPC(loc)

        elif nibbles[0] == 0x20:
            loc = (nibbles[1] << 8 )+ data[1]
            self.stack.append(loc)
            self.ram.setPC(loc)

        elif nibbles[0] == 0x30:
            if self.var.nibbles[1] == data[1]:
                self.ram.incPC(2)

        elif nibbles[0] == 0x40:
            if not self.var.nibbles[1] == data[1]:
                self.ram.incPC(2)

        elif nibbles[0] == 0x50:
            if not self.var[nibbles[1]] == self.var[nibbles[2]] :
                self.ram.incPC(2)

        elif nibbles[0] == 0x60:
            self.var[nibbles[1]] = data[1]

        elif nibbles[0] == 0x70:
            self.var[nibbles[1]] += data[1]
            self.overflow(nibbles[1],False)

        elif nibbles[0] == 0x80:
            if nibbles[3] == 0x00:
                self.var[nibbles[1]] = self.var[nibbles[2]]
            elif nibbles[3] == 0x01:
                self.var[nibbles[1]] |= self.var[nibbles[2]]
            elif nibbles[3] == 0x02:
                self.var[nibbles[1]] &= self.var[nibbles[2]]
            elif nibbles[3] == 0x03:
                self.var[nibbles[1]] ^= self.var[nibbles[2]]
            elif nibbles[3] == 0x04:
                self.var[nibbles[1]] += self.var[nibbles[2]]
                self.overflow(nibbles[1])
            elif nibbles[3] == 0x05:
                self.var[nibbles[1]] -= self.var[nibbles[2]]
                self.underflow()
            elif nibbles[3] == 0x06:
                self.var[nibbles[1]] = self.var[nibbles[1]] < 1
                self.overflow()
            elif nibbles[3] == 0x07:
                self.var[nibbles[1]] = self.var[nibbles[2]] - self.var[nibbles[1]]
                self.underflow()
            elif nibbles[3] == 0x0E:
                self.setFlag(self.var[nibbles[1]]%2)
                self.var[nibbles[1]] = self.var[nibbles[1]] > 1
            


        elif nibbles[0] == 0x90:
            pass
        elif nibbles[0] == 0xA0:
            
            self.I = (nibbles[1] << 8) + data[1]
        elif nibbles[0] == 0xB0:
            adr = (nibbles[1] << 8 + data[1]) + self.var[0]
            self.ram.setPC(adr)

        elif nibbles[0] == 0xC0:
            self.var[nibbles[1]] = random.randint(0,255) &  data[1]
            
        elif nibbles[0] == 0xD0:
            print(nibbles)
            length = nibbles[3]
            data = []
            for i in range(length):
                data.append(self.ram.readMemLoc(self.I+i))
            print (self.var[nibbles[1]], self.var[nibbles[2]],data)
            return (self.var[nibbles[1]], self.var[nibbles[2]],data)
        elif nibbles[0] == 0xE0:
            pass
        elif nibbles[0] == 0xF0:
            pass


