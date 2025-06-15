import sys
import os
import ast
from collections import defaultdict
import argparse
import hashlib
from rich.console import Console

# --- AST Transformer for Prefixing ---


class Prefixer(ast.NodeTransformer):
    """
    A transformer that renames top-level symbols and their references
    based on a global rename map.
    """

    def __init__(self, file_path, rename_map, symbol_origins, declared_symbols):
        self.rename_map = rename_map
        self.origins = symbol_origins.get(file_path, {})
        self.declarations = declared_symbols.get(file_path, set())
        self.file_renames = self.rename_map.get(file_path, {})

    def visit_Name(self, node):
        # A name is a variable, function call, etc.
        original_name = node.id

        # Check if this name is a declaration in the current file
        if original_name in self.declarations and isinstance(
            node.ctx, (ast.Store, ast.Del)
        ):
            node.id = self.file_renames.get(original_name, original_name)
        # Check if this is a reference to a symbol from the current file
        elif original_name in self.declarations:
            node.id = self.file_renames.get(original_name, original_name)
        # Check if this is a reference to an imported symbol
        elif original_name in self.origins:
            origin_file, original_import_name = self.origins[original_name]
            new_name = self.rename_map.get(origin_file, {}).get(original_import_name)
            if new_name:
                node.id = new_name

        return node

    def visit_FunctionDef(self, node):
        original_name = node.name
        if original_name in self.declarations:
            node.name = self.file_renames.get(original_name, original_name)
        # Visit argument annotations
        for arg in node.args.args + node.args.kwonlyargs:
            self.visit(arg)
        if node.args.vararg:
            self.visit(node.args.vararg)
        if node.args.kwarg:
            self.visit(node.args.kwarg)
        # Visit return annotation
        if node.returns:
            node.returns = self._visit_annotation(node.returns)
        self.generic_visit(node)
        return node

    def visit_AsyncFunctionDef(self, node):
        # Same logic as FunctionDef
        return self.visit_FunctionDef(node)

    def visit_arg(self, node):
        if node.annotation:
            node.annotation = self._visit_annotation(node.annotation)
        return node

    def visit_AnnAssign(self, node):
        if node.annotation:
            node.annotation = self._visit_annotation(node.annotation)
        self.generic_visit(node)
        return node

    def _visit_annotation(self, annotation):
        # Recursively visit annotation nodes and rename if needed
        if isinstance(annotation, ast.Name):
            original_name = annotation.id
            # Check if this is a declaration in the current file
            if original_name in self.declarations:
                annotation.id = self.file_renames.get(original_name, original_name)
            # Check if this is a reference to an imported symbol
            elif original_name in self.origins:
                origin_file, original_import_name = self.origins[original_name]
                new_name = self.rename_map.get(origin_file, {}).get(
                    original_import_name
                )
                if new_name:
                    annotation.id = new_name
        elif isinstance(annotation, ast.Attribute):
            # Handle qualified names (e.g., module.C)
            annotation.value = self._visit_annotation(annotation.value)
        elif isinstance(annotation, ast.Subscript):
            annotation.value = self._visit_annotation(annotation.value)
            annotation.slice = self._visit_annotation(annotation.slice)
        elif isinstance(annotation, ast.Tuple):
            annotation.elts = [self._visit_annotation(e) for e in annotation.elts]
        return annotation

    def visit_ClassDef(self, node):
        original_name = node.name
        if original_name in self.declarations:
            node.name = self.file_renames.get(original_name, original_name)
        self.generic_visit(node)
        return node

    def visit_Global(self, node):
        # Rename variables in global statements to match the prefixed versions
        for i, name in enumerate(node.names):
            # Check if this is a declaration in the current file
            if name in self.declarations:
                node.names[i] = self.file_renames.get(name, name)
            # Check if this is a reference to an imported symbol
            elif name in self.origins:
                origin_file, original_import_name = self.origins[name]
                new_name = self.rename_map.get(origin_file, {}).get(
                    original_import_name
                )
                if new_name:
                    node.names[i] = new_name
        return node

    # Remove local imports, as they are now resolved by prefixing
    def visit_Import(self, node):
        return None

    def visit_ImportFrom(self, node):
        return None


# --- Helper Functions ---


