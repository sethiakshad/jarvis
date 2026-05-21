from manim import *

class Scene2(Scene):
    def construct(self):
        # 1. Create Title and Hub
        title = Text("Hub: Broadcast Transmission", color=WHITE).scale(0.8).to_edge(UP)
        hub = Square(side_length=1.5, color=TEAL, fill_opacity=0.4)
        hub_label = Text("HUB", color=WHITE).scale(0.6).move_to(hub.get_center())
        hub_group = VGroup(hub, hub_label)

        # 2. Create Network Devices (PCs)
        pc1 = Square(side_length=1.0, color=BLUE, fill_opacity=0.2).shift(4 * LEFT)
        pc2 = Square(side_length=1.0, color=BLUE, fill_opacity=0.2).shift(3 * UP + 4 * RIGHT)
        pc3 = Square(side_length=1.0, color=BLUE, fill_opacity=0.2).shift(4 * RIGHT)
        pc4 = Square(side_length=1.0, color=BLUE, fill_opacity=0.2).shift(3 * DOWN + 4 * RIGHT)
        
        pcs = VGroup(pc1, pc2, pc3, pc4)
        
        labels = VGroup(
            Text("PC 1", color=WHITE).scale(0.5).next_to(pc1, DOWN),
            Text("PC 2", color=WHITE).scale(0.5).next_to(pc2, RIGHT),
            Text("PC 3", color=WHITE).scale(0.5).next_to(pc3, RIGHT),
            Text("PC 4", color=WHITE).scale(0.5).next_to(pc4, RIGHT)
        )
        
        # 3. Create Connections
        line1 = Line(pc1.get_right(), hub.get_left(), color=GRAY)
        line2 = Line(hub.get_corner(UR), pc2.get_left(), color=GRAY)
        line3 = Line(hub.get_right(), pc3.get_left(), color=GRAY)
        line4 = Line(hub.get_corner(DR), pc4.get_left(), color=GRAY)
        lines = VGroup(line1, line2, line3, line4)

        # 4. Create Packet
        packet = Rectangle(width=0.5, height=0.3, color=YELLOW, fill_opacity=1.0)
        packet_text = Text("Data", color=BLACK).scale(0.2).move_to(packet.get_center())
        data_packet = VGroup(packet, packet_text).move_to(pc1.get_center())

        # 5. Scene Animations
        self.play(Write(title))
        self.play(Create(hub_group), Create(pcs), Create(lines), Write(labels))
        self.wait(1)

        # Packet moves to Hub
        self.play(data_packet.animate.move_to(hub.get_center()), run_time=1.5)
        
        # Explanation Text
        explanation = Text("Lack of Filtering: Broadcast to All", color=GOLD).scale(0.6).to_edge(DOWN)
        self.play(Write(explanation))

        # Create copies for broadcasting
        packet2 = data_packet.copy()
        packet3 = data_packet.copy()
        packet4 = data_packet.copy()

        # Simultaneous Broadcast Animation
        self.play(
            packet2.animate.move_to(pc2.get_center()),
            packet3.animate.move_to(pc3.get_center()),
            packet4.animate.move_to(pc4.get_center()),
            data_packet.animate.set_fill(fill_opacity=0),
            run_time=2,
            rate_func=linear
        )
        
        self.wait(2)

        # Final Highlight on Broadcast
        red_circles = VGroup(
            Circle(radius=0.7, color=RED).move_to(pc2.get_center()),
            Circle(radius=0.7, color=RED).move_to(pc3.get_center()),
            Circle(radius=0.7, color=RED).move_to(pc4.get_center())
        )
        self.play(Create(red_circles))
        self.wait(2)

        # End of Scene
        self.play(FadeOut(hub_group), FadeOut(pcs), FadeOut(lines), FadeOut(labels), FadeOut(packet2), FadeOut(packet3), FadeOut(packet4), FadeOut(explanation), FadeOut(red_circles), FadeOut(title), FadeOut(data_packet))