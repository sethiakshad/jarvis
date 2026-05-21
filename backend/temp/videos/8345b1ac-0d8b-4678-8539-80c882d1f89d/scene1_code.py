from manim import *

class Scene1(Scene):
    def construct(self):
        # Title
        title = Text("The Purpose of Data Collection", color=WHITE, font_size=40).to_edge(UP)
        
        # Raw Data Representation (Pile of Documents)
        doc_color = BLUE
        d1 = Rectangle(height=0.8, width=0.6, color=doc_color, fill_opacity=0.5)
        d2 = Rectangle(height=0.8, width=0.6, color=doc_color, fill_opacity=0.5).shift(RIGHT * 0.2 + DOWN * 0.1)
        d3 = Rectangle(height=0.8, width=0.6, color=doc_color, fill_opacity=0.5).shift(LEFT * 0.2 + UP * 0.1)
        raw_data = VGroup(d1, d2, d3).to_edge(LEFT, buff=1.5)
        data_label = Text("Raw Data", font_size=24).next_to(raw_data, DOWN)

        # Magnifying Glass (The Process)
        glass_circle = Circle(radius=0.7, color=TEAL, stroke_width=10)
        glass_handle = Line(
            start=glass_circle.point_from_proportion(0.875),
            end=glass_circle.point_from_proportion(0.875) + DOWN * 0.6 + RIGHT * 0.6,
            color=WHITE,
            stroke_width=10
        )
        magnifier = VGroup(glass_circle, glass_handle).move_to(ORIGIN)
        process_label = Text("Systematic Collection", font_size=24).next_to(magnifier, DOWN, buff=0.5)

        # Insights Representation (Lightbulb)
        bulb_top = Circle(radius=0.6, color=YELLOW, fill_opacity=0.8)
        bulb_base = Rectangle(height=0.2, width=0.4, color=GOLD, fill_opacity=1).next_to(bulb_top, DOWN, buff=0)
        insights_label = Text("Insights", font_size=28, color=YELLOW).next_to(bulb_base, DOWN)
        insights_group = VGroup(bulb_top, bulb_base, insights_label).to_edge(RIGHT, buff=1.5)

        # Arrows
        arrow_in = Arrow(raw_data.get_right(), magnifier.get_left(), color=WHITE, buff=0.2)
        arrow_out = Arrow(magnifier.get_right(), insights_group.get_left(), color=WHITE, buff=0.2)

        # Animation Sequence
        self.play(Write(title))
        self.wait(1)

        self.play(
            Create(raw_data),
            Write(data_label)
        )
        self.wait(1)

        self.play(
            Create(magnifier),
            Write(process_label)
        )
        self.play(GrowArrow(arrow_in))
        self.wait(1)

        self.play(
            Create(insights_group),
            GrowArrow(arrow_out)
        )
        self.wait(2)

        # Final emphasis
        self.play(
            insights_group.animate.scale(1.2),
            bulb_top.animate.set_color(WHITE),
            run_time=1
        )
        self.play(
            insights_group.animate.scale(1.0/1.2),
            bulb_top.animate.set_color(YELLOW),
            run_time=1
        )
        self.wait(2)

        # Cleanup
        self.play(
            FadeOut(title),
            FadeOut(raw_data),
            FadeOut(data_label),
            FadeOut(magnifier),
            FadeOut(process_label),
            FadeOut(insights_group),
            FadeOut(arrow_in),
            FadeOut(arrow_out)
        )
        self.wait(1)