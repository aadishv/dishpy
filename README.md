# DishPy

![DishPy logo](https://raw.githubusercontent.com/aadishv/dishpy/refs/heads/main/logo.png)

**[GitHub](https://github.com/aadishv/dishpy) ・ [Docs](https://aadishv.github.io/dishpy) ・ [PyPI](https://pypi.org/project/dishpy/)**

A Python development tool for VEX Competition robotics that combines multi-file Python projects into single scripts and uploads them to VEX V5 brains.

**Looking for tutorials? See [here](https://aadishv.github.io/dishpy/Tutorial/1_installation/)**

## Roadmap

**Feature parity w/ VEX VSC extension**

 - [x] Bindings to vexcom
 - [x] Project initialization CLI
 - [x] Better documentation for using vexcom's common functions
 - [x] VEXcom wrappers for ease-of-use
 - [x] templates

**Core premise**

 - [x] Script amalgamation through AST parsing
 - [x] Library creation functionality
 - [x] Library installation functionality
 - [x] Really good docs!

**Future-leaning**

 - [ ] Simulation API
 - [ ] Import from VScode

## Why/when should I use DishPy over X?

* PROS/VEXcode text -> you don't like C++
* vexide -> you don't like Rust
* VEXcode blocks -> you're a grown up /j
* VEXcode Python -> you want multifile support, an editor other than VEXcode/VSCode, libraries, and a CLI

Note that, unlike PROS & vexide, DishPy is not a *from-scratch* rewrite that does scheduling and everything (as an eight grader I am physically unable to make such a thing). Instead, it uses the exact same Python VM as VEXcode and the VScode extension and uploads code in the exact same way and binds to the same SDK -- the only difference is that the DX of DishPy is wayyy better.

## Should you use DishPy?

Yes! If you are currently using Python in VEXcode or VSCode, it is **zero cost** to switch; your current code will Just Work™.


To be clear, DishPy is still in active development and is not fully finished -- there will definitely be some sharp corners. I cannot confirm I will be available to debug or maintain this at all times, so keep that in mind. If you want to be safe when using this in competition, make sure to read the amalgamated files before running the programs to make sure nothing was lost in translation.

## Features

- **Project Management**: Initialize new VEX robotics projects with a structured template
- **Code Amalgamation**: Combine multi-file Python projects into single scripts with intelligent symbol prefixing
- **VEX Integration**: Built-in VEX library support and seamless upload to V5 brains
- **Cross-Platform**: Works on Linux (x64, ARM32, ARM64), macOS, and Windows

## Platform Support

DishPy includes pre-compiled vexcom binaries for:

- Linux x64
- Linux ARM32 (Raspberry Pi)
- Linux ARM64 (Raspberry Pi 4+)
- macOS
- Windows 32-bit

## Requirements

- Python 3.12+ with uv (see [1. Installation](https://aadishv.github.io/dishpy/Tutorial/1_installation/))
- VEX V5 Brain with USB connection

## Contributing

Contributions are welcome for:

* Literally anything

If you want to help improve DishPy, feel free to

1. Contribute and file a PR. The entire repository is open-source (that's probably how you are reading this :P)
2. Fork it! This is MIT licensed so you can do whatever you want
3. Play with it, report errors, and ping me in VTOW about them.

## License

This project is licensed under the MIT License.

## Changelog

**v1.2.1**

* Reverted to our initial amalgamator implementation -- the library we used for the rewrite was way simpler but failed on some larger repos. The old (vibe-coded) solution was janky but it works, so oh well.
* Fix minor typos in README.

**v1.2**

* New `dishpy mut` command: builds the project, uploads it to the V5 brain, then opens a terminal session.
* Improved build pipeline to have faster and simpler builds.
* Uploads now shows progress and timer.
* DishPy will now automatically scaffold missing project files if a requested project is nonexistent and falls back to an empty template when appropriate.

**v1.1**

* We have an actual logo(!!!). It is... wait for it... a pie... on a dish 🤯
* We now support templates! These templates are the exact same as those available in VEXcode and VSCode
* Added a `dishpy terminal` command
* Added docs for terminal, as well as a dedicated section on advanced uses of DishPy.
* Lightning bugfixes
  * Fixed `dishpy vexcom args` not correctly passing through `args`
  * Fixed bug in `time.sleep` call in Python stubs

**v1.0.1**

* Added `requests` as a dependency to avoid installation not working.

**v1.0**

* This marks an important milestone for DishPy. All of the core features of DishPy (read: most of the codebase) is fully stable. I won't need to make any more changes to add major new features.
* There is still a lot to do to get to feature parity with VEXcode, but all of the core premise has now been fulfilled. I'll slowly add all of that soon.
* Package management API is now fully stabilized, with helpful tutorials as well (plus some design changes to docs to look better). Registry commands are now under the `dishpy package` namespace.
* Added separate `build` and `upload` commands by popular request.
* We are now on PyPI! Previously on test.pypi which required some manual setup by users.

**v0.5**

* v0.5 ships with (*an experimental version of*) package management! It uses a PROS-like approach with decentralized packages maintaining their own metadata and users fetching that into a local registry. It is, however, much more limited than PROS. I would **not** recommend using it until it stabilizes (at which point I will also write a tutorial for it).
* Overhauled our [docs](https://aadishv.github.io/dishpy) to match the styling for the rest of my website, a.k.a. very minimal.
* Fixed some small bugs in the amalgamator and create CLI.

**v0.4**

* This is a **ground-up** rewrite of the entire DishPy CLI to now be significantly smaller and simpler. (It isn't vibe-coded anymore!)
* There are now slightly less debug messages which will hopefully be less annoying.
* We have removed `dishpy init` in favor of the more commonly used `dishpy create`.
* All of these changes go a long way towards having ✨libraries✨ in the near future!

**v0.3**

* Added a breaking bug that affected all users on v0.2.2. In the port to vexcom downloading, I accidentally deleted the vex.py resource. This will not affect creating or uploading projects, but will throw an error with running `dishpy init` or `dishpy create`. Fixed by adding back the file.
* Made docs look more modern! Plus, updated the home page with all of the new tidbits we have here.

**v0.2.2**

* Created a changelog!
* Instead of bundling the VEXcom executable with the repository, we now extract it from the VSCode extension. This better accomodates VEX licensing, although it does slightly worsen the UX as the CLI takes a few minutes to install on first VEXcom call.
* Vastly improved [documentation](https://aadishv.github.io/dishpy)! Hopefully I'll start writing topical tutorials as well soon.


## Credits

* Lewis | vexide (reverse-engineering vexcom calls)
* andrew | 781X (digging thru extension code w/ me)
* Aadish | 3151A (me)
* Chroma | 3332A | 3151A (inspiration)
* Gemini 2.5 Pro (LLM -- first run)
* Claude 4 Sonnet (LLM -- agentic tasks)
