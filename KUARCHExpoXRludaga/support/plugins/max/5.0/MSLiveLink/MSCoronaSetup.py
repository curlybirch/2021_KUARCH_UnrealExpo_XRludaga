import os, sys, json
import MSLiveLinkHelpers
helper = MSLiveLinkHelpers.LiveLinkHelper()

class CoronaSetup():

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

        specularLUT = "SPECULARTOIOR"

        MAT_NODE_NAME = CoronaMtl()
        MAT_NODE_NAME.name = ("MS_MATNAME")

        -- Metal IOR Falloff Map Generator
        fn getMetalIORFalloffMap type =
        (
            --  Most of the code in this function is taken from the cg-talk thread 
            --  "Is it possible To Create and Edit Output Map Curve?"
            --  http://forums.cgsociety.org/showthread.php?f=98&t=993502  
            --  Thanks goes to denisT for sharing these great tech tips.
            --  Thanks goes to Martin Geupel for the backup system.
            --  Modified by dubcat to work with falloff map.
            falloffmap = undefined
            backupMtl = undefined
            selectedSlot = undefined
            isEditOpen = undefined
            
            try(destroydialog easyCCurve) catch()
            rollout easyCCurve "Easy CCurve" width:208 height:215
            (
                fn mouseWindowMove hwnd x y sx sy =
                (
                    fn makeParam LoWord HiWord =
                    (
                        bit.or (bit.shift HiWord 16) (bit.and LoWord 0xFFFF)
                    )
                    WM_LBUTTONDOWN  = 0x0201
                    WM_LBUTTONUP    = 0x0202
                    WM_MOUSEMOVE    = 0x0200
                    MK_LBUTTON    = 0x0001
                    
                    p0 = makeParam x y
                    p1 = makeParam (x+sx) (y+sy)
                    
                    uiaccessor.sendmessage hwnd WM_LBUTTONDOWN 0 p0 
                    uiaccessor.sendmessage hwnd WM_MOUSEMOVE MK_LBUTTON p1 
                    uiaccessor.sendmessage hwnd WM_LBUTTONUP 0 p1 
                )
                curveControl cc numcurves:1 width:200 height:200 pos:[4,4] \
                    zoomvalues:[200,100] scrollvalues:[4,2] uiFlags:#() rcmFlags:#()
            )
            createdialog easyCCurve style:#() pos:[-1000,300]
            
            with redraw off
            (
                d_hwnd = (windows.getChildHWND 0 easyCCurve.title)[1]
                c_hwnd = for w in (windows.getChildrenHWND d_hwnd) where w[4] == "DefCurveWindow" do exit with w[1]
                
                cc = easyCCurve.cc.curves[1]
                cc.color = black
                cc.numpoints = 3
                
                pp = easyCCurve.cc.curves[1].points
                pp.selected = on

                cc.numpoints = 3
                pp = easyCCurve.cc.curves[1].points
                pp.selected = on
                
                pp[1].outtangent = [0,0]
                
                pp[2].value = [0.39,0.0]
                pp[2].outtangent = [0.51,0]
                pp[2].intangent = [-0.39,0]
                
                pp[3].value = [1,1]
            
                -- Make Backups
                backupMtl = meditmaterials[1]
                selectedSlot = medit.GetActiveMtlSlot()
                isEditOpen = MatEditor.isOpen()
                matEditorMode = MatEditor.mode 
                
                if matEditorMode == #advanced then (
                    MatEditor.mode = #basic
                )
                
                -- Make Falloff Map
                falloffmap = falloff name:"Complex IOR"
                medit.PutMtlToMtlEditor falloffmap 1
                medit.SetActiveMtlSlot 1 on
                    
                -- Replace Curve
                replaceinstances falloffmap.MixCurve.curve_1 easyCCurve.cc.curves[1][1].parent
                    
                -- Restore Backups
                medit.PutMtlToMtlEditor backupMtl 1
                medit.SetActiveMtlSlot selectedSlot on
                if not isEditOpen do MatEditor.Close()
                MatEditor.mode = matEditorMode
            )
            destroydialog easyCCurve
            free easyCCurve
            
            falloffmap
        )

        -- If Fabric is true
        if isFabric == true then
        (
            --Diffuse
            -- If there is an AO map
            if aoBitmap != undefined then
            (
                MAT_NODE_NAME.texmapDiffuse = falloff ()
                MAT_NODE_NAME.texmapDiffuse.name = ("Fabric Falloff")
                MAT_NODE_NAME.texmapDiffuse.map1on = on
            
                -- Corona Mix
                MAT_NODE_NAME.texmapDiffuse.map1 = CoronaMix()
                MAT_NODE_NAME.texmapDiffuse.map1.name = ("Diffuse")
                MAT_NODE_NAME.texmapDiffuse.map1.mixOperation = 2
                MAT_NODE_NAME.texmapDiffuse.map1.mixAmount = 1
                -- AO (Top Slot)
                MAT_NODE_NAME.texmapDiffuse.map1.texmapTop = CoronaBitmap()
                MAT_NODE_NAME.texmapDiffuse.map1.texmapTop.name = ("Ambient Occlusion")
                MAT_NODE_NAME.texmapDiffuse.map1.texmapTop.filename = ("TEX_AO")
                MAT_NODE_NAME.texmapDiffuse.map1.texmapTop.gamma = 2.2
                MAT_NODE_NAME.texmapDiffuse.map1.texmapTop.interpolation = 1
                MAT_NODE_NAME.texmapDiffuse.map1.texmapTop.filteringBlur = 0.01
                -- Albedo (Bottom Slot)
                -- If there is an Albedo map
                if albedoBitmap != undefined then
                (
                    MAT_NODE_NAME.texmapDiffuse.map1.texmapBottom = CoronaBitmap()
                    MAT_NODE_NAME.texmapDiffuse.map1.texmapBottom.name = ("Albedo")
                    MAT_NODE_NAME.texmapDiffuse.map1.texmapBottom.filename = ("TEX_ALBEDO")
                    MAT_NODE_NAME.texmapDiffuse.map1.texmapBottom.gamma = 2.2
                    MAT_NODE_NAME.texmapDiffuse.map1.texmapBottom.interpolation = 1
                    MAT_NODE_NAME.texmapDiffuse.map1.texmapBottom.filteringBlur = 0.01
                )
                -- Color Correct Albedo
                MAT_NODE_NAME.texmapDiffuse.map2on = on
                MAT_NODE_NAME.texmapDiffuse.map2 = Color_Correction()
                MAT_NODE_NAME.texmapDiffuse.map2.name = ("Gamma 1.5")
                MAT_NODE_NAME.texmapDiffuse.map2.lightnessMode = 1
                MAT_NODE_NAME.texmapDiffuse.map2.gammaRGB = 1.5
                
                -- Corona Mix
                MAT_NODE_NAME.texmapDiffuse.map2.map = CoronaMix()
                MAT_NODE_NAME.texmapDiffuse.map2.map.name = ("Diffuse")
                MAT_NODE_NAME.texmapDiffuse.map2.map.mixOperation = 2
                MAT_NODE_NAME.texmapDiffuse.map2.map.mixAmount = 1
                -- AO (Top Slot)
                MAT_NODE_NAME.texmapDiffuse.map2.map.texmapTop = CoronaBitmap()
                MAT_NODE_NAME.texmapDiffuse.map2.map.texmapTop.name = ("Ambient Occlusion")
                MAT_NODE_NAME.texmapDiffuse.map2.map.texmapTop.filename = ("TEX_AO")
                MAT_NODE_NAME.texmapDiffuse.map2.map.texmapTop.gamma = 2.2
                MAT_NODE_NAME.texmapDiffuse.map2.map.texmapTop.interpolation = 1
                MAT_NODE_NAME.texmapDiffuse.map2.map.texmapTop.filteringBlur = 0.01
                -- Albedo (Bottom Slot)
                -- If there is an Albedo map
                if albedoBitmap != undefined then
                (
                    MAT_NODE_NAME.texmapDiffuse.map2.map.texmapBottom = CoronaBitmap()
                    MAT_NODE_NAME.texmapDiffuse.map2.map.texmapBottom.name = ("Albedo")
                    MAT_NODE_NAME.texmapDiffuse.map2.map.texmapBottom.filename = ("TEX_ALBEDO")
                    MAT_NODE_NAME.texmapDiffuse.map2.map.texmapBottom.gamma = 2.2
                    MAT_NODE_NAME.texmapDiffuse.map2.map.texmapBottom.interpolation = 1
                    MAT_NODE_NAME.texmapDiffuse.map2.map.texmapBottom.filteringBlur = 0.01
                )
                
            )
        )
        
        --Diffuse
        -- If there is an AO map and no Metalness and not fabric
        if aoBitmap != undefined and metallicBitmap == undefined and isFabric == false then
        (
            -- Corona Mix
            MAT_NODE_NAME.texmapDiffuse = CoronaMix()
            MAT_NODE_NAME.texmapDiffuse.name = ("Diffuse")
            MAT_NODE_NAME.texmapDiffuse.mixOperation = 2
            MAT_NODE_NAME.texmapDiffuse.mixAmount = 1
            -- AO (Top Slot)
            MAT_NODE_NAME.texmapDiffuse.texmapTop = CoronaBitmap()
            MAT_NODE_NAME.texmapDiffuse.texmapTop.name = ("Ambient Occlusion")
            MAT_NODE_NAME.texmapDiffuse.texmapTop.filename = ("TEX_AO")
            MAT_NODE_NAME.texmapDiffuse.texmapTop.gamma = 2.2
            MAT_NODE_NAME.texmapDiffuse.texmapTop.interpolation = 1
            MAT_NODE_NAME.texmapDiffuse.texmapTop.filteringBlur = 0.01
            -- Albedo (Bottom Slot)
            -- If there is an Albedo map but no Fuzz map
            if albedoBitmap != undefined and fuzzBitmap == undefined then
            (
                MAT_NODE_NAME.texmapDiffuse.texmapBottom = CoronaBitmap()
                MAT_NODE_NAME.texmapDiffuse.texmapBottom.name = ("Albedo")
                MAT_NODE_NAME.texmapDiffuse.texmapBottom.filename = ("TEX_ALBEDO")
                MAT_NODE_NAME.texmapDiffuse.texmapBottom.gamma = 2.2
                MAT_NODE_NAME.texmapDiffuse.texmapBottom.interpolation = 1
                MAT_NODE_NAME.texmapDiffuse.texmapBottom.filteringBlur = 0.01
            )
            -- If there is an Albedo map and a Fuzz map
            if albedoBitmap != undefined and fuzzBitmap != undefined then
            (
                MAT_NODE_NAME.texmapDiffuse.texmapBottom = CoronaMix()
                MAT_NODE_NAME.texmapDiffuse.texmapBottom.name = ("Fuzzy Shading")
                MAT_NODE_NAME.texmapDiffuse.texmapBottom.mixOperation = 6
                
                MAT_NODE_NAME.texmapDiffuse.texmapBottom.texmapTop = CoronaMix()
                MAT_NODE_NAME.texmapDiffuse.texmapBottom.texmapTop.name = ("Multiply")
                MAT_NODE_NAME.texmapDiffuse.texmapBottom.texmapTop.mixOperation = 2
                
                MAT_NODE_NAME.texmapDiffuse.texmapBottom.texmapBottom = CoronaBitmap()
                MAT_NODE_NAME.texmapDiffuse.texmapBottom.texmapBottom.name = ("Albedo")
                MAT_NODE_NAME.texmapDiffuse.texmapBottom.texmapBottom.filename = ("TEX_ALBEDO")
                MAT_NODE_NAME.texmapDiffuse.texmapBottom.texmapBottom.gamma = 2.2
                MAT_NODE_NAME.texmapDiffuse.texmapBottom.texmapBottom.interpolation = 1
                MAT_NODE_NAME.texmapDiffuse.texmapBottom.texmapBottom.filteringBlur = 0.01
                
                MAT_NODE_NAME.texmapDiffuse.texmapBottom.texmapMix = CoronaBitmap()
                MAT_NODE_NAME.texmapDiffuse.texmapBottom.texmapMix.name = ("Fuzz Mask")
                MAT_NODE_NAME.texmapDiffuse.texmapBottom.texmapMix.filename = ("TEX_FUZZ")
                MAT_NODE_NAME.texmapDiffuse.texmapBottom.texmapMix.gamma = 2.2
                MAT_NODE_NAME.texmapDiffuse.texmapBottom.texmapMix.interpolation = 1
                MAT_NODE_NAME.texmapDiffuse.texmapBottom.texmapMix.filteringBlur = 0.01
                
                MAT_NODE_NAME.texmapDiffuse.texmapBottom.texmapTop.texmapTop = CoronaBitmap()
                MAT_NODE_NAME.texmapDiffuse.texmapBottom.texmapTop.texmapTop.name = ("Albedo")
                MAT_NODE_NAME.texmapDiffuse.texmapBottom.texmapTop.texmapTop.filename = ("TEX_ALBEDO")
                MAT_NODE_NAME.texmapDiffuse.texmapBottom.texmapTop.texmapTop.gamma = 2.2
                MAT_NODE_NAME.texmapDiffuse.texmapBottom.texmapTop.texmapTop.interpolation = 1
                MAT_NODE_NAME.texmapDiffuse.texmapBottom.texmapTop.texmapTop.filteringBlur = 0.01
                
                MAT_NODE_NAME.texmapDiffuse.texmapBottom.texmapTop.texmapBottom = CoronaMix()
                MAT_NODE_NAME.texmapDiffuse.texmapBottom.texmapTop.texmapBottom.name = ("Add")
                MAT_NODE_NAME.texmapDiffuse.texmapBottom.texmapTop.texmapBottom.mixOperation = 0
                
                MAT_NODE_NAME.texmapDiffuse.texmapBottom.texmapTop.texmapBottom.texmapTop = CoronaMix()
                MAT_NODE_NAME.texmapDiffuse.texmapBottom.texmapTop.texmapBottom.texmapTop.name = ("Subtract")
                MAT_NODE_NAME.texmapDiffuse.texmapBottom.texmapTop.texmapBottom.texmapTop.mixOperation = 1
                MAT_NODE_NAME.texmapDiffuse.texmapBottom.texmapTop.texmapBottom.texmapTop.colorBottom = color 255 255 255
                MAT_NODE_NAME.texmapDiffuse.texmapBottom.texmapTop.texmapBottom.texmapTop.mixInSRgb = off
                
                MAT_NODE_NAME.texmapDiffuse.texmapBottom.texmapTop.texmapBottom.texmapTop.texmapTop = CoronaMix()
                MAT_NODE_NAME.texmapDiffuse.texmapBottom.texmapTop.texmapBottom.texmapTop.texmapTop.name = ("Multiply")
                MAT_NODE_NAME.texmapDiffuse.texmapBottom.texmapTop.texmapBottom.texmapTop.texmapTop.mixOperation = 2
                
                MAT_NODE_NAME.texmapDiffuse.texmapBottom.texmapTop.texmapBottom.texmapTop.texmapTop.texmapTop = CoronaColor()
                MAT_NODE_NAME.texmapDiffuse.texmapBottom.texmapTop.texmapBottom.texmapTop.texmapTop.texmapTop.name = ("Core Darkness | ADJUST")
                MAT_NODE_NAME.texmapDiffuse.texmapBottom.texmapTop.texmapBottom.texmapTop.texmapTop.texmapTop.color = color 255 255 255
                MAT_NODE_NAME.texmapDiffuse.texmapBottom.texmapTop.texmapBottom.texmapTop.texmapTop.texmapTop.multiplier = 0.8
                
                MAT_NODE_NAME.texmapDiffuse.texmapBottom.texmapTop.texmapBottom.texmapTop.texmapTop.texmapBottom = falloff()
                MAT_NODE_NAME.texmapDiffuse.texmapBottom.texmapTop.texmapBottom.texmapTop.texmapTop.texmapBottom.name = ("Falloff")
                MAT_NODE_NAME.texmapDiffuse.texmapBottom.texmapTop.texmapBottom.texmapTop.texmapTop.texmapBottom.color1 = color 255 255 255
                MAT_NODE_NAME.texmapDiffuse.texmapBottom.texmapTop.texmapBottom.texmapTop.texmapTop.texmapBottom.color2 = color 0 0 0
                
                MAT_NODE_NAME.texmapDiffuse.texmapBottom.texmapTop.texmapBottom.texmapBottom = CoronaMix()
                MAT_NODE_NAME.texmapDiffuse.texmapBottom.texmapTop.texmapBottom.texmapBottom.name = ("Multiply")
                MAT_NODE_NAME.texmapDiffuse.texmapBottom.texmapTop.texmapBottom.texmapBottom.mixOperation = 2
                
                MAT_NODE_NAME.texmapDiffuse.texmapBottom.texmapTop.texmapBottom.texmapBottom.texmapTop = CoronaColor()
                MAT_NODE_NAME.texmapDiffuse.texmapBottom.texmapTop.texmapBottom.texmapBottom.texmapTop.name = ("Edge Brightness | ADJUST")
                MAT_NODE_NAME.texmapDiffuse.texmapBottom.texmapTop.texmapBottom.texmapBottom.texmapTop.color = color 255 255 255
                MAT_NODE_NAME.texmapDiffuse.texmapBottom.texmapTop.texmapBottom.texmapBottom.texmapTop.multiplier = 0.8
                
                MAT_NODE_NAME.texmapDiffuse.texmapBottom.texmapTop.texmapBottom.texmapBottom.texmapBottom = Color_Correction()
                MAT_NODE_NAME.texmapDiffuse.texmapBottom.texmapTop.texmapBottom.texmapBottom.texmapBottom.name = ("Power | ADJUST")
                MAT_NODE_NAME.texmapDiffuse.texmapBottom.texmapTop.texmapBottom.texmapBottom.texmapBottom.lightnessMode = 1
                MAT_NODE_NAME.texmapDiffuse.texmapBottom.texmapTop.texmapBottom.texmapBottom.texmapBottom.gammaRGB = 0.167
                
                MAT_NODE_NAME.texmapDiffuse.texmapBottom.texmapTop.texmapBottom.texmapBottom.texmapBottom.map = falloff()
                MAT_NODE_NAME.texmapDiffuse.texmapBottom.texmapTop.texmapBottom.texmapBottom.texmapBottom.map.name = ("Falloff")
            )
        )

        if aoBitmap == undefined and albedoBitmap != undefined and fuzzBitmap != undefined and metallicBitmap == undefined and isFabric == false then
        (
            MAT_NODE_NAME.texmapDiffuse = CoronaMix()
            MAT_NODE_NAME.texmapDiffuse.name = ("Fuzzy Shading")
            MAT_NODE_NAME.texmapDiffuse.mixOperation = 6
            
            MAT_NODE_NAME.texmapDiffuse.texmapTop = CoronaMix()
            MAT_NODE_NAME.texmapDiffuse.texmapTop.name = ("Multiply")
            MAT_NODE_NAME.texmapDiffuse.texmapTop.mixOperation = 2
            
            MAT_NODE_NAME.texmapDiffuse.texmapBottom = CoronaBitmap()
            MAT_NODE_NAME.texmapDiffuse.texmapBottom.name = ("Albedo")
            MAT_NODE_NAME.texmapDiffuse.texmapBottom.filename = ("TEX_ALBEDO")
            MAT_NODE_NAME.texmapDiffuse.texmapBottom.gamma = 2.2
            MAT_NODE_NAME.texmapDiffuse.texmapBottom.interpolation = 1
            MAT_NODE_NAME.texmapDiffuse.texmapBottom.filteringBlur = 0.01
            
            MAT_NODE_NAME.texmapDiffuse.texmapMix = CoronaBitmap()
            MAT_NODE_NAME.texmapDiffuse.texmapMix.name = ("Fuzz Mask")
            MAT_NODE_NAME.texmapDiffuse.texmapMix.filename = ("TEX_FUZZ")
            MAT_NODE_NAME.texmapDiffuse.texmapMix.gamma = 2.2
            MAT_NODE_NAME.texmapDiffuse.texmapMix.interpolation = 1
            MAT_NODE_NAME.texmapDiffuse.texmapMix.filteringBlur = 0.01
            
            MAT_NODE_NAME.texmapDiffuse.texmapTop.texmapTop = CoronaBitmap()
            MAT_NODE_NAME.texmapDiffuse.texmapTop.texmapTop.name = ("Albedo")
            MAT_NODE_NAME.texmapDiffuse.texmapTop.texmapTop.filename = ("TEX_ALBEDO")
            MAT_NODE_NAME.texmapDiffuse.texmapTop.texmapTop.gamma = 2.2
            MAT_NODE_NAME.texmapDiffuse.texmapTop.texmapTop.interpolation = 1
            MAT_NODE_NAME.texmapDiffuse.texmapTop.texmapTop.filteringBlur = 0.01
            
            MAT_NODE_NAME.texmapDiffuse.texmapTop.texmapBottom = CoronaMix()
            MAT_NODE_NAME.texmapDiffuse.texmapTop.texmapBottom.name = ("Add")
            MAT_NODE_NAME.texmapDiffuse.texmapTop.texmapBottom.mixOperation = 0
            
            MAT_NODE_NAME.texmapDiffuse.texmapTop.texmapBottom.texmapTop = CoronaMix()
            MAT_NODE_NAME.texmapDiffuse.texmapTop.texmapBottom.texmapTop.mixOperation = 1
            MAT_NODE_NAME.texmapDiffuse.texmapTop.texmapBottom.texmapTop.name = ("Subtract")
            MAT_NODE_NAME.texmapDiffuse.texmapTop.texmapBottom.texmapTop.colorBottom = color 255 255 255
            MAT_NODE_NAME.texmapDiffuse.texmapTop.texmapBottom.texmapTop.mixInSRgb = off
            
            MAT_NODE_NAME.texmapDiffuse.texmapTop.texmapBottom.texmapTop.texmapTop = CoronaMix()
            MAT_NODE_NAME.texmapDiffuse.texmapTop.texmapBottom.texmapTop.texmapTop.name = ("Multiply")
            MAT_NODE_NAME.texmapDiffuse.texmapTop.texmapBottom.texmapTop.texmapTop.mixOperation = 2
            
            MAT_NODE_NAME.texmapDiffuse.texmapTop.texmapBottom.texmapTop.texmapTop.texmapTop = CoronaColor()
            MAT_NODE_NAME.texmapDiffuse.texmapTop.texmapBottom.texmapTop.texmapTop.texmapTop.name = ("Core Darkness | ADJUST")
            MAT_NODE_NAME.texmapDiffuse.texmapTop.texmapBottom.texmapTop.texmapTop.texmapTop.color = color 255 255 255
            MAT_NODE_NAME.texmapDiffuse.texmapTop.texmapBottom.texmapTop.texmapTop.texmapTop.multiplier = 0.8
            
            MAT_NODE_NAME.texmapDiffuse.texmapTop.texmapBottom.texmapTop.texmapTop.texmapBottom = falloff()
            MAT_NODE_NAME.texmapDiffuse.texmapTop.texmapBottom.texmapTop.texmapTop.texmapBottom.name = ("Falloff")
            MAT_NODE_NAME.texmapDiffuse.texmapTop.texmapBottom.texmapTop.texmapTop.texmapBottom.color1 = color 255 255 255
            MAT_NODE_NAME.texmapDiffuse.texmapTop.texmapBottom.texmapTop.texmapTop.texmapBottom.color2 = color 0 0 0
            
            MAT_NODE_NAME.texmapDiffuse.texmapTop.texmapBottom.texmapBottom = CoronaMix()
            MAT_NODE_NAME.texmapDiffuse.texmapTop.texmapBottom.texmapBottom.name = ("Multiply")
            MAT_NODE_NAME.texmapDiffuse.texmapTop.texmapBottom.texmapBottom.mixOperation = 2
            
            MAT_NODE_NAME.texmapDiffuse.texmapTop.texmapBottom.texmapBottom.texmapTop = CoronaColor()
            MAT_NODE_NAME.texmapDiffuse.texmapTop.texmapBottom.texmapBottom.texmapTop.name = ("Edge Brightness | ADJUST")
            MAT_NODE_NAME.texmapDiffuse.texmapTop.texmapBottom.texmapBottom.texmapTop.color = color 255 255 255
            MAT_NODE_NAME.texmapDiffuse.texmapTop.texmapBottom.texmapBottom.texmapTop.multiplier = 0.8
            
            MAT_NODE_NAME.texmapDiffuse.texmapTop.texmapBottom.texmapBottom.texmapBottom = Color_Correction()
            MAT_NODE_NAME.texmapDiffuse.texmapTop.texmapBottom.texmapBottom.texmapBottom.name = ("Power | ADJUST")
            MAT_NODE_NAME.texmapDiffuse.texmapTop.texmapBottom.texmapBottom.texmapBottom.lightnessMode = 1
            MAT_NODE_NAME.texmapDiffuse.texmapTop.texmapBottom.texmapBottom.texmapBottom.gammaRGB = 0.167
            
            MAT_NODE_NAME.texmapDiffuse.texmapTop.texmapBottom.texmapBottom.texmapBottom.map = falloff()
            MAT_NODE_NAME.texmapDiffuse.texmapTop.texmapBottom.texmapBottom.texmapBottom.map.name = ("Falloff")
        )

        -- If there is no AO map and no Fuzz map and no Metalness
        if aoBitmap == undefined and fuzzBitmap == undefined and metallicBitmap == undefined and isFabric == false then
        (
            -- Albedo
            -- If there is an Albedo map
            if albedoBitmap != undefined then
            (
                MAT_NODE_NAME.texmapDiffuse = CoronaBitmap()
                MAT_NODE_NAME.texmapDiffuse.name = ("Diffuse")
                MAT_NODE_NAME.texmapDiffuse.filename = ("TEX_ALBEDO")
                MAT_NODE_NAME.texmapDiffuse.gamma = 2.2
                MAT_NODE_NAME.texmapDiffuse.interpolation = 1
                MAT_NODE_NAME.texmapDiffuse.filteringBlur = 0.01
            )
        )

        -- Albedo
        -- If there is a metalness map
        if metallicBitmap != undefined and isFabric == false then
        (
            MAT_NODE_NAME.texmapDiffuse = CoronaBitmap()
            MAT_NODE_NAME.texmapDiffuse.name = ("Diffuse")
            MAT_NODE_NAME.texmapDiffuse.filename = ("TEX_ALBEDO")
            MAT_NODE_NAME.texmapDiffuse.gamma = 2.2
            MAT_NODE_NAME.texmapDiffuse.interpolation = 1
            MAT_NODE_NAME.texmapDiffuse.filteringBlur = 0.01
        )

        -- Reflection
        MAT_NODE_NAME.levelReflect = 1

        -- If there is a metalness map
        if metallicBitmap != undefined then
        (
            -- Disable IOR
            MAT_NODE_NAME.fresnelIor = 999
            
            -- New Metal IOR
            -- If there is a specular map
            if specularBitmap != undefined then
            (
                MAT_NODE_NAME.texmapReflect = getMetalIORFalloffMap(1)
                MAT_NODE_NAME.texmapReflect.map1On = on
                MAT_NODE_NAME.texmapReflect.map1 = CoronaBitmap()
                MAT_NODE_NAME.texmapReflect.map1.name = ("Complex IOR Color")
                MAT_NODE_NAME.texmapReflect.map1.filename = ("TEX_SPECULAR")
                MAT_NODE_NAME.texmapReflect.map1.gamma = 2.2
                MAT_NODE_NAME.texmapReflect.map1.interpolation = 1
                MAT_NODE_NAME.texmapReflect.map1.filteringBlur = 0.01
            )
        )
        
        --Bump
        if bumpBitmap != undefined then
        (
            BumpNode = CoronaBitmap ()
            BumpNode.gamma = 1.0
            BumpNode.filename =("TEX_BUMP")
            BumpNode.name = ("Bump")
            ActiveSMEView.CreateNode BumpNode [-300, 700]
        )
        
        --Cavity
        if cavityBitmap != undefined then
        (
            CavityNode = CoronaBitmap ()
            CavityNode.gamma = 1.0
            CavityNode.filename =("TEX_CAVITY")
            CavityNode.name = ("CAVITY")
            ActiveSMEView.CreateNode CavityNode [-300, 800]
        )
              
        -- Glossiness
        -- If there is a Glossiness map
        if glossBitmap != undefined then
        (
            MAT_NODE_NAME.texmapReflectGlossiness = CoronaBitmap()
            MAT_NODE_NAME.texmapReflectGlossiness.name = ("Glossiness")
            MAT_NODE_NAME.texmapReflectGlossiness.filename = ("TEX_GLOSS")
            MAT_NODE_NAME.texmapReflectGlossiness.gamma = 1.0
            MAT_NODE_NAME.texmapReflectGlossiness.interpolation = 1
            MAT_NODE_NAME.texmapReflectGlossiness.filteringBlur = 0.01
        )
        else if roughnessBitmap != undefined then
        (
            MAT_NODE_NAME.texmapReflectGlossiness = CoronaBitmap()
            MAT_NODE_NAME.texmapReflectGlossiness.name = ("Glossiness")
            MAT_NODE_NAME.texmapReflectGlossiness.filename = ("TEX_ROUGHNESS")
            MAT_NODE_NAME.texmapReflectGlossiness.gamma = 1.0
            MAT_NODE_NAME.texmapReflectGlossiness.interpolation = 1
            MAT_NODE_NAME.texmapReflectGlossiness.filteringBlur = 0.01
            MAT_NODE_NAME.texmapReflectGlossiness.output.invert = true
        )

        --Index of Refraction
        if metallicBitmap == undefined then
        (
            MAT_NODE_NAME.fresnelIor = 1.5
            -- If there is a specular map and an IOR LUT and no Metalness
            if specularBitmap != undefined and specularLUT != undefined then
            (
                -- Color Correction
                MAT_NODE_NAME.texmapFresnelIor = Color_Correction()
                MAT_NODE_NAME.texmapFresnelIor.name = ("Convert to sRGB")
                MAT_NODE_NAME.texmapFresnelIor.lightnessMode = 1
                MAT_NODE_NAME.texmapFresnelIor.gammaRGB = 2.2
                MAT_NODE_NAME.texmapFresnelIor.map = CoronaColorCorrect()
                
                -- Corona Color Correct
                MAT_NODE_NAME.texmapFresnelIor.map.name = ("Reflectance to IOR")
                MAT_NODE_NAME.texmapFresnelIor.map.lutEnable = on
                MAT_NODE_NAME.texmapFresnelIor.map.lutFile = "SPECULARTOIOR"
                MAT_NODE_NAME.texmapFresnelIor.map.inputTexmap = Color_Correction()
                
                -- Color Correction
                MAT_NODE_NAME.texmapFresnelIor.map.inputTexmap.name = ("Convert to Linear")
                MAT_NODE_NAME.texmapFresnelIor.map.inputTexmap.lightnessMode = 1
                MAT_NODE_NAME.texmapFresnelIor.map.inputTexmap.gammaRGB = 0.45
                MAT_NODE_NAME.texmapFresnelIor.map.inputTexmap.map = CoronaBitmap()
                
                -- Corona Bitmap
                MAT_NODE_NAME.texmapFresnelIor.map.inputTexmap.map.name = ("Specular")
                MAT_NODE_NAME.texmapFresnelIor.map.inputTexmap.map.filename = ("TEX_SPECULAR")
                MAT_NODE_NAME.texmapFresnelIor.map.inputTexmap.map.gamma = 1.0
                MAT_NODE_NAME.texmapFresnelIor.map.inputTexmap.map.interpolation = 1
                MAT_NODE_NAME.texmapFresnelIor.map.inputTexmap.map.filteringBlur = 0.01
            )
        )

        --Translucency
        -- If there is a translucency map
        if translucencyBitmap != undefined and metallicBitmap == undefined then
        (
            MAT_NODE_NAME.texmapTranslucency = CoronaBitmap()
            MAT_NODE_NAME.texmapTranslucency.name = ("Translucency")
            MAT_NODE_NAME.texmapTranslucency.filename = ("TEX_TRANSLUCENCY")
            MAT_NODE_NAME.texmapTranslucency.gamma = 2.2
            MAT_NODE_NAME.texmapTranslucency.interpolation = 1
            MAT_NODE_NAME.texmapTranslucency.filteringBlur = 0.01
            MAT_NODE_NAME.texmapTranslucency.output.rgb_level = 2
            MAT_NODE_NAME.levelTranslucency = 0.5
        )

        --Transmission
        -- If there is a translucency map
        if transmissionBitmap != undefined and metallicBitmap == undefined then
        (
            MAT_NODE_NAME.texmapTranslucencyFraction = CoronaBitmap()
            MAT_NODE_NAME.texmapTranslucencyFraction.name = ("Transmission")
            MAT_NODE_NAME.texmapTranslucencyFraction.filename = ("TEX_TRANSMISSION")
            MAT_NODE_NAME.texmapTranslucencyFraction.gamma = 1.0
            MAT_NODE_NAME.texmapTranslucencyFraction.interpolation = 1
            MAT_NODE_NAME.texmapTranslucencyFraction.filteringBlur = 0.01
        )

        --Opacity
        -- If there is an opacity map
        if opacityBitmap != undefined then
        (
            MAT_NODE_NAME.texmapOpacity = CoronaBitmap()
            MAT_NODE_NAME.texmapOpacity.name = ("Opacity")
            MAT_NODE_NAME.texmapOpacity.filename = ("TEX_OPACITY")
            MAT_NODE_NAME.texmapOpacity.gamma = 1.0
            MAT_NODE_NAME.texmapOpacity.interpolation = 1
            MAT_NODE_NAME.texmapOpacity.filteringBlur = 0.01
        )
        

        --Normal Map
        -- If there is a normal map
        if normalBitmap != undefined then
        (
            --Corona Normal
            MAT_NODE_NAME.texmapBump = CoronaNormal()
            MAT_NODE_NAME.texmapBump.name = ("Corona Normal")
            MAT_NODE_NAME.texmapBump.flipgreen = on
            MAT_NODE_NAME.mapamountBump = 99

            --Normal
            MAT_NODE_NAME.texmapBump.NormalMap = CoronaBitmap()
            MAT_NODE_NAME.texmapBump.NormalMap.name = ("Normal")
            MAT_NODE_NAME.texmapBump.NormalMap.filename = ("TEX_NORMAL")
            MAT_NODE_NAME.texmapBump.NormalMap.gamma = 1.0
            MAT_NODE_NAME.texmapBump.NormalMap.interpolation = 1
            MAT_NODE_NAME.texmapBump.NormalMap.filteringBlur = 0.01
        )

        if assetLOD != "high" do (
        --Displacement
        if displacementBitmap != undefined then
        (

            dispValue = 2.54
            if (assetType == "surface") do
            (
            dispValue = MS_HEIGHT*50
            )


            select CurOBJs
            dispMod = CoronaDisplacementMod ()
            dispMod.mapSource = 0
            dispMod.levelMin = -dispValue
            dispMod.levelMax = dispValue
            modPanel.addModToSelection (dispMod)

            MAT_NODE_NAME.texmapDisplace = CoronaBitmap()
            MAT_NODE_NAME.texmapDisplace.name = ("Displacement | Disabled by Default")
            MAT_NODE_NAME.texmapDisplace.filename = ("TEX_DISPLACEMENT")
            MAT_NODE_NAME.texmapDisplace.gamma = 1.0
            MAT_NODE_NAME.texmapDisplace.interpolation = 0
            MAT_NODE_NAME.texmapDisplace.filteringBlur = 0.01
            MAT_NODE_NAME.texmapOnDisplacement = on
            MAT_NODE_NAME.displacementMaximum = (dispValue)

        ))

        """).replace("MAT_NODE_NAME", nodeName).replace("MS_MATNAME", matName)

    def GetGlassMaterial(self, nodeName, matName):
        return ("""

        MAT_NODE_NAME = CoronaMtl()
        MAT_NODE_NAME.name = ("MS_MATNAME")

        MAT_NODE_NAME.levelDiffuse = 0
        MAT_NODE_NAME.levelReflect = 1
        MAT_NODE_NAME.reflectGlossiness = 1
        MAT_NODE_NAME.fresnelIor = 1.5
        MAT_NODE_NAME.ior = 1.5
        MAT_NODE_NAME.levelRefract = 1
        MAT_NODE_NAME.refractGlossiness = 1

        if glossBitmap != undefined then
        (
            MAT_NODE_NAME.texmapReflectGlossiness = CoronaBitmap()
            MAT_NODE_NAME.texmapReflectGlossiness.name = ("Glossiness")
            MAT_NODE_NAME.texmapReflectGlossiness.filename = ("TEX_GLOSS")
            MAT_NODE_NAME.texmapReflectGlossiness.gamma = 1.0
            MAT_NODE_NAME.texmapReflectGlossiness.interpolation = 1
            MAT_NODE_NAME.texmapReflectGlossiness.filteringBlur = 0.01
        )
        else if roughnessBitmap != undefined then
        (
            MAT_NODE_NAME.texmapReflectGlossiness = CoronaBitmap()
            MAT_NODE_NAME.texmapReflectGlossiness.name = ("Roughness")
            MAT_NODE_NAME.texmapReflectGlossiness.filename = ("TEX_ROUGHNESS")
            MAT_NODE_NAME.texmapReflectGlossiness.gamma = 1.0
            MAT_NODE_NAME.texmapReflectGlossiness.interpolation = 1
            MAT_NODE_NAME.texmapReflectGlossiness.filteringBlur = 0.01
            MAT_NODE_NAME.texmapReflectGlossiness.output.invert = true
        )

        if normalBitmap != undefined then
        (
            --Corona Normal
            MAT_NODE_NAME.texmapBump = CoronaNormal()
            MAT_NODE_NAME.texmapBump.name = ("Corona Normal")
            MAT_NODE_NAME.texmapBump.flipgreen = on

            --Normal
            MAT_NODE_NAME.texmapBump.NormalMap = CoronaBitmap()
            MAT_NODE_NAME.texmapBump.NormalMap.name = ("Normal")
            MAT_NODE_NAME.texmapBump.NormalMap.filename = ("TEX_NORMAL")
            MAT_NODE_NAME.texmapBump.NormalMap.gamma = 1.0
            MAT_NODE_NAME.texmapBump.NormalMap.interpolation = 1
            MAT_NODE_NAME.texmapBump.NormalMap.filteringBlur = 0.01
        )

        """).replace("MAT_NODE_NAME", nodeName).replace("MS_MATNAME", matName)