from manim import *

class Scene2(Scene):
    def construct(self):
        # Title and Layout Setup
        title = Text("Forwarding Techniques", font_size=36, color=WHITE).to_edge(UP)
        divider = Line(UP * 2, DOWN * 3, color=WHITE)
        
        label_cut = Text("Cut-through", color=BLUE, font_size=28).shift(LEFT * 3.5 + UP * 2)
        label_buff = Text("Fully-buffered", color=TEAL, font_size=28).shift(RIGHT * 3.5 + UP * 2)
        
        port_left = Rectangle(width=3.5, height=1.2, color=WHITE).shift(LEFT * 3.5)
        port_right = Rectangle(width=3.5, height=1.2, color=WHITE).shift(RIGHT * 3.5)
        
        self.add(title, divider, label_cut, label_buff, port_left, port_right)

        # Cut-through Frame Components
        header_l = Rectangle(width=0.6, height=0.6, fill_color=RED, fill_opacity=1, stroke_width=1)
        data_l = Rectangle(width=1.4, height=0.6, fill_color=YELLOW, fill_opacity=1, stroke_width=1)
        frame_l = VGroup(header_l, data_l).arrange(RIGHT, buff=0)
        frame_l.move_to(LEFT * 7)

        # Fully-buffered Frame Components
        header_r = Rectangle(width=0.6, height=0.6, fill_color=RED, fill_opacity=1, stroke_width=1)
        data_r = Rectangle(width=1.4, height=0.6, fill_color=YELLOW, fill_opacity=1, stroke_width=1)
        frame_r = VGroup(header_r, data_r).arrange(RIGHT, buff=0)
        frame_r.move_to(RIGHT * 0.5)

        # Animation: Cut-through (Fast movement)
        self.play(frame_l.animate.move_to(LEFT * 3.5), run_time=1.5)
        # As soon as header is in, it starts exiting
        self.play(frame_l.animate.move_to(LEFT * 0.5), run_time=1.5)
        
        # Animation: Fully-buffered (Delayed movement)
        self.play(frame_r.animate.move_to(RIGHT * 3.5), run_time=1.5)
        
        # Error Check Visuals
        check_text = Text("Error Check", color=GREEN, font_size=24).next_to(port_right, DOWN)
        check_mark_part1 = Line(start=LEFT*0.2 + DOWN*0.1, end=ORIGIN, color=GREEN, stroke_width=6)
        check_mark_part2 = Line(start=ORIGIN, end=RIGHT*0.3 + UP*0.4, color=GREEN, stroke_width=6)
        check_mark = VGroup(check_mark_part1, check_mark_part2).next_to(check_text, RIGHT)
        
        self.play(Write(check_text), Create(check_mark))
        self.wait(1)
        
        # Forward Fully-buffered frame
        self.play(
            frame_r.animate.move_to(RIGHT * 7),
            FadeOut(check_text),
            FadeOut(check_mark),
            run_time=1.5
        )

        # Final Concept Highlight
        desc_l = Text("Low Latency", color=BLUE, font_size=20).next_to(port_left, DOWN)
        desc_r = Text("Error Free", color=TEAL, font_size=20).next_to(port_right, DOWN)
        
        self.play(Write(desc_l), Write(desc_r))
        self.wait(2)

        # Cleanup for scene duration rules
        self.play(FadeOut(VGroup(frame_l, frame_r, port_left, port_right, divider, title, label_cut, label_buff, desc_l, desc_r)))