def _get_local_module_map(project_dir, verbose=False):
    if verbose:
        print(f"DEBUG: Scanning project directory: {project_dir}")
    local_modules = {}
    for root, _, files in os.walk(project_dir):
        if "site-packages" in root or "venv" in root or ".venv" in root:
            continue
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.abspath(os.path.join(root, file))
                module_name = os.path.relpath(file_path, project_dir).replace(
                    os.sep, "."
                )
                if file == "__init__.py":
                    module_name = module_name[:-12]
                else:
                    module_name = module_name[:-3]
                local_modules[module_name] = file_path
                if verbose:
                    print(f"DEBUG: Found module '{module_name}' at {file_path}")
    if verbose:
        print(f"DEBUG: Total local modules found: {len(local_modules)}")
    return local_modules


def _topological_sort(dep_graph):
    # (Same as previous version)
    sorted_list = []
    visited = set()
    all_nodes = set(dep_graph.keys())
    for deps in dep_graph.values():
        all_nodes.update(deps)

    def visit(node):
        if node in visited:
            return
        visited.add(node)
        for dep in dep_graph.get(node, []):
            visit(dep)
        sorted_list.append(node)

    for node in sorted(list(all_nodes)):
        if node not in visited:
            visit(node)

    return sorted_list


def _analyze_project(entry_file, local_module_map, verbose=False):
    """
    Analyzes the entire project to understand dependencies, declarations,
    and the origins of imported symbols.
    """
    if verbose:
        print(f"DEBUG: Starting project analysis from entry file: {entry_file}")
    dep_graph = defaultdict(list)
    declared_symbols = defaultdict(set)
    symbol_origins = defaultdict(dict)
    external_imports = set()

    files_to_scan = [os.path.abspath(entry_file)]
    scanned_files = set()

    while files_to_scan:
        current_file = files_to_scan.pop(0)
        if current_file in scanned_files:
            continue
        scanned_files.add(current_file)
        if verbose:
            print(f"DEBUG: Scanning file: {current_file}")

        try:
            with open(current_file, "r", encoding="utf-8") as f:
                content = f.read()
            tree = ast.parse(content, filename=current_file)
        except Exception as e:
            if verbose:
                print(f"DEBUG: Error reading/parsing {current_file}: {e}")
            continue

        # Find declared symbols
        for node in tree.body:
            if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
                declared_symbols[current_file].add(node.name)
                if verbose:
                    print(
                        f"DEBUG: Found {type(node).__name__} '{node.name}' in {os.path.basename(current_file)}"
                    )
            elif isinstance(node, (ast.Assign, ast.AnnAssign, ast.AugAssign)):
                targets = (
                    node.targets if isinstance(node, ast.Assign) else [node.target]
                )
                for target in targets:
                    if isinstance(target, ast.Name):
                        declared_symbols[current_file].add(target.id)
                        if verbose:
                            print(
                                f"DEBUG: Found variable '{target.id}' in {os.path.basename(current_file)}"
                            )

        # Find imports
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if verbose:
                        print(
                            f"DEBUG: Found import '{alias.name}' in {os.path.basename(current_file)}"
                        )
                    # Special treatment: always treat 'vex' as external
                    if alias.name == "vex" or alias.name.startswith("vex."):
                        if verbose:
                            print(
                                f"DEBUG: '{alias.name}' is treated as external (vex library)"
                            )
                        external_imports.add(ast.unparse(node))
                    elif alias.name in local_module_map:
                        dep_path = local_module_map[alias.name]
                        dep_graph[current_file].append(dep_path)
                        if verbose:
                            print(
                                f"DEBUG: '{alias.name}' is local module at {dep_path}"
                            )
                        if dep_path not in scanned_files:
                            files_to_scan.append(dep_path)
                    else:
                        if verbose:
                            print(f"DEBUG: '{alias.name}' is external import")
                        external_imports.add(ast.unparse(node))
            elif isinstance(node, ast.ImportFrom):
                module_name = node.module
                if verbose:
                    print(
                        f"DEBUG: Found 'from {module_name} import ...' in {os.path.basename(current_file)}"
                    )

                # Special treatment: always treat 'vex' as external
                if module_name == "vex" or (
                    module_name and module_name.startswith("vex.")
                ):
                    if verbose:
                        print(
                            f"DEBUG: '{module_name}' is treated as external (vex library)"
                        )
                    external_imports.add(ast.unparse(node))
                else:
                    is_local = module_name in local_module_map
                    origin_file = None

                    if is_local:
                        origin_file = local_module_map[module_name]
                    else:
                        # Check if this is a package-relative import
                        # Find the package context of the current file
                        current_rel_path = os.path.relpath(
                            current_file, os.path.dirname(os.path.dirname(current_file))
                        )
                        current_module_path = current_rel_path.replace(
                            os.sep, "."
                        ).replace(".py", "")
                        if current_module_path.endswith(".__init__"):
                            current_module_path = current_module_path[
                                :-9
                            ]  # Remove .__init__

                        # Try to resolve as package-relative import
                        package_parts = current_module_path.split(".")
                        for i in range(len(package_parts)):
                            package_prefix = ".".join(
                                package_parts[: len(package_parts) - i]
                            )
                            if package_prefix:
                                potential_module = f"{package_prefix}.{module_name}"
                                if potential_module in local_module_map:
                                    origin_file = local_module_map[potential_module]
                                    is_local = True
                                    if verbose:
                                        print(
                                            f"DEBUG: Resolved '{module_name}' as package-relative import to '{potential_module}'"
                                        )
                                    break

                    if is_local and origin_file:
                        dep_graph[current_file].append(origin_file)
                        if verbose:
                            print(
                                f"DEBUG: '{module_name}' is local module at {origin_file}"
                            )
                        if origin_file not in scanned_files:
                            files_to_scan.append(origin_file)
                        # Track that 'name' in this file comes from 'origin_file'
                        for alias in node.names:
                            if alias.name == "*":
                                # For wildcard imports, we need to import ALL symbols from the origin file
                                # We'll handle this after we've analyzed all files
                                if verbose:
                                    print(
                                        f"DEBUG: Wildcard import from {os.path.basename(origin_file)} in {os.path.basename(current_file)}"
                                    )
                                # Mark this for later processing
                                symbol_origins[current_file]["__WILDCARD_FROM__"] = (
                                    origin_file
                                )
                            else:
                                symbol_origins[current_file][alias.name] = (
                                    origin_file,
                                    alias.name,
                                )
                                if verbose:
                                    print(
                                        f"DEBUG: Symbol '{alias.name}' in {os.path.basename(current_file)} comes from {os.path.basename(origin_file)}"
                                    )
                    elif node.level == 0:  # Absolute import not in project is external
                        if verbose:
                            print(f"DEBUG: '{module_name}' is external import")
                        external_imports.add(ast.unparse(node))

    # Handle wildcard imports - add all symbols from imported modules
    for file_path, origins in symbol_origins.items():
        if "__WILDCARD_FROM__" in origins:
            wildcard_source = origins["__WILDCARD_FROM__"]
            del origins["__WILDCARD_FROM__"]  # Remove the marker
            # Import all declared symbols from the wildcard source
            for symbol in declared_symbols.get(wildcard_source, set()):
                origins[symbol] = (wildcard_source, symbol)
                if verbose:
                    print(
                        f"DEBUG: Wildcard import: '{symbol}' in {os.path.basename(file_path)} comes from {os.path.basename(wildcard_source)}"
                    )

    if verbose:
        print(f"DEBUG: Analysis complete. Scanned {len(scanned_files)} files")
        print(f"DEBUG: Dependency graph: {dict(dep_graph)}")
    return dep_graph, declared_symbols, symbol_origins, external_imports, scanned_files


