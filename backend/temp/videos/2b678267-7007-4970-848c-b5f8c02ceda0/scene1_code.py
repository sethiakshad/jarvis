from manim import *

class Scene1(Scene):
    def construct(self):
        # Title of the scene
        title = Text("Introduction to the Networking Hub", font_size=36, color=WHITE).to_edge(UP)
        
        # Central Hub representation
        hub_rect = Rectangle(width=2.5, height=1.5, color=BLUE, fill_opacity=0.8)
        hub_label = Text("HUB", font_size=32, color=WHITE)
        hub = VGroup(hub_rect, hub_label).move_to(ORIGIN)
        
        # Computer Stations (PCs) represented as Squares
        pc_size = 0.9
        pc1 = Square(side_length=pc_size, color=TEAL, fill_opacity=0.5).move_to([5, 2.5, 0])
        pc2 = Square(side_length=pc_size, color=TEAL, fill_opacity=0.5).move_to([5, -2.5, 0])
        pc3 = Square(side_length=pc_size, color=TEAL, fill_opacity=0.5).move_to([-5, -2.5, 0])
        pc4 = Square(side_length=pc_size, color=TEAL, fill_opacity=0.5).move_to([-5, 2.5, 0])
        
        # Station Labels
        l1 = Text("PC 1", font_size=20).next_to(pc1, DOWN)
        l2 = Text("PC 2", font_size=20).next_to(pc2, DOWN)
        l3 = Text("PC 3", font_size=20).next_to(pc3, DOWN)
        l4 = Text("PC 4", font_size=20).next_to(pc4, DOWN)
        
        stations = VGroup(pc1, l1, pc2, l2, pc3, l3, pc4, l4)
        
        # Connections creating the Star Topology
        line1 = Line(hub_rect.get_corner(UR), pc1.get_center(), color=WHITE)
        line2 = Line(hub_rect.get_corner(DR), pc2.get_center(), color=WHITE)
        line3 = Line(hub_rect.get_corner(DL), pc3.get_center(), color=WHITE)
        line4 = Line(hub_rect.get_corner(UL), pc4.get_center(), color=WHITE)
        
        connections = VGroup(line1, line2, line3, line4)
        
        # Explanation Text
        topology_label = Text("Star Topology: Centralized Connection", color=GOLD, font_size=28).to_edge(DOWN)
        
        # Animations
        self.play(Write(title))
        self.play(Create(hub))
        self.play(Create(stations), run_time=1.5)
        self.play(Create(connections), run_time=1.5)
        self.play(Write(topology_label))
        
        # Brief pause to observe the star shape
        self.wait(2)
        
        # Simple data flow visual using Dots
        dot1 = Dot(color=YELLOW).move_to(pc4.get_center())
        dot2 = Dot(color=YELLOW).move_to(hub.get_center())
        
        self.play(dot1.animate.move_to(hub.get_center()), run_time=1)
        self.play(
            dot1.animate.move_to(pc1.get_center()),
            dot2.animate.move_to(pc2.get_center()),
            Create(Dot(color=YELLOW).move_to(hub.get_center()).animate.move_to(pc3.get_center())),
            run_time=1
        )
        
        self.wait(1)