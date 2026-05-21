from manim import *

class Scene1(Scene):
    def construct(self):
        # 1. Title and Explanation Labels
        title = Text("Hub: Central Connector", color=GOLD).scale(0.8)
        title.to_edge(UP, buff=0.5)

        # 2. Central Hub Representation
        hub_rect = Rectangle(width=4.0, height=1.8, color=TEAL, fill_opacity=0.3)
        hub_label = Text("HUB", color=WHITE).scale(0.7)
        repeater_label = Text("Multi-port Repeater", color=YELLOW).scale(0.4)
        repeater_label.next_to(hub_label, DOWN, buff=0.2)
        
        hub_group = VGroup(hub_rect, hub_label, repeater_label).move_to(DOWN * 0.5)

        # 3. Stations (Nodes) in Star Topology
        # Positions for a star shape
        pos_up = hub_group.get_center() + UP * 2.5
        pos_down = hub_group.get_center() + DOWN * 2.5
        pos_right = hub_group.get_center() + RIGHT * 5.0
        pos_left = hub_group.get_center() + LEFT * 5.0

        # Create PC station circles and labels
        s1_circ = Circle(radius=0.5, color=BLUE, fill_opacity=0.6).move_to(pos_up)
        s1_txt = Text("PC 1", color=WHITE).scale(0.4).move_to(pos_up)
        st1 = VGroup(s1_circ, s1_txt)

        s2_circ = Circle(radius=0.5, color=BLUE, fill_opacity=0.6).move_to(pos_down)
        s2_txt = Text("PC 2", color=WHITE).scale(0.4).move_to(pos_down)
        st2 = VGroup(s2_circ, s2_txt)

        s3_circ = Circle(radius=0.5, color=BLUE, fill_opacity=0.6).move_to(pos_right)
        s3_txt = Text("PC 3", color=WHITE).scale(0.4).move_to(pos_right)
        st3 = VGroup(s3_circ, s3_txt)

        s4_circ = Circle(radius=0.5, color=BLUE, fill_opacity=0.6).move_to(pos_left)
        s4_txt = Text("PC 4", color=WHITE).scale(0.4).move_to(pos_left)
        st4 = VGroup(s4_circ, s4_txt)

        stations = VGroup(st1, st2, st3, st4)

        # 4. Connection Lines (Star Layout)
        l1 = Line(hub_rect.get_top(), s1_circ.get_bottom(), color=WHITE)
        l2 = Line(hub_rect.get_bottom(), s2_circ.get_top(), color=WHITE)
        l3 = Line(hub_rect.get_right(), s3_circ.get_left(), color=WHITE)
        l4 = Line(hub_rect.get_left(), s4_circ.get_right(), color=WHITE)
        
        connections = VGroup(l1, l2, l3, l4)

        # 5. Final Descriptive Text
        topology_text = Text("Physical Star Topology", color=GREEN).scale(0.6)
        topology_text.to_edge(DOWN, buff=0.4)

        # Animation Sequence
        self.play(Write(title))
        self.play(Create(hub_rect), Write(hub_label))
        self.wait(0.5)
        self.play(Write(repeater_label))
        self.wait(1)

        # Draw topology
        self.play(Create(connections))
        self.play(Create(stations))
        self.wait(0.5)
        
        self.play(Write(topology_text))
        
        # Highlight functionality with a quick color pulse on the hub
        self.play(hub_rect.animate.set_fill(color=TEAL, fill_opacity=0.6), run_time=1)
        self.play(hub_rect.animate.set_fill(color=TEAL, fill_opacity=0.3), run_time=1)
        
        self.wait(2.5)