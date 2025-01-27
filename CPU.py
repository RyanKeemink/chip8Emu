import RAM
import time

class CPU:
    ram = RAM()
    stack = []
    delayTimer = 0
    soundTimer = 0
    currtime = time.time_ns()
    I = 0
    var = [0 in range(16)]

    def timerHandler(self):
        hz = (1000000000/60)
        diffrence = time.time_ns() - self.currtime
        cycles = diffrence // hz
        self.delaytimer = max(0, self.delaytimer -cycles)
        self.soundTimer = max(0, self.soundTimer -cycles)
        self.currtime += (cycles*hz)

    def CPUcycle(self):
        self.timerHandler()

        fetch = (self.ram.readMem(), self.ram.readMem())
        return self.execute(fetch)

    def overflow(self,register,flag =True):
        if self.var[register] > 255:
            self.var[register] - 255



    def execute(self, data):
        firstNibble = data[0] & 0xF0

        if firstNibble == 0x00:
            if data[1] == 0xE0:
                return "clean"
            else:
                self.ram.setPC = self.stack.pop()
            
        elif firstNibble == 0x01:
            data = ((data[0] & 0x0F) << 8 ) | data[1]
            self.ram.setPC(data)

        elif firstNibble == 0x02:
            data = ((data[0] & 0x0F) << 8 ) | data[1]
            self.ram.setPC(data)
            self.stack.append(data)

        elif firstNibble == 0x03:
            x = data[0] & 0x0F
            if self.var[x] == data[1]:
                self.ram.incPC(2)

        elif firstNibble == 0x04:
            x = data[0] & 0x0F
            if not self.var[x] == data[1]:
                self.ram.incPC(2)

        elif firstNibble == 0x05:
            x = data[0] & 0x0F
            y =data[1] & 0xF0
            if self.var[x] == self.var[y]:
                self.ram.incPC(2)

        elif firstNibble == 0x06:
            x = data[0] & 0x0F
            self.var[x] = data[1]

        elif firstNibble == 0x07:
            x = data[0] & 0x0F
            self.var[x] += data[1]
            self.overflow(x)
            

        elif firstNibble == 0x08:
            pass
        elif firstNibble == 0x09:
            x = data[0] & 0x0F
            y =data[1] & 0xF0
            if not self.var[x] == self.var[y]:
                self.ram.incPC(2)
        elif firstNibble == 0x0A:
            pass
        elif firstNibble == 0x0B:
            pass
        elif firstNibble == 0x0C:
            pass
        elif firstNibble == 0x0D:
            pass
        elif firstNibble == 0x0E:
            pass
        elif firstNibble == 0x0F:
            pass


