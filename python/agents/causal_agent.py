"""
Causal Agent for 4D Nexus
Handles causal graph building and fact integration
"""
import json
import hashlib
from datetime import datetime
from typing import Dict, List, Any, Optional
import networkx as nx
import numpy as np

class CausalAgent:
    """
    4D Causal Agent for building spatio-temporal graphs
    """

    def __init__(self):
        self.graph = nx.DiGraph()
        self.facts_db = {}
        self.coherence_threshold = 0.9
        self.initialize_base_facts()

    def initialize_base_facts(self):
        """Initialize base facts for the ecosystem"""
        base_facts = {
            "mom_birthday": {
                "content": "Mom's birthday is 2025-05-27",
                "timestamp": "2025-09-20T00:00:00Z",
                "type": "temporal",
                "attribution": "@AxiomHive"
            },
            "gym_move": {
                "content": "Planning gym membership and SF move",
                "timestamp": "2025-09-20T00:00:00Z",
                "type": "action",
                "attribution": "@devdollzai"
            },
            "ecosystem_bind": {
                "content": "AxiomHive ecosystem binding active",
                "timestamp": "2025-09-20T00:00:00Z",
                "type": "system",
                "attribution": "@AxiomHive @devdollzai"
            }
        }

        for fact_id, fact_data in base_facts.items():
            self.facts_db[fact_id] = fact_data
            self.graph.add_node(fact_id, **fact_data)

    def build_4d_graph(self, command: str) -> Dict[str, Any]:
        """
        Build 4D causal graph from command
        Returns coherence score and graph structure
        """
        # Create command hash for node ID
        command_hash = hashlib.sha256(command.encode()).hexdigest()[:8]

        # Add command as node
        self.graph.add_node(command_hash,
                          content=command,
                          timestamp=datetime.now().isoformat(),
                          type="command",
                          attribution="@AxiomHive @devdollzai")

        # Build causal relationships
        self._build_causal_relationships(command_hash, command)

        # Calculate coherence
        coherence = self._calculate_coherence()

        return {
            "coherence": coherence,
            "nodes": len(self.graph.nodes),
            "edges": len(self.graph.edges),
            "graph_hash": hashlib.sha256(str(self.graph.nodes).encode()).hexdigest()[:8]
        }

    def _build_causal_relationships(self, node_id: str, command: str):
        """Build causal relationships between nodes"""
        # Simple rule-based causal inference
        command_lower = command.lower()

        # Temporal relationships
        if "birthday" in command_lower or "date" in command_lower:
            self.graph.add_edge(node_id, "mom_birthday", relation="temporal")

        # Action relationships
        if any(word in command_lower for word in ["move", "plan", "gym", "sf"]):
            self.graph.add_edge(node_id, "gym_move", relation="action")

        # System relationships
        if any(word in command_lower for word in ["ecosystem", "bind", "nexus", "4d"]):
            self.graph.add_edge(node_id, "ecosystem_bind", relation="system")

    def _calculate_coherence(self) -> float:
        """Calculate graph coherence score"""
        if len(self.graph.nodes) < 2:
            return 0.0

        # Simple coherence based on connectivity
        connectivity = len(self.graph.edges) / len(self.graph.nodes)
        return min(connectivity, 1.0)

    def integrate_facts(self, facts_data: Dict[str, Any]) -> List[str]:
        """Integrate new facts into the graph"""
        processed_facts = []

        for fact_id, fact_content in facts_data.items():
            if isinstance(fact_content, str):
                fact_content = {"content": fact_content}

            # Add to facts database
            self.facts_db[fact_id] = {
                **fact_content,
                "timestamp": datetime.now().isoformat(),
                "attribution": fact_content.get("attribution", "@AxiomHive @devdollzai")
            }

            # Add to graph
            self.graph.add_node(fact_id, **self.facts_db[fact_id])
            processed_facts.append(fact_id)

        return processed_facts

    def get_facts(self) -> Dict[str, Any]:
        """Get current facts state"""
        return {
            "facts": self.facts_db,
            "graph_stats": {
                "nodes": len(self.graph.nodes),
                "edges": len(self.graph.edges),
                "coherence": self._calculate_coherence()
            },
            "timestamp": datetime.now().isoformat()
        }

    def get_causal_chain(self, start_node: str, max_depth: int = 3) -> List[Dict]:
        """Get causal chain from a starting node"""
        if start_node not in self.graph:
            return []

        chains = []
        for path in nx.single_source_shortest_path(self.graph, start_node, cutoff=max_depth):
            chain = []
            for node in path:
                chain.append({
                    "node": node,
                    "data": dict(self.graph.nodes[node]),
                    "relations": [self.graph.edges[edge] for edge in self.graph.edges(node)]
                })
            chains.append(chain)

        return chains
