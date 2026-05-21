from manim import *

class Scene3(Scene):
    def setup(self):
        # Configure a background-like layout using allowed objects
        self.title = Text("Fully-Buffered Forwarding", color=BLUE).to_edge(UP)
        self.explanation = Text("Checks full frame for errors before sending", color=WHITE).scale(0.4).next_to(self.title, DOWN)
        
        # Buffer area
        self.buffer_rect = Rectangle(width=4, height=2.5, color=WHITE).move_to(ORIGIN)
        self.buffer_label = Text("Buffer Memory").scale(0.4).next_to(self.buffer_rect, UP)
        
        # Ports
        self.in_arrow = Arrow(start=LEFT*6, end=LEFT*2, color=TEAL)
        self.out_arrow = Arrow(start=RIGHT*2, end=RIGHT*6, color=TEAL)
        self.in_label = Text("Input Port").scale(0.3).next_to(self.in_arrow, DOWN)
        self.out_label = Text("Output Port").scale(0.3).next_to(self.out_arrow, DOWN)

        # Data Frame
        frame_box = Rectangle(width=2.5, height=1.2, color=GOLD, fill_opacity=0.7)
        frame_text = Text("Data Frame").scale(0.4)
        self.data_frame = VGroup(frame_box, frame_text)
        self.data_frame.move_to(LEFT * 7)

        # Validation Mark
        # Replaced MathTex with Text to avoid LaTeX subprocess errors
        self.check_mark = Text("✔", color=GREEN).scale(3)
        self.check_mark.move_to(self.buffer_rect.get_center())
        self.valid_text = Text("Error Check: OK", color=GREEN).scale(0.4).next_to(self.buffer_rect, DOWN)

    def construct(self):
        # 1. Initial Scene Setup
        self.play(Write(self.title), Write(self.explanation))
        self.play(Create(self.buffer_rect), Write(self.buffer_label))
        self.play(Create(self.in_arrow), Create(self.out_arrow), Write(self.in_label), Write(self.out_label))
        
        # 2. Frame entering the buffer
        self.play(self.data_frame.animate.move_to(self.buffer_rect.get_center()), run_time=2)
        self.wait(1)

        # 3. Validation Process
        self.play(Write(self.check_mark))
        self.play(Write(self.valid_text))
        self.wait(2)

        # 4. Forwarding the frame
        self.play(FadeOut(self.check_mark), FadeOut(self.valid_text))
        self.play(self.data_frame.animate.move_to(RIGHT * 7), run_time=2)
        
        self.wait(1)

        # 5. Clean up
        self.play(
            FadeOut(self.data_frame),
            FadeOut(self.buffer_rect),
            FadeOut(self.buffer_label),
            FadeOut(self.in_arrow),
            FadeOut(self.out_arrow),
            FadeOut(self.title),
            FadeOut(self.explanation),
            FadeOut(self.in_label),
            FadeOut(self.out_label)
        )