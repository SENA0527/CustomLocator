# -*- coding: utf-8 -*-
import sys

import maya.api.OpenMaya as OpenMaya
import maya.api.OpenMayaUI as OpenMayaUI
import maya.api.OpenMayaRender as OpenMayaRender

def maya_useNewAPI():
    pass

#=========================================
class CustomLocator( OpenMayaUI.MPxLocatorNode ):
    
    # ノードのアトリビュート名
    kPluginNodeTypeName = "CustomLocator"
    
    #TypeIDを入れる
    NodeId = OpenMaya.MTypeId(0x80031)#ユニークID
    
    #オーバーライド用のID
    classfication = 'drawdb/geometry/CustomLocator'
    registrantId = 'CustomLocatorPlugin'
    
    #-----------------------------------------------
    def __init__(self):
        OpenMayaUI.MPxLocatorNode.__init__(self)
    
    #-----------------------------------------------
    def draw( self, view, path, style, status ):
        pass
    
    #-----------------------------------------------
    def isBounded( self ):
        return True
    
    #-----------------------------------------------
    def boundingBox( self ):
    
        return OpenMaya.MBoundingBox( OpenMaya.MPoint( 1.0, 1.0, 1.0 ), 
        OpenMaya.MPoint( -1.0, -1.0, -1.0 ) )
    
    #-----------------------------------------------
    # creator
    @staticmethod
    def nodeCreator():
        return CustomLocator()
    
    #-----------------------------------------------
    # initializer
    @staticmethod
    def nodeInitializer():

        # アトリビュートの種類の定義
        nAttr = OpenMaya.MFnNumericAttribute()

        # 形状変更用のアトリビュート
        CustomLocator.input = nAttr.create('type', 'ty', OpenMaya.MFnNumericData.kInt, 0)
        nAttr.writable = True
        nAttr.readable = False
        nAttr.keyable = True

        # Rアトリビュート
        CustomLocator.red = nAttr.create('red', 'r', OpenMaya.MFnNumericData.kFloat, 0.5)
        nAttr.writable = True
        nAttr.readable = False
        nAttr.keyable = True

        # Gアトリビュート
        CustomLocator.green = nAttr.create('green', 'g', OpenMaya.MFnNumericData.kFloat, 0.5)
        nAttr.writable = True
        nAttr.readable = False
        nAttr.keyable = True

        # Bアトリビュート
        CustomLocator.bleu = nAttr.create('bleu', 'b', OpenMaya.MFnNumericData.kFloat, 0.5)
        nAttr.writable = True
        nAttr.readable = False
        nAttr.keyable = True

        # アトリビュートをセットする
        CustomLocator.addAttribute( CustomLocator.input )
        CustomLocator.addAttribute( CustomLocator.red )
        CustomLocator.addAttribute( CustomLocator.green )
        CustomLocator.addAttribute( CustomLocator.bleu )
        return True
        
        
#=========================================
class UserData( OpenMaya.MUserData ):

    #CustomLocatorに渡すデータ
    size = 0.0
    #-----------------------------------------------
    def __init__( self ):
        OpenMaya.MUserData.__init__( self, False )
        self.datas = []
        self.colorR = []
        self.colorG = []
        self.colorB = []
#=========================================
class CustomLocatorOverride( OpenMayaRender.MPxDrawOverride ):
    
    #-----------------------------------------------
    def __init__( self, obj ):
        OpenMayaRender.MPxDrawOverride.__init__( self, obj, CustomLocatorOverride.draw )
    
    #-----------------------------------------------
    @staticmethod
    def draw( context, data ):
        pass
    
    #-----------------------------------------------
    def supportedDrawAPIs( self ):

        #DirectXを使用して描画する
        #return OpenMayaRender.MRenderer.kDirectX11
        #OpenGLを使用して描画する
        return OpenMayaRender.MRenderer.kOpenGL
    #-----------------------------------------------
    def hasUIDrawables( self ):
        return True
    
    #-----------------------------------------------
    def isBounded( self, objPath, cameraPath ):
        return True
    
    #-----------------------------------------------
    def boundingBox( self, objPath, cameraPath ):
    
        boxsize = 10000.0
        bbox = OpenMaya.MBoundingBox(OpenMaya.MPoint(boxsize, boxsize, boxsize),
        OpenMaya.MPoint(-boxsize, -boxsize, -boxsize))
    
        return bbox
    #-----------------------------------------------
    def disableInternalBoundingBoxDraw( self ):
        return True
    
    #-----------------------------------------------
    def prepareForDraw( self, objPath, cameraPath, frameContext, oldData ):

        # データ更新処理
        if( objPath ):
            newData = None
            if( oldData ):
                newData = oldData
                newData.datas = []
                newData.colorR = []
                newData.colorG = []
                newData.colorB = []
            else:
                newData = UserData()
            
            # 自身のロケータの情報を読み込む
            thisNode = objPath.node()
            fnNode = OpenMaya.MFnDependencyNode( thisNode )

            # typeアトリビュートの情報を取得
            typePlug = fnNode.findPlug( 'type', False ).asInt()
            newData.datas.append(typePlug)
            
            #RGBの情報を取得
            colorPlugR = fnNode.findPlug( 'red', False ).asFloat()
            newData.colorR.append(colorPlugR)
            colorPlugG = fnNode.findPlug( 'green', False ).asFloat()
            newData.colorG.append(colorPlugG)
            colorPlugB = fnNode.findPlug( 'bleu', False ).asFloat()
            newData.colorB.append(colorPlugB)

            return newData

        return None
    
    #-----------------------------------------------
    def addUIDrawables( self, objPath, drawManager, frameContext, data ):

        # ベースメッシュのデータが空でなければ、描画処理を実行する
        if data.datas != []:
        
            type = data.datas[0]
            color_r = data.colorR[0]
            color_g = data.colorG[0]
            color_b = data.colorB[0]

            # ボックスの描画処理   
            drawManager.beginDrawable()
            color = OpenMaya.MColor([color_r,color_g,color_b])
            drawManager.setColor( color )
            #box
            if type == 0:
                drawManager.box(OpenMaya.MPoint(0.0,0.0,0.0,1),
                OpenMaya.MVector(0.0,1.0,0.0),
                OpenMaya.MVector(0.0,0.0,1.0),
                1.0,1.0,1.0,True) # ←表示されるボックスのサイズ

            #sphere
            if type == 1:
                drawManager.sphere(OpenMaya.MPoint(0.0,0.0,0.0,1),
                1.0,True) # ←表示されるボックスのサイズ

            #cone
            if type == 2:
                drawManager.cone(OpenMaya.MPoint(0.0,0.0,0.0,1),
                OpenMaya.MVector(0.0,1.0,0.0),
                1.0,1.0,True) # ←表示されるボックスのサイズ

            #circle
            if type == 3:
                drawManager.circle(OpenMaya.MPoint(0.0,0.0,0.0,1),
                OpenMaya.MVector(0.0,1.0,0.0),
                1.0,True) 

            #rect
            if type == 4:
                drawManager.rect(OpenMaya.MPoint(0.0,0.0,0.0,1),
                OpenMaya.MVector(0.0,1.0,0.0),
                OpenMaya.MVector(0.0,0.0,1.0),
                1.0,1.0,True) # ←表示されるボックスのサイズ

            drawManager.endDrawable()
        return True
    
    #-----------------------------------------------
    @staticmethod
    def creator( obj ):
        return CustomLocatorOverride( obj )
    
#-----------------------------------------------
# initialize
def initializePlugin( obj ):
    
    mplugin = OpenMaya.MFnPlugin( obj, "CustomLocator", "3.0", "Any" )
    try:
        mplugin.registerNode( CustomLocator.kPluginNodeTypeName, CustomLocator.NodeId, 
        CustomLocator.nodeCreator, CustomLocator.nodeInitializer, OpenMaya.MPxNode.kLocatorNode,
        CustomLocator.classfication )

        OpenMayaRender.MDrawRegistry.registerDrawOverrideCreator( CustomLocator.classfication,
        CustomLocator.registrantId,CustomLocatorOverride.creator )
    													  
    except:
        sys.stderr.write( "Failed to register node: %s" % CustomLocator.kPluginNodeTypeName )
        raise
    
#-----------------------------------------------
# uninitialize
def uninitializePlugin( obj ):
    
    mplugin = OpenMaya.MFnPlugin( obj, "CustomLocator", "3.0", "Any" )
    try:
        mplugin.deregisterNode( CustomLocator.NodeId )
        OpenMayaRender.MDrawRegistry.deregisterDrawOverrideCreator( CustomLocator.classfication,
        CustomLocator.registrantId )
    except:
        sys.stderr.write( "Failed to deregister node: %s" % CustomLocator.kPluginNodeTypeName )
        raise