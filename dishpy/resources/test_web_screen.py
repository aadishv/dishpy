#!/usr/bin/env python3

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'dishpy', 'resources'))

from vex_gui_test import *


class AutonProgram:
    def __init__(self, name, function, alliance_color="NONE"):
        self.name = name
        self.function = function
        self.alliance_color = alliance_color

class AutonSelector:
    def __init__(self, brain, auton_list):
        self.brain = brain
        self.screen = brain.screen
        self.auton_list = auton_list
        self.selected_index = 0
        self.current_page = 0
        self.autons_per_page = 4
        self.running = True

        # Screen dimensions and layout
        self.screen_width = 480
        self.screen_height = 240
        self.button_height = 40
        self.button_margin = 10

        # Colors
        self.bg_color = 0x000000  # Black
        self.button_color = 0x333333  # Dark gray
        self.selected_color = 0x0066CC  # Blue
        self.text_color = 0xFFFFFF  # White

        # Setup event handlers
        self.screen.pressed(self._on_screen_pressed)

    def _on_screen_pressed(self):
        """Handle screen touch events"""
        x = self.screen.x_position()
        y = self.screen.y_position()

        # Check if touch is on navigation buttons
        if y >= 200:  # Bottom navigation area
            if x < 120:  # Previous button
                self._previous_page()
            elif x >= 360:  # Next button
                self._next_page()
            elif 160 <= x <= 320:  # Select button
                self._confirm_selection()
        else:
            # Check if touch is on auton buttons
            button_index = (y - 40) // (self.button_height + 5)
            if 0 <= button_index < self.autons_per_page:
                global_index = self.current_page * self.autons_per_page + button_index
                if global_index < len(self.auton_list):
                    self.selected_index = global_index
                    self._draw_screen()

    def _previous_page(self):
        """Navigate to previous page"""
        if self.current_page > 0:
            self.current_page -= 1
            # Adjust selected index to first item on new page
            self.selected_index = self.current_page * self.autons_per_page
            self._draw_screen()

    def _next_page(self):
        """Navigate to next page"""
        max_page = (len(self.auton_list) - 1) // self.autons_per_page
        if self.current_page < max_page:
            self.current_page += 1
            # Adjust selected index to first item on new page
            self.selected_index = self.current_page * self.autons_per_page
            self._draw_screen()

    def _confirm_selection(self):
        """Confirm the selected auton and exit selector"""
        self.running = False

    def _draw_screen(self):
        """Draw the selector interface"""
        # Clear screen
        self.screen.clear_screen(self.bg_color)

        # Draw title
        self.screen.set_pen_color(self.text_color)
        self.screen.print_at("Autonomous Selector", x=10, y=10)

        # Calculate which autons to show on current page
        start_index = self.current_page * self.autons_per_page
        end_index = min(start_index + self.autons_per_page, len(self.auton_list))

        # Draw auton buttons
        for i in range(start_index, end_index):
            y_pos = 40 + (i - start_index) * (self.button_height + 5)

            # Choose button color based on selection
            if i == self.selected_index:
                button_bg = self.selected_color
            else:
                button_bg = self.button_color

            # Draw button background
            self.screen.set_fill_color(button_bg)
            self.screen.set_pen_color(button_bg)
            self.screen.draw_rectangle(10, y_pos, 460, self.button_height)

            # Draw button text
            self.screen.set_pen_color(self.text_color)
            auton_name = self.auton_list[i].name
            alliance = self.auton_list[i].alliance_color

            # Add color indicator for alliance
            if alliance == "RED":
                prefix = "[R] "
            elif alliance == "BLUE":
                prefix = "[B] "
            else:
                prefix = "[S] "  # Skills

            display_text = f"{prefix}{auton_name}"
            self.screen.print_at(display_text, x=15, y=y_pos + 15)

        # Draw navigation buttons
        self.screen.set_fill_color(self.button_color)
        self.screen.set_pen_color(self.button_color)

        # Previous button
        if self.current_page > 0:
            self.screen.draw_rectangle(10, 200, 100, 30)
            self.screen.set_pen_color(self.text_color)
            self.screen.print_at("< Prev", x=15, y=210)

        # Select button
        self.screen.set_pen_color(self.selected_color)
        self.screen.set_fill_color(self.selected_color)
        self.screen.draw_rectangle(160, 200, 160, 30)
        self.screen.set_pen_color(self.text_color)
        self.screen.print_at("SELECT", x=220, y=210)

        # Next button
        max_page = (len(self.auton_list) - 1) // self.autons_per_page
        if self.current_page < max_page:
            self.screen.set_pen_color(self.button_color)
            self.screen.set_fill_color(self.button_color)
            self.screen.draw_rectangle(370, 200, 100, 30)
            self.screen.set_pen_color(self.text_color)
            self.screen.print_at("Next >", x=375, y=210)

        # Draw page indicator
        page_text = f"Page {self.current_page + 1}/{max_page + 1}"
        self.screen.print_at(page_text, x=200, y=175)

    def run(self):
        """Run the selector and return the selected auton"""
        self._draw_screen()

        # Main loop - wait for selection
        while self.running:
            # Simple delay to prevent excessive CPU usage
            # In real VEX implementation, you'd use proper timing
            pass

        return self.auton_list[int(self.selected_index)]

# Example usage:
def red_safe_auton():
    print("Running Red Safe Auton")

def blue_rush_auton():
    print("Running Blue Rush Auton")

def skills_auton():
    print("Running Skills Auton")

# Create auton list
autons = [
    AutonProgram("Safe Red", red_safe_auton, "RED"),
    AutonProgram("Rush Red", red_safe_auton, "RED"),
    AutonProgram("Safe Blue", blue_rush_auton, "BLUE"),
    AutonProgram("Rush Blue", blue_rush_auton, "BLUE"),
    AutonProgram("Skills", skills_auton, "NONE"),
]

# Initialize and run selector
brain = Brain()
selector = AutonSelector(brain, autons)
selected_auton = selector.run()

# Execute selected auton
selected_auton.function()
