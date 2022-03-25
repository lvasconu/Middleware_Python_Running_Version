def get_all_models():
    ''' Getting all models in models.py.	
    Ref: https://stackoverflow.com/questions/1796180/how-can-i-get-a-list-of-all-classes-within-current-module-in-python	
    '''	
    try:
        from django.db import models
        import sys, inspect
        from . import models as models_ga

        model_list = []	
        for name, obj in inspect.getmembers(sys.modules[models_ga.__name__]):
            if inspect.isclass(obj):	
                model_list.append(obj)	
        return model_list

    except:
        return []