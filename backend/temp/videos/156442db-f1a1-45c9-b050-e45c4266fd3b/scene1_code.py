from manim import *

class Scene1(Scene):
    def construct(self):
        # 1. Create the Central Hub
        hub_rect = Rectangle(width=2.2, height=1.4, color=BLUE, fill_opacity=0.3)
        hub_label = Text("HUB", font_size=32, color=BLUE).move_to(hub_rect.get_center())
        hub = VGroup(hub_rect, hub_label).move_to(ORIGIN)

        # 2. Create Stations (Nodes)
        station_a = Circle(radius=0.4, color=WHITE).move_to(UP*2.5 + LEFT*3.5)
        station_b = Circle(radius=0.4, color=WHITE).move_to(UP*2.5 + RIGHT*3.5)
        station_c = Circle(radius=0.4, color=WHITE).move_to(DOWN*2.5 + LEFT*3.5)
        station_d = Circle(radius=0.4, color=WHITE).move_to(DOWN*2.5 + RIGHT*3.5)

        label_a = Text("A", font_size=24).move_to(station_a.get_center())
        label_b = Text("B", font_size=24).move_to(station_b.get_center())
        label_c = Text("C", font_size=24).move_to(station_c.get_center())
        label_d = Text("D", font_size=24).move_to(station_d.get_center())

        stations = VGroup(station_a, station_b, station_c, station_d)
        labels = VGroup(label_a, label_b, label_c, label_d)

        # 3. Create Connections (Lines)
        line_a = Line(station_a.get_bottom(), hub_rect.get_top() + LEFT*0.5, color=GRAY)
        line_b = Line(station_b.get_bottom(), hub_rect.get_top() + RIGHT*0.5, color=GRAY)
        line_c = Line(station_c.get_top(), hub_rect.get_bottom() + LEFT*0.5, color=GRAY)
        line_d = Line(station_d.get_top(), hub_rect.get_bottom() + RIGHT*0.5, color=GRAY)
        lines = VGroup(line_a, line_b, line_c, line_d)

        # 4. Title and Concept Text
        title = Text("Star Topology: Hub as Multi-port Repeater", font_size=30, color=GOLD).to_edge(UP)

        # Build Scene
        self.add(title)
        self.play(Create(hub), run_time=1)
        self.play(Create(stations), Write(labels), run_time=1.5)
        self.play(Create(lines), run_time=1)
        self.wait(1)

        # 5. Signal Animation
        # Signal enters from A to Hub
        signal_in = Dot(color=RED).move_to(station_a.get_center())
        self.play(signal_in.animate.move_to(hub.get_center()), run_time=1)
        self.remove(signal_in)

        # Hub flashes to show regeneration
        flash = hub_rect.copy().set_color(YELLOW).set_stroke(width=8)
        self.play(hub_rect.animate.set_fill(opacity=0.8), Create(flash), run_time=0.3)
        self.play(hub_rect.animate.set_fill(opacity=0.3), FadeOut(flash), run_time=0.3)

        # Hub duplicates and broadcasts signal to B, C, and D
        signal_out_b = Dot(color=RED).move_to(hub.get_center())
        signal_out_c = Dot(color=RED).move_to(hub.get_center())
        signal_out_d = Dot(color=RED).move_to(hub.get_center())

        self.play(
            signal_out_b.animate.move_to(station_b.get_center()),
            signal_out_c.animate.move_to(station_c.get_center()),
            signal_out_d.animate.move_to(station_d.get_center()),
            run_time=1.5
        )

        # Final explanation label
        explanation = Text("Regenerated signals sent to all other ports", font_size=24, color=TEAL).to_edge(DOWN)
        self.play(Write(explanation))
        self.wait(2)