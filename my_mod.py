# this module will be imported in the into your flowgraph

from analyzer import get_max_at
from numpy import savetxt, array

power = []
freqs = []
f0 = 2.2e9
f1 = 2.6e9
df = 1e6

f = f0

def sweeper(prob_lvl):

	global f, f1, f0, df, power, freqs
	
	power.append(get_max_at(f))
	freqs.append(f)
	savetxt("setup_result.txt", array([freqs, power]))
	
	if prob_lvl:
		f += df
	
	if f >= f1:
		f = f0
		
	return f
