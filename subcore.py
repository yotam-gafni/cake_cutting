from copy import copy
from itertools import combinations

def ties(agent_values):
	for av in agent_values:
		if len(set(av)) != len(av):
			return True

	return False



def subcore(agent_values, reserves):
	if ties(agent_values):
		print("Tie situation")
		return 
	M = len(agent_values)
	allocated = []
	new_reserves = copy(reserves)
	final_allocation_map = {}
	for m in range(M):
		next_argmax = agent_values[m].index(max(agent_values[m])) 
		allocated = [val[0] for val in final_allocation_map.values()]

		if next_argmax not in allocated:
			final_allocation_map[m] = [next_argmax, agent_values[m][next_argmax]]
		else:
			contested = [val[0] for val in final_allocation_map.values()]
			final_allocation_map = {}
			contesting = range(m+1)
			for i in contesting:
				max_value = 0
				for j in range(len(agent_values[i])):
					if j not in contested:
						max_value = max(max_value, agent_values[i][j])

				new_reserves[i] = max(reserves[i],max_value)


			W = []
			for cpiece in contested:
				cuts = []
				for i in range(m+1):
					if agent_values[i][cpiece] == 0:
						cuts.append(0)
					else:
						cuts.append(max(0, 1 - new_reserves[i]/agent_values[i][cpiece]))
				if ties([list(filter(lambda x: x != 0, cuts))]):
					print("Tie situation")
					return
				else:
					W.append(cuts.index(max(cuts)))

			W = list(set(W))




			while len(W) <= m:
				filt_reserves = []
				for nr_ind in range(len(new_reserves)):
					if nr_ind in W:
						filt_reserves.append(new_reserves[nr_ind])

				contested_cuts = []
				cutting_agents = []
				for cpiece in contested:
					cuts = []
					cutters = []
					for i in range(m+1):
						if i not in W:
							if agent_values[i][cpiece] == 0:
								cuts.append(0)
								cutters.append(i)
							else:
								cuts.append(max(0, 1 - new_reserves[i]/agent_values[i][cpiece]))
								cutters.append(i)

					cut_agent = cutters[cuts.index(max(cuts))]
					contested_cuts.append(1 - max(cuts))
					cutting_agents.append(cut_agent)
				new_agent_values = []
				for agent in range(len(agent_values)):
					if agent in W:
						new_agent = []
						cuts_ind = 0
						for j in range(len(agent_values[agent])):
							if j in contested:
								new_agent.append(agent_values[agent][j] * contested_cuts[cuts_ind])
								cuts_ind += 1
						new_agent_values.append(new_agent)



				allocation_map = subcore(new_agent_values, filt_reserves)

				if allocation_map == None:
					return None

				if len(W) < m:
					for agent in allocation_map.keys():
						new_reserves[contesting[agent]] = allocation_map[agent][1]

					used_intervals = [val[0] for val in allocation_map.values()]
					for i in range(len(new_agent_values[0])):
						if i not in used_intervals:
							ag = cutting_agents[i]
							W.append(ag)

				else:

					for agent in allocation_map.keys():
						new_reserves[W[agent]] = allocation_map[agent][1]
						final_allocation_map[W[agent]] = [contested[allocation_map[agent][0]], allocation_map[agent][1]]



					for i in range(m+1):
						if i not in W:
							max_val = 0
							argmax = 0
							used_intervals = [val[0] for val in final_allocation_map.values()]
							for j in range(len(agent_values[i])):
								if j not in used_intervals:
									if agent_values[i][j] > max_val:
										max_val = agent_values[i][j] 
										argmax = j
							final_allocation_map[i] = [argmax, max_val]
							new_reserves[i] = max_val
							W.append(i)



	return final_allocation_map


def partitions(n, m = None):
  """Partition n with a maximum part size of m. Yield non-increasing
  lists in decreasing lexicographic order. The default for m is
  effectively n, so the second argument is not needed to create the
  generator unless you do want to limit part sizes.
  """
  if m is None or m >= n: yield [n]
  for f in range(n-1 if (m is None or m >= n) else m, 0, -1):
    for p in partitions(n-f, f): yield [f] + p

#ret = subcore([[3/4,1/4,0],[3/5,2/5,0],[0.01,0.02,0.97]], [0,0,0])
ret2 = subcore([[0.5555555555555556, 0.046296296296296294], [0.37037037037037035, 0.20833333333333331]],[0.37037037037037035, 0.07407407407407407])

M = 3
N = 3
denom = N**M
agent_values = []

all_part = list(filter(lambda x: len(x) == N, partitions(denom)))

comb = ([24, 2, 1], [16, 10, 1], [16, 9, 2])
for comb in combinations(all_part, M):
	ret = subcore([[c/denom for c in combi] for combi in comb], [0 for i in range(M)])
	if ret == None or len(ret) == 3:
		print("HELLO {}".format(ret))
	else:
		import pdb
		pdb.set_trace()





