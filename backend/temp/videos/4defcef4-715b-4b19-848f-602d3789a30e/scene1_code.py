from manim import *

class Scene1(Scene):
    def construct(self):
        # Title of the scene
        title = Text("Hub: Multi-Port Repeater", color=GOLD, font_size=36)
        title.to_edge(UP)

        # Central Hub representation
        hub_box = Rectangle(width=2.5, height=1.2, color=BLUE, fill_opacity=0.8)
        hub_label = Text("HUB", color=WHITE, font_size=30).move_to(hub_box.get_center())
        hub = VGroup(hub_box, hub_label).move_to(ORIGIN)

        # Peripheral PCs in Star Topology
        pc_positions = [
            UP * 2.8,
            RIGHT * 4 + UP * 1.5,
            RIGHT * 4 + DOWN * 1.5,
            LEFT * 4 + DOWN * 1.5,
            LEFT * 4 + UP * 1.5
        ]
        
        pc_group = VGroup()
        line_group = VGroup()

        for i, pos in enumerate(pc_positions):
            pc_shape = Square(side_length=0.8, color=TEAL, fill_opacity=1.0).move_to(pos)
            pc_id = Text(f"PC {i+1}", color=WHITE, font_size=20).move_to(pc_shape.get_center())
            pc = VGroup(pc_shape, pc_id)
            pc_group.add(pc)
            
            # Connection lines from the Hub to each PC
            connection = Line(hub_box.get_center(), pc_shape.get_center(), color=WHITE, stroke_width=2)
            line_group.add(connection)

        # Visualizing the scene
        self.play(Write(title))
        self.play(Create(line_group), run_time=1.5)
        self.play(Create(hub), Create(pc_group))
        self.wait(1)

        # Incoming Signal: From PC 1 to the Hub
        incoming_signal = Dot(color=YELLOW, radius=0.12).move_to(pc_group[0].get_center())
        self.play(incoming_signal.animate.move_to(hub.get_center()), run_time=1.2)
        
        # Hub "repeating" the signal (visual flash)
        self.play(hub_box.animate.set_fill(YELLOW, opacity=0.4), run_time=0.2)
        self.play(hub_box.animate.set_fill(BLUE, opacity=0.8), run_time=0.2)

        # Outgoing Signals: Hub repeats to all other PCs (Multi-port repeater action)
        outgoing_dots = VGroup()
        for i in range(1, 5):
            d = Dot(color=YELLOW, radius=0.15).move_to(hub.get_center())
            outgoing_dots.add(d)

        # Animate signal flooding to all other ports
        self.play(
            *[outgoing_dots[i-1].animate.move_to(pc_group[i].get_center()) for i in range(1, 5)],
            incoming_signal.animate.scale(0),
            run_time=2
        )

        # Explanatory caption
        explanation = Text("Signals are boosted and repeated to all ports.", font_size=24, color=WHITE)
        explanation.to_edge(DOWN, buff=0.5)
        self.play(Write(explanation))
        
        # Cleanup signals
        self.play(
            *[d.animate.scale(0) for d in outgoing_dots],
            run_time=1
        )
        
        self.wait(2)