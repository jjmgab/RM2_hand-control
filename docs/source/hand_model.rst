hand\_model module
==================

This module is responsible for defining and calculating the model of the hand prosthetics. After calculations, *V* (coordinates and orientation) and *K* (*i* into *i+1* joint transformations) matrices are pickled into *pickles* directory, which can then be unpickled anywhere else - for further processing.

The aim of creating this module was to carry out calculations concerning assumed model only one, since considered matrices are complex and there is a vast amount of calculations.

.. automodule:: hand_model
    :members:
    :undoc-members:
    :show-inheritance:
