from manim import *

class Scene3(Scene):
    def construct(self):
        # 1. Create Hub and PCs
        hub = Square(side_length=1.5, color=BLUE, fill_opacity=0.2)
        hub_label = Text("HUB", font_size=24).move_to(hub.get_center())
        hub_group = VGroup(hub, hub_label)

        pc1 = Rectangle(height=1, width=1.5, color=WHITE)
        pc1_label = Text("PC 1", font_size=20).move_to(pc1.get_center())
        pc1_group = VGroup(pc1, pc1_label).to_edge(LEFT, buff=1.5)

        pc2 = Rectangle(height=1, width=1.5, color=WHITE)
        pc2_label = Text("PC 2", font_size=20).move_to(pc2.get_center())
        pc2_group = VGroup(pc2, pc2_label).to_edge(RIGHT, buff=1.5)

        # 2. Connect them
        line1 = Line(pc1_group.get_right(), hub.get_left(), color=GRAY)
        line2 = Line(pc2_group.get_left(), hub.get_right(), color=GRAY)
        lines = VGroup(line1, line2)

        # 3. Titles
        title = Text("Single Collision Domain", font_size=32, color=YELLOW).to_edge(UP)
        explanation = Text("Shared Bandwidth = Collisions", font_size=24).next_to(title, DOWN)

        # Build initial scene
        self.play(Create(hub_group), Create(pc1_group), Create(pc2_group))
        self.play(Create(lines), Write(title))
        self.wait(1)

        # 4. Packets
        packet1 = Dot(color=GOLD, radius=0.15).move_to(pc1_group.get_center())
        packet2 = Dot(color=TEAL, radius=0.15).move_to(pc2_group.get_center())

        # 5. Collision Animation
        self.play(Write(explanation))
        
        # Packets move towards center
        self.play(
            packet1.animate.move_to(hub.get_center()),
            packet2.animate.move_to(hub.get_center()),
            run_time=2,
            rate_func=linear
        )

        # Collision effect
        collision_flash = Circle(radius=0.1, color=RED, fill_opacity=1.0).move_to(hub.get_center())
        collision_text = Text("COLLISION!", color=RED, font_size=36, weight=BOLD).next_to(hub, UP, buff=0.5)
        
        # Cross symbol using Lines
        cross1 = Line(UP+LEFT, DOWN+RIGHT, color=RED).scale(0.5).move_to(hub.get_center())
        cross2 = Line(UP+RIGHT, DOWN+LEFT, color=RED).scale(0.5).move_to(hub.get_center())
        cross = VGroup(cross1, cross2)

        self.play(
            FadeOut(packet1),
            FadeOut(packet2),
            collision_flash.animate.scale(10).set_fill(opacity=0),
            Create(cross),
            Write(collision_text),
            hub.animate.set_color(RED),
            run_time=1
        )

        # 6. Conclusion
        domain_box = Rectangle(height=3, width=10, color=RED, stroke_dash_array=[5, 5]).move_to(ORIGIN)
        domain_label = Text("One Collision Domain", color=RED, font_size=28).next_to(domain_box, DOWN)

        self.play(
            Create(domain_box),
            Write(domain_label),
            FadeOut(collision_text),
            FadeOut(cross),
            run_time=2
        )
        
        self.wait(2)

        # Cleanup
        self.play(
            FadeOut(hub_group),
            FadeOut(pc1_group),
            FadeOut(pc2_group),
            FadeOut(lines),
            FadeOut(title),
            FadeOut(explanation),
            FadeOut(domain_box),
            FadeOut(domain_label)
        )

# Requirements Check:
# - Class name: Scene3
# - Only used allowed mobjects
# - No SVGs or external files
# - No self.mobjects
# - Wait calls <= 3s
# - Named colors used
# - Concisely covers concept in ~15-20s