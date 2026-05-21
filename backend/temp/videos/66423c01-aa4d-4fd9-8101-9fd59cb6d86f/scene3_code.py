from manim import *

class Scene3(Scene):
    def construct(self):
        # Title and background elements
        title = Text("Fully-Buffered Forwarding", color=BLUE).to_edge(UP)
        
        # Create the switch representation
        switch_frame = Rectangle(width=8, height=4, color=WHITE)
        buffer_area = Rectangle(width=3, height=2, color=GOLD, fill_opacity=0.2).move_to(switch_frame.get_center())
        buffer_text = Text("Switch Buffer", color=GOLD).scale(0.6).next_to(buffer_area, UP)
        
        switch_vgroup = VGroup(switch_frame, buffer_area, buffer_text)
        
        # Create the data frame
        data_rect = Rectangle(width=1.5, height=0.8, fill_color=TEAL, fill_opacity=0.8)
        data_label = Text("Frame", color=WHITE).scale(0.4).move_to(data_rect.get_center())
        data_frame = VGroup(data_rect, data_label)
        data_frame.move_to(LEFT * 6)
        
        # Error check icons (Magnifying glass using Circle and Line)
        glass_circle = Circle(radius=0.4, color=YELLOW).move_to(buffer_area.get_center())
        glass_handle = Line(glass_circle.get_bottom(), glass_circle.get_bottom() + [0.3, -0.3, 0], color=YELLOW)
        magnifier = VGroup(glass_circle, glass_handle)
        
        check_mark = Text("✔", color=GREEN).scale(0.8).move_to(glass_circle.get_center())
        status_text = Text("Error Check: Pass", color=GREEN).scale(0.5).next_to(buffer_area, DOWN)

        # Sequence of animations
        self.play(Write(title))
        self.play(Create(switch_vgroup))
        self.wait(1)
        
        # 1. Frame enters the switch and stops in the buffer
        self.play(data_frame.animate.move_to(buffer_area.get_center()), run_time=2)
        self.wait(0.5)
        
        # 2. Perform error checking
        self.play(Create(magnifier))
        self.play(Write(check_mark), Write(status_text))
        self.wait(1.5)
        
        # 3. Frame is forwarded out
        self.play(
            FadeOut(magnifier),
            FadeOut(check_mark),
            FadeOut(status_text)
        )
        
        arrow_out = Arrow(start=buffer_area.get_right(), end=RIGHT * 6, color=WHITE)
        self.play(Create(arrow_out))
        self.play(data_frame.animate.move_to(RIGHT * 6), run_time=2)
        
        # Final cleanup
        self.play(FadeOut(data_frame), FadeOut(arrow_out), FadeOut(switch_vgroup), FadeOut(title))
        self.wait(1)

# End of code