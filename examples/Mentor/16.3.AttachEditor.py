#!/usr/bin/env python

###
# Copyright (c) 2002, Tamer Fahmy <tamer@tammura.at>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#   * Redistributions of source code must retain the above copyright
#     notice, this list of conditions and the following disclaimer.
#   * Redistributions in binary form must reproduce the above copyright
#     notice, this list of conditions and the following disclaimer in
#     the documentation and/or other materials provided with the
#     distribution.
#   * Neither the name of the copyright holder nor the names of its
#     contributors may be used to endorse or promote products derived
#     from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

###
# This is an example from the Inventor Mentor,
# chapter 16, example 3.
#
# This example builds a render area in a window supplied by
# the application and a Material Editor in its own window.
# It attaches the editor to the material of an object.
#

import sys

from pivy.coin import *
from pivy.sogui import *

def main():
    # Initialize Inventor and Qt
    myWindow = SoGui.init(sys.argv[0])  
   
    # Build the render area in the applications main window
    myRenderArea = SoGuiRenderArea(myWindow)
    myRenderArea.setSize(SbVec2s(200, 200))
   
    # Build the material editor in its own window
    try:
        myEditor = SoGuiMaterialEditor()
    except:
        print "The SoGuiMaterialEditor node has not been implemented in the " + \
              "SoGui bindings of Coin!"
        sys.exit(1)
   
    # Create a scene graph
    root =SoSeparator()
    myCamera = SoPerspectiveCamera()
    myMaterial = SoMaterial()
   
    root.ref()
    myCamera.position = (0.212482, -0.881014, 2.5)
    myCamera.heightAngle = M_PI/4
    root.addChild(myCamera)
    root.addChild(SoDirectionalLight())
    root.addChild(myMaterial)

    # Read the geometry from a file and add to the scene
    myInput = SoInput()
    if not myInput.openFile("dogDish.iv"):
        sys.exit(1)
    geomObject = SoDB.readAll(myInput)
    if geomObject == None:
        sys.exit(1)
    root.addChild(geomObject)
   
    # Set the scene graph 
    myRenderArea.setSceneGraph(root)
   
    # Attach material editor to the material
    myEditor.attach(myMaterial)
   
    # Show the application window and the material editor
    myRenderArea.setTitle("Attach Editor")
    myRenderArea.show()
    SoGui.show(myWindow)
    myEditor.show()

    # Loop forever
    SoGui.mainLoop()

if __name__ == "__main__":
    main()
