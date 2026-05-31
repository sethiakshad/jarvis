from manim import *

class Scene2(Scene):
    def construct(self):
        # 1. Background Infrastructure
        title = Text("Broadcasting Data Packets", color=GOLD).to_edge(UP)
        
        # Hub setup
        hub = Square(color=BLUE, fill_opacity=0.8).scale(0.6).move_to(ORIGIN)
        hub_label = Text("HUB", color=WHITE).scale(0.4).move_to(hub.get_center())
        
        # Computer positions (1 Source + 4 Receivers)
        pos_src = LEFT * 4
        pos_r1 = [3, 2.5, 0]
        pos_r2 = [4.5, 0, 0]
        pos_r3 = [3, -2.5, 0]
        pos_r4 = [-1.5, 2.5, 0]
        
        # Create Nodes (Computers)
        src_node = Square(color=WHITE, fill_opacity=0.2).scale(0.5).move_to(pos_src)
        r1 = Square(color=WHITE, fill_opacity=0.2).scale(0.5).move_to(pos_r1)
        r2 = Square(color=WHITE, fill_opacity=0.2).scale(0.5).move_to(pos_r2)
        r3 = Square(color=WHITE, fill_opacity=0.2).scale(0.5).move_to(pos_r3)
        r4 = Square(color=WHITE, fill_opacity=0.2).scale(0.5).move_to(pos_r4)
        
        # Connections
        l_src = Line(pos_src, ORIGIN, color=WHITE)
        l1 = Line(ORIGIN, pos_r1, color=WHITE)
        l2 = Line(ORIGIN, pos_r2, color=WHITE)
        l3 = Line(ORIGIN, pos_r3, color=WHITE)
        l4 = Line(ORIGIN, pos_r4, color=WHITE)
        
        # Text Labels
        src_text = Text("Source", color=WHITE).scale(0.3).next_to(src_node, DOWN)
        
        # Grouping for clean management
        nodes = VGroup(src_node, r1, r2, r3, r4, hub)
        lines = VGroup(l_src, l1, l2, l3, l4)
        labels = VGroup(hub_label, src_text, title)
        
        self.add(lines, nodes, labels)
        
        # 2. Data Movement Animation
        # Primary packet coming from Source
        packet = Rectangle(width=0.4, height=0.2, color=YELLOW, fill_opacity=1).move_to(pos_src)
        
        self.play(Create(packet))
        self.play(packet.animate.move_to(ORIGIN), run_time=1.5)
        
        # 3. Broadcasting Step
        # Create 4 clones for the 4 ports
        p1 = packet.copy()
        p2 = packet.copy()
        p3 = packet.copy()
        p4 = packet.copy()
        
        # Hide original as it's "processed"
        self.remove(packet)
        
        # Simultaneous broadcast animation
        self.play(
            p1.animate.move_to(pos_r1),
            p2.animate.move_to(pos_r2),
            p3.animate.move_to(pos_r3),
            p4.animate.move_to(pos_r4),
            run_time=2
        )
        
        # 4. Educational Context
        explanation = Text("Hubs lack intelligence: Broadcasting to all ports.", color=TEAL).scale(0.5).to_edge(DOWN)
        self.play(Write(explanation))
        
        self.wait(2)
        
        # Clean exit sequence (keeping within 25s limit)
        broadcast_group = VGroup(p1, p2, p3, p4)
        self.play(FadeOut(broadcast_group), FadeOut(explanation))
        self.wait(1)