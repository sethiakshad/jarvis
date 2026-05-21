from manim import *

class Scene3(Scene):
    def construct(self):
        # Title
        title = Text("Collision Domain & Shared Bandwidth", color=GOLD).scale(0.8)
        title.to_edge(UP, buff=0.5)
        self.add(title)

        # Network Components
        hub_box = Square(color=GOLD, fill_opacity=0.1).scale(0.7)
        hub_label = Text("HUB", color=GOLD).scale(0.5).move_to(hub_box.get_center())
        hub = VGroup(hub_box, hub_label).move_to(ORIGIN)

        pc1_box = Rectangle(width=1.2, height=0.8, color=BLUE, fill_opacity=0.2)
        pc1_label = Text("PC A", color=BLUE).scale(0.4).move_to(pc1_box.get_center())
        pc1 = VGroup(pc1_box, pc1_label).next_to(hub, LEFT, buff=2.5)

        pc2_box = Rectangle(width=1.2, height=0.8, color=BLUE, fill_opacity=0.2)
        pc2_label = Text("PC B", color=BLUE).scale(0.4).move_to(pc2_box.get_center())
        pc2 = VGroup(pc2_box, pc2_label).next_to(hub, RIGHT, buff=2.5)

        link1 = Line(pc1.get_right(), hub.get_left(), color=WHITE)
        link2 = Line(pc2.get_left(), hub.get_right(), color=WHITE)

        self.play(Create(hub), Create(pc1), Create(pc2), Create(link1), Create(link2))

        # Data Packets (Envelopes)
        env1 = Rectangle(width=0.4, height=0.3, color=TEAL, fill_opacity=1).move_to(pc1.get_center())
        env2 = Rectangle(width=0.4, height=0.3, color=TEAL, fill_opacity=1).move_to(pc2.get_center())

        # Collision Action
        self.play(
            env1.animate.move_to(hub.get_center()),
            env2.animate.move_to(hub.get_center()),
            run_time=2
        )

        # Collision Visual (Red X)
        line_x1 = Line(hub.get_center() + UL*0.4, hub.get_center() + DR*0.4, color=RED, stroke_width=6)
        line_x2 = Line(hub.get_center() + UR*0.4, hub.get_center() + DL*0.4, color=RED, stroke_width=6)
        collision_x = VGroup(line_x1, line_x2)
        
        self.remove(env1, env2)
        self.play(Create(collision_x))
        
        collision_text = Text("COLLISION!", color=RED).scale(0.5).next_to(hub, UP, buff=0.2)
        self.play(Write(collision_text))
        self.wait(1)

        # Shared Bandwidth Visualization
        bw_label = Text("Shared Bandwidth Capacity", color=WHITE).scale(0.5)
        bw_label.to_edge(DOWN, buff=1.2)
        
        bw_bar_outline = Rectangle(width=6, height=0.4, color=WHITE)
        bw_bar_outline.next_to(bw_label, DOWN, buff=0.2)
        
        bw_fill = Rectangle(width=5.9, height=0.3, color=YELLOW, fill_opacity=0.8)
        bw_fill.move_to(bw_bar_outline.get_center())

        self.play(Write(bw_label), Create(bw_bar_outline))
        self.play(Create(bw_fill), run_time=2)
        
        bandwidth_note = Text("One stream at a time", color=YELLOW).scale(0.4)
        bandwidth_note.next_to(bw_bar_outline, DOWN, buff=0.2)
        self.play(Write(bandwidth_note))

        self.wait(2)