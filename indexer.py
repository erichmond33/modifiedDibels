import os
import ast
import json
import networkx as nx
from typing import Dict, List, Tuple

class CodeIndexer:
    """
    A simple code indexer that builds a graph-based representation of a Python codebase.
    It parses files using AST, extracts entities (files, classes, functions, variables),
    and maps relationships (imports, function calls, variable references).
    
    Dependencies: Requires networkx for graph handling. Install with `pip install networkx`.
    
    Usage:
    indexer = CodeIndexer(repo_path='/path/to/repo')
    indexer.index()
    indexer.save_graph('index_graph.json')
    """
    
    def __init__(self, repo_path: str):
        self.repo_path = os.path.abspath(repo_path)
        self.graph = nx.DiGraph()  # Directed graph for relationships
        self.file_entities: Dict[str, List[Dict]] = {}  # Store entities per file
    
    def index(self):
        """Walk through the repository and index all Python files."""
        for root, _, files in os.walk(self.repo_path):
            for file in files:
                if file.endswith('.py'):
                    file_path = os.path.join(root, file)
                    rel_path = os.path.relpath(file_path, self.repo_path)
                    self._parse_file(rel_path, file_path)
        
        self._add_relationship_edges()
    
    def _parse_file(self, rel_path: str, full_path: str):
        """Parse a single Python file using AST and extract entities."""
        with open(full_path, 'r', encoding='utf-8') as f:
            try:
                tree = ast.parse(f.read())
            except SyntaxError:
                print(f"Skipping {rel_path}: Syntax error")
                return
        
        # Add file node
        self.graph.add_node(rel_path, type='file', entities=[])
        
        entities = []
        visitor = EntityVisitor()
        visitor.visit(tree)
        
        for entity in visitor.entities:
            entity_id = f"{rel_path}:{entity['name']}"
            self.graph.add_node(entity_id, type=entity['type'], file=rel_path, line=entity['line'])
            self.graph.add_edge(rel_path, entity_id, relationship='contains')
            entities.append(entity_id)
        
        # Store for later relationship analysis
        self.file_entities[rel_path] = visitor.entities
        self.graph.nodes[rel_path]['entities'] = entities
        
        # Add import edges (preliminary)
        for imp in visitor.imports:
            self.graph.add_edge(rel_path, imp, relationship='imports')
    
    def _add_relationship_edges(self):
        """Add cross-file relationships like function calls and variable refs."""
        for rel_path, entities in self.file_entities.items():
            # Re-parse to find calls/references (could optimize by storing tree)
            with open(os.path.join(self.repo_path, rel_path), 'r', encoding='utf-8') as f:
                tree = ast.parse(f.read())
            visitor = RelationshipVisitor(self.graph, rel_path, self.file_entities)
            visitor.visit(tree)

    def save_graph(self, output_path: str):
        """Save the graph to a JSON file for later use."""
        data = nx.node_link_data(self.graph)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)
        print(f"Graph saved to {output_path}")

class EntityVisitor(ast.NodeVisitor):
    """AST visitor to extract classes, functions, variables, and imports."""
    
    def __init__(self):
        self.entities: List[Dict] = []
        self.imports: List[str] = []  # Imported modules
    
    def visit_ClassDef(self, node: ast.ClassDef):
        self.entities.append({'type': 'class', 'name': node.name, 'line': node.lineno})
        self.generic_visit(node)
    
    def visit_FunctionDef(self, node: ast.FunctionDef):
        self.entities.append({'type': 'function', 'name': node.name, 'line': node.lineno})
        self.generic_visit(node)
    
    def visit_Assign(self, node: ast.Assign):
        for target in node.targets:
            if isinstance(target, ast.Name):
                self.entities.append({'type': 'variable', 'name': target.id, 'line': node.lineno})
        self.generic_visit(node)
    
    def visit_Import(self, node: ast.Import):
        for alias in node.names:
            self.imports.append(alias.name)
        self.generic_visit(node)
    
    def visit_ImportFrom(self, node: ast.ImportFrom):
        self.imports.append(node.module)
        self.generic_visit(node)

class RelationshipVisitor(ast.NodeVisitor):
    """AST visitor to find relationships like function calls and variable references."""
    
    def __init__(self, graph: nx.DiGraph, current_file: str, file_entities: Dict[str, List[Dict]]):
        self.graph = graph
        self.current_file = current_file
        self.file_entities = file_entities
    
    def visit_Call(self, node: ast.Call):
        if isinstance(node.func, ast.Name):
            func_name = node.func.id
            self._add_call_edge(func_name, node.lineno)
        elif isinstance(node.func, ast.Attribute):
            # Handle attr calls like obj.method(), simplistic
            attr_chain = self._get_attr_chain(node.func)
            self._add_call_edge(attr_chain, node.lineno)
        self.generic_visit(node)
    
    def visit_Name(self, node: ast.Name):
        # Variable reference (not definition)
        if isinstance(node.ctx, (ast.Load, ast.Store)):
            self._add_ref_edge(node.id, node.lineno)
        self.generic_visit(node)
    
    def _get_attr_chain(self, node):
        """Get full attribute chain like 'module.submodule.func'."""
        chain = []
        while isinstance(node, ast.Attribute):
            chain.append(node.attr)
            node = node.value
        if isinstance(node, ast.Name):
            chain.append(node.id)
        return '.'.join(reversed(chain))
    
    def _add_call_edge(self, target_name: str, line: int):
        """Add edge for function/method call if target found."""
        target_id = self._find_entity_id('function', target_name)
        if target_id:
            # Find enclosing function or file for source
            source_id = self._find_enclosing_entity(line)
            self.graph.add_edge(source_id, target_id, relationship='calls')
    
    def _add_ref_edge(self, var_name: str, line: int):
        """Add edge for variable reference if target found."""
        target_id = self._find_entity_id('variable', var_name)
        if target_id:
            source_id = self._find_enclosing_entity(line)
            self.graph.add_edge(source_id, target_id, relationship='references')
    
    def _find_entity_id(self, entity_type: str, name: str) -> str:
        """Search all files for matching entity."""
        for file, entities in self.file_entities.items():
            for ent in entities:
                if ent['type'] == entity_type and ent['name'] == name:
                    return f"{file}:{name}"
        # Could expand to handle imports/aliases, but keeping simple
        return None
    
    def _find_enclosing_entity(self, line: int) -> str:
        """Find the function/class containing this line, or fallback to file."""
        entities = self.file_entities.get(self.current_file, [])
        # Find the entity with the smallest scope containing the line (simplistic: assume non-nested for now)
        for ent in entities:
            if ent['type'] in ('function', 'class') and ent['line'] <= line:
                return f"{self.current_file}:{ent['name']}"
        return self.current_file

# Example usage
if __name__ == "__main__":
    indexer = CodeIndexer('/Users/erichmond_33/github/completed/modifiedDibels')  # Replace with your repo path
    indexer.index()
    indexer.save_graph('code_index_graph.json')