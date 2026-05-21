from manim import *

class Scene3(Scene):
    def construct(self):
        # 1. Setup Network Topology
        hub = Square(side_length=1.2, color=BLUE, fill_opacity=0.5)
        hub_label = Text("Hub", font_size=24, color=WHITE).move_to(hub.get_center())
        hub_group = VGroup(hub, hub_label)

        # Positions for computers
        pos_list = [[-3, 2, 0], [3, 2, 0], [-3, -2, 0], [3, -2, 0]]
        pcs = VGroup()
        lines = VGroup()
        
        for pos in pos_list:
            pc = Rectangle(width=1.0, height=0.7, color=TEAL, fill_opacity=0.8).move_to(pos)
            pc_text = Text("PC", font_size=20).move_to(pc.get_center())
            pcs.add(VGroup(pc, pc_text))
            lines.add(Line(pc.get_center(), hub.get_center(), color=WHITE, stroke_width=2))

        # 2. Collision Domain Bubble
        domain_circle = Circle(radius=4.0, color=GOLD, stroke_width=4).set_fill(GOLD, fill_opacity=0.1)
        domain_label = Text("Single Collision Domain", font_size=32, color=GOLD).to_edge(UP)

        # 3. Create initial scene
        self.play(Create(hub_group), Create(pcs), Create(lines))
        self.wait(1)
        self.play(Create(domain_circle), Write(domain_label))
        self.wait(1)

        # 4. Data Transmission
        dot1 = Dot(color=RED).move_to(pcs[0].get_center())
        dot2 = Dot(color=YELLOW).move_to(pcs[1].get_center())
        
        # Labels for shared bandwidth concept
        bandwidth_text = Text("Shared Bandwidth", font_size=24, color=WHITE).next_to(hub, DOWN, buff=0.5)
        self.play(Write(bandwidth_text))

        # 5. Collision Animation
        self.play(
            dot1.animate.move_to(hub.get_center()),
            dot2.animate.move_to(hub.get_center()),
            run_time=2,
            rate_func=linear
        )

        # Starburst effect using lines and a circle
        collision_circle = Circle(radius=0.5, color=RED, fill_opacity=0.8).move_to(hub.get_center())
        collision_text = Text("COLLISION!", font_size=36, color=RED, weight=BOLD).next_to(hub, UP)
        
        star_lines = VGroup()
        for i in range(8):
            angle = i * 45 * DEGREES
            l = Line(ORIGIN, [0.8 * np.cos(angle), 0.8 * np.sin(angle), 0], color=YELLOW, stroke_width=5).move_to(hub.get_center())
            l.shift([0.5 * np.cos(angle), 0.5 * np.sin(angle), 0])
            star_lines.add(l)

        self.play(
            Create(collision_circle),
            Create(star_lines),
            Write(collision_text),
            dot1.animate.set_fill(fill_opacity=0),
            dot2.animate.set_fill(fill_opacity=0)
        )
        self.wait(2)

        # 6. Cleanup / Conclusion
        self.play(
            FadeOut(collision_circle),
            FadeOut(star_lines),
            FadeOut(collision_text),
            FadeOut(dot1),
            FadeOut(dot2)
        )
        self.wait(1)