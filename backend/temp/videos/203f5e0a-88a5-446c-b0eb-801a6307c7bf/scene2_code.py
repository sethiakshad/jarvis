from manim import *

class Scene2(Scene):
    def construct(self):
        # Title
        title = Text("Data Broadcasting Mechanism", color=YELLOW, font_size=36)
        title.to_edge(UP)
        self.add(title)

        # Central Hub
        hub = Square(side_length=1.5, color=GOLD, fill_opacity=0.8)
        hub_label = Text("HUB", font_size=24, color=WHITE).move_to(hub.get_center())
        hub_group = VGroup(hub, hub_label)

        # Connected Devices (PCs)
        pc1 = Circle(radius=0.5, color=BLUE, fill_opacity=0.7).shift(LEFT * 4)
        pc2 = Circle(radius=0.5, color=TEAL, fill_opacity=0.7).shift(UP * 2 + RIGHT * 3)
        pc3 = Circle(radius=0.5, color=TEAL, fill_opacity=0.7).shift(RIGHT * 4)
        pc4 = Circle(radius=0.5, color=TEAL, fill_opacity=0.7).shift(DOWN * 2 + RIGHT * 3)

        pc1_label = Text("Sender", font_size=18).next_to(pc1, DOWN)
        devices = VGroup(pc1, pc2, pc3, pc4, pc1_label)

        # Connections
        line1 = Line(pc1.get_right(), hub.get_left(), color=WHITE)
        line2 = Line(hub.get_corner(UP + RIGHT), pc2.get_left(), color=WHITE)
        line3 = Line(hub.get_right(), pc3.get_left(), color=WHITE)
        line4 = Line(hub.get_corner(DOWN + RIGHT), pc4.get_left(), color=WHITE)
        lines = VGroup(line1, line2, line3, line4)

        # Layout Setup
        self.play(Create(hub_group), Create(devices), Create(lines))
        self.wait(1)

        # Packet Creation
        packet_rect = Rectangle(width=0.8, height=0.4, color=WHITE, fill_opacity=1)
        packet_text = Text("Packet", color=BLACK, font_size=14).move_to(packet_rect.get_center())
        packet = VGroup(packet_rect, packet_text).move_to(pc1.get_center())

        # Step 1: Packet to Hub
        self.play(packet.animate.move_to(hub.get_center()), run_time=1.5)
        self.wait(0.5)

        # Step 2: Hub broadcasts (Copies)
        packet_copy1 = packet.copy()
        packet_copy2 = packet.copy()
        packet_copy3 = packet.copy()

        # Explanation Text
        explanation = Text("Broadcasting to all ports...", font_size=24, color=RED).next_to(hub, DOWN, buff=1)
        self.play(Write(explanation))

        # Step 3: Simultaneous movement to all other PCs
        self.play(
            packet_copy1.animate.move_to(pc2.get_center()),
            packet_copy2.animate.move_to(pc3.get_center()),
            packet_copy3.animate.move_to(pc4.get_center()),
            packet.animate.set_fill(opacity=0),
            run_time=2
        )
        
        # Conclusion text
        no_intelligence = Text("No data filtering or routing logic", font_size=20, color=WHITE).to_edge(DOWN, buff=0.5)
        self.play(Write(no_intelligence))
        self.wait(2)

        # Cleanup for concise ending
        self.play(FadeOut(VGroup(packet_copy1, packet_copy2, packet_copy3, packet, explanation, no_intelligence, hub_group, devices, lines, title)))