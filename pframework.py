"""
This class serves as a wrapper for PFramework and a model selector.
"""
from resources.config import models

def main():
    print("Welcome to the Traffic Predictor! Please choose your model:")
    for model in models:
        x = models.index(model)
        print("{0}: {1}".format(x, model))

    selection = input("Prompt: ")

    for model in models:
        x = str(models.index(model))
        if selection == x:
            print("Choose: {0}".format(model))
            call_model(model)

def call_model(module_name):
    models_root='PModules.' + module_name
    model_class_name = module_name
    model = my_import('PModules.model_1.model_1.model_1')
    my_model = model() # Your model class instance
    my_model.call_model()

def my_import(name):
    components = name.split('.')
    mod = __import__(components[0])
    for comp in components[1:]:
        mod = getattr(mod, comp)
    return mod

main()
