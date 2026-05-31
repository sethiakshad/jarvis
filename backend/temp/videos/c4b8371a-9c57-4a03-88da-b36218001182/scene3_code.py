from manim import *

class Scene3(Scene):
    def construct(self):
        # Scene Heading
        title = Text("Logical Bus Behavior", color=TEAL).scale(0.8)
        title.to_edge(UP)

        # Main Hub Container
        hub_frame = Rectangle(width=7, height=3.5, color=BLUE, fill_opacity=0.1)
        hub_label = Text("HUB", color=BLUE).scale(0.5).next_to(hub_frame, UP, buff=0.1)

        # Logical Shared Bus Path (The yellow path mentioned in the plan)
        shared_bus = Line(LEFT * 2.5, RIGHT * 2.5, color=YELLOW, stroke_width=10)
        shared_bus.move_to(hub_frame.get_center())
        bus_label = Text("Shared Bandwidth", color=YELLOW).scale(0.5).next_to(shared_bus, DOWN, buff=0.3)

        # Ports (Visualized as squares)
        port_left = Square(side_length=0.4, color=WHITE, fill_opacity=0.5)
        port_left.move_to(hub_frame.get_top() + LEFT * 2 + DOWN * 0.6)
        
        port_right = Square(side_length=0.4, color=WHITE, fill_opacity=0.5)
        port_right.move_to(hub_frame.get_top() + RIGHT * 2 + DOWN * 0.6)

        # Connection lines from ports to the shared yellow bus
        conn_left = Line(port_left.get_bottom(), [port_left.get_x(), shared_bus.get_y(), 0], color=WHITE)
        conn_right = Line(port_right.get_bottom(), [port_right.get_x(), shared_bus.get_y(), 0], color=WHITE)

        # Data Packets
        packet_a = Dot(color=RED).move_to(port_left.get_center())
        packet_b = Dot(color=RED).move_to(port_right.get_center())

        # Collision Indicator
        collision_mark = Text("COLLISION", color=RED).scale(0.9)
        collision_mark.move_to(shared_bus.get_center() + UP * 0.5)
        
        domain_info = Text("Single Collision Domain", color=GOLD).scale(0.7)
        domain_info.to_edge(DOWN, buff=0.5)

        # Animation Sequence
        self.play(Write(title))
        self.play(Create(hub_frame), Write(hub_label))
        self.play(Create(shared_bus), Write(bus_label))
        self.play(
            Create(VGroup(port_left, port_right, conn_left, conn_right))
        )
        self.wait(1)

        # Move packets toward the center of the shared bus
        self.play(
            packet_a.animate.move_to(shared_bus.get_center()),
            packet_b.animate.move_to(shared_bus.get_center()),
            run_time=2
        )

        # Show collision effect
        self.play(
            packet_a.animate.scale(3).set_color(ORANGE),
            packet_b.animate.scale(3).set_color(ORANGE),
            Write(collision_mark)
        )
        
        self.play(Write(domain_info))
        self.wait(2)

        # Final cleanup for timing
        self.play(FadeOut(VGroup(packet_a, packet_b, collision_mark)))
        self.wait(1)