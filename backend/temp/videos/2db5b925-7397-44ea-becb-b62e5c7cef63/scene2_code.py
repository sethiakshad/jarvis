from manim import *

class Scene2(Scene):
    def construct(self):
        # Title
        title = Text("The Four Necessary Conditions", color=YELLOW, font_size=36)
        title.to_edge(UP)
        self.play(Write(title))

        # 1. Mutual Exclusion
        me_box = Square(side_length=1.2, color=BLUE, fill_opacity=0.2)
        me_circle = Circle(radius=0.3, color=WHITE, fill_opacity=0.8).move_to(me_box.get_center())
        me_label = Text("Mutual Exclusion", font_size=20).next_to(me_box, DOWN)
        me_group = VGroup(me_box, me_circle, me_label).move_to([-3.5, 1, 0])

        # 2. Hold and Wait
        hw_r1 = Square(side_length=0.6, color=RED, fill_opacity=0.4)
        hw_p = Dot(color=TEAL).next_to(hw_r1, RIGHT, buff=1)
        hw_r2 = Square(side_length=0.6, color=RED, fill_opacity=0.4).next_to(hw_p, RIGHT, buff=1)
        hw_line = Line(hw_p.get_center(), hw_r1.get_center(), color=WHITE)
        hw_arrow = Arrow(hw_p.get_center(), hw_r2.get_left(), buff=0.1, color=WHITE, tip_length=0.2)
        hw_label = Text("Hold and Wait", font_size=20).next_to(hw_p, DOWN, buff=0.8)
        hw_group = VGroup(hw_r1, hw_p, hw_r2, hw_line, hw_arrow, hw_label).move_to([3.5, 1, 0])

        # 3. No Preemption
        np_circle = Circle(radius=0.6, color=GOLD, stroke_width=6)
        np_line = Line(start=[-0.4, 0.4, 0], end=[0.4, -0.4, 0], color=RED, stroke_width=6)
        np_line2 = Line(start=[0.4, 0.4, 0], end=[-0.4, -0.4, 0], color=RED, stroke_width=6)
        np_icon = VGroup(np_circle, np_line, np_line2)
        np_label = Text("No Preemption", font_size=20).next_to(np_icon, DOWN)
        np_group = VGroup(np_icon, np_label).move_to([-3.5, -2, 0])

        # 4. Circular Wait
        d1 = Dot(color=WHITE).move_to([0.5, 0.5, 0])
        d2 = Dot(color=WHITE).move_to([1.5, 0.5, 0])
        d3 = Dot(color=WHITE).move_to([1.5, -0.5, 0])
        d4 = Dot(color=WHITE).move_to([0.5, -0.5, 0])
        a1 = Arrow(d1.get_center(), d2.get_center(), buff=0.1, color=WHITE, tip_length=0.15)
        a2 = Arrow(d2.get_center(), d3.get_center(), buff=0.1, color=WHITE, tip_length=0.15)
        a3 = Arrow(d3.get_center(), d4.get_center(), buff=0.1, color=WHITE, tip_length=0.15)
        a4 = Arrow(d4.get_center(), d1.get_center(), buff=0.1, color=WHITE, tip_length=0.15)
        cw_icon = VGroup(d1, d2, d3, d4, a1, a2, a3, a4)
        cw_label = Text("Circular Wait", font_size=20).next_to(cw_icon, DOWN)
        cw_group = VGroup(cw_icon, cw_label).move_to([3.5, -2, 0])

        # Animations
        self.play(Create(me_group))
        self.wait(1)
        self.play(Create(hw_group))
        self.wait(1)
        self.play(Create(np_group))
        self.wait(1)
        self.play(Create(cw_group))
        self.wait(2)

        # Final emphasis
        rect = Rectangle(width=14, height=8, color=WHITE, fill_opacity=0).scale(0.9)
        self.play(Create(rect))
        self.wait(2)