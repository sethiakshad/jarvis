from manim import *

class Scene1(Scene):
    def construct(self):
        # 1. Create the central HUB
        hub_box = Rectangle(width=2.5, height=1.3, color=BLUE, fill_opacity=0.6)
        hub_label = Text("HUB", font_size=32, color=WHITE).move_to(hub_box.get_center())
        hub = VGroup(hub_box, hub_label)

        # 2. Define PC positions in a star formation
        pc_positions = [
            UP * 2.8,
            UR * 3.5,
            DR * 3.5,
            DL * 3.5,
            UL * 3.5
        ]

        pcs = VGroup()
        lines = VGroup()
        signals = VGroup()

        for i in range(5):
            # Create PC representation
            pc_square = Square(side_length=0.8, color=TEAL, fill_opacity=0.4)
            pc_square.move_to(pc_positions[i])
            pc_text = Text(f"PC {i+1}", font_size=20).move_to(pc_square.get_center())
            pc_node = VGroup(pc_square, pc_text)
            pcs.add(pc_node)

            # Create Connection lines
            connection = Line(hub_box.get_center(), pc_square.get_center(), color=WHITE)
            lines.add(connection)

            # Create signal dots for regeneration visual
            sig_dot = Dot(color=YELLOW).move_to(hub_box.get_center())
            signals.add(sig_dot)

        # 3. Animation Sequence
        # Initial hub display
        self.play(Create(hub))
        self.wait(1)

        # Build Star Topology
        self.play(Create(lines))
        self.play(Create(pcs))
        self.wait(1)

        # 4. Demonstrate Multi-Port Repeater (Signal Regeneration)
        # Visual effect: Hub glows and sends signals to all ports
        regeneration_pulse = Circle(radius=0.2, color=YELLOW, fill_opacity=0.3).move_to(hub_box.get_center())
        
        # Displaying concept label
        concept_label = Text("Multi-Port Repeater: Signal Regeneration", font_size=26, color=GOLD).to_edge(DOWN)
        
        self.play(Create(regeneration_pulse))
        self.play(
            regeneration_pulse.animate.scale(20).set_fill(fill_opacity=0),
            *[signals[i].animate.move_to(pc_positions[i]) for i in range(5)],
            Write(concept_label),
            run_time=2.5
        )

        # 5. Finalize the star topology visual
        topology_label = Text("Star Topology", font_size=28, color=WHITE).to_edge(UP)
        self.play(Write(topology_label))
        self.wait(2)