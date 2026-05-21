from manim import *

class Scene3(Scene):
    def construct(self):
        # Title and Domain Highlight Setup
        title = Text("Single Collision Domain", font_size=32).to_edge(UP)
        domain_label = Text("Shared Bandwidth Logic", color=GOLD, font_size=24).to_edge(DOWN)
        
        # Hub and Network Components
        hub = Square(side_length=1.4, color=BLUE, fill_opacity=0.7)
        hub_text = Text("HUB", font_size=20).move_to(hub.get_center())
        hub_node = VGroup(hub, hub_text)

        # Computers as Rectangles
        c1 = Rectangle(height=0.6, width=1.0, color=TEAL, fill_opacity=0.5).move_to(LEFT * 4 + UP * 1.5)
        c2 = Rectangle(height=0.6, width=1.0, color=TEAL, fill_opacity=0.5).move_to(RIGHT * 4 + UP * 1.5)
        c3 = Rectangle(height=0.6, width=1.0, color=TEAL, fill_opacity=0.5).move_to(LEFT * 4 + DOWN * 1.5)
        c4 = Rectangle(height=0.6, width=1.0, color=TEAL, fill_opacity=0.5).move_to(RIGHT * 4 + DOWN * 1.5)
        
        # Connection Lines
        l1 = Line(c1.get_center(), hub.get_center(), color=WHITE)
        l2 = Line(c2.get_center(), hub.get_center(), color=WHITE)
        l3 = Line(c3.get_center(), hub.get_center(), color=WHITE)
        l4 = Line(c4.get_center(), hub.get_center(), color=WHITE)
        
        lines = VGroup(l1, l2, l3, l4)
        computers = VGroup(c1, c2, c3, c4)
        
        # Step 1: Initialize Network
        self.play(Write(title))
        self.play(Create(lines), Create(computers), Create(hub_node))
        self.wait(1)

        # Step 2: Show Collision Domain Concept
        domain_highlight = Rectangle(width=10, height=5, color=GOLD, stroke_width=3, fill_opacity=0.1)
        self.play(
            Create(domain_highlight),
            Write(domain_label),
            lines.animate.set_color(GOLD),
            computers.animate.set_color(GOLD),
            run_time=2
        )
        self.wait(1)

        # Step 3: Simultaneous Packets Leading to Collision
        p1 = Dot(c1.get_center(), color=YELLOW, radius=0.15)
        p2 = Dot(c2.get_center(), color=YELLOW, radius=0.15)
        
        # Packets move toward the central hub
        self.play(
            p1.animate.move_to(hub.get_center()),
            p2.animate.move_to(hub.get_center()),
            run_time=2,
            rate_func=linear
        )
        
        # Step 4: Collision Visual Effect
        collision_circle = Circle(radius=0.5, color=RED, fill_opacity=0.9).move_to(hub.get_center())
        collision_text = Text("COLLISION!", color=RED, font_size=36).next_to(hub, UP)
        
        self.play(
            FadeOut(p1),
            FadeOut(p2),
            Create(collision_circle),
            Write(collision_text),
            hub.animate.set_color(RED)
        )
        self.wait(2)
        
        # Step 5: Final Scene Transition
        self.play(
            FadeOut(lines),
            FadeOut(computers),
            FadeOut(hub_node),
            FadeOut(collision_circle),
            FadeOut(collision_text),
            FadeOut(domain_highlight),
            FadeOut(title),
            FadeOut(domain_label)
        )