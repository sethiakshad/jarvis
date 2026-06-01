from manim import *

class Scene3(Scene):
    def construct(self):
        # Title and Concept
        title = Text("Resource Allocation Graph (RAG)", color=WHITE).scale(0.8)
        title.to_edge(UP)
        
        explanation = Text("Detecting Deadlock via Cycles", color=YELLOW).scale(0.5)
        explanation.next_to(title, DOWN)

        # Create Processes (Circles)
        p1 = Circle(radius=0.6, color=BLUE, fill_opacity=0.4).move_to(LEFT * 3 + UP * 1.5)
        p2 = Circle(radius=0.6, color=BLUE, fill_opacity=0.4).move_to(RIGHT * 3 + DOWN * 1.5)
        
        p1_label = Text("P1", color=WHITE).move_to(p1.get_center())
        p2_label = Text("P2", color=WHITE).move_to(p2.get_center())
        
        # Create Resources (Rectangles)
        r1 = Rectangle(width=1.2, height=1.2, color=GOLD, fill_opacity=0.4).move_to(RIGHT * 3 + UP * 1.5)
        r2 = Rectangle(width=1.2, height=1.2, color=GOLD, fill_opacity=0.4).move_to(LEFT * 3 + DOWN * 1.5)
        
        r1_label = Text("R1", color=GOLD).next_to(r1, RIGHT)
        r2_label = Text("R2", color=GOLD).next_to(r2, LEFT)
        
        # Dots representing single instances inside Resources
        dot_r1 = Dot(r1.get_center(), color=WHITE)
        dot_r2 = Dot(r2.get_center(), color=WHITE)
        
        # Create Edges (Arrows)
        # P1 requests R1
        e1 = Arrow(p1.get_right(), r1.get_left(), buff=0.1, color=WHITE)
        # R1 (dot) assigned to P2
        e2 = Arrow(dot_r1.get_center(), p2.get_top(), buff=0.1, color=WHITE)
        # P2 requests R2
        e3 = Arrow(p2.get_left(), r2.get_right(), buff=0.1, color=WHITE)
        # R2 (dot) assigned to P1
        e4 = Arrow(dot_r2.get_center(), p1.get_bottom(), buff=0.1, color=WHITE)

        # Groups for animation
        nodes = VGroup(p1, p2, r1, r2, p1_label, p2_label, r1_label, r2_label, dot_r1, dot_r2)
        edges = VGroup(e1, e2, e3, e4)

        # Animation Sequence
        self.play(Write(title))
        self.play(FadeIn(explanation))
        self.play(Create(nodes))
        self.wait(1)
        
        self.play(Create(edges), run_time=3)
        self.wait(1)

        # Highlight the cycle
        cycle_highlight = VGroup(e1, e2, e3, e4)
        self.play(cycle_highlight.animate.set_color(RED), run_time=1.5)
        
        deadlock_text = Text("DEADLOCK DETECTED", color=RED).scale(1.2)
        deadlock_text.move_to(ORIGIN)
        
        # Draw a box around the deadlock text
        box = Rectangle(width=6, height=1.5, color=RED).move_to(deadlock_text)
        deadlock_group = VGroup(deadlock_text, box)

        self.play(FadeIn(deadlock_group))
        self.play(deadlock_group.animate.scale(1.1), run_time=0.5)
        self.play(deadlock_group.animate.scale(1/1.1), run_time=0.5)
        
        self.wait(2)

        # Cleanup for concise ending
        self.play(FadeOut(nodes), FadeOut(edges), FadeOut(deadlock_group), FadeOut(title), FadeOut(explanation))