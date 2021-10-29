import sys
import itertools

vertices = []
edges = []

def read_graph(filename):
	with open(filename) as f:
		vert_num = -1
		edg_num = -1
		for line in f.readlines():
			if line.startswith('c '): # ignore comments
				continue
			if line.startswith('e '): # add an edge, check vertex number are consistent
				parts = line.split(' ')
				u, v = int(parts[1]), int(parts[2])
				if u > vert_num or v > vert_num:
					print('Warning: invalid vertex number found in edge:', line)
				edges.append((u, v))
				
			if line.startswith('p edge'): # parse problem specification
				parts = line.split(' ')
				vert_num = int(parts[2])
				edg_num = int(parts[3])
				vertices = list(range(1, vert_num + 1))

		if edg_num != len(edges):
			print('Warning: number of edges does not match file header: %d != %d' % (len(edges), edg_num))

	return vertices, edges

def write_cnf(cnf, filename):

	variables =  max(map(abs, itertools.chain(*cnf))) 
	cnf_str = '\n'.join(map(lambda c: ' '.join(map(str, c)) + ' 0', cnf))

	print('CNF created, it has %d variables and %d clauses' % (variables, len(cnf)))

	with open(filename, 'w') as f:
		f.write('p cnf %d %d\n' % (variables, len(cnf)))
		f.write(cnf_str)


def is_prime(number):
	for i in range(2,int(number**(0.5))+2):
		if  number % i == 0: return False
	
	return True

def generate_primes(start, quantity):
	primes = []
	number = start + 1

	while len(primes) != quantity:
		if is_prime(number): primes.append(number)
		number += 1

	return primes

def one_color_clause(vertex, colors):
    clauses = [[vertex*color for color in colors]]        
    pained_vertex = [-vertex*color for color in colors]
    clauses.extend(set(itertools.combinations(pained_vertex, 2)))

    return clauses

def same_color_clause(edges, colors):
	clauses = []

	for i,j in edges:
		for color in colors:
			clauses.append([-i*color,-j*color])

	return clauses

def find_neighbours(vertex, edges):
	return [i for i in edges if i[0] == vertex]

def generate_cnf(vertices, edges, colors):
	clauses = []

	for vertex in vertices:
		clauses.extend(one_color_clause(vertex, colors))
		clauses.extend(same_color_clause(find_neighbours(vertex, edges), colors))

	return clauses

if __name__ == '__main__':
	vertices, edges = read_graph(sys.argv[1])

	print('Number of vertices:', len(vertices))
	print('Number of edges:', len(edges))
	print('Number of colors:', int(sys.argv[2]))
    
	colors = generate_primes(max(vertices), int(sys.argv[2]))
	cnf = generate_cnf(vertices, edges, colors)

	write_cnf(cnf, sys.argv[1] + '.cnf')