# --- MAIN SCRIPT FUNCTION ---


def combine_project(main_file, output_file, verbose=False):
    """
    Combines and prefixes a multi-file Python project into a single script.
    """
    console = Console()
    try:
        ast.unparse
    except AttributeError:
        print("Error: This script requires Python 3.9 or newer.")
        return

    main_file_abs = os.path.abspath(main_file)
    project_dir = os.path.dirname(main_file_abs)

    # 1. First Pass: Analyze the entire project
    if verbose:
        print(f"DEBUG: Starting analysis of project at {project_dir}")
    local_module_map = _get_local_module_map(project_dir, verbose)
    analysis_result = _analyze_project(main_file_abs, local_module_map, verbose)
    dep_graph, declared_symbols, symbol_origins, external_imports, scanned_files = (
        analysis_result
    )

    # 2. Create a global rename map for all symbols (except main file)
    if verbose:
        print("DEBUG: Creating global rename map...")
    global_rename_map = defaultdict(dict)
    for file_path, symbols in declared_symbols.items():
        relative_path = os.path.relpath(file_path, project_dir)
        # Skip prefixing for the main entry file
        if file_path == main_file_abs:
            if verbose:
                print(f"DEBUG: Skipping prefix for main file {relative_path}")
            continue
        # Create a unique hash-based prefix to avoid any collision
        file_hash = hashlib.md5(relative_path.encode()).hexdigest()[:8]
        prefix = f"mod_{file_hash}"
        if verbose:
            print(f"DEBUG: File {relative_path} will use prefix '{prefix}'")
        for symbol in symbols:
            new_name = f"{prefix}_{symbol}"
            global_rename_map[file_path][symbol] = new_name
            if verbose:
                print(f"DEBUG: {symbol} -> {new_name}")

    # 3. Topologically sort files
    if verbose:
        print("DEBUG: Sorting files topologically...")
    sorted_files = _topological_sort(dep_graph)
    # Ensure main file is always included, even if it's not in the dependency graph (e.g., single-file project)
    if main_file_abs not in sorted_files:
        sorted_files.append(main_file_abs)
    if verbose:
        print(
            f"DEBUG: File processing order: {[os.path.basename(f) for f in sorted_files]}"
        )

    # 4. Second Pass: Transform each file and combine
    if verbose:
        print("DEBUG: Starting file transformation...")
    all_code_blocks = []

    for file_path in sorted_files:
        if file_path not in scanned_files:
            if verbose:
                print(f"DEBUG: Skipping {file_path} (not in scanned files)")
            continue

        if verbose:
            print(f"DEBUG: Processing {os.path.basename(file_path)}")
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        tree = ast.parse(content, filename=file_path)

        # This transformer does all the work: prefixes symbols and removes local imports
        transformer = Prefixer(
            file_path, global_rename_map, symbol_origins, declared_symbols
        )
        transformed_tree = transformer.visit(tree)
        ast.fix_missing_locations(transformed_tree)

        modified_code = ast.unparse(transformed_tree).strip()

        relative_path = os.path.relpath(file_path, project_dir)
        header = f"\n# {'-' * 20} Content from: {relative_path} {'-' * 20}\n"
        all_code_blocks.append(header + modified_code)
        if verbose:
            print(f"DEBUG: Transformed {relative_path}")

    # 5. Write the final script
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(
            "# This script was generated by combining and prefixing multiple files.\n\n"
        )
        f.write("# --- Combined External Imports ---\n")
        if external_imports:
            for imp in sorted(list(external_imports)):
                f.write(f"{imp}\n")
        else:
            f.write("# No external imports found.\n")

        f.write("".join(all_code_blocks))
        f.write("\n\n# --- End of combined script ---")

    console.print(
        f"✅ [green]Project combined successfully into[/green] [bold cyan]{output_file}[/bold cyan]"
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Combine and prefix a multi-file Python project into a single script."
    )
    parser.add_argument(
        "input_file", help="Path to the main Python file of the project"
    )
    parser.add_argument("output_file", help="Path for the combined output script")

    args = parser.parse_args()

    main_project_file = args.input_file
    combined_script_file = args.output_file

    # Create dummy files for testing if main.py doesn't exist
    if not os.path.exists("main.py") and main_project_file == "main.py":
        print("Creating dummy 'main.py' and 'test.py' for demonstration.")
        with open("main.py", "w") as f:
            f.write(
                "from test import a, b\nimport os\n\nANSWER = 42\n\nprint(f'The result is {a(b()) + ANSWER}')\n"
            )
        with open("test.py", "w") as f:
            f.write("def a(x):\n    return x + 1\n\ndef b():\n    return 2\n")

    if not os.path.exists(main_project_file):
        print(f"Error: The main file '{main_project_file}' was not found.")
    else:
        verbose = "--verbose" in sys.argv
        if verbose:
            print(f"DEBUG: Starting combination of project from {main_project_file}")
        combine_project(main_project_file, combined_script_file, verbose)
