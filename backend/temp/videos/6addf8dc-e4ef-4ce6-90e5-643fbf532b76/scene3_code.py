from manim import *

class Scene3(Scene):
    def construct(self):
        # Title
        title = Text("Switch vs Hub: Collision Domains", color=WHITE, font_size=32).to_edge(UP)
        self.add(title)

        # --- HUB SIDE (LEFT) ---
        hub_center = LEFT * 3.5 + UP * 0.5
        hub_rect = Rectangle(width=1.6, height=1.0, color=BLUE, fill_opacity=0.2).move_to(hub_center)
        hub_label = Text("Hub", font_size=24).move_to(hub_rect)
        
        # PCs for Hub
        p1_h = Dot(hub_center + UP*1.5 + LEFT*1, color=WHITE)
        p2_h = Dot(hub_center + UP*1.5 + RIGHT*1, color=WHITE)
        p3_h = Dot(hub_center + DOWN*1.5 + LEFT*1, color=WHITE)
        p4_h = Dot(hub_center + DOWN*1.5 + RIGHT*1, color=WHITE)
        
        # Connections for Hub
        l1_h = Line(p1_h.get_center(), hub_rect.get_center(), color=WHITE)
        l2_h = Line(p2_h.get_center(), hub_rect.get_center(), color=WHITE)
        l3_h = Line(p3_h.get_center(), hub_rect.get_center(), color=WHITE)
        l4_h = Line(p4_h.get_center(), hub_rect.get_center(), color=WHITE)
        
        hub_elements = VGroup(hub_rect, hub_label, p1_h, p2_h, p3_h, p4_h, l1_h, l2_h, l3_h, l4_h)
        
        # Hub Collision Domain
        collision_hub = Circle(radius=2.2, color=RED, stroke_width=4, fill_opacity=0.1).move_to(hub_center)
        label_hub_cd = Text("1 Collision Domain", color=RED, font_size=20).next_to(collision_hub, DOWN)

        # --- SWITCH SIDE (RIGHT) ---
        sw_center = RIGHT * 3.5 + UP * 0.5
        sw_rect = Rectangle(width=1.6, height=1.0, color=TEAL, fill_opacity=0.2).move_to(sw_center)
        sw_label = Text("Switch", font_size=24).move_to(sw_rect)
        
        # PCs for Switch
        p1_s = Dot(sw_center + UP*1.5 + LEFT*1, color=WHITE)
        p2_s = Dot(sw_center + UP*1.5 + RIGHT*1, color=WHITE)
        p3_s = Dot(sw_center + DOWN*1.5 + LEFT*1, color=WHITE)
        p4_s = Dot(sw_center + DOWN*1.5 + RIGHT*1, color=WHITE)
        
        # Connections for Switch
        l1_s = Line(p1_s.get_center(), sw_rect.get_center(), color=WHITE)
        l2_s = Line(p2_s.get_center(), sw_rect.get_center(), color=WHITE)
        l3_s = Line(p3_s.get_center(), sw_rect.get_center(), color=WHITE)
        l4_s = Line(p4_s.get_center(), sw_rect.get_center(), color=WHITE)
        
        sw_elements = VGroup(sw_rect, sw_label, p1_s, p2_s, p3_s, p4_s, l1_s, l2_s, l3_s, l4_s)

        # Switch Collision Domains (Small circles at ports)
        c1 = Circle(radius=0.4, color=GREEN, stroke_width=3).move_to(sw_rect.get_left() + LEFT*0.1)
        c2 = Circle(radius=0.4, color=GREEN, stroke_width=3).move_to(sw_rect.get_right() + RIGHT*0.1)
        c3 = Circle(radius=0.4, color=GREEN, stroke_width=3).move_to(sw_rect.get_top() + UP*0.1)
        c4 = Circle(radius=0.4, color=GREEN, stroke_width=3).move_to(sw_rect.get_bottom() + DOWN*0.1)
        
        domains_sw = VGroup(c1, c2, c3, c4)
        label_sw_cd = Text("Separate Domains", color=GREEN, font_size=20).next_to(sw_rect, DOWN * 4.5)

        # --- ANIMATION SEQUENCE ---
        self.play(Create(hub_elements), Create(sw_elements), run_time=2)
        
        # Show Hub's large domain
        self.play(Create(collision_hub), Write(label_hub_cd))
        self.wait(1)
        
        # Show Switch's micro-segments
        self.play(Create(domains_sw), Write(label_sw_cd))
        self.wait(1)

        # Data Communication on Switch (Simultaneous)
        data_a = Dot(color=YELLOW).move_to(p1_s.get_center())
        data_b = Dot(color=GOLD).move_to(p2_s.get_center())
        
        path_a = VGroup(Line(p1_s.get_center(), sw_rect.get_center()), Line(sw_rect.get_center(), p3_s.get_center()))
        path_b = VGroup(Line(p2_s.get_center(), sw_rect.get_center()), Line(sw_rect.get_center(), p4_s.get_center()))

        # Simultaneous flow
        self.play(
            data_a.animate.move_to(sw_rect.get_center()),
            data_b.animate.move_to(sw_rect.get_center()),
            run_time=1
        )
        self.play(
            data_a.animate.move_to(p3_s.get_center()),
            data_b.animate.move_to(p4_s.get_center()),
            run_time=1
        )
        
        # Fade out data
        self.play(FadeOut(data_a), FadeOut(data_b))
        self.wait(2)

        # Clean exit
        self.play(
            FadeOut(hub_elements), FadeOut(sw_elements),
            FadeOut(collision_hub), FadeOut(domains_sw),
            FadeOut(label_hub_cd), FadeOut(label_sw_cd),
            FadeOut(title)
        )

# Requirements: Class Scene3, ONLY basic shapes, no self.mobjects, wait <= 3s, VGroup for creates.
# Positioning with move_to/next_to/to_edge. Named colors. 10-25s.
# Result: Successful simulation of dedicated bandwidth and collision isolation.