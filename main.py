import machine
import time
import tm1637
photo_pin = machine.ADC(28)

SAMP_SIZE = 12
NUM_SPOKES = 3
NOISE_THRESHOLD = 500
SAMP_RATE = 0.003
up = True
t = [time.ticks_ms(), 0]
val = [0, 0]
max = min = 0
count = 0
display = tm1637.TM1637Decimal(clk=machine.Pin(26), dio=machine.Pin(27))
display.write([0, 0, 0, 0])

# Debug loop
# while True:
#     val = photo_pin.read_u16()
#     print(val)
#     display.number(int(round(val/1000,0)))
#     time.sleep(0.2)

while True:
    val[0] = photo_pin.read_u16()
    time.sleep(SAMP_RATE)
    val[1] = photo_pin.read_u16()
    # Going up
    if (val[0] < val[1]):
        if (not up):
            print(val, "bottom")
            up = True
            min = val[0]
    # Going down
    elif (val[0] > val[1]):
        if (up):
            print(val, "top")
            count = count + 1
            up = False
            max = val[0]
    # print("count", count, "diff", abs(max - min))
    if (abs(max - min) > NOISE_THRESHOLD):
        if (count == SAMP_SIZE * NUM_SPOKES):
            count = 0
            t[1] = time.ticks_ms()
            spin_period = time.ticks_diff(t[1], t[0]) / SAMP_SIZE / 1000
            spin_freq = 1 / spin_period
            t[0] = t[1]
            spin_freq_round = round(spin_freq,2)
            spin_freq_a = int(spin_freq_round)
            spin_freq_b = int(round((spin_freq_round % 1) * 100,0))
            display.numbers(spin_freq_a, spin_freq_b, colon=True)
            print(f"{spin_freq:.2f} spin/s")
    else:
        count = 0
        t[0] = time.ticks_ms()
        
