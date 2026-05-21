from manim import *

class Scene3(Scene):
    def construct(self):
        # 1. Setup Hub Section (Top)
        hub_title = Text("Hub: Single Collision Domain", color=RED, font_size=28).to_edge(UP, buff=0.3)
        hub_box = Rectangle(color=WHITE, width=2.5, height=1.2, fill_opacity=0.1).move_to(UP * 1.8)
        hub_text = Text("HUB", font_size=20).move_to(hub_box.get_center())
        
        p1 = Dot(hub_box.get_left() + LEFT * 1.5, color=WHITE)
        p2 = Dot(hub_box.get_right() + RIGHT * 1.5, color=WHITE)
        l1 = Line(p1.get_center(), hub_box.get_left(), color=WHITE)
        l2 = Line(p2.get_center(), hub_box.get_right(), color=WHITE)
        
        hub_ui = VGroup(hub_title, hub_box, hub_text, p1, p2, l1, l2)
        
        # 2. Setup Switch Section (Bottom)
        divider = Line(LEFT * 7, RIGHT * 7, color=GREY).move_to(UP * 0.4)
        
        switch_title = Text("Switch: Dedicated Collision Domains", color=GREEN, font_size=28).move_to(DOWN * 0.1)
        switch_box = Rectangle(color=WHITE, width=2.5, height=1.2, fill_opacity=0.1).move_to(DOWN * 2)
        switch_text = Text("SWITCH", font_size=20).move_to(switch_box.get_center())
        
        # Ports for Switch
        s1 = Dot(switch_box.get_left() + LEFT * 1.5 + UP * 0.3, color=BLUE)
        s2 = Dot(switch_box.get_right() + RIGHT * 1.5 + UP * 0.3, color=BLUE)
        s3 = Dot(switch_box.get_left() + LEFT * 1.5 + DOWN * 0.3, color=GOLD)
        s4 = Dot(switch_box.get_right() + RIGHT * 1.5 + DOWN * 0.3, color=GOLD)
        
        switch_ui = VGroup(divider, switch_title, switch_box, switch_text, s1, s2, s3, s4)

        self.play(Create(hub_ui), Create(switch_ui))
        self.wait(1)

        # 3. Hub Collision Animation
        sig_h1 = Dot(p1.get_center(), color=YELLOW)
        sig_h2 = Dot(p2.get_center(), color=YELLOW)
        
        collision_mark = Circle(radius=0.5, color=RED, fill_opacity=0.6).move_to(hub_box.get_center())
        collision_text = Text("COLLISION!", color=RED, font_size=22).next_to(hub_box, UP, buff=0.1)

        self.play(
            sig_h1.animate.move_to(hub_box.get_center()),
            sig_h2.animate.move_to(hub_box.get_center()),
            run_time=1.5
        )
        self.play(
            Create(collision_mark),
            Write(collision_text),
            sig_h1.animate.scale(0),
            sig_h2.animate.scale(0),
            run_time=0.5
        )
        self.play(FadeOut(collision_mark), run_time=0.5)

        # 4. Switch Dedicated Paths Animation
        # Path lines inside the switch
        path_a = Line(s1.get_center(), s2.get_center(), color=BLUE, stroke_width=2)
        path_b = Line(s3.get_center(), s4.get_center(), color=GOLD, stroke_width=2)
        
        sig_s1 = Dot(s1.get_center(), color=WHITE)
        sig_s2 = Dot(s3.get_center(), color=WHITE)
        
        dedicated_text = Text("Parallel Transfers", color=GREEN, font_size=22).next_to(switch_box, DOWN, buff=0.2)

        self.play(
            Create(path_a),
            Create(path_b),
            Write(dedicated_text),
            run_time=1
        )
        
        self.play(
            sig_s1.animate.move_to(s2.get_center()),
            sig_s2.animate.move_to(s4.get_center()),
            run_time=2,
            rate_func=linear
        )
        
        # 5. Conclusion
        summary = Text("No interference", color=WHITE, font_size=20).next_to(dedicated_text, DOWN, buff=0.1)
        self.play(Write(summary))
        self.wait(2)