from django.shortcuts import render
from aco_core.algo.min_max import MinMax


from django.shortcuts import render
from django.http import HttpResponse,HttpResponseBadRequest


# Create your views here.

def home(request):
	MinMax().run()

	return HttpResponse()
