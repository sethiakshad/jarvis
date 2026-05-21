from manim import *

class Scene2(Scene):
    def construct(self):
        # Title and Splitter
        title = Text("Collision Domains: Hub vs Switch", font_size=32).to_edge(UP)
        divider = Line(start=[0, 2.5, 0], end=[0, -3.5, 0], color=WHITE)
        hub_label = Text("HUB (Shared)", color=TEAL, font_size=24).move_to([-3.5, 2.5, 0])
        switch_label = Text("SWITCH (Dedicated)", color=BLUE, font_size=24).move_to([3.5, 2.5, 0])
        
        self.add(title, divider, hub_label, switch_label)

        # Hub Layout (Left)
        hub_center = Circle(radius=0.4, color=TEAL, fill_opacity=0.3).move_to([-3.5, 0, 0])
        hub_text = Text("Hub", font_size=20).move_to(hub_center.get_center())
        pc_h1 = Square(side_length=0.5, color=WHITE).move_to([-5.5, 1.5, 0])
        pc_h2 = Square(side_length=0.5, color=WHITE).move_to([-1.5, 0, 0])
        pc_h3 = Square(side_length=0.5, color=WHITE).move_to([-5.5, -1.5, 0])
        
        line_h1 = Line(pc_h1.get_center(), hub_center.get_center(), stroke_width=2)
        line_h2 = Line(pc_h2.get_center(), hub_center.get_center(), stroke_width=2)
        line_h3 = Line(pc_h3.get_center(), hub_center.get_center(), stroke_width=2)
        
        hub_group = VGroup(hub_center, hub_text, pc_h1, pc_h2, pc_h3, line_h1, line_h2, line_h3)
        self.play(Create(hub_group))

        # Switch Layout (Right)
        switch_center = Rectangle(width=1.2, height=0.8, color=BLUE, fill_opacity=0.3).move_to([3.5, 0, 0])
        switch_text = Text("Switch", font_size=20).move_to(switch_center.get_center())
        pc_s1 = Square(side_length=0.5, color=WHITE).move_to([1.5, 1.5, 0])
        pc_s2 = Square(side_length=0.5, color=WHITE).move_to([5.5, 1.5, 0])
        pc_s3 = Square(side_length=0.5, color=WHITE).move_to([1.5, -1.5, 0])
        pc_s4 = Square(side_length=0.5, color=WHITE).move_to([5.5, -1.5, 0])
        
        line_s1 = Line(pc_s1.get_center(), switch_center.get_center(), stroke_width=2)
        line_s2 = Line(pc_s2.get_center(), switch_center.get_center(), stroke_width=2)
        line_s3 = Line(pc_s3.get_center(), switch_center.get_center(), stroke_width=2)
        line_s4 = Line(pc_s4.get_center(), switch_center.get_center(), stroke_width=2)
        
        switch_group = VGroup(switch_center, switch_text, pc_s1, pc_s2, pc_s3, pc_s4, line_s1, line_s2, line_s3, line_s4)
        self.play(Create(switch_group))

        # Hub Animation: Broadcast Collision logic
        hub_dot = Dot(color=YELLOW).move_to(pc_h1.get_center())
        self.play(hub_dot.animate.move_to(hub_center.get_center()), run_time=1)
        
        # Split dots to all other ports
        hub_dot2 = Dot(color=RED).move_to(hub_center.get_center())
        hub_dot3 = Dot(color=RED).move_to(hub_center.get_center())
        
        self.play(
            hub_dot2.animate.move_to(pc_h2.get_center()),
            hub_dot3.animate.move_to(pc_h3.get_center()),
            line_h1.animate.set_color(RED),
            line_h2.animate.set_color(RED),
            line_h3.animate.set_color(RED),
            run_time=1.5
        )
        self.play(FadeOut(hub_dot, hub_dot2, hub_dot3), 
                  line_h1.animate.set_color(WHITE), 
                  line_h2.animate.set_color(WHITE), 
                  line_h3.animate.set_color(WHITE))

        # Switch Animation: Parallel Dedicated Paths
        s_dot_a1 = Dot(color=YELLOW).move_to(pc_s1.get_center())
        s_dot_b1 = Dot(color=GOLD).move_to(pc_s3.get_center())
        
        # Move to switch simultaneously
        self.play(
            s_dot_a1.animate.move_to(switch_center.get_center()),
            s_dot_b1.animate.move_to(switch_center.get_center()),
            line_s1.animate.set_color(YELLOW),
            line_s3.animate.set_color(GOLD),
            run_time=1
        )
        
        # Move to dedicated destinations simultaneously without collision
        self.play(
            s_dot_a1.animate.move_to(pc_s2.get_center()),
            s_dot_b1.animate.move_to(pc_s4.get_center()),
            line_s2.animate.set_color(YELLOW),
            line_s4.animate.set_color(GOLD),
            run_time=1.5
        )
        
        # Final Text Summary
        explanation = Text("Separate Collision Domains", color=YELLOW, font_size=24).to_edge(DOWN)
        self.play(Write(explanation))
        self.wait(2)
        
        # Cleanup
        self.play(
            FadeOut(hub_group),
            FadeOut(switch_group),
            FadeOut(explanation),
            FadeOut(title),
            FadeOut(divider),
            FadeOut(hub_label),
            FadeOut(switch_label),
            FadeOut(s_dot_a1),
            FadeOut(s_dot_b1)
        )