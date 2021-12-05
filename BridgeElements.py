import numpy as np
from stl import mesh

class Bridge:
    def __init__(self,length,thickness,deck_thickness,stay_number,cable_thickness):
        self.height = length*0.7
        self.width = length/2
        self.thickness = thickness
        self.deck_thickness = deck_thickness
        self.stay_number = stay_number
        self.cable_thickness = cable_thickness
        self.deck_height = self.height*0.4

    def tower(self):
        """creates one tower"""
        h=self.height
        tt=self.thickness
        tb=self.deck_thickness*0.7
        bt=self.thickness
        bb=tb
        #defining the corners of the tower
        vertices=np.array([\
            [-bb/2,0,0],    #0 bottom of tower
            [-bb/2,0,tb],    #1
            [bb/2,0,0],     #2 bottom of tower
            [bb/2,0,tb],     #3
            [-bt/2,h,0],    #4 top of tower
            [-bt/2,h,tt],    #5
            [bt/2,h,0],     #8 top of tower
            [bt/2,h,tt]      #9
        ])
        #defining how those points are connected by surfaces
        #going bottom up
        faces=np.array([\
            #floor
            [0,1,2],
            [2,1,3],
            #tower sides
            [0,1,4],
            [4,1,5],

            [2,0,4],
            [2,4,6],

            [3,2,7],
            [7,2,6],

            [1,3,5],
            [5,3,7],
            #top
            [4,5,6],
            [6,5,7]])
        # Create the mesh
        volume = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
        for i, f in enumerate(faces):
            for j in range(3):
                volume.vectors[i][j] = vertices[f[j],:]
        return volume

    def deck(self):
        h=self.height*0.4
        hb=h-self.height*0.015
        t=self.deck_thickness
        l=self.width
        #defining the corners of the deck
        vertices=np.array([
            [-l,h,0],       #0 
            [-l,h,t],       #1
            [-l,hb,0],      #2 
            [-l,hb,t],      #3
            [l,h,0],        #4 
            [l,h,t],        #5
            [l,hb,0],       #6 
            [l,hb,t]        #7
        ])
        #defining how those points are connected by surfaces
        #going bottom up
        faces=np.array([
            #end
            [0,1,2],
            [2,1,3],
            #deck sides
            [0,1,4],
            [4,1,5],

            [2,0,4],
            [2,4,6],

            [3,2,7],
            [7,2,6],

            [1,3,5],
            [5,3,7],
            #other end
            [4,5,6],
            [6,5,7]
        ])
        # Create the mesh
        volume = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
        for i, f in enumerate(faces):
            for j in range(3):
                volume.vectors[i][j] = vertices[f[j],:]

        return volume


    def one_cable(self,top,bottom,span,direction):
        """create one cable"""
        ht=top          # height at the top of the cable
        hb=bottom       # height at the bottom of the cable = top of deck
        b=span          # width that the cable spans across (center of tower/ edge of cable)
        t=self.thickness # thickness of print
        tc=self.cable_thickness*1.6 # width of cable*tan(45)
        d=direction     #1 / -1 for whether right or left
        #defining the corners of the tower
        vertices=np.array([
            [d*b,hb,0],       
            [d*b,hb,t],       
            [d*b-d*tc,hb,0],       
            [d*b-d*tc,hb,t],     
            [0,ht,0],        
            [0,ht,t],        
            [0,ht-tc,0],        
            [0,ht-tc,t]         
        ])
        #defining how those points are connected by surfaces
        #going bottom up
        faces=np.array([
            #end
            [0,1,2],
            [2,1,3],
            #deck sides
            [0,1,4],
            [4,1,5],

            [2,0,4],
            [2,4,6],

            [3,2,7],
            [7,2,6],

            [1,3,5],
            [5,3,7],
            #other end
            [4,5,6],
            [6,5,7]
        ])
        # Create the mesh
        volume = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
        for i, f in enumerate(faces):
            for j in range(3):
                volume.vectors[i][j] = vertices[f[j],:]
        return volume

    def cables(self):
        """create all the cables with the previous one_cable function"""
        n=self.stay_number
        h=self.height
        dh=self.deck_height
        #find the distance between attachment points
        #top cable
        span1=h*0.6
        #steps
        delta_h=span1/n
        delta_span=span1/n

        #cables=[]
        
        #top cables
        top=h
        span=span1
        #create the right cable
        right_cable=self.one_cable(top,dh,span1,1)
        #create the left cable
        left_cable=self.one_cable(top,dh,span1,-1)
        
        cables=mesh.Mesh(np.concatenate([right_cable.data.copy(),left_cable.data.copy(),]))
        
        if n > 1:
            for i in range(1, n):
                top=h-i*delta_h
                span=span1-i*delta_span
                #create the right cable
                right_cable=self.one_cable(top,dh,span,1)
                #create the left cable
                left_cable=self.one_cable(top,dh,span,-1)
                
                cables=mesh.Mesh(np.concatenate([cables.data.copy(),right_cable.data.copy(),left_cable.data.copy(),]))
        
            
        #meshes=[mesh.Mesh(i.data.copy() for i in cables)]
        
        #all_cables=mesh.Mesh(np.concatenate(meshes))

        return cables

    def nissehue(self):
        #reusing the points form the deck and the cable function
        #use deck and cable functions from the bridge class 
        #to create a little triangle to attach the ornament to the christmas tree
        h=self.height
        hb=h-self.cable_thickness
        t=self.thickness
        l=(self.width*2-self.height)/2
        if l>1:
            l=1
        #defining the corners of the bottom triangle line
        vertices=np.array([
            [-l,h,0],       #0 
            [-l,h,t],       #1
            [-l,hb,0],      #2 
            [-l,hb,t],      #3
            [l,h,0],        #4 
            [l,h,t],        #5
            [l,hb,0],       #6 
            [l,hb,t]        #7
        ])
        #defining how those points are connected by surfaces
        #going bottom up
        faces=np.array([
            #end
            [0,1,2],
            [2,1,3],
            #sides
            [0,1,4],
            [4,1,5],

            [2,0,4],
            [2,4,6],

            [3,2,7],
            [7,2,6],

            [1,3,5],
            [5,3,7],
            #other end
            [4,5,6],
            [6,5,7]
        ])
        # Create the mesh
        bottom = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
        for i, f in enumerate(faces):
            for j in range(3):
                bottom.vectors[i][j] = vertices[f[j],:]
        
        # creating the inclined sides
        right=self.one_cable(h+l, h, l,1)
        left=self.one_cable(h+l, h, l,-1)

        Nissehue=mesh.Mesh(np.concatenate([bottom.data.copy(), right.data.copy(), left.data.copy(),]))
        return Nissehue
        


            
            





