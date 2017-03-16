# Nernst equation didn't work yet.
# Therefore sensitivy curve was simulated (work-in-progress on Nernst in book+laptop).

import sys, getopt, math, time,random

MAX_SAMPLE_INVTERVAL = 500
MIN_MEASURE = 350
MAX_MEASURE = 450

MIN_EMF = 0.3049
MAX_EMF = 0.3236
MIN_V = 0;
MAX_V = 3.3;


def nernst(T, ppm): #ppm CO2 (actually the Partial Pressure, but formula is changed to work with ppm)
	# Theoretically correct
	# EMF = 0.223-((4.31*10.^-5*(T+273.15))*log(ppm/1000000));
	# Practically correct
	EMF = 0.182-((5.91*10**-5.0*(T+273.15))*math.log(ppm/1000000))
	return EMF

def sensor_output(EMF): #set sensor output (between 0 and 3.3V)
	output = MAX_V-(MAX_V-MIN_V)*(EMF-MIN_EMF)/(MAX_EMF-MIN_EMF)+MIN_V;
	if output < MIN_V: 
		output = MIN_V
	if output > MAX_V:
		output = MAX_V
	return output

def main(argv):
	outputfile = 'output.txt' # Default output file
	sample_interval = 500 # Time between samples in ms
	mode = 'r' # Default mode
	temp = 28.0 # Default temp (should always be around this, due to onboard heater)

	found_s = False

	try:
		opts, args = getopt.getopt(argv, "m:s:t:o:",["mode=,sampleinterval=,temp=,ofile="])
	except getopt.GetoptError:
		print("sensor_sim.py -m <mode 'r'|'t'|'m'> -s <sampleinterval (ms)> -t <temp in C> -o <outputfile>")
		sys.exit(2)
	for opt, arg in opts:
		if opt in ("-s", "--sampleinterval"):
			if int(arg) < 500:
				print("Minimum time between samples is ", MAX_SAMPLE_INVTERVAL)
				sys.exit(2)
			else:
				sample_interval = int(arg)
				found_s = True
		if opt in ("-o", "--ofile"):
			outputfile = arg
		if opt in ("-m", "--mode"):
			mode = str(arg)
		if opt in ("-t", "--temp"):
			temp = float(arg)

	if found_s is False:
		print("-s is required! (Should be larger than", MAX_SAMPLE_INVTERVAL, ")")
		sys.exit(2)	

	logfile = open(outputfile, "w")

	if(mode is 't'):
		print("Testing mode started!");
		for i in range(350, 1001, 50):
			logfile.write("%.0f\n" % i);
			print('CO2: ', i, 'ppm\t EMF: %.2f' % (nernst(temp,i)*1000), 'mV\t Sensor_out: %.2f' % sensor_output(nernst(temp, i)), "V");
			time.sleep(sample_interval/1000)
	elif(mode is 'r'):
		print("Random mode started!")
		while(True):
			r_ppm = random.randint(350,1000)
			r_nernst = nernst(temp, r_ppm)
			logfile.write("%.0f\n" % r_ppm)
			print('CO2: ', r_ppm, 'ppm\t EMF: %.2f' % (r_nernst*1000), 'mV\t Sensor_out: %.2f' % sensor_output(r_nernst), "V");
			time.sleep(sample_interval/1000)
	elif(mode is 'm'):
		print("Manual mode started!")
		while(True):
			m_ppm = int(input("Enter CO2 (in ppm): "))
			m_nernst = nernst(temp, m_ppm)
			logfile.write("%.0f\n" % m_ppm)
			print('CO2: ', m_ppm, 'ppm\t EMF: %.2f' % (m_nernst*1000), 'mV\t Sensor_out: %.2f' % sensor_output(m_nernst), "V");
			time.sleep(sample_interval/1000)

if __name__ == "__main__":
	main(sys.argv[1:])