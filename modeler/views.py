from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.generic import View
import requests
import pickle
import json
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .models import PythonModels, ModelsTypes, ScoresTypes, Tests, TestsModels
from joblib import dump, load
import numpy as np
from django.conf import settings
from sklearn.model_selection import train_test_split
from sklearn import datasets
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from sklearn import linear_model
from sklearn.metrics import mean_squared_error, r2_score


from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.generic import View
import requests
import json
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .models import PythonModels, ModelsTypes, ScoresTypes, Tests, TestsModels
from joblib import dump, load
from django.conf import settings

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
# from IPython.display import Image
# import pydotplus as pydot
from sklearn.model_selection import KFold, train_test_split, ShuffleSplit
from sklearn import linear_model, tree
from sklearn.linear_model import LogisticRegression
from sklearn import metrics
from sklearn.metrics import mean_squared_error, r2_score, f1_score, accuracy_score


# Create your views here.

def index(request):
    # return JsonResponse({'foo':'bar'})
    return HttpResponse("<body><H1>Hello, world. You're at the ht-line modeler index.</H1></body>")


class CalcScore(View):
    def get(self, req, *args, **kwargs):
        a = req.GET.get('param', 'undef')
        return HttpResponse(u"Слово" + a + "Слово")

    def post(self, req, *args, **kwargs):
        json_data = req.POST.get('out', 'undef')
        request_data = json.loads(json_data)
        model = request_data['model']
        stens = request_data['stens']
        stens = np.array([stens])
        PM = PythonModels.objects.get(model_name=model)
        model_path = PM.model_file
        model_path = settings.MEDIA_ROOT + '/' + str(model_path)
        Model = load(model_path)
        prediction = Model.predict(stens)
        temp = ''
        return HttpResponse(prediction)
        #return HttpResponse(u"Слово" + model)
