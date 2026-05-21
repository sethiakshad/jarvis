from manim import *

class Scene2(Scene):
    def construct(self):
        # 1. Setup UI elements
        title = Text("Broadcasting Data Packets", color=YELLOW).to_edge(UP)
        explanation = Text("Hubs broadcast data to every connected port.", font_size=24, color=TEAL).to_edge(DOWN)

        # 2. Create the Network Architecture
        # The Central Hub
        hub_square = Square(side_length=1.5, color=BLUE, fill_opacity=0.6)
        hub_label = Text("HUB", font_size=28).move_to(hub_square.get_center())
        hub = VGroup(hub_square, hub_label)

        # Connected Devices (PCs)
        pc_source = Circle(radius=0.5, color=GREEN, fill_opacity=0.3).move_to(LEFT * 4)
        pc_source_label = Text("Sender", font_size=20).next_to(pc_source, DOWN)

        pc_a = Circle(radius=0.5, color=WHITE, fill_opacity=0.2).move_to(RIGHT * 4 + UP * 2)
        pc_a_label = Text("PC A", font_size=20).next_to(pc_a, RIGHT)

        pc_b = Circle(radius=0.5, color=WHITE, fill_opacity=0.2).move_to(RIGHT * 4)
        pc_b_label = Text("PC B", font_size=20).next_to(pc_b, RIGHT)

        pc_c = Circle(radius=0.5, color=WHITE, fill_opacity=0.2).move_to(RIGHT * 4 + DOWN * 2)
        pc_c_label = Text("PC C", font_size=20).next_to(pc_c, RIGHT)

        # Connections (Lines)
        line1 = Line(pc_source.get_right(), hub_square.get_left(), color=WHITE)
        line2 = Line(hub_square.get_corner(UR), pc_a.get_left(), color=WHITE)
        line3 = Line(hub_square.get_right(), pc_b.get_left(), color=WHITE)
        line4 = Line(hub_square.get_corner(DR), pc_c.get_left(), color=WHITE)

        all_network = VGroup(hub, pc_source, pc_a, pc_b, pc_c, pc_source_label, pc_a_label, pc_b_label, pc_c_label, line1, line2, line3, line4)

        # 3. Animation Sequence
        self.play(Write(title))
        self.play(Create(all_network), run_time=2)
        self.wait(1)

        # Initial packet from Source to Hub
        packet = Square(side_length=0.3, color=GOLD, fill_opacity=1).move_to(pc_source.get_center())
        self.play(Create(packet))
        self.play(packet.animate.move_to(hub.get_center()), run_time=1.5)
        
        # Broadcast phase
        self.play(Write(explanation))
        
        # Create copies for broadcasting
        p_copy1 = packet.copy()
        p_copy2 = packet.copy()
        p_copy3 = packet.copy()

        # Hide original packet as it splits
        self.play(
            p_copy1.animate.move_to(pc_a.get_center()),
            p_copy2.animate.move_to(pc_b.get_center()),
            p_copy3.animate.move_to(pc_c.get_center()),
            packet.animate.set_fill(opacity=0),
            run_time=2
        )

        # Highlight that this is inefficient
        no_filter_text = Text("No Destination Filtering", color=RED, font_size=24).next_to(explanation, UP)
        self.play(Write(no_filter_text))
        
        self.wait(3)