from django.shortcuts import render
from aco_core.algo.min_max import MinMax
from aco_core.algo.greedy import Greedy

from django.shortcuts import render
from django.http import HttpResponse,HttpResponseBadRequest


# Create your views here.

results_list = []
times_list = []

def home(request):
	cycles =100
	for x in range(0, cycles):
		run_min_max()
		print x 
		print "----------------------------------------------------------------"
		#run_greedy()

	print results_list
	print times_list
	return HttpResponse()

def run_min_max():
	min_max = MinMax()
	min_max.run()

	print str(min_max.best_ant.expected_val) + ":" + str(min_max.best_ant.iter)
	print min_max.best_ant.path
	print min_max.best_ant.timeToFind

	results_list.append(int(min_max.best_ant.expected_val))
	times_list.append(min_max.best_ant.timeToFind)


def run_greedy():
	greedy = Greedy()
	greedy.run()