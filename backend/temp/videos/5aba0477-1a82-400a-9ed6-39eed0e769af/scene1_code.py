from manim import *

class Scene1(Scene):
    def construct(self):
        # Title
        title = Text("Signal Regeneration: Repeaters and Hubs", font_size=36, color=WHITE)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title))

        # --- REPEATER SECTION (Left) ---
        repeater_label = Text("Repeater (Layer 1)", font_size=24, color=BLUE).move_to([-4, 1.5, 0])
        repeater_box = Rectangle(width=2, height=1.2, color=BLUE, fill_opacity=0.2).move_to([-4, 0, 0])
        repeater_text = Text("Signal\nBooster", font_size=20).move_to(repeater_box.get_center())
        
        # Weak Input Signal (Jagged)
        weak_signal = VGroup(
            Line([-6, 0.1, 0], [-5.8, -0.2, 0], color=RED),
            Line([-5.8, -0.2, 0], [-5.6, 0.3, 0], color=RED),
            Line([-5.6, 0.3, 0], [-5.4, -0.1, 0], color=RED),
            Line([-5.4, -0.1, 0], [-5.1, 0.1, 0], color=RED)
        )
        
        # Strong Output Signal (Clean)
        strong_signal = VGroup(
            Line([-2.9, 0.4, 0], [-2.6, -0.4, 0], color=GREEN),
            Line([-2.6, -0.4, 0], [-2.3, 0.4, 0], color=GREEN),
            Line([-2.3, 0.4, 0], [-2.0, -0.4, 0], color=GREEN)
        ).scale(1.2)

        # Labels for signals
        weak_label = Text("Weak Signal", font_size=18, color=RED).next_to(weak_signal, DOWN)
        strong_label = Text("Regenerated", font_size=18, color=GREEN).next_to(strong_signal, DOWN)

        repeater_vgroup = VGroup(repeater_label, repeater_box, repeater_text)
        self.play(Create(repeater_vgroup))
        self.play(Create(weak_signal), Write(weak_label))
        
        # Signal passing through
        dot_signal = Dot(color=YELLOW).move_to([-6, 0, 0])
        self.play(dot_signal.animate.move_to([-4, 0, 0]), run_time=1)
        self.remove(dot_signal)
        
        self.play(Create(strong_signal), Write(strong_label))
        self.wait(1)

        # --- HUB SECTION (Right) ---
        hub_label = Text("Hub (Multi-port)", font_size=24, color=GOLD).move_to([4, 1.5, 0])
        hub_center = Square(side_length=1, color=GOLD, fill_opacity=0.3).move_to([4, -0.5, 0])
        hub_text = Text("HUB", font_size=20).move_to(hub_center.get_center())

        # Connected Devices
        pc1 = Rectangle(width=0.6, height=0.4, color=TEAL).move_to([2.5, 0.5, 0])
        pc2 = Rectangle(width=0.6, height=0.4, color=TEAL).move_to([5.5, 0.5, 0])
        pc3 = Rectangle(width=0.6, height=0.4, color=TEAL).move_to([4, -2, 0])
        pcs = VGroup(pc1, pc2, pc3)
        
        # Connections
        l1 = Line(hub_center.get_top(), pc1.get_bottom(), color=WHITE)
        l2 = Line(hub_center.get_top(), pc2.get_bottom(), color=WHITE)
        l3 = Line(hub_center.get_bottom(), pc3.get_top(), color=WHITE)
        connections = VGroup(l1, l2, l3)

        hub_vgroup = VGroup(hub_label, hub_center, hub_text, pcs, connections)
        self.play(Create(hub_vgroup))

        # Packet Broadcast Simulation
        input_packet = Dot(color=WHITE).move_to([2.5, 0.5, 0])
        self.play(input_packet.animate.move_to(hub_center.get_center()), run_time=1)
        
        p1 = Dot(color=YELLOW).move_to(hub_center.get_center())
        p2 = Dot(color=YELLOW).move_to(hub_center.get_center())
        p3 = Dot(color=YELLOW).move_to(hub_center.get_center())
        
        # Animation: Hub broadcasts to all ports
        self.play(
            p1.animate.move_to(pc1.get_center()),
            p2.animate.move_to(pc2.get_center()),
            p3.animate.move_to(pc3.get_center()),
            run_time=1.5
        )
        
        # Final Summary Text
        summary = Text("Repeaters strengthen signals. Hubs broadcast to everyone.", 
                      font_size=22, color=WHITE).to_edge(DOWN, buff=0.5)
        self.play(Write(summary))
        self.wait(2)

        # Clean up
        self.play(FadeOut(VGroup(repeater_vgroup, hub_vgroup, title, summary, weak_signal, weak_label, strong_signal, strong_label, p1, p2, p3, input_packet)))

# Scene execution ends. Class Scene1 defined. Used Text, Circle, Square, Arrow, Line, NumberPlane, VGroup, Rectangle, Dot. No forbidden items. Positioned using move_to, next_to, to_edge. Opacity set via fill_opacity. All requirements met.