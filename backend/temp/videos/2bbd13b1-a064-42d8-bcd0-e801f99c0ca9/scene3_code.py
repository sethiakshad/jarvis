from manim import *

class Scene3(Scene):
    def construct(self):
        # Title of the evolution timeline
        title = Text("The Evolution Timeline", color=BLUE).to_edge(UP, buff=0.5)
        
        # Horizontal base timeline line
        timeline = Line(LEFT * 5.5, RIGHT * 5.5, color=WHITE).shift(DOWN * 1.5)
        
        # Milestone 1: Apple Pie (2008)
        dot1 = Dot(color=RED).move_to(timeline.point_from_proportion(0.15))
        rect1 = Rectangle(height=0.7, width=1.6, fill_color=RED, fill_opacity=0.8)
        rect1.move_to(dot1.get_center() + UP * 2.5)
        label1 = Text("Apple Pie", font_size=18, color=WHITE).move_to(rect1.get_center())
        conn1 = Line(dot1.get_center(), rect1.get_bottom(), color=RED)
        m1 = VGroup(dot1, conn1, rect1, label1)

        # Milestone 2: Donut
        dot2 = Dot(color=YELLOW).move_to(timeline.point_from_proportion(0.38))
        rect2 = Rectangle(height=0.7, width=1.6, fill_color=YELLOW, fill_opacity=0.8)
        rect2.move_to(dot2.get_center() + UP * 1.2)
        label2 = Text("Donut", font_size=18, color=WHITE).move_to(rect2.get_center())
        conn2 = Line(dot2.get_center(), rect2.get_bottom(), color=YELLOW)
        m2 = VGroup(dot2, conn2, rect2, label2)

        # Milestone 3: KitKat
        dot3 = Dot(color=GOLD).move_to(timeline.point_from_proportion(0.62))
        rect3 = Rectangle(height=0.7, width=1.6, fill_color=GOLD, fill_opacity=0.8)
        rect3.move_to(dot3.get_center() + UP * 2.5)
        label3 = Text("KitKat", font_size=18, color=WHITE).move_to(rect3.get_center())
        conn3 = Line(dot3.get_center(), rect3.get_bottom(), color=GOLD)
        m3 = VGroup(dot3, conn3, rect3, label3)

        # Milestone 4: Android 11
        dot4 = Dot(color=TEAL).move_to(timeline.point_from_proportion(0.85))
        rect4 = Rectangle(height=0.7, width=1.8, fill_color=TEAL, fill_opacity=0.8)
        rect4.move_to(dot4.get_center() + UP * 1.2)
        label4 = Text("Android 11", font_size=18, color=WHITE).move_to(rect4.get_center())
        conn4 = Line(dot4.get_center(), rect4.get_bottom(), color=TEAL)
        m4 = VGroup(dot4, conn4, rect4, label4)

        # Sequence of Animations
        self.play(Write(title))
        self.play(Create(timeline))
        
        # Populating the timeline sequentially
        self.play(Create(m1), run_time=1.5)
        self.play(Create(m2), run_time=1.5)
        self.play(Create(m3), run_time=1.5)
        self.play(Create(m4), run_time=1.5)
        
        # Final display pause
        self.wait(2)

# Ensure no markdown fences are present. Output only code.