from manim import *

class Scene1(Scene):
    def construct(self):
        title = Text("Defining Deadlock", color=WHITE).to_edge(UP)
        
        p1 = Circle(radius=0.6, color=BLUE, fill_opacity=0.4).move_to([-3, 1.5, 0])
        r2 = Rectangle(height=1.0, width=1.0, color=GOLD, fill_opacity=0.4).move_to([3, 1.5, 0])
        p2 = Circle(radius=0.6, color=BLUE, fill_opacity=0.4).move_to([3, -1.5, 0])
        r1 = Rectangle(height=1.0, width=1.0, color=GOLD, fill_opacity=0.4).move_to([-3, -1.5, 0])
        
        p1_lab = Text("P1").move_to(p1)
        r2_lab = Text("R2").move_to(r2)
        p2_lab = Text("P2").move_to(p2)
        r1_lab = Text("R1").move_to(r1)
        
        nodes = VGroup(p1, r2, p2, r1, p1_lab, r2_lab, p2_lab, r1_lab)
        
        a_hold1 = Arrow(r1.get_top(), p1.get_bottom(), color=GREEN, buff=0.1)
        a_req1 = Arrow(p1.get_right(), r2.get_left(), color=RED, buff=0.1)
        a_hold2 = Arrow(r2.get_bottom(), p2.get_top(), color=GREEN, buff=0.1)
        a_req2 = Arrow(p2.get_left(), r1.get_right(), color=RED, buff=0.1)
        
        hold_txt = Text("Held", font_size=20, color=GREEN).next_to(a_hold1, LEFT)
        wait_txt = Text("Request", font_size=20, color=RED).next_to(a_req1, UP)
        
        self.play(Write(title))
        self.wait(1)
        
        self.play(Create(nodes))
        self.wait(1)
        
        self.play(
            Create(a_hold1), 
            Create(a_req1), 
            Create(a_hold2), 
            Create(a_req2),
            Write(hold_txt),
            Write(wait_txt),
            run_time=3
        )
        
        conclusion = Text("Mutual waiting loop creates a deadlock.", font_size=28, color=YELLOW).to_edge(DOWN)
        self.play(Write(conclusion))
        
        self.wait(3)