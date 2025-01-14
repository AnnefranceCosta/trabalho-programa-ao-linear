import numpy as np
import pandas as pd

# Método das Duas Fases
# Objetivo: Resolver problemas de Programação Linear com restrições de igualdade ou >= utilizando o Método das Duas Fases

# 1. Coeficientes da função objetivo (lucro por produto ou custo)
lucro = [
    22.5, 35.0, 26.4, 35.0, 43.5, 50.0, 46.3, 56.0, 46.3, 27.0, 29.5, 31.0,
    22.5, 84.0, 53.0, 29.6, 26.7, 42.0, 48.0, 44.9, 52.5, 44.8, 39.7, 62.0,
    23.0, 28.0, 26.5, 28.0, 52.9, 40.1, 199.0, 47.8
]

# 2. Coeficientes das restrições (linhas = restrições, colunas = variáveis)
restricoes = [
    [9.1, 5.3, 9.2, 0, 0, 0, 0, 0, 0, 8.6, 9.1, 9.2, 7.0, 9.2, 9.2, 10.0, 9.9, 8.9, 10.0, 10.0, 10.0, 9.9, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 11.0, 10.0, 12.0], # Leite de vaca
    [0, 0, 0, 5.0, 5.6, 6.5, 6.5, 6.4, 1.6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], # Leite de búfala
    [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], # Forma 600g
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], # Forma 900g
    [0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], # Forma búfala
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0], # Forma coalho
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], # Forma cunha
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0], # Forma filados
    [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], # Forma frescal
    [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], # Forma mussarela
    [0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], # Forma requeijão
    [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # Forma trufado
]

# 3. Lado direito das restrições (limites)
constantes = [500000, 70000, 10000, 20000, 4000, 1700, 2500, 18000, 2000, 8000, 13500, 3000]

# Número de restrições e variáveis
n_restricoes = len(constantes)
n_variaveis = len(lucro)

# 4. Adicionar variáveis de folga para converter inequações em equações
matriz = np.zeros((n_restricoes, n_variaveis + n_restricoes))
for i, restricao in enumerate(restricoes):
    matriz[i, :n_variaveis] = restricao
    matriz[i, n_variaveis + i] = 1

# 5. Montar o quadro inicial com as restrições e constantes
quadro = np.hstack((matriz, np.array(constantes).reshape(-1, 1)))

# 6. Configurar a função objetivo auxiliar para a Fase 1
linha_objetivo_auxiliar = np.zeros(quadro.shape[1])
linha_objetivo_auxiliar[-1] = 0  # Última coluna para resultados

# 7. Configuração de títulos para as variáveis básicas e não básicas
titulos_linhas = [f"f{i+1}" for i in range(n_restricoes)]
titulos_colunas = [f"x{i+1}" for i in range(n_variaveis)] + [f"f{i+1}" for i in range(n_restricoes)] + ["b"]

# 8. Iterações do Método Simplex para Fase 1
max_iter = 50
iteracao = 0
quadro_iterativo = quadro.copy()
while iteracao < max_iter:
    # Escolher coluna pivô (menor valor negativo na linha da função objetivo)
    coluna_pivo_idx = np.argmin(quadro_iterativo[-1, :-1])
    if quadro_iterativo[-1, coluna_pivo_idx] >= 0:
        break  # Solução ótima encontrada

    # Determinar linha pivô com teste da razão
    col_pivo = quadro_iterativo[:-1, coluna_pivo_idx]
    n_restricoes_validas = len(col_pivo)
    razoes = np.array([quadro_iterativo[i, -1] / col_pivo[i] if col_pivo[i] > 0 else np.inf for i in range(n_restricoes_validas)])
    linha_pivo_idx = np.argmin(razoes)

    # Normalizar linha pivô
    elemento_pivo = quadro_iterativo[linha_pivo_idx, coluna_pivo_idx]
    quadro_iterativo[linha_pivo_idx] /= elemento_pivo

    # Ajustar demais linhas
    for i in range(quadro_iterativo.shape[0]):
        if i != linha_pivo_idx:
            fator = quadro_iterativo[i, coluna_pivo_idx]
            quadro_iterativo[i] -= fator * quadro_iterativo[linha_pivo_idx]

    # Atualizar títulos das linhas
    titulos_linhas[linha_pivo_idx] = titulos_colunas[coluna_pivo_idx]
    iteracao += 1

# 9. Preparar para a Fase 2 com a função objetivo original
linha_objetivo_original = np.zeros_like(quadro_iterativo[-1])
linha_objetivo_original[:n_variaveis] = np.array(lucro)  # Correção: manter positivo na Fase 2
quadro_iterativo[-1] = -linha_objetivo_original  # Negativo para maximização no Simplex

# Continuar iterações para a Fase 2
while iteracao < max_iter:
    coluna_pivo_idx = np.argmin(quadro_iterativo[-1, :-1])
    if quadro_iterativo[-1, coluna_pivo_idx] >= 0:
        break

    col_pivo = quadro_iterativo[:-1, coluna_pivo_idx]
    n_restricoes_validas = len(col_pivo)
    razoes = np.array([quadro_iterativo[i, -1] / col_pivo[i] if col_pivo[i] > 0 else np.inf for i in range(n_restricoes_validas)])
    linha_pivo_idx = np.argmin(razoes)

    elemento_pivo = quadro_iterativo[linha_pivo_idx, coluna_pivo_idx]
    quadro_iterativo[linha_pivo_idx] /= elemento_pivo

    for i in range(quadro_iterativo.shape[0]):
        if i != linha_pivo_idx:
            fator = quadro_iterativo[i, coluna_pivo_idx]
            quadro_iterativo[i] -= fator * quadro_iterativo[linha_pivo_idx]

    titulos_linhas[linha_pivo_idx] = titulos_colunas[coluna_pivo_idx]
    iteracao += 1

# Resultado final
df_resultado = pd.DataFrame(quadro_iterativo, columns=titulos_colunas, index=titulos_linhas)

# Mapear variáveis para nomes de produtos
nomes_produtos = {
    "x1": "Leite de vaca",
    "x2": "Leite de búfala",
    "x3": "Forma 600g",
    "x4": "Forma 900g",
    "x5": "Forma búfala",
    "x6": "Forma coalho",
    "x7": "Forma cunha",
    "x8": "Forma filados",
    "x9": "Forma frescal",
    "x10": "Forma mussarela",
    "x11": "Forma requeijão",
    "x12": "Forma trufado",
    # Adicione nomes para outras variáveis conforme necessário
}

# Extrair os valores das variáveis básicas
resultados = {}
for linha, titulo_linha in zip(quadro_iterativo[:-1, -1], titulos_linhas):
    if titulo_linha.startswith("x"):
        resultados[titulo_linha] = linha

# Exibir os resultados no formato desejado
print("Resultados finais:")
for var, valor in resultados.items():
    nome_produto = nomes_produtos.get(var, var)
    print(f"{nome_produto} - {var}: {valor:.2f}")

# Valor da função objetivo
valor_objetivo = quadro_iterativo[-1, -1]  # Correção: não inverter sinal duas vezes
print(f"Lucro máximo: {valor_objetivo:.2f}")

