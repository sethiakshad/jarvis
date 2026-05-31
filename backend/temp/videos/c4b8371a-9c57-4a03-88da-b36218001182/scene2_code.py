from manim import *

class Scene2(Scene):
    def construct(self):
        # Title and Labels
        title = Text("Data Broadcasting Mechanism", color=GOLD, font_size=32).to_edge(UP)
        concept_text = Text("Lack of Intelligence: No Filtering", color=RED, font_size=24).next_to(title, DOWN)
        
        # Central Hub (represented by a Square)
        hub_rect = Square(side_length=1.5, color=TEAL, fill_opacity=0.4)
        hub_label = Text("HUB", font_size=20).move_to(hub_rect.get_center())
        hub = VGroup(hub_rect, hub_label)

        # Peripheral PCs (represented by Rectangles)
        pc1 = VGroup(Rectangle(width=1, height=0.8, color=BLUE, fill_opacity=0.6), Text("PC 1", font_size=16)).move_to([-4, 0, 0])
        pc2 = VGroup(Rectangle(width=1, height=0.8, color=BLUE, fill_opacity=0.6), Text("PC 2", font_size=16)).move_to([0, 2.5, 0])
        pc3 = VGroup(Rectangle(width=1, height=0.8, color=BLUE, fill_opacity=0.6), Text("PC 3", font_size=16)).move_to([4, 0, 0])
        pc4 = VGroup(Rectangle(width=1, height=0.8, color=BLUE, fill_opacity=0.6), Text("PC 4", font_size=16)).move_to([0, -2.5, 0])

        # Connection Lines
        line1 = Line(pc1.get_right(), hub_rect.get_left(), color=WHITE)
        line2 = Line(pc2.get_bottom(), hub_rect.get_top(), color=WHITE)
        line3 = Line(pc3.get_left(), hub_rect.get_right(), color=WHITE)
        line4 = Line(pc4.get_top(), hub_rect.get_bottom(), color=WHITE)
        connections = VGroup(line1, line2, line3, line4)

        # Initial Setup Animation
        self.play(Write(title))
        self.play(Create(hub), Create(pc1), Create(pc2), Create(pc3), Create(pc4))
        self.play(Create(connections))
        self.play(Write(concept_text))
        self.wait(1)

        # Data Packet Animation
        # Packet starts at PC 1
        packet = Dot(color=YELLOW, radius=0.12).move_to(pc1.get_center())
        
        # 1. Packet moves from PC 1 to Hub
        self.play(packet.animate.move_to(hub_rect.get_center()), run_time=1.5)
        self.play(hub_rect.animate.set_fill(YELLOW, opacity=0.6), run_time=0.3)
        self.play(hub_rect.animate.set_fill(TEAL, opacity=0.4), run_time=0.3)

        # 2. Create duplicated packets and broadcast arrows
        p2 = Dot(color=YELLOW, radius=0.12).move_to(hub_rect.get_center())
        p3 = Dot(color=YELLOW, radius=0.12).move_to(hub_rect.get_center())
        p4 = Dot(color=YELLOW, radius=0.12).move_to(hub_rect.get_center())
        
        arr2 = Arrow(hub_rect.get_top(), pc2.get_bottom(), color=GOLD, buff=0.1)
        arr3 = Arrow(hub_rect.get_right(), pc3.get_left(), color=GOLD, buff=0.1)
        arr4 = Arrow(hub_rect.get_bottom(), pc4.get_top(), color=GOLD, buff=0.1)
        broadcast_arrows = VGroup(arr2, arr3, arr4)

        # Show the broadcast
        self.play(Create(broadcast_arrows))
        self.play(
            p2.animate.move_to(pc2.get_center()),
            p3.animate.move_to(pc3.get_center()),
            p4.animate.move_to(pc4.get_center()),
            packet.animate.set_opacity(0), # Original packet vanishes/stays in hub
            run_time=2
        )

        # Final explanatory text
        explanation = Text("Data is sent to EVERY connected device.", font_size=22, color=YELLOW).to_edge(DOWN)
        self.play(Write(explanation))
        self.wait(2)

        # Clean up
        self.play(FadeOut(VGroup(title, concept_text, hub, pc1, pc2, pc3, pc4, connections, broadcast_arrows, p2, p3, p4, explanation)))

        # End of Scene2
        self.wait(1)

# Execution Requirements: Class Scene2, Concise, No external files, specific shapes.
# Total duration: ~12-15 seconds.