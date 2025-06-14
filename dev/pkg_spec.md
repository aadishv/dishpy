**User runs `dishpy add add-two-numbers` to add a new package**

1. the user has previously registered `dishpy register add_two_numbers https://github.com/innovationfirst/add-two-numbers.git`
    OR `dishpy register add_two_numbers:latest ../add-two-numbers`
2. the `register` command stores the soruce code in application contents
3. the `add` command updates `dishpy.toml` with, under dependencies, `add_two_numbers = "${add_two_numbers/dishpy.toml - [package]/version}"`
4; dishpy copies in the source code

**Format of the repository**

*dishpy.toml*

```toml
[project]
name = "Add Two Numbers"
slot = 1

[package]
package_name = "add_two_nums"
version = "0.1.0"
```

*src/add_two_nums/\_\_init__.py*

```python
def add_two_numbers(a, b):
    return a + b
```


**TODOS**

 - [ ] Allow register command to work with GH repositories
 - [x] Add install command
 - [x] Add registry-list command
 - [ ] Handle dependency trees?! (for now restrict packages to not have any dependencies)
 - [ ] Update docs
