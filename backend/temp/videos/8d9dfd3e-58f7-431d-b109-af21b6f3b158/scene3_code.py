from manim import *

class Scene3(Scene):
    def construct(self):
        # Title and Labels
        title = Text("Fully-Buffered Forwarding", color=WHITE).scale(0.8)
        title.to_edge(UP)
        
        # Switch components
        switch_box = Rectangle(width=6, height=4, color=WHITE)
        switch_label = Text("Switch", color=WHITE).scale(0.6)
        switch_label.next_to(switch_box, UP, buff=0.1)
        
        buffer_area = Rectangle(width=2.5, height=1.5, color=TEAL, fill_opacity=0.2)
        buffer_area.move_to(switch_box.get_center())
        buffer_text = Text("Buffer", color=TEAL).scale(0.5)
        buffer_text.next_to(buffer_area, DOWN, buff=0.1)
        
        switch_group = VGroup(switch_box, switch_label, buffer_area, buffer_text)

        # Data Frame
        frame_rect = Rectangle(width=1.8, height=0.8, color=BLUE, fill_opacity=0.8)
        frame_label = Text("FRAME", color=WHITE).scale(0.4)
        data_frame = VGroup(frame_rect, frame_label)
        data_frame.move_to(LEFT * 6)

        # Error Check Visuals (Magnifying glass + Checkmark)
        mag_circle = Circle(radius=0.4, color=GOLD)
        mag_handle = Line(mag_circle.get_bottom(), mag_circle.get_bottom() + (DOWN * 0.3 + RIGHT * 0.3), color=GOLD)
        magnifier = VGroup(mag_circle, mag_handle).next_to(buffer_area, UP, buff=0.3)
        
        check_mark = Text("CRC PASS", color=GREEN).scale(0.6)
        check_mark.next_to(buffer_area, UP, buff=0.4)

        # Animations
        self.add(title)
        self.play(Create(switch_group))
        self.wait(1)

        # 1. Frame enters the switch and fills the buffer
        self.play(data_frame.animate.move_to(buffer_area.get_center()), run_time=2)
        self.wait(0.5)

        # 2. Error Check (Simulation)
        self.play(Create(magnifier))
        self.play(magnifier.animate.shift(RIGHT * 0.5), run_time=0.5)
        self.play(magnifier.animate.shift(LEFT * 1.0), run_time=0.5)
        self.play(magnifier.animate.shift(RIGHT * 0.5), run_time=0.5)
        
        self.play(ReplacementTransform(magnifier, check_mark))
        self.wait(1)

        # 3. Frame is forwarded out
        arrow_out = Arrow(buffer_area.get_right(), RIGHT * 6, color=YELLOW)
        self.play(Create(arrow_out))
        self.play(
            data_frame.animate.move_to(RIGHT * 6),
            check_mark.animate.set_fill(opacity=0),
            FadeOut(arrow_out),
            run_time=2
        )
        
        # Closing
        explanation = Text("Frame verified and forwarded.", color=YELLOW).scale(0.5)
        explanation.next_to(switch_box, DOWN, buff=0.5)
        self.play(Write(explanation))
        self.wait(2)