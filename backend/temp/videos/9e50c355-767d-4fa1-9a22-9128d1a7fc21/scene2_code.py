from manim import *

class Scene2(Scene):
    def construct(self):
        # 1. Create the Hub in the center
        hub_box = Rectangle(color=BLUE, height=1.5, width=2.2, fill_opacity=0.2)
        hub_label = Text("HUB", color=BLUE, font_size=32).move_to(hub_box.get_center())
        hub = VGroup(hub_box, hub_label)

        # 2. Create Computers (PCs) at corners
        pc1 = VGroup(Circle(radius=0.5, color=WHITE), Text("PC 1", font_size=24)).shift(LEFT * 4 + UP * 2)
        pc2 = VGroup(Circle(radius=0.5, color=WHITE), Text("PC 2", font_size=24)).shift(RIGHT * 4 + UP * 2)
        pc3 = VGroup(Circle(radius=0.5, color=WHITE), Text("PC 3", font_size=24)).shift(RIGHT * 4 + DOWN * 2)
        pc4 = VGroup(Circle(radius=0.5, color=WHITE), Text("PC 4", font_size=24)).shift(LEFT * 4 + DOWN * 2)
        pcs = VGroup(pc1, pc2, pc3, pc4)

        # 3. Create Connection Lines
        line1 = Line(pc1.get_center(), hub_box.get_left(), color=GRAY)
        line2 = Line(pc2.get_center(), hub_box.get_top(), color=GRAY)
        line3 = Line(pc3.get_center(), hub_box.get_right(), color=GRAY)
        line4 = Line(pc4.get_center(), hub_box.get_bottom(), color=GRAY)
        lines = VGroup(line1, line2, line3, line4)

        # 4. Scene setup
        self.play(Create(hub), Create(pcs), Create(lines))
        self.wait(1)

        # 5. Data packet from PC 1
        packet_shape = Square(side_length=0.6, fill_opacity=1, color=GOLD)
        packet_text = Text("Data", font_size=14, color=BLACK).move_to(packet_shape.get_center())
        packet = VGroup(packet_shape, packet_text).move_to(pc1.get_center())

        explanation = Text("Hub broadcasting data to all ports", font_size=28, color=YELLOW).to_edge(UP)
        
        # 6. Animation sequence
        self.play(Write(explanation))
        
        # Packet moves to Hub
        self.play(packet.animate.move_to(hub_box.get_center()), run_time=1.5)
        
        # Instant Cloning
        p2 = packet.copy()
        p3 = packet.copy()
        p4 = packet.copy()

        # Packets move to all other PCs simultaneously
        self.play(
            p2.animate.move_to(pc2.get_center()),
            p3.animate.move_to(pc3.get_center()),
            p4.animate.move_to(pc4.get_center()),
            packet.animate.set_fill(opacity=0), # Original stays in hub then fades
            run_time=2
        )
        
        # Indicate broadcast nature
        broadcast_text = Text("Every device receives the same packet", font_size=24, color=RED).to_edge(DOWN)
        self.play(Write(broadcast_text))
        self.wait(2)

        # Cleanup
        self.play(
            FadeOut(packet),
            FadeOut(p2),
            FadeOut(p3),
            FadeOut(p4),
            FadeOut(explanation),
            FadeOut(broadcast_text)
        )
        self.wait(1)