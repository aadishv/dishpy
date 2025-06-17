#!/usr/bin/env python3

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'dishpy', 'resources'))

from vex_gui_test import *
import time

def test_basic_drawing():
    """Test basic drawing functions with web interface"""
    brain = Brain()
    
    print("Starting VEX Brain Screen Web Interface...")
    print("A browser window should open automatically.")
    print("If not, navigate to http://localhost:8080")
    
    # Clear screen to black
    brain.screen.clear_screen()
    time.sleep(1)
    
    # Set pen color to red and draw some pixels
    brain.screen.set_pen_color(Color.RED)
    brain.screen.draw_pixel(10, 10)
    brain.screen.draw_pixel(11, 10)
    brain.screen.draw_pixel(12, 10)
    time.sleep(1)
    
    # Draw a line
    brain.screen.set_pen_color(Color.GREEN)
    brain.screen.draw_line(20, 20, 100, 80)
    time.sleep(1)
    
    # Draw a rectangle
    brain.screen.set_pen_color(Color.BLUE)
    brain.screen.set_fill_color(Color.YELLOW)
    brain.screen.draw_rectangle(150, 50, 80, 60)
    time.sleep(1)
    
    # Draw a circle
    brain.screen.set_pen_color(Color.PURPLE)
    brain.screen.set_fill_color(Color.CYAN)
    brain.screen.draw_circle(350, 120, 40)
    time.sleep(1)
    
    # Print some text
    brain.screen.set_pen_color(Color.WHITE)
    brain.screen.set_cursor(1, 1)
    brain.screen.print("Hello VEX Brain Web!")
    time.sleep(1)
    
    brain.screen.print_at("Touch me!", x=200, y=200)
    
    return brain

def test_touch_events():
    """Test touch event handling"""
    brain = Brain()
    brain.screen.clear_screen()
    
    brain.screen.set_pen_color(Color.WHITE)
    brain.screen.print_at("Touch the screen to draw circles!", x=100, y=100)
    
    def on_touch():
        x = brain.screen.x_position()
        y = brain.screen.y_position()
        brain.screen.set_pen_color(Color.RED)
        brain.screen.draw_circle(x, y, 5)
        brain.screen.set_pen_color(Color.WHITE)
        brain.screen.print_at(f"Touch at ({x}, {y})", x=10, y=220)
        print(f"Touch detected at ({x}, {y})")
    
    def on_release():
        brain.screen.set_pen_color(Color.GREEN)
        brain.screen.print_at("Released!", x=300, y=220)
        print("Touch released")
    
    brain.screen.pressed(on_touch)
    brain.screen.released(on_release)
    
    return brain

def test_animation():
    """Test animation with web interface"""
    brain = Brain()
    brain.screen.clear_screen()
    
    brain.screen.set_pen_color(Color.WHITE)
    brain.screen.print_at("Animated Circle Demo", x=150, y=20)
    
    # Animate a bouncing circle
    x, y = 50, 50
    dx, dy = 3, 2
    radius = 20
    
    for i in range(100):
        # Clear previous circle area (simple approach)
        brain.screen.set_fill_color(Color.BLACK)
        brain.screen.draw_rectangle(0, 40, brain.screen.width, brain.screen.height - 40)
        
        # Update position
        x += dx
        y += dy
        
        # Bounce off walls
        if x + radius >= brain.screen.width or x - radius <= 0:
            dx = -dx
        if y + radius >= brain.screen.height or y - radius <= 40:
            dy = -dy
            
        # Draw circle
        brain.screen.set_fill_color(Color.CYAN)
        brain.screen.set_pen_color(Color.BLUE)
        brain.screen.draw_circle(x, y, radius)
        
        time.sleep(0.05)
    
    return brain

def main():
    """Main test function"""
    print("VEX Brain Web Screen Test")
    print("Choose a test:")
    print("1. Basic Drawing")
    print("2. Touch Events")
    print("3. Animation")
    print("4. All Tests")
    
    try:
        choice = input("Enter choice (1-4): ").strip()
    except KeyboardInterrupt:
        print("\nExiting...")
        return
    
    if choice == "1":
        brain = test_basic_drawing()
        print("Basic drawing test running. Check your browser!")
    elif choice == "2":
        brain = test_touch_events()
        print("Touch test running. Touch the screen in your browser!")
    elif choice == "3":
        brain = test_animation()
        print("Animation test running. Check your browser!")
    elif choice == "4":
        print("Running all tests sequentially...")
        
        print("1. Basic Drawing Test")
        brain = test_basic_drawing()
        input("Press Enter to continue to next test...")
        
        print("2. Touch Events Test")
        brain = test_touch_events()
        input("Press Enter to continue to next test...")
        
        print("3. Animation Test")
        brain = test_animation()
        print("All tests complete!")
    else:
        print("Invalid choice")
        return
    
    # Keep the program running
    print("\nServer running. Press Ctrl+C to exit.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nExiting...")

if __name__ == "__main__":
    main()