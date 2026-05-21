from manim import *

class Scene3(Scene):
    def construct(self):
        # 1. Setup Title and basic components
        title = Text("Fully-Buffered Forwarding", font_size=36, color=WHITE)
        title.to_edge(UP)
        
        explanation = Text("Checks whole frame for errors before forwarding", font_size=20, color=GOLD)
        explanation.next_to(title, DOWN)

        # Switch representation
        switch_body = Rectangle(width=4.5, height=3, color=BLUE, fill_opacity=0.1)
        switch_body.move_to(LEFT * 2)
        switch_label = Text("Switch", font_size=24, color=BLUE)
        switch_label.next_to(switch_body, UP)

        # Buffer inside the switch
        buffer_box = Rectangle(width=3, height=0.8, color=WHITE)
        buffer_box.move_to(switch_body.get_center())
        buffer_text = Text("Port Buffer", font_size=18).next_to(buffer_box, DOWN)

        # Destination PC
        destination = Circle(radius=0.6, color=TEAL, fill_opacity=0.2)
        destination.move_to(RIGHT * 4.5)
        pc_label = Text("Destination PC", font_size=20).next_to(destination, DOWN)

        # Incoming Data Frame
        frame = Rectangle(width=0.8, height=0.5, color=YELLOW, fill_opacity=0.8)
        frame.move_to(LEFT * 7)

        # 2. Animations
        self.play(
            Write(title),
            Create(VGroup(switch_body, buffer_box, switch_label, buffer_text)),
            Create(VGroup(destination, pc_label))
        )
        self.play(Write(explanation))
        self.wait(1)

        # Frame arrives at the switch
        self.play(frame.animate.move_to(buffer_box.get_left() + RIGHT * 0.5), run_time=1.5)
        
        # Buffer filling animation
        filling_rect = Rectangle(width=0.1, height=0.6, color=YELLOW, fill_opacity=0.5)
        filling_rect.move_to(buffer_box.get_left(), aligned_edge=LEFT)
        filling_rect.shift(RIGHT * 0.1)

        self.play(
            filling_rect.animate.stretch_to_fit_width(2.8).move_to(buffer_box.get_left() + RIGHT * 0.1, aligned_edge=LEFT),
            frame.animate.set_fill(opacity=0),
            run_time=2
        )

        # Error Checking Indicator
        check_text = Text("Error-Free", color=GREEN, font_size=24)
        check_text.next_to(buffer_box, UP, buff=0.2)
        
        # Manually construct a green checkmark
        line1 = Line(start=LEFT * 0.2 + DOWN * 0.1, end=ORIGIN, color=GREEN)
        line2 = Line(start=ORIGIN, end=RIGHT * 0.3 + UP * 0.4, color=GREEN)
        checkmark = VGroup(line1, line2).next_to(check_text, RIGHT)

        self.play(Write(check_text), Create(checkmark))
        self.wait(1)

        # Forwarding to Destination
        # Re-materialize the frame to show it leaving
        outgoing_frame = Rectangle(width=0.8, height=0.5, color=YELLOW, fill_opacity=0.8)
        outgoing_frame.move_to(buffer_box.get_right())

        self.play(
            outgoing_frame.animate.move_to(destination.get_center()),
            filling_rect.animate.set_fill(opacity=0),
            FadeOut(VGroup(check_text, checkmark)),
            run_time=1.5
        )

        # End sequence
        self.play(
            VGroup(outgoing_frame, destination).animate.scale(1.1).set_color(GREEN),
            run_time=1
        )
        self.wait(2)