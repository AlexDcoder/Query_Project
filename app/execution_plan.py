# execution_plan.py
# Gerador de plano de execução baseado na árvore de Álgebra Relacional

# Importa as classes de operadores relacionais utilizados na árvore
from relational_algebra import Relation, Selection, Join, Projection

def get_execution_steps(original_tree, optimized_tree, graph, optimization_steps=None):
    """
    Gera o plano de execução da árvore de Álgebra Relacional otimizada.

    Args:
        original_tree: nó raiz da árvore de RA original (não usado)
        optimized_tree: nó raiz da árvore de RA otimizada
        graph: grafo de operadores (NetworkX DiGraph)
        optimization_steps (list, opcional): lista de strings com passos de otimização

    Returns:
        list: lista de passos executáveis (descrições textuais do plano)
    """
    steps = []

    # 1) Adiciona os passos de otimização, se fornecidos
    if optimization_steps:
        steps.extend(optimization_steps)

    # 2) Função recursiva auxiliar para percorrer a árvore em pós-ordem
    def _walk(node):
        if isinstance(node, Relation):
            # Caso base: nó é uma relação (tabela)
            steps.append(f"Acesso à tabela base: {node.name}")
        elif isinstance(node, Selection):
            # Primeiro processa o filho (subárvore) da seleção
            _walk(node.child)
            # Depois adiciona o passo de filtragem
            steps.append(f"Filtro: {node.condition}")
        elif isinstance(node, Join):
            # Processa primeiro o lado esquerdo da junção
            _walk(node.left)
            # Depois o lado direito
            _walk(node.right)
            # Adiciona o passo da junção
            steps.append(f"Junção: {node.condition}")
        elif isinstance(node, Projection):
            # Processa o filho da projeção
            _walk(node.child)
            # Adiciona o passo da projeção com os atributos selecionados
            attrs = ", ".join(node.attributes)
            steps.append(f"Projeção: {attrs}")
        else:
            # Se o tipo de nó não é reconhecido, ignora (poderia logar ou lançar exceção)
            pass

    # Inicia o percurso da árvore a partir da raiz otimizada
    _walk(optimized_tree)

    # Retorna a lista com os passos de execução montados
    return steps
