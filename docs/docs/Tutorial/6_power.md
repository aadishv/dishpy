# 6. DishPy for power users

If you are a more advanced user, DishPy offers some more powerful functionality as well.

## Interactive Python REPL

One of the most powerful features for debugging and experimentation is the ability to access the MicroPython REPL (Read-Eval-Print Loop) directly on your V5 brain.

After running your Python program and opening the terminal with `uvx dishpy terminal`, once your competition task finishes executing, you can press Enter to drop into the MicroPython REPL. The REPL is an interactive Python shell that allows you to type Python commands and see them execute immediately on the V5 brain.

Here's how to use it:

1. Run your program and open the terminal:
   ```bash
   uvx dishpy mu
   uvx dishpy terminal
   ```

2. Wait for your program to finish running (or reach a stopping point)

3. Press Enter to access the REPL prompt (`>>>`)

4. Type Python code directly and see it execute on the V5 brain:

```python
>>> print("Hello from the REPL!")
Hello from the REPL!
>>> import vex
>>> brain = vex.Brain()
>>> brain.screen.print("Direct control!")
>>> motor = vex.Motor(vex.Ports.PORT1)
>>> motor.spin(vex.FORWARD, 50, vex.PERCENT)
```

This is incredibly useful for:

- Testing motor movements without redeploying code
- Debugging sensor values in real-time
- Experimenting with new code snippets
- Learning the VEX API interactively

## Separate Build and Upload Commands

While `dishpy mu` is the most convenient command for everyday development (as it builds and uploads your project in one step), DishPy also provides separate `build` and `upload` commands for more advanced workflows.

### Build Only

To build your project without uploading it to the brain:

```bash
uvx dishpy build
```

This command:

- Combines all your project files into a single Python file
- Places the result in `.out/main.py`
- Does not attempt to connect to or upload to the V5 brain

This is useful when you want to:

- Check that your code compiles without having a brain connected
- Inspect the combined output before uploading
- Build as part of a CI/CD pipeline

### Upload Only

To upload a previously built file to the brain:

```bash
uvx dishpy upload .out/main.py
```

This command uploads the specified file directly to the V5 brain without building first.

### When to Use Separate Commands

You should generally use `dishpy mu` unless you have a specific reason to separate the build and upload steps, such as:

- Building on one machine and uploading on another
- Testing the build process in automated environments
- Uploading different versions of code without rebuilding
- Debugging build issues by examining the intermediate output

## Simulation API

One of the powerful aspects of DishPy is that all DishPy programs are regular Python programs. This means you can run your robot code directly on your computer for testing and simulation purposes:

```bash
python3 src/main.py
```

### Understanding Stubbed Functions

When you run your code on your computer, calling VEX functions (like `motor.spin()` or `brain.screen.print()`) results in nothing happening. These functions are "stubbed" in `src/vex/__init__.py`.

Stubbing means that the functions are defined but contain no actual implementation - they're empty placeholders that do nothing when called. This allows your code to run without errors even when the actual VEX hardware isn't available.

### Creating Custom Simulations

If you want to simulate specific robot behaviors, you can modify the functions in `src/vex/__init__.py` to add your own implementation. For example, you could:

- Make `motor.spin()` print debug information about motor commands
- Have `brain.screen.print()` display text in a GUI window
- Make sensors return simulated values based on your test scenarios

### Simulation Frontends

You can leverage this simulation capability to attach your own simulation frontends:

- Connect to robotics simulators like Webots or Gazebo
- Create visual representations of your robot's behavior
- Build automated testing frameworks that run your code against various scenarios
- Develop debugging tools that visualize sensor data and motor commands

This flexibility makes DishPy programs highly testable and allows for rapid development without constant hardware deployment.
