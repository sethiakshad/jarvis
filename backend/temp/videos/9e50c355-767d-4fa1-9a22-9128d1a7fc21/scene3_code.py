from manim import *

class Scene3(Scene):
    def construct(self):
        # 1. Setup Hub and Nodes
        hub_rect = Rectangle(height=1.2, width=2.2, color=BLUE, fill_opacity=0.4)
        hub_label = Text("HUB", font_size=24, color=WHITE).move_to(hub_rect.get_center())
        hub = VGroup(hub_rect, hub_label)

        # Nodes (labeled A, B, C)
        c1 = Circle(radius=0.4, color=WHITE, fill_opacity=0.2).shift(LEFT * 4 + UP * 1.5)
        c2 = Circle(radius=0.4, color=WHITE, fill_opacity=0.2).shift(LEFT * 4 + DOWN * 1.5)
        c3 = Circle(radius=0.4, color=WHITE, fill_opacity=0.2).shift(RIGHT * 4)
        
        t1 = Text("A", font_size=20).move_to(c1.get_center())
        t2 = Text("B", font_size=20).move_to(c2.get_center())
        t3 = Text("C", font_size=20).move_to(c3.get_center())
        
        nodes = VGroup(c1, c2, c3, t1, t2, t3)
        
        # Connections
        l1 = Line(c1.get_right(), hub_rect.get_left(), color=GRAY)
        l2 = Line(c2.get_right(), hub_rect.get_left(), color=GRAY)
        l3 = Line(c3.get_left(), hub_rect.get_right(), color=GRAY)
        connections = VGroup(l1, l2, l3)

        # 2. Bandwidth visualization
        bw_bar = Rectangle(width=6, height=0.5, color=TEAL, fill_opacity=0.3).to_edge(UP, buff=0.5)
        bw_text = Text("Shared Bandwidth Pipe", font_size=22, color=TEAL).next_to(bw_bar, DOWN, buff=0.1)
        bw_group = VGroup(bw_bar, bw_text)

        # Initial Appearance
        self.play(Create(hub), Create(nodes), Create(connections))
        self.play(FadeIn(bw_group))
        self.wait(1)

        # 3. Data Collision Sequence
        # Two signals (dots) moving toward the hub simultaneously
        signal1 = Dot(c1.get_center(), color=RED)
        signal2 = Dot(c2.get_center(), color=RED)
        
        self.play(
            signal1.animate.move_to(hub_rect.get_center()),
            signal2.animate.move_to(hub_rect.get_center()),
            run_time=2,
            rate_func=linear
        )

        # 4. Collision Effect (Starburst and Text)
        collision_mark = Text("COLLISION", color=YELLOW, weight=BOLD).scale(0.8).move_to(hub_rect.get_center())
        
        # Simple starburst using lines
        line_a = Line(ORIGIN, UP*0.6 + RIGHT*0.6, color=RED).move_to(hub_rect.get_center())
        line_b = Line(ORIGIN, UP*0.6 + LEFT*0.6, color=RED).move_to(hub_rect.get_center())
        line_c = Line(ORIGIN, DOWN*0.6 + RIGHT*0.6, color=RED).move_to(hub_rect.get_center())
        line_d = Line(ORIGIN, DOWN*0.6 + LEFT*0.6, color=RED).move_to(hub_rect.get_center())
        starburst = VGroup(line_a, line_b, line_c, line_d)
        
        # Expanding impact ring
        impact_ring = Circle(radius=0.1, color=RED).move_to(hub_rect.get_center())

        self.remove(signal1, signal2)
        self.play(
            FadeIn(collision_mark),
            Create(starburst),
            impact_ring.animate.scale(15).set_stroke(opacity=0),
            run_time=1
        )
        self.wait(1)

        # 5. Explanation Text
        footer_text = Text("Single Collision Domain = Logical Bus", color=GOLD, font_size=24).to_edge(DOWN, buff=0.5)
        math_desc = MathTex(r"\text{Total Bandwidth} / n", color=WHITE, font_size=30).next_to(footer_text, UP)
        
        self.play(Write(footer_text), Write(math_desc))
        self.wait(2)

        # Cleanup
        self.play(FadeOut(VGroup(hub, nodes, connections, bw_group, collision_mark, starburst, footer_text, math_desc)))