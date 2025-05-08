# graph_generator.py
# Gerador de grafo de operadores a partir da árvore de Álgebra Relacional otimizada

import networkx as nx
import matplotlib.pyplot as plt
import tempfile
import os
import textwrap
from relational_algebra import Relation, Selection, Projection, Join
import matplotlib.patches as mpatches

# Função auxiliar que cria um rótulo resumido para o nó com base em seu tipo
def resumir_label(node, max_len=30):
    if isinstance(node, Projection):
        # Mostra π com até duas colunas e reticências, se necessário
        cols = ', '.join(node.attributes[:2])
        if len(node.attributes) > 2:
            cols += ', ...'
        return f"π{{{cols}}}"
    elif isinstance(node, Selection):
        # Mostra σ com condição truncada se for muito longa
        cond = str(node.condition)
        if len(cond) > 15:
            cond = cond[:12] + '...'
        return f"σ{{{cond}}}"
    elif isinstance(node, Join):
        # Mostra ⋈ com condição truncada
        cond = str(node.condition)
        if len(cond) > 15:
            cond = cond[:12] + '...'
        return f"⋈{{{cond}}}"
    elif isinstance(node, Relation):
        # Mostra o nome da tabela
        return node.name
    else:
        # Default: mostra uma versão encurtada do `str(node)`
        label = str(node)
        return label[:max_len] + ("..." if len(label) > max_len else "")

# Gera o grafo a partir da árvore de operadores
def generate_operator_graph(original_tree, optimized_tree):
    """
    Cria graficamente uma visualização da árvore de operadores de álgebra relacional.

    Args:
        original_tree: raiz da árvore original (não utilizado)
        optimized_tree: raiz da árvore otimizada

    Returns:
        Tuple contendo:
            - DiGraph do NetworkX com nós e arestas dos operadores
            - Caminho para a imagem PNG gerada da árvore
    """
    tree = optimized_tree
    G = nx.DiGraph().to_directed()  # Cria grafo orientado

    # 1) Função recursiva que constrói os nós e arestas a partir da árvore
    def _add(node, is_root=False):
        nid = id(node)  # ID único baseado no endereço do objeto
        if nid in G:
            return  # Evita duplicação
        # Gera o rótulo com quebra de linha
        short_label = resumir_label(node, 30)
        wrapped_label = textwrap.fill(short_label, width=18)
        # Determina o tipo e a forma visual do nó
        if isinstance(node, Relation):
            ntype, shape = 'table', 'o'
        elif isinstance(node, Join):
            ntype, shape = 'join', 'D'
        elif isinstance(node, Selection):
            ntype, shape = 'where', 's'
        elif isinstance(node, Projection):
            ntype, shape = 'select', 's'
        else:
            ntype, shape = 'other', 'o'
        # Destaca visualmente o nó raiz
        border = 4.0 if is_root else 1.0
        G.add_node(nid, label=wrapped_label, type=ntype, shape=shape, tooltip=str(node), border=border)
        # Conecta o nó aos seus filhos, se existirem
        if hasattr(node, 'child'):
            _add(node.child)
            G.add_edge(nid, id(node.child))
        if hasattr(node, 'left') and hasattr(node, 'right'):
            for sub in (node.left, node.right):
                _add(sub)
                G.add_edge(nid, id(sub))

    _add(tree, is_root=True)  # Inicia a construção a partir da raiz

    # 2) Define a posição dos nós no grafo (poderia ser substituído por layout do Graphviz)
    pos = nx.spring_layout(G, seed=0)

    # 3) Desenha o grafo usando Matplotlib
    fig, ax = plt.subplots(figsize=(18, 12))  # Aumenta o tamanho para visualização clara
    color_map = {
        'table':  'lightcoral',
        'join':   'lightgoldenrodyellow',
        'where':  'lightgreen',
        'select': 'lightskyblue',
        'other':  'lightgrey'
    }

    # Desenha os nós agrupando por forma e tipo
    for shape in set(nx.get_node_attributes(G, 'shape').values()):
        nodes = [n for n, d in G.nodes(data=True) if d['shape'] == shape]
        colors = [color_map[G.nodes[n]['type']] for n in nodes]
        borders = [G.nodes[n].get('border', 1.0) for n in nodes]
        nx.draw_networkx_nodes(
            G,
            pos,
            nodelist=nodes,
            node_color=colors,
            node_shape=shape,
            node_size=2200,
            linewidths=borders,
            edgecolors='black',
            alpha=0.95,
            ax=ax
        )

    # Desenha as conexões entre os operadores
    nx.draw_networkx_edges(G, pos, arrows=True, arrowsize=18, width=1.6, ax=ax)

    # Adiciona rótulos aos nós
    labels = nx.get_node_attributes(G, 'label')
    nx.draw_networkx_labels(
        G,
        pos,
        labels=labels,
        font_size=12,
        font_family='sans-serif',
        font_weight='bold',
        ax=ax
    )

    # Adiciona legenda para as cores dos tipos de operadores
    legend_handles = [
        mpatches.Patch(color=color, label=ntype.capitalize())
        for ntype, color in color_map.items()
    ]
    ax.legend(
        handles=legend_handles,
        title='Tipos de Operadores',
        loc='lower left',
        fontsize=8,
        title_fontsize=9,
        frameon=True
    )

    # Remove eixos visuais e aplica layout automático
    ax.set_axis_off()
    plt.tight_layout()

    # 4) Salva a imagem do grafo em um diretório temporário
    tmp = tempfile.gettempdir()
    path = os.path.join(tmp, 'operator_graph.png')
    fig.savefig(path, dpi=200, bbox_inches='tight')  # Salva com alta resolução
    plt.close(fig)  # Fecha figura para liberar memória

    return G, path  # Retorna o grafo e o caminho da imagem
