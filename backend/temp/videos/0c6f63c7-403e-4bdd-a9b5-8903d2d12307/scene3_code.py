from manim import *

class Scene3(Scene):
    def construct(self):
        # 1. Setup Hub and Network Stations
        hub_box = Square(side_length=1.5, color=BLUE, fill_opacity=0.2)
        hub_text = Text("HUB", font_size=24, color=WHITE).move_to(hub_box.get_center())
        hub = VGroup(hub_box, hub_text)

        comp_a = Square(side_length=0.8, color=GREEN, fill_opacity=0.3).to_edge(LEFT, buff=2)
        label_a = Text("Station A", font_size=18).next_to(comp_a, UP)
        comp_b = Square(side_length=0.8, color=GREEN, fill_opacity=0.3).to_edge(RIGHT, buff=2)
        label_b = Text("Station B", font_size=18).next_to(comp_b, UP)

        line_a = Line(comp_a.get_right(), hub_box.get_left(), color=WHITE)
        line_b = Line(comp_b.get_left(), hub_box.get_right(), color=WHITE)
        
        topology = VGroup(hub, comp_a, label_a, comp_b, label_b, line_a, line_b)
        
        # 2. Setup Bandwidth Bar
        bw_outline = Rectangle(width=6, height=0.4, color=WHITE).to_edge(DOWN, buff=1)
        bw_fill = Rectangle(width=6, height=0.4, color=GOLD, fill_opacity=0.8).move_to(bw_outline.get_center())
        bw_label = Text("Total Shared Bandwidth", font_size=20).next_to(bw_outline, UP)
        bandwidth_ui = VGroup(bw_outline, bw_fill, bw_label)

        # Initial display
        self.play(Create(topology))
        self.play(Create(bandwidth_ui))
        self.wait(1)

        # 3. Collision Animation
        packet_a = Dot(color=TEAL).move_to(comp_a.get_center())
        packet_b = Dot(color=TEAL).move_to(comp_b.get_center())

        # Packets move toward the hub simultaneously
        self.play(
            packet_a.animate.move_to(hub_box.get_center()),
            packet_b.animate.move_to(hub_box.get_center()),
            run_time=2,
            rate_func=linear
        )

        # Starburst effect for collision
        star_lines = VGroup(*[
            Line(ORIGIN, 0.6 * UP).rotate(angle).move_to(hub_box.get_center())
            for angle in [0, 45*DEGREES, 90*DEGREES, 135*DEGREES, 180*DEGREES, 225*DEGREES, 270*DEGREES, 315*DEGREES]
        ]).set_color(RED)
        collision_text = Text("COLLISION!", font_size=32, color=RED).next_to(hub_box, UP)
        collision_flash = Circle(radius=0.5, color=YELLOW, fill_opacity=0.5).move_to(hub_box.get_center())

        self.play(
            Create(star_lines),
            Write(collision_text),
            FadeIn(collision_flash),
            packet_a.animate.scale(0),
            packet_b.animate.scale(0)
        )
        self.wait(1)
        self.play(FadeOut(star_lines), FadeOut(collision_flash))

        # 4. Bandwidth Sharing Animation
        # Explain shared bandwidth by dividing the bar
        divider = Line(bw_fill.get_top(), bw_fill.get_bottom(), color=WHITE)
        label_shared_a = Text("A's Segment", font_size=14).move_to(bw_fill.get_left() + RIGHT * 1.5)
        label_shared_b = Text("B's Segment", font_size=14).move_to(bw_fill.get_right() + LEFT * 1.5)

        self.play(
            bw_fill.animate.set_color(TEAL),
            Write(divider),
            Write(label_shared_a),
            Write(label_shared_b),
            run_time=2
        )
        
        # Final Text
        final_info = Text("Single Collision Domain", font_size=24, color=GOLD).to_edge(UP, buff=0.5)
        self.play(Write(final_info))
        self.wait(2)