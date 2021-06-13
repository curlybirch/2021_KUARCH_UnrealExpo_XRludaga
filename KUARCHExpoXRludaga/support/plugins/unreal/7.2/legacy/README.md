# Megascans - Unreal Engine LiveLink

The Megascans **LiveLink** for Unreal Engine 4 is an **open-source, python-written** integration for Megascans inside unreal engine 4. The plugin is written with **[UnrealEnginePython](https://github.com/20tab/UnrealEnginePython)** and is available for UE4 versions **4.15 and above**.

UnrealEnginePython is developed by Roberto De Ioris (20Tab S.r.l, [20tab.com](http://20tab.com)) with sponsorship from Accademia Italiana Videogiochi ([aiv01.it](http://aiv01.it)), Kite & Lightning ([kiteandlightning.la](http://kiteandlightning.la/)),  GOODTH.INC ([goodthinc.com](https://www.goodthinc.com/)) and QUIXEL AB (Quixel.se).

Windows binaries are currently provided, and **OSX and Linux coming soon**.

If you're facing issues with and this documentation isn't helping you please let us know : **[support@quixel.se](mailto:support@quixe.se)** . We'll help you get things fixed ASAP.

##
![ ](https://raw.githubusercontent.com/Quixel/Megascans-UE4LiveLink/master/Resources/unreal_viewport.jpg)

## Installing the LiveLink with Megascans Bridge
Megascans is an ecosystem consisting of a huge scan library and a set of tools to help you work with that library, and Bridge is one of those tools.
Megascans Bridge lets you Instantly access the entire Megascans library, batch export straight to your game engine or 3D software, and unleash your imagination without having to waste time on importing assets.

How to install the LiveLink with Bridge :

One minute video guide (Recommended) : [Video Installation Tutorial](https://www.youtube.com/watch?v=WUNdfZM9cps)

Manual instructions :

- go to https://megascans.se/apps/bridge and download it.
- Click on the export icon of any asset in your downloaded library, this will open the export options pop-up. set the "Application" drop-down to "Unreal Engine" and click on "Download Plugin". 

- Once the plugin is downloaded you'll need to select which version of unreal you want to install the LiveLink on with the "Engine Version" drop-down. If your using an official unreal engine version just just select which version (**4.18, 4.19, 4.0, etc...**) you want to install the LiveLink on. If on the other hand you're trying to install the LiveLink on a custom unreal engine build then pick up the **"Custom Build"** option in that drop-down.

- Now set the "Engine Version Path" option to where your engine's plugins are installed, like this for instance: **C:\Program Files\Epic Games\UE_4.20\Engine\Plugins**. The path should basically be where your engine's plugins are installed.

- As soon as you've picked the version and the path in the previous step, Bridge will notify you that it's currently installing the plugin, and once it's done it will tell you in a pop-up. 

- Once the installation is done, simply start or restart unreal and click on the green "Export" button in the export dialog of any asset you want to export in Bridge in Bridge. 

	-  **Optional for building the plugin on an OS other than Windows** : If you're looking into building the Megascans LiveLink plugin on a non-windows platform, you'll need to build PySide2 with a python installation on your system (`  
pip install PySide2`), then copy the PySide2 folder from the python/lib/site-packages folder to the UnrealEnginePython/Binaries/Win64 folder. You can confirm to replace if it's asking you to remove an existing installation.

This is what your installation settings for unreal engine 4.19 would look like :

![ ](https://raw.githubusercontent.com/Quixel/Megascans-UE4LiveLink/master/Resources/official_build.png)


This is what your installation settings for a custom build would look like :

![ ](https://raw.githubusercontent.com/Quixel/Megascans-UE4LiveLink/master/Resources/custom_build.png)

##

The LiveLink currently relies on a hard-coded port to receive data from Megascans Bridge : **13428**. It can only work with one engine open on your system at a time.


##
![ - ](https://raw.githubusercontent.com/Quixel/Megascans-UE4LiveLink/master/Resources/img_02.jpg)

## User Interface and Functionalities

![](https://raw.githubusercontent.com/Quixel/Megascans-UE4LiveLink/master/Resources/livelink_ui.png)


This window is expected to receive many updates during the next few months, as we keep adding more features to give you the best Unreal Engine integration possible. With that said, let’s dig in:
  

![](https://lh4.googleusercontent.com/H3dzRrPsW2JDmz65SAcM4N2MsJ1vANTsrD4LbyO92r4xwY_LkYKoXsBfRyADaKRXzur-gErBtBGX_dBOEVf9ocVDQSVvJWUKAq16sGQt-Xxm5lhJQh0-izLbAHl7PC0yLoJv5957)![](https://lh4.googleusercontent.com/z1E-BHdbic2aPxcd4NdPZVUwZHZE_oFLyx1jbA1b9-cFp_ltzHMa0Ci3Ne9XcJwMfjOc-d7vKGAISXpJE2yvQHB8qaRrQqXmiG0s0pUWJzgVeKdGK7P714NLZ3a_8CIbCFHxSEHg)

  

The top-most bar has a close and minimize button. By clicking the Megascans icon you will access a context menu including an always on top toggle, access to help documentation, a one-click jump to megascans.se, and more information about the plugin.

  

## The Blend Material Workflow

![](https://lh6.googleusercontent.com/YO1CjzaDVtGhz3lZo1g48F4v6lY7TppD2DodOw7GkDDjSzHK33SMCopsW0v4bchLM7G_eklZQn1mFCPO8lgDW708zmdrjYVt7OTO9wUp4eogjkul1ZvaTiIuOJz-4UgAta_-dF28)

  

Quick Video Guide - [Blend Materials Workflow](https://www.youtube.com/watch?v=wfHJ0zYgsdU)

  

The LiveLink comes with a really neat blend-based master material that has support for up to three different texture sets, world-aligned blend, fuzzy shading, per-layer attribute editing and much, much more.

  

To create a the assets you wanblend material simply select 2 or 3 material instances of t to import in the content browser, then click “Create Material Blend”:

  

![](https://lh3.googleusercontent.com/YrlczKlhIrnIxpeQI-Cf8yvrL6l8CnuZa53_ZnyEQTyOt40lSi1p9IC95w9yGZ1zVHHrrytaT2G8JdoJX0QVmAeGuy_mUMPka6QzWWO0AfhTw6D30PNds0J1QIz8_WoggNNXKhKH)

  

In this specific screenshot we’ve selected three assets in the content browser: the first selection is the moss, which will be the topmost layer, second is the forest ground, which is the middle layer, and third is a generic mud soil, which is the bottom layer.

  

You can control the middle and bottom layers with the R and G vertex channels by vertex painting on your mesh, and the topmost layer can be controlled with the World-Aligned Blend feature that you can enable in your material instance.

  

You can use the B vertex channel to paint water puddles.

  

This workflow may seem a little daunting at first, but with a little experience you’ll find yourself creating and modifying these blend materials really fast. You can also use your own custom blend master material, just make sure all texture parameters inside the master material use the following naming conventions:

  

-   Base Albedo, Base Normal, Base Roughness and so on for the base layer.
    
-   R Albedo, R Normal, R Roughness and so on for the Red vertex channel.
    
-   G Albedo, G Normal, G Roughness and so on for the Green vertex channel.
    
-   B Albedo, B Normal, B Roughness and so on for the Blue vertex channel.
    
-   A Albedo, A Normal, A Roughness and so on for the Alpha vertex channel.
    

  

This is how a base albedo is set up in the default master material, for instance:

  

![](https://lh6.googleusercontent.com/fxSA05XY_LclzoPtzWX3khvx3mnpnuEOJ1vUYRBG30ierO4R0p-W5DhhfuCyx7sICYvhGf_yIYoDkGqr8MmT1BKBLuGsdQD3Csxsvvd4MvcaMSmVjmgdWalGYQheGM-EnEXVyXTb)

  

If you follow this naming convention the LiveLink will auto-detect all textures that need to be connected and do its job accordingly.

  

## Using Custom Master Materials

![](https://lh5.googleusercontent.com/YFh8MozjqzHhFXSAv9uyJeY4UqMN98Dqqhg3ewyZdRgPdpC5TcZXxtjROgdJVFdRfAYKNf5X70iKrEgjM6BypnR18k_WbeitGHaPq1qlF1Hfas0UF3kWjh8svx9mi_StPPNUSgOH)

  

Quick Video Guide - [Custom Master Materials Workflow](https://www.youtube.com/watch?v=RDiWgZyDI-Y)

  

The LiveLink comes with all the master materials needed to use the library, but using your own master materials is also possible and very easy to set up.

  

After following the naming conventions discussed in the previous section, save your master material and click on the arrow icon on the LiveLink window while your master material is selected in the content browser. It will now be used as the default master material for a specific category.

  

You can change the categories by clicking the “Surface” dropdown button at the top-left of the LiveLink window, there you have a list of all the different asset types, each one having their own master material that you can change.

  

## Working with Foliage and Scatter assets

![](https://lh4.googleusercontent.com/qL4k5vSGCw7XvGV9X7_vF7Jr7O_Ps3ADQdylSOOZhPHVnf8Eig-C4OP5uLYJRFrIDUiP6lV1s20vuHBw1uzZe6mflIX-KGgbhG96GcI9DPhy1PfIHj60wIFFmW8NSrWMOaPTeNa8)

  

Quick Video Guide - [Scatter and Foliage Workflow](https://www.youtube.com/watch?v=Tx3Gbmesu_w)

  

One of the aspects of the LiveLink we’ve worked on the most was the scatter/foliage system. Unreal already has a robust foliage editor and with the Megascans LiveLink you can scatter your assets in a click or two.

  

If you want to automatically populate your foliage editor’s asset list with the latest imported assets, check the “Auto-Populate Foliage Painter” checkbox in the LiveLink window and then click on export in Bridge to immediately start painting inside UE4.




##
![ - ](https://i.imgur.com/IrnXhDI.png)

## Extending the LiveLink with Python Scripting

Having the plugin work 100% with python comes with a lot of advantages if you're looking into extending it.
First, the entire source code is completely open, and you can find all the LiveLink script files in the LiveLink folder, where they all have the .py format.
UnrealEnginePython also has it's code open-source for you to modify as you want.

The LiveLink gives you access to a set of useful commands, like this one to import a mesh for instance :

```python
ms_import_mesh('C:/Meshes/MyMesh.fbx', '/Game/Mesh_Folder')
```
Or this one to apply a texture map to a material instance :

```python
ms_apply_tex2d_to_inst(inst_uobject, '/Game/Textures/bark_Albedo', 'Albedo')
```
You could push this a lot further and write a relatively small file that automatically imports and sets up your assets : 
```python
# We start off by initializing the unreal_engine module, then we execute the Megascans LiveLink's ms_main.
import unreal_engine as ue
ue.exec('ms_main.py')
 
folderpath_ = "/Game/Wood_Tree"
 
# QFileDialog is a PySide2.QtGui class. We use it to open a file browser for the texture maps and another one for the mesh files.
Textures_Path = QFileDialog.getOpenFileNames(None, str("Select your texture maps"), "", str("Image Files (*.png *.jpg)"))
Mesh_Path = QFileDialog.getOpenFileNames(None, str("Select your geometry files"), "", str("Image Files (*.fbx *.obj)"))

texture_paths = Textures_Path[0]
meshes_ = Mesh_Path[0]

# ms_import_mesh is a ms_main function that imports a given mesh to the input path folderpath_.
for mesh_ in meshes_:
    ms_import_mesh(mesh_, folderpath_)


# ms_import_texture_list imports an array of textures to the input path folderpath_.
ms_import_texture_list(texture_paths, folderpath_)

# Now we create our material instance, which is based on the material Basic_Master.
parent_mat = ue.load_object(Material, "/Game/Basic_Master")
ms_create_material_instance(parent_mat, "Wood_Tree_inst", folderpath_)

# Then we load it.
inst_uobj = ue.load_object(MaterialInstance, folderpath_ + "/" + "Wood_Tree_inst")

# This will return a list of all the meshes available in the folderpath_ folder.
static_mesh_array = [[item, (folderpath_ + "/" + item.get_name())] for item in ue.get_assets(folderpath_) if item.is_a(StaticMesh)]

# Assigning a material instance to our geometry is done by calling ms_main's ms_inst_2_mesh function.
if mesh_path != None:
    ms_inst_2_mesh(inst_uobj, static_mesh_array)

# Once you have our material instance applied to the geometry, we can start applying the textures from texture_paths to the material instance.
for texture in [item for item in ue.get_assets(folderpath_) if item.is_a(Texture2D)]:
    try:
        text_input = ms_get_map(texture.get_name())
        text_input = "metallic" if text_input.lower() == "metalness" else text_input
        # This ms_main function takes the material instance's UObject, the texture's name and an str of the map type (albedo, normal, etc...).
        ms_apply_tex2d_to_inst(inst_uobj, texture.get_path_name(), text_input)
    except:
        pass
 
# Finally we sync the content browser to the folderpath_'s content.
ue.sync_browser_to_assets(ue.get_assets(folderpath_))

```

That file should give you an idea on how to interact with the Megascans LiveLink and UnrealEnginePython in general. If you have any questions feel free to check the UnrealEnginePython GitHub page or send a, email to adnan at quixel.se !
