import os, sys, json
import MSLiveLinkHelpers
helper = MSLiveLinkHelpers.LiveLinkHelper()

class RedshiftSetup():

    def GetMaterialSetup(self, assetData):
        materialScript = helper.GetActiveSMEView()

        if helper.HasMultipleMaterial(assetData.meta):
            multiNodeName = "MutliMaterial"
            materialScript += helper.CreateMultiSubMaterial(multiNodeName, assetData.materialName, helper.GetNumberOfUniqueMaterial(assetData.meta))
            index = 1
            matsData = helper.ExtractMatData(assetData.meta)
            for matData in matsData:
                matName = assetData.materialName + "_" + str(index)
                nodeName = "MatNode_" + str(index)
                if matData.matType == "glass":
                    materialScript += self.GetGlassMaterial(nodeName, matName)
                else:
                    materialScript += self.GetOpaqueMaterial(nodeName, matName)
                materialScript += helper.AssignMaterialToMultiSlots(multiNodeName, nodeName, matData.matIDs)
                index += 1
            materialScript += helper.CreateNodeInSME(multiNodeName, 0, 0)
            materialScript += helper.AssignMaterialToObjects(multiNodeName)
            materialScript += helper.ShowInViewport(multiNodeName)
        else:
            nodeName = "MatNode"
            materialScript += self.GetOpaqueMaterial(nodeName, assetData.materialName)
            materialScript += helper.CreateNodeInSME(nodeName, 0, 0)
            materialScript += helper.AssignMaterialToObjects(nodeName)
            materialScript += helper.ShowInViewport(nodeName)
        
        helper.DeselectEverything()
        return materialScript

    def GetOpaqueMaterial(self, nodeName, matName):
        return ("""

        --#########################################################################
        -- MATERIAL CREATION : Creates and sets up the material's base parameters. MS_MATNAME is replaced by the material's name.
        --#########################################################################

        MAT_NODE_NAME = rsMaterial()
        MAT_NODE_NAME.name = "MS_MATNAME"
        ActiveSMEView = sme.GetView (sme.activeView)
        ActiveSMEView.CreateNode mat [0, 0]

        --Base Settings
        MAT_NODE_NAME.refl_brdf = 1
        MAT_NODE_NAME.refl_ior = 1.5

        --Generate and Assign Material
        meditMaterials[activeMeditSlot] = MAT_NODE_NAME
        activeMeditSlot = activeMeditSlot + 1

        --MAT_NODE_NAME.showInViewport = true
        CurOBJs.material = meditMaterials[activeMeditSlot - 1]

        if assetLOD != "high" do (
        dispValue = MS_HEIGHT
        if (assetType == "surface") do
        (
        dispValue = 2.0
        )
        dispMod = Redshift_Mesh_Parameters ()
        modPanel.addModToSelection (dispMod)
        dispMod.displacementScale = dispValue
        dispMod.maxDisplacement = 10.0
        )

        --Diffuse Composite
        if aoBitmap != undefined then
        (
            MAT_NODE_NAME.diffuse_color_map = CompositeTexturemap()
            MAT_NODE_NAME.diffuse_color_map.mapEnabled.count = 2
            MAT_NODE_NAME.diffuse_color_map.blendMode[2] = 5
            MAT_NODE_NAME.diffuse_color_map.opacity[2] = 0
            --Diffuse AO
            MAT_NODE_NAME.diffuse_color_map.mapList[2] = Bitmaptexture bitmap:aoBitmap
            MAT_NODE_NAME.diffuse_color_map.mapList[2].coords.blur = 0.01
            --Diffuse Albedo
            if diffuseBitmap != undefined then
            (
                MAT_NODE_NAME.diffuse_color_map.mapList[1] = Bitmaptexture bitmap:diffuseBitmap
                MAT_NODE_NAME.diffuse_color_map.mapList[1].coords.blur = 0.01
            )
        )
        else
        (
            --Diffuse Albedo
            if diffuseBitmap != undefined then
            (
                MAT_NODE_NAME.diffuse_color_map = Bitmaptexture bitmap:diffuseBitmap
                MAT_NODE_NAME.diffuse_color_map.coords.blur = 0.01
            )
        )

        --Metalness
        if metallicBitmap != undefined then
        (
        MAT_NODE_NAME.refl_fresnel_mode = 2
        MAT_NODE_NAME.refl_metalness_map = Bitmaptexture bitmap:metallicBitmap
        MAT_NODE_NAME.refl_metalness_map.coords.blur = 0.01
        )

        --Reflection
        MAT_NODE_NAME.refl_color = color 255 255 255
        
        --Specular
        if specularBitmap != undefined then
        (
            MAT_NODE_NAME.refl_weight_map = Bitmaptexture bitmap:specularBitmap
        )
        else(
            MAT_NODE_NAME.refl_weight = 1
        ) 
        
        --Roughness
        if roughnessBitmap != undefined then
        (
            MAT_NODE_NAME.refl_roughness_map = Bitmaptexture bitmap:roughnessBitmap
            MAT_NODE_NAME.refl_roughness_map.coords.blur = 0.01
        )
        else
        (
            if glossBitmap != undefined then
                (
                MAT_NODE_NAME.refl_roughness_map = Bitmaptexture bitmap:glossBitmap
                MAT_NODE_NAME.refl_roughness_map.output.invert = true
                MAT_NODE_NAME.refl_roughness_map.coords.blur = 0.01
                )
        )

        --Translucency
        if translucencyBitmap != undefined then
        (
        MAT_NODE_NAME.transl_color_map = Bitmaptexture bitmap:translucencyBitmap
        MAT_NODE_NAME.transl_color_map.coords.blur = 0.01
        MAT_NODE_NAME.transl_weight = 0.5
        )

        --Transmission
        if transmissionBitmap != undefined then
        (
        MAT_NODE_NAME.refr_weight_map = Bitmaptexture bitmap:transmissionBitmap
        MAT_NODE_NAME.refr_weight_map.coords.blur = 0.01
        )

        --Opacity
        if opacityBitmap != undefined then
        (
        MAT_NODE_NAME.opacity_color_map = Bitmaptexture bitmap:opacityBitmap
        MAT_NODE_NAME.opacity_color_map.coords.blur = 0.01
        )

        --Normal
        if normalBitmap != undefined then
        (
            MAT_NODE_NAME.bump_input_map = rsNormalMap()
            MAT_NODE_NAME.bump_input_map.tex0 = normalBitmap
        )

        if assetLOD != "high" do (
        --Displacement
        if displacementBitmap != undefined then
        (
            MAT_NODE_NAME.displacement_input_map = rsDisplacement()
            MAT_NODE_NAME.displacement_input_map.scale = 10
            MAT_NODE_NAME.displacement_input_map.texMap_map = Bitmaptexture bitmap:displacementBitmap
            MAT_NODE_NAME.displacement_input_map.texMap_map.coords.blur = 0.01
            MAT_NODE_NAME.displacement_input_map.newrange_min = 0.0
            MAT_NODE_NAME.displacement_input_map.newrange_max = 1.0
            MAT_NODE_NAME.displacement_input_map.scale = 1

        )
        MAT_NODE_NAME.displacement_input_mapenable = on
        )

        select CurOBJs
        for o in selection do o.material = MAT_NODE_NAME
        
        --Bump
        if doesFileExist "TEX_BUMP" do
        (
            myBmp = bitmaptexture filename:"TEX_BUMP"
            myBmp.name = ("Bump") 
            ActiveSMEView.CreateNode myBmp [-300, 700]

        )
        
        --Cavity
        if doesFileExist "TEX_CAVITY" do
        (
            myBmp = bitmaptexture filename:"TEX_CAVITY"
            myBmp.name = ("Cavity") 
            ActiveSMEView.CreateNode myBmp [-300, 800]
     
        )
        --Fuzz
        if doesFileExist "TEX_FUZZ" do
        (
            myBmp = bitmaptexture filename:"TEX_FUZZ" 
            myBmp.name = ("Fuzz") 
            ActiveSMEView.CreateNode myBmp [-300, 900]
   
        )
        
            
            
        actionMan.executeAction 0 "40043"  -- Selection: Select None

        """).replace("MAT_NODE_NAME", nodeName).replace("MS_MATNAME", matName)

    def GetGlassMaterial(self, nodeName, matName):
        return ("""

        MAT_NODE_NAME = rsMaterial()
        MAT_NODE_NAME.name = "MS_MATNAME"
        MAT_NODE_NAME.refr_weight = 1
      
       --Roughness
        if roughnessBitmap != undefined then
        (
            MAT_NODE_NAME.refl_roughness_map = Bitmaptexture bitmap:roughnessBitmap
            MAT_NODE_NAME.refl_roughness_map.coords.blur = 0.01
        )
        else
        (
            if glossBitmap != undefined then
                (
                MAT_NODE_NAME.refl_roughness_map = Bitmaptexture bitmap:glossBitmap
                MAT_NODE_NAME.refl_roughness_map.output.invert = true
                MAT_NODE_NAME.refl_roughness_map.coords.blur = 0.01
                )
        )
        
        if doesFileExist "TEX_NORMAL" do (
            MAT_NODE_NAME.bump_input_map = rsNormalMap()
            MAT_NODE_NAME.bump_input_map.tex0 = normalBitmap
        )


        """).replace("MAT_NODE_NAME", nodeName).replace("MS_MATNAME", matName)
    