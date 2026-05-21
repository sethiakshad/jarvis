from manim import *

class Scene2(Scene):
    def construct(self):
        # Title
        title = Text("Qualitative Data Characteristics", color=BLUE).scale(0.8)
        title.to_edge(UP, buff=0.5)

        # Speech Bubble Construction
        bubble_rect = Rectangle(width=4.5, height=2.5, color=TEAL, fill_opacity=0.2)
        feelings_text = Text("Feelings", color=WHITE).scale(0.7)
        perceptions_text = Text("Perceptions", color=WHITE).scale(0.7)
        feelings_text.move_to(bubble_rect.get_center() + UP * 0.4)
        perceptions_text.move_to(bubble_rect.get_center() + DOWN * 0.4)
        
        # Small triangle for speech bubble tail
        tail_line1 = Line(bubble_rect.get_bottom() + LEFT * 0.5, bubble_rect.get_bottom() + LEFT * 1.5 + DOWN * 0.5, color=TEAL)
        tail_line2 = Line(bubble_rect.get_bottom() + LEFT * 1.5 + DOWN * 0.5, bubble_rect.get_bottom() + LEFT * 1.0, color=TEAL)
        bubble_tail = VGroup(tail_line1, tail_line2)
        
        speech_bubble = VGroup(bubble_rect, feelings_text, perceptions_text, bubble_tail)
        speech_bubble.to_edge(LEFT, buff=1).shift(DOWN * 0.5)

        # Microphone Icon Construction
        mic_top = Circle(radius=0.4, color=WHITE, fill_opacity=0.8)
        mic_handle = Rectangle(width=0.3, height=0.8, color=WHITE, fill_opacity=1)
        mic_handle.next_to(mic_top, DOWN, buff=0)
        mic_base = Line(LEFT * 0.4, RIGHT * 0.4, color=WHITE).next_to(mic_handle, DOWN, buff=0)
        microphone = VGroup(mic_top, mic_handle, mic_base)
        microphone.to_edge(RIGHT, buff=2).shift(DOWN * 0.5)

        # Floating labels
        how_label = Text("How?", color=YELLOW).scale(0.8)
        why_label = Text("Why?", color=YELLOW).scale(0.8)
        how_label.move_to(microphone.get_top() + UP * 0.5)
        why_label.move_to(microphone.get_top() + UP * 0.5)

        # Animations
        self.play(Write(title))
        self.wait(1)

        self.play(
            Create(bubble_rect),
            Create(bubble_tail),
            Write(feelings_text),
            Write(perceptions_text),
            run_time=2
        )

        self.play(Create(microphone))
        
        # Pulsing and Floating sequence
        self.play(
            microphone.animate.scale(1.2),
            how_label.animate.shift(UP * 1.5).set_opacity(0),
            run_time=1.5
        )
        self.play(
            microphone.animate.scale(0.833), # Back to original
            why_label.animate.shift(UP * 2.0).set_opacity(0),
            run_time=1.5
        )

        # Final explanation text
        explanation = Text("Non-numerical & Descriptive", color=GOLD).scale(0.6)
        explanation.next_to(title, DOWN, buff=0.3)
        self.play(Write(explanation))
        
        self.wait(2)

        # Cleanup
        self.play(
            FadeOut(speech_bubble),
            FadeOut(microphone),
            FadeOut(title),
            FadeOut(explanation)
        )