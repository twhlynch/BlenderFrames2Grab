# Blender Frames 2 Grab
**Using Babylon.js**
> This will only work if you have access to Animations or once they have released to the public.

> Currently all objects are assumed to be cubes.
### Usage
- Run `pip install -r requirements.txt`
- Install the [BabylonJS Blender Exporter](https://github.com/BabylonJS/BlenderExporter) Add-on
- Edit>Preferences>Add-ons>Install>`Blender2Babylon-X.X.zip`>Enable
- Create a Physics scene with Collisions and Rigid-bodies.
- Select all of the physics objects and run Object>Rigid body>Bake to keyframes
- Once the keyframes are created, use File>Export>Babylon.js ver X.X.X
- Save it as `data.babylon` in this directory
- Ensure the latest version of `generated` is in this directory (From [Slin/Grab-Level-Format](https://github.com/Slin/GRAB-Level-Format))
- Run `BlenderFrames2Grab.py`
- Transfer the .level file to `Android/data/com.slindev.grab_demo`
