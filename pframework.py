"""
This class serves as a wrapper for PFramework and a model selector.
When adding a new model, it should follow a structure:
PModules                root folder for all models
    |
    model_name          folder dedicated to a model
        |
        model_name      model_name.py file
            |
            model_name  model_name class
"""
from predictor_resources.config import models
from pydoc import locate


class TrafficPredictor:

    _selected_model = None

    def main(self):
        print("Welcome to the Traffic Predictor!")
        print("Please choose your model (enter its index):")
        for model in models:
            x = models.index(model)
            print("{0}: {1}".format(x, model))
        print("-: Exit")

        selection = input("Prompt: ")

        for model in models:
            x = str(models.index(model))
            if selection == '-':
                return
            elif selection == x:
                try:
                    self.call_model(model)
                except TypeError:
                    print("ERROR: The model import failed. Please make sure to properly add your model.")
            else:
                print("ERROR: there's no such model")

    def call_model(self, model_name):
        result = None
        model_root = 'PModules.' + model_name + "." + model_name + "." + model_name
        model = locate(model_root)
        self._selected_model = model() # Your model class instance
        result = self._selected_model.call_model()


        return result

