import plantDynamics as pD
import matplotlib.pyplot as plt

"""
This script implements runMulti function which has the ability to change tE and tP in between commutations
"""
pd = pD.inputChannel_class(channelNumber=1, voltage=0, capacitance=10e-6, energiseClocks=200
                           , periodClocks=33333.3, eGearFast=0, dGearFast=0, lastEnergizeEndClock=0, channelType=pD.HarvesterType_t.THEVENIN, vOpenSource=6, resistance=5000, frequency=0)

fig, ax1 = plt.subplots()
ax2 = ax1.twinx()

volts = []
currs = []
times = []


def runMulti(lastIndex, lastTimeStamp, turns, tE, tP, psuVolt, resistance):
    """
    runMulti takes new tEnergize and tPeriod to run certain number of turns
    return index and timeStamp to keep track of the commutation history
    """
    if len(volts) != 0:
        lastVolt = volts[lastIndex - 1]
    else:
        lastVolt = 3  # starting voltage
    timeStamp = lastTimeStamp
    pd.tEnergise = tE
    pd.tPeriod = tP
    for i in range(turns):
        volt, curr, time, gSimClock = pd.runOneCommutation(tE=tE, tP=tP, psuVolt=psuVolt, resistance=resistance, time=timeStamp, volt=lastVolt)
        volts.extend(volt)
        currs.extend(curr)
        times.extend(time)
        index = 1 + 2 * i + lastIndex
        lastVolt = volts[index]  # need to record the voltage from last commutation
        timeStamp = gSimClock

    return index + 1, timeStamp


lastIndex, lastTime = runMulti(lastIndex=0, lastTimeStamp=0, turns=20, tE=200, tP=10000, psuVolt=6, resistance=5000)
lastIndex2, lastTime2 = runMulti(lastIndex, lastTime, 20, tE=200, tP=33333, psuVolt=6, resistance=5000)
lastIndex3, lastTime3 = runMulti(lastIndex2, lastTime2, 20, tE=100, tP=20000, psuVolt=6, resistance=5000)

print(volts)
print(currs)
print(times)
ax1.plot(times, volts, 'b-')
ax2.plot(times, currs, 'g-')

# ax1.set_ylim([0, 6])
ax1.set_xlabel('Time')
ax1.set_ylabel('Voltage', color='b')
ax2.set_ylabel('Inductor Current', color='g')
plt.title('commutations voltage={} vOS={} res={} tE={} tP={}'.format(0, 6, 5000, 200, '10000-33333-20000'))

plt.show()
