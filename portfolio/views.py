from django.shortcuts import render
from aco_core.algo.min_max import MinMax


from django.shortcuts import render
from django.http import HttpResponse,HttpResponseBadRequest


# Create your views here.

results_list = []

def home(request):

	cycles =1
	for x in range(0, cycles):
		run_min_max()

	print results_list
	return HttpResponse()

def run_min_max():
	min_max = MinMax()
	min_max.run()

	print str(min_max.best_ant.expected_val) + ":" + str(min_max.best_ant.iter)
	print min_max.best_ant.path

	results_list.append(int(min_max.best_ant.expected_val))
