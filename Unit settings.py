__author__ = "samu.karli"
__version__ = "2022.05.20"

import rhinoscriptsyntax as rs
import Rhino

if Rhino.RhinoDoc.ActiveDoc.ModelUnitSystem.ToString() == "Meters":
    a = 1
elif Rhino.RhinoDoc.ActiveDoc.ModelUnitSystem.ToString() == "Centimeters":
    a = 100
else:
    a = 1000