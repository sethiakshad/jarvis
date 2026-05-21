from manim import *

class Scene2(Scene):
    def construct(self):
        # Title of the scene
        title = Text("Dedicated Bandwidth & Collision Domains", font_size=32, color=GOLD).to_edge(UP)
        
        # Switch body representation
        switch_rect = Rectangle(width=7, height=4, color=WHITE, fill_opacity=0.05)
        switch_name = Text("Network Switch", font_size=24).next_to(switch_rect, UP, buff=0.1)
        
        # Defining individual ports as squares
        p1 = Square(side_length=0.6, color=WHITE).move_to(switch_rect.get_left() + RIGHT * 0.8 + UP * 1)
        p2 = Square(side_length=0.6, color=WHITE).move_to(switch_rect.get_right() + LEFT * 0.8 + UP * 1)
        p3 = Square(side_length=0.6, color=WHITE).move_to(switch_rect.get_left() + RIGHT * 0.8 + DOWN * 1)
        p4 = Square(side_length=0.6, color=WHITE).move_to(switch_rect.get_right() + LEFT * 0.8 + DOWN * 1)
        
        # Port labels
        p1_l = Text("P1", font_size=16).next_to(p1, LEFT, buff=0.1)
        p2_l = Text("P2", font_size=16).next_to(p2, RIGHT, buff=0.1)
        p3_l = Text("P3", font_size=16).next_to(p3, LEFT, buff=0.1)
        p4_l = Text("P4", font_size=16).next_to(p4, RIGHT, buff=0.1)
        
        # Grouping ports and labels
        ports = VGroup(p1, p2, p3, p4, p1_l, p2_l, p3_l, p4_l)
        
        # Dedicated communication lines (paths)
        path1 = Line(p1.get_center(), p2.get_center(), color=BLUE)
        path2 = Line(p3.get_center(), p4.get_center(), color=TEAL)
        
        # Packets (Two per stream to show a "pair" of data units)
        pkt1a = Circle(radius=0.12, color=BLUE, fill_opacity=1).move_to(p1.get_center())
        pkt1b = Circle(radius=0.12, color=BLUE, fill_opacity=1).move_to(p1.get_center())
        pkt2a = Circle(radius=0.12, color=TEAL, fill_opacity=1).move_to(p3.get_center())
        pkt2b = Circle(radius=0.12, color=TEAL, fill_opacity=1).move_to(p3.get_center())
        
        # Middle explanation text
        mid_text = Text("Simultaneous parallel traffic", font_size=22, color=WHITE).move_to(switch_rect.get_center())
        
        # Animation sequence
        self.play(Write(title))
        self.play(Create(switch_rect), Write(switch_name))
        self.play(Create(ports))
        self.wait(1)
        
        # Show paths and descriptive text
        self.play(Create(path1), Create(path2), Write(mid_text))
        
        # Animate simultaneous packet movement - Wave 1
        self.play(
            pkt1a.animate.move_to(p2.get_center()),
            pkt2a.animate.move_to(p4.get_center()),
            run_time=1.5,
            rate_func=linear
        )
        
        # Animate simultaneous packet movement - Wave 2
        self.play(
            pkt1b.animate.move_to(p2.get_center()),
            pkt2b.animate.move_to(p4.get_center()),
            run_time=1.5,
            rate_func=linear
        )
        
        # Collision Domain explanation at the bottom
        cd_info = Text("Each port functions as its own collision domain.", font_size=24, color=YELLOW).to_edge(DOWN)
        self.play(Write(cd_info))
        
        # Hold for a final look
        self.wait(2)