from manim import *

class Scene2(Scene):
    def construct(self):
        # Background objects: Hub and Computers
        hub = Circle(radius=0.7, color=TEAL, fill_opacity=0.8)
        hub_text = Text("HUB", font_size=24, color=WHITE).move_to(hub.get_center())
        hub_group = VGroup(hub, hub_text)

        pc_a = Square(side_length=1.2, color=BLUE, fill_opacity=0.2).move_to(LEFT * 4 + UP * 2)
        pc_b = Square(side_length=1.2, color=BLUE, fill_opacity=0.2).move_to(RIGHT * 4 + UP * 2)
        pc_c = Square(side_length=1.2, color=BLUE, fill_opacity=0.2).move_to(LEFT * 4 + DOWN * 2)
        pc_d = Square(side_length=1.2, color=BLUE, fill_opacity=0.2).move_to(RIGHT * 4 + DOWN * 2)

        label_a = Text("Source PC", font_size=18).next_to(pc_a, UP)
        label_b = Text("PC 2", font_size=18).next_to(pc_b, UP)
        label_c = Text("PC 3", font_size=18).next_to(pc_c, DOWN)
        label_d = Text("PC 4", font_size=18).next_to(pc_d, DOWN)

        line_a = Line(pc_a.get_center(), hub.get_center(), color=WHITE, stroke_opacity=0.5)
        line_b = Line(pc_b.get_center(), hub.get_center(), color=WHITE, stroke_opacity=0.5)
        line_c = Line(pc_c.get_center(), hub.get_center(), color=WHITE, stroke_opacity=0.5)
        line_d = Line(pc_d.get_center(), hub.get_center(), color=WHITE, stroke_opacity=0.5)

        # Initial layout
        static_elements = VGroup(hub_group, pc_a, pc_b, pc_c, pc_d, label_a, label_b, label_c, label_d, line_a, line_b, line_c, line_d)
        self.add(static_elements)

        # Narrative title
        title = Text("Hub Broadcasting Logic", font_size=32, color=YELLOW).to_edge(UP)
        explanation = Text("Hubs repeat data to all ports", font_size=24).to_edge(DOWN)
        
        self.play(Write(title))
        self.play(Write(explanation))
        self.wait(1)

        # Data Packet Creation
        packet = Rectangle(width=0.5, height=0.3, color=GOLD, fill_opacity=1).move_to(pc_a.get_center())
        packet_label = Text("DATA", font_size=12, color=BLACK).move_to(packet.get_center())
        packet_group = VGroup(packet, packet_label)

        # Animation 1: PC A sends packet to Hub
        self.play(packet_group.animate.move_to(hub.get_center()), run_time=1.5)
        self.wait(0.5)

        # Animation 2: Hub broadcasts to B, C, D simultaneously
        packet_b = packet_group.copy()
        packet_c = packet_group.copy()
        packet_d = packet_group.copy()

        # Remove the original packet visual as it splits
        self.remove(packet_group)

        self.play(
            packet_b.animate.move_to(pc_b.get_center()),
            packet_c.animate.move_to(pc_c.get_center()),
            packet_d.animate.move_to(pc_d.get_center()),
            run_time=2,
            rate_func=smooth
        )

        # Final emphasis
        conclusion = Text("Every device receives the signal", font_size=24, color=RED).to_edge(DOWN)
        self.play(FadeOut(explanation))
        self.play(Write(conclusion))
        self.wait(2)

        # Clean up
        self.play(FadeOut(packet_b, packet_c, packet_d, title, conclusion, static_elements))