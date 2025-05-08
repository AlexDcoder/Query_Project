# graph_generator.py
# Gerador de grafo de operadores a partir da árvore de Álgebra Relacional otimizada

import networkx as nx
import matplotlib.pyplot as plt
import tempfile
import os
import textwrap
from relational_algebra import Relation, Selection, Projection, Join
import matplotlib.patches as mpatches

# Função para gerar labels mais curtos e legíveis para os nós do grafo
def resumir_label(node, max_len=30):
    # Projeção: mostra π e as primeiras colunas
    if isinstance(node, Projection):
        cols = ', '.join(node.attributes[:2])
        if len(node.attributes) > 2:
            cols += ', ...'
        return f"π{{{cols}}}"
    # Seleção: mostra σ e condição resumida
    elif isinstance(node, Selection):
        cond = str(node.condition)
        if len(cond) > 15:
            cond = cond[:12] + '...'
        return f"σ{{{cond}}}"
    # Junção: mostra ⋈ e condição resumida
    elif isinstance(node, Join):
        cond = str(node.condition)
        if len(cond) > 15:
            cond = cond[:12] + '...'
        return f"⋈{{{cond}}}"
    # Relação base (tabela): mostra apenas o nome
    elif isinstance(node, Relation):
        return node.name
    # Outros casos: corta o label se for muito longo
    else:
        label = str(node)
        return label[:max_len] + ("..." if len(label) > max_len else "")

# Função principal para gerar o grafo de operadores
def generate_operator_graph(original_tree, optimized_tree):
    """
    Gera um grafo hierárquico para a árvore de Álgebra Relacional otimizada,
    com layout bottom-up, espaçamento controlado, labels quebrados em múltiplas linhas,
    e estilos distintos por tipo de nó, incluindo legenda de cores.
    """
    tree = optimized_tree
    G = nx.DiGraph().to_directed()

    # Função recursiva para construir o grafo
    def _add(node, is_root=False):
        nid = id(node)  # ID único baseado no objeto
        if nid in G:
            return  # Evita duplicação
        # Gera label e quebra de linha para melhor visualização
        short_label = resumir_label(node, 30)
        wrapped_label = textwrap.fill(short_label, width=18)

        # Define tipo de nó e forma visual
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

        # Aumenta a borda do nó raiz para destaque
        border = 4.0 if is_root else 1.0

        # Adiciona o nó ao grafo com os atributos visuais
        G.add_node(nid, label=wrapped_label, type=ntype, shape=shape, tooltip=str(node), border=border)

        # Adiciona filhos: operadores unários ou binários
        if hasattr(node, 'child'):  # Operador unário (ex: seleção, projeção)
            _add(node.child)
            G.add_edge(nid, id(node.child))
        elif hasattr(node, 'left') and hasattr(node, 'right'):  # Operador binário (ex: junção)
            for sub in (node.left, node.right):
                _add(sub)
                G.add_edge(nid, id(sub))

    _add(tree, is_root=True)

    # Layout do grafo (spring_layout usado como fallback ao Graphviz)
    pos = nx.spring_layout(G, seed=0)

    # Criação do gráfico com Matplotlib
    fig, ax = plt.subplots(figsize=(18, 12))  # Aumenta o tamanho para melhor visualização

    # Mapeamento de tipos para cores
    color_map = {
        'table':  'lightcoral',
        'join':   'lightgoldenrodyellow',
        'where':  'lightgreen',
        'select': 'lightskyblue',
        'other':  'lightgrey'
    }

    # Desenha os nós agrupados por forma
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

    # Desenha arestas (ligações entre nós)
    nx.draw_networkx_edges(G, pos, arrows=True, arrowsize=18, width=1.6, ax=ax)

    # Desenha labels dos nós
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

    # Adiciona legenda explicando as cores dos tipos de nós
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

    # Remove os eixos para uma aparência mais limpa
    ax.set_axis_off()
    plt.tight_layout()

    # Salva a imagem em um diretório temporário
    tmp = tempfile.gettempdir()
    path = os.path.join(tmp, 'operator_graph.png')
    fig.savefig(path, dpi=200, bbox_inches='tight')
    plt.close(fig)

    # Retorna o grafo e o caminho da imagem gerada
    return G, path
