from os import path
from enum import Enum
# This argument is pointing to Resources folder, cross-platform
RESOURCES_DIR = path.dirname(path.abspath(__file__))

# This list contains the statistical models that can be used by Predictor
# They should all follow the similar structure
models = ['SimpleMovingAverage']

class Stride(Enum):
    DAILY = 96
    WEEKLY = 672
