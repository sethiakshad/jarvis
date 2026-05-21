from manim import *

class Scene2(Scene):
    def construct(self):
        # Titles and Partition
        title = Text("Switch vs. Hub: Traffic Efficiency", font_size=36, color=WHITE).to_edge(UP)
        divider = Line(UP * 2.5, DOWN * 3, color=GRAY)
        
        hub_label = Text("Hub (Shared)", font_size=28, color=RED).shift(LEFT * 3.5 + UP * 2.5)
        switch_label = Text("Switch (Dedicated)", font_size=28, color=BLUE).shift(RIGHT * 3.5 + UP * 2.5)

        # Hub Construction (Left)
        hub_rect = Rectangle(height=1, width=1.5, color=RED, fill_opacity=0.2).shift(LEFT * 3.5)
        hub_text = Text("HUB", font_size=20, color=RED).move_to(hub_rect.get_center())
        
        p1_h = Dot(LEFT * 5 + UP * 0, color=WHITE)
        p2_h = Dot(LEFT * 3.5 + UP * 1.5, color=WHITE)
        p3_h = Dot(LEFT * 2 + UP * 0, color=WHITE)
        p4_h = Dot(LEFT * 3.5 + DOWN * 1.5, color=WHITE)
        
        l1_h = Line(p1_h.get_center(), hub_rect.get_left())
        l2_h = Line(p2_h.get_center(), hub_rect.get_top())
        l3_h = Line(p3_h.get_center(), hub_rect.get_right())
        l4_h = Line(p4_h.get_center(), hub_rect.get_bottom())
        
        hub_group = VGroup(hub_rect, hub_text, p1_h, p2_h, p3_h, p4_h, l1_h, l2_h, l3_h, l4_h)

        # Switch Construction (Right)
        switch_rect = Rectangle(height=1, width=1.5, color=BLUE, fill_opacity=0.2).shift(RIGHT * 3.5)
        switch_text = Text("SWITCH", font_size=20, color=BLUE).move_to(switch_rect.get_center())
        
        p1_s = Dot(RIGHT * 2 + UP * 0, color=WHITE)
        p2_s = Dot(RIGHT * 3.5 + UP * 1.5, color=WHITE)
        p3_s = Dot(RIGHT * 5 + UP * 0, color=WHITE)
        p4_s = Dot(RIGHT * 3.5 + DOWN * 1.5, color=WHITE)
        
        l1_s = Line(p1_s.get_center(), switch_rect.get_left())
        l2_s = Line(p2_s.get_center(), switch_rect.get_top())
        l3_s = Line(p3_s.get_center(), switch_rect.get_right())
        l4_s = Line(p4_s.get_center(), switch_rect.get_bottom())
        
        switch_group = VGroup(switch_rect, switch_text, p1_s, p2_s, p3_s, p4_s, l1_s, l2_s, l3_s, l4_s)

        # Collision Labels
        hub_collision = Text("Collision Domain: ALL", font_size=18, color=RED).next_to(hub_group, DOWN)
        switch_collision = Text("Separate Domains", font_size=18, color=BLUE).next_to(switch_group, DOWN)

        # Animations
        self.play(Write(title))
        self.play(Create(divider))
        self.play(Create(hub_group), Create(switch_group), Write(hub_label), Write(switch_label))
        self.wait(1)

        # Hub Pulse Animation (Broadcasts to all)
        pulse_h = Circle(radius=0.1, color=RED, fill_opacity=1).move_to(p1_h.get_center())
        self.play(pulse_h.animate.move_to(hub_rect.get_center()), run_time=1)
        
        pulse_h2 = pulse_h.copy()
        pulse_h3 = pulse_h.copy()
        
        self.play(
            pulse_h.animate.move_to(p2_h.get_center()),
            pulse_h2.animate.move_to(p3_h.get_center()),
            pulse_h3.animate.move_to(p4_h.get_center()),
            run_time=1.5
        )
        self.play(FadeOut(pulse_h, pulse_h2, pulse_h3), Write(hub_collision))

        # Switch Pulse Animation (Direct connection)
        pulse_s = Circle(radius=0.1, color=TEAL, fill_opacity=1).move_to(p1_s.get_center())
        bandwidth_label = Text("Dedicated Bandwidth", font_size=18, color=YELLOW).next_to(l3_s, UP, buff=0.1)
        
        self.play(pulse_s.animate.move_to(switch_rect.get_center()), run_time=1)
        self.play(
            pulse_s.animate.move_to(p3_s.get_center()),
            Write(bandwidth_label),
            run_time=1.5
        )
        self.play(FadeOut(pulse_s), Write(switch_collision))
        
        self.wait(2)
        
        # Closing Comparison Text
        summary = Text("Switch = Efficiency & Security", font_size=24, color=GREEN).to_edge(DOWN)
        self.play(Write(summary))
        self.wait(2)
[Scene2]