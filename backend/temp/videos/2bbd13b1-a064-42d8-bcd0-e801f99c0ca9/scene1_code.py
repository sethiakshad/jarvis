from manim import *

class Scene1(Scene):
    def construct(self):
        # 1. Title
        title = Text("Android's Global Presence", color=WHITE).scale(0.8).to_edge(UP)

        # 2. Globe Representation (Left side)
        # Using Circle and Lines to simulate a stylized globe
        globe_outline = Circle(radius=1.8, color=BLUE, fill_opacity=0.1)
        lat1 = Line(LEFT * 1.4, RIGHT * 1.4).shift(UP * 0.8)
        lat2 = Line(LEFT * 1.8, RIGHT * 1.8)
        lat3 = Line(LEFT * 1.4, RIGHT * 1.4).shift(DOWN * 0.8)
        lon1 = Line(UP * 1.4, DOWN * 1.4).shift(LEFT * 0.8)
        lon2 = Line(UP * 1.8, DOWN * 1.8)
        lon3 = Line(UP * 1.4, DOWN * 1.4).shift(RIGHT * 0.8)
        
        globe_lines = VGroup(lat1, lat2, lat3, lon1, lon2, lon3)
        globe = VGroup(globe_outline, globe_lines).to_edge(LEFT, buff=1)

        # 3. Market Share Graphic (Right side)
        # Replaced MathTex with Text to avoid LaTeX subprocess issues
        percent_val = Text("75%", color=YELLOW).scale(2.5)
        percent_label = Text("Global Market Share", font_size=24).next_to(percent_val, DOWN)
        share_group = VGroup(percent_val, percent_label).shift(RIGHT * 3 + UP * 1.5)

        # 4. Countries Info
        countries_text = Text("190+ Countries", color=TEAL, font_size=32).next_to(share_group, DOWN, buff=0.6)

        # 5. Simplified Android Logo
        # Constructed using Circle, Rectangle, Line, and Dot
        head = Circle(radius=0.4, color=GREEN, fill_opacity=1)
        body = Rectangle(width=0.8, height=0.7, color=GREEN, fill_opacity=1).next_to(head, DOWN, buff=-0.1)
        # Eyes
        eye_l = Dot(head.get_center() + LEFT * 0.15 + UP * 0.1, color=WHITE, radius=0.04)
        eye_r = Dot(head.get_center() + RIGHT * 0.15 + UP * 0.1, color=WHITE, radius=0.04)
        # Antennae
        ant1 = Line(head.get_center(), head.get_center() + [0.3, 0.4, 0], color=GREEN, stroke_width=4)
        ant2 = Line(head.get_center(), head.get_center() + [-0.3, 0.4, 0], color=GREEN, stroke_width=4)
        # Arms
        arm_l = Rectangle(width=0.15, height=0.5, color=GREEN, fill_opacity=1).next_to(body, LEFT, buff=0.1)
        arm_r = Rectangle(width=0.15, height=0.5, color=GREEN, fill_opacity=1).next_to(body, RIGHT, buff=0.1)
        
        android_logo = VGroup(head, body, eye_l, eye_r, ant1, ant2, arm_l, arm_r).scale(0.8).next_to(countries_text, DOWN, buff=0.5)

        # Animations
        self.play(Write(title))
        self.play(Create(globe_outline), Create(globe_lines), run_time=2)
        
        # Simultaneous rotation and text appearance
        self.play(
            Rotate(globe_lines, angle=PI/2),
            FadeIn(percent_val, shift=UP),
            Write(percent_label),
            run_time=2
        )
        
        self.play(
            Rotate(globe_lines, angle=PI/2),
            Write(countries_text),
            run_time=2
        )
        
        self.play(
            Rotate(globe_lines, angle=PI/4),
            FadeIn(android_logo),
            run_time=2
        )

        self.wait(2)