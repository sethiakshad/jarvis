from manim import *

class Scene2(Scene):
    def construct(self):
        # Title and Layout
        title = Text("Switching Techniques", font_size=36, color=WHITE).to_edge(UP, buff=0.5)
        divider = Line(start=UP * 2, end=DOWN * 3, color=WHITE)
        
        label_cut = Text("Cut-through", color=YELLOW, font_size=28).shift(LEFT * 3.5 + UP * 2.2)
        label_buff = Text("Fully-buffered", color=TEAL, font_size=28).shift(RIGHT * 3.5 + UP * 2.2)
        
        self.add(title, divider, label_cut, label_buff)

        # Left Side: Cut-through components
        port_in_l = Circle(radius=0.4, color=WHITE).shift(LEFT * 6 + UP * 0.5)
        port_out_l = Circle(radius=0.4, color=WHITE).shift(LEFT * 1 + UP * 0.5)
        arrow_l = Arrow(port_in_l.get_right(), port_out_l.get_left(), buff=0.1, color=GRAY)
        data_packet_l = Rectangle(width=0.6, height=0.4, fill_color=BLUE, fill_opacity=0.8, color=BLUE).move_to(port_in_l)
        
        # Right Side: Fully-buffered components
        buffer_frame = Rectangle(width=3, height=1.5, color=WHITE).shift(RIGHT * 3.5 + UP * 0.5)
        buffer_text = Text("Switch Buffer", font_size=20).next_to(buffer_frame, UP, buff=0.1)
        
        progress_bg = Rectangle(width=2.5, height=0.4, color=GRAY, fill_opacity=0.2).move_to(buffer_frame)
        progress_fill = Rectangle(width=0.01, height=0.4, color=BLUE, fill_opacity=1.0).align_to(progress_bg, LEFT)
        
        port_in_r = Circle(radius=0.4, color=WHITE).shift(RIGHT * 0.8 + UP * 0.5)
        port_out_r = Circle(radius=0.4, color=WHITE).shift(RIGHT * 6.2 + UP * 0.5)
        
        data_packet_r = Rectangle(width=0.6, height=0.4, fill_color=BLUE, fill_opacity=0.8, color=BLUE).move_to(port_in_r)

        # Build VGroups
        cut_group = VGroup(port_in_l, port_out_l, arrow_l)
        buff_group = VGroup(buffer_frame, buffer_text, progress_bg, port_in_r, port_out_r)

        self.play(Create(cut_group), Create(buff_group))
        
        # Animation: Cut-through
        self.play(data_packet_l.animate.move_to(port_out_l), run_time=1.5, rate_func=linear)
        self.play(FadeOut(data_packet_l, shift=RIGHT))

        # Animation: Fully-buffered
        # 1. Packet enters buffer
        self.play(data_packet_r.animate.move_to(progress_bg.get_left() + RIGHT * 0.3), run_time=1)
        
        # 2. Buffer fills (Error Checking simulation)
        check_text = Text("Checking CRC...", font_size=18, color=YELLOW).next_to(progress_bg, DOWN, buff=0.2)
        self.play(Write(check_text))
        self.play(
            progress_fill.animate.stretch_to_fit_width(2.5).align_to(progress_bg, LEFT),
            run_time=2.5,
            rate_func=smooth
        )
        
        ok_text = Text("Frame Valid", font_size=18, color=GREEN).move_to(check_text)
        self.play(ReplacementTransform(check_text, ok_text))
        
        # 3. Packet leaves buffer
        self.play(
            data_packet_r.animate.move_to(port_out_r),
            FadeOut(progress_fill),
            run_time=1.5
        )
        self.play(FadeOut(data_packet_r, shift=RIGHT))
        
        self.wait(2)

# End of Script