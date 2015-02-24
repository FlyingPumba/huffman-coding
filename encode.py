import argparse
from heapq import *
__author__ = 'flyingpumba'

parser = argparse.ArgumentParser(description='Example of compression using Huffman coding')
parser.add_argument('-d','--debug',help='Debug mode will output some useful Debug mode will output some useful information.', required=False, action="store_true")
parser.add_argument('-i','--input', help='Input file name',required=True)
parser.add_argument('-o','--output',help='Output file name', required=True)
args = parser.parse_args()

# recursive function to find a code for a char in a huffman tree
def findCode(tree, char):
	aux = tree
	if aux[0][1] == ord(char):
		return '2'
	elif aux[1] != None:
		i = findCode(aux[1][1], char) # search right
		j = findCode(aux[1][0], char) # search left
		if i == '2':
			return '1'
		elif j == '2':
			return '0'
		elif i != '-1':
			return '1' + i
		elif j != '-1':
			return '0' + j
		else:
			return '-1'
	else:
		return '-1'

## identify debug mode
debug = args.debug
 
## show values
if debug:
	print ("Input file: %s" % args.input )
	print ("Output file: %s" % args.output )

## get frecuencies for each char
frecs = [0] * 512

file = open(args.input, 'r')
while 1:
	char = file.read(1)
	if not char:
		break
	else:
		frecs[ord(char)] = frecs[ord(char)] + 1

file.close()

## store the frecuencies in a heap
h = []
if debug:
	print "Freqs for each char:"
for i in range(512):
	if frecs[i] != 0:
		if debug:
			print chr(i), ': ', frecs[i]
		heappush(h, (frecs[i], i))

#print "Sorted freqs:"
#while h != []:
#	aux = heappop(h)
#	print chr(aux[1]), ': ', aux[0]

## assemble huffman tree
auxtree = []
for x in h:
	#print x
	heappush(auxtree, (x, None))

while len(auxtree) != 1:
	izq = heappop(auxtree)
	der = heappop(auxtree)
	s = (izq[0] + der[0], -1)
	heappush(auxtree, (s, (izq,der)))

huffmantree = heappop(auxtree)
if debug:
	print huffmantree

## encode the file
file = open(args.input, 'r')
out = open(args.output, 'w+')

while 1:
	char = file.read(1)
	if not char:
		break
	else:
		out.write('%s ' % findCode(huffmantree, char))

file.close()
out.close()

## write debug file with the codes for each char
if debug:
	debug_file = open('char-codes.txt', 'w+')
	for x in h:
		debug_file.write('%s: %s\n' % (chr(x[1]), findCode(huffmantree, chr(x[1]))))
	debug_file.close()
