from manim import *

class Scene1(Scene):
    def construct(self):
        # Title and Concept Labels
        title = Text("Star Topology: The Hub", color=GOLD, font_size=36).to_edge(UP)
        layer_info = Text("Physical Layer Device", color=WHITE, font_size=24).next_to(title, DOWN)
        
        # Central Hub representation
        hub_box = Rectangle(width=2.5, height=1.2, color=BLUE, fill_opacity=0.8)
        hub_label = Text("HUB", color=WHITE, font_size=28)
        hub = VGroup(hub_box, hub_label).move_to(ORIGIN)

        # Peripheral Stations (Computers)
        def create_station(name, pos):
            box = Square(side_length=0.9, color=TEAL, fill_opacity=0.5)
            label = Text(name, color=WHITE, font_size=18)
            return VGroup(box, label).move_to(pos)

        pc1 = create_station("PC 1", 2.5 * UP + 4 * LEFT)
        pc2 = create_station("PC 2", 2.5 * UP + 4 * RIGHT)
        pc3 = create_station("PC 3", 2.5 * DOWN + 4 * LEFT)
        pc4 = create_station("PC 4", 2.5 * DOWN + 4 * RIGHT)
        stations = VGroup(pc1, pc2, pc3, pc4)

        # Connection Lines (Star shape)
        line1 = Line(hub.get_center(), pc1.get_center(), color=WHITE, stroke_width=2)
        line2 = Line(hub.get_center(), pc2.get_center(), color=WHITE, stroke_width=2)
        line3 = Line(hub.get_center(), pc3.get_center(), color=WHITE, stroke_width=2)
        line4 = Line(hub.get_center(), pc4.get_center(), color=WHITE, stroke_width=2)
        connections = VGroup(line1, line2, line3, line4)

        # Animation Sequence
        self.play(Write(title))
        self.play(Write(layer_info))
        self.wait(0.5)
        
        self.play(Create(hub))
        self.play(Create(connections), Create(stations), run_time=2)
        self.wait(1)

        # Multi-port Repeater Logic Visualization
        # A signal comes from PC1 to the Hub
        signal_start = Dot(color=YELLOW).move_to(pc1.get_center())
        self.play(signal_start.animate.move_to(hub.get_center()), run_time=1)
        
        # The Hub repeats the signal to all other ports
        s2 = Dot(color=YELLOW).move_to(hub.get_center())
        s3 = Dot(color=YELLOW).move_to(hub.get_center())
        s4 = Dot(color=YELLOW).move_to(hub.get_center())
        
        self.play(
            signal_start.animate.move_to(pc2.get_center()),
            s2.animate.move_to(pc3.get_center()),
            s3.animate.move_to(pc4.get_center()),
            s4.animate.move_to(pc1.get_center()),
            run_time=1.5
        )
        
        # Cleanup
        self.play(
            FadeOut(signal_start),
            FadeOut(s2),
            FadeOut(s3),
            FadeOut(s4)
        )
        
        explanation = Text("Acts as a multi-port repeater", font_size=20, color=YELLOW).to_edge(DOWN)
        self.play(Write(explanation))
        self.wait(2)