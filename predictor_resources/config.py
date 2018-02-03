from os import path
# This argument is pointing to Resources folder, cross-platform
RESOURCES_DIR = path.dirname(path.abspath(__file__))

# This list contains the statistical models that can be used by Predictor
# They should all follow the similar structure
models = ['SimpleMovingAverage']
