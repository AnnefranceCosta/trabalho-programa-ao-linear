# Simplex - Método na Forma Canônica
# Objetivo: Maximizar Z, com restrições <= e condições de não negatividade

# Coeficientes das restrições (linhas = restrições, colunas = variáveis x1 a x32)
matriz_restricoes = [
    [9.1, 5.3, 9.2, 0, 0, 0, 0, 0, 0, 8.6, 9.1, 9.2, 7.0, 9.2, 9.2, 10.0, 9.9, 8.9, 10.0, 10.0, 10.0, 9.9, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 11.0, 10.0, 12.0],  # Leite de vaca
    [0, 0, 0, 5.0, 5.6, 6.5, 6.5, 6.4, 1.6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # Leite de búfala
    [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # Forma 600g
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # Forma 900g
    [0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # Forma búfala
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],  # Forma coalho
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],  # Forma cunha
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0],  # Forma filados
    [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # Forma frescal
    [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # Forma mussarela
    [0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # Forma requeijão
    [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # Forma trufado
]

# Lado direito das restrições
vetor_constantes = [500000, 70000, 10000, 20000, 4000, 1700, 2500, 18000, 2000, 8000, 13500, 3000]

# Coeficientes da função objetivo (lucro por produto)
coef_funcao_objetivo = [
    22.5, 35.0, 26.4, 35.0, 43.5, 50.0, 46.3, 56.0, 46.3, 27.0, 29.5, 31.0,
    22.5, 84.0, 53.0, 29.6, 26.7, 42.0, 48.0, 44.9, 52.5, 44.8, 39.7, 62.0,
    23.0, 28.0, 26.5, 28.0, 52.9, 40.1, 199.0, 47.8
]

# Número de restrições e variáveis
num_restricoes = len(vetor_constantes)
num_variaveis = len(coef_funcao_objetivo)

# Ajuste dos coeficientes da função objetivo (multiplicação por -1 para maximização)
coef_funcao_objetivo = [-c for c in coef_funcao_objetivo]

# Número de restrições e variáveis
num_restricoes = len(vetor_constantes)
num_variaveis = len(coef_funcao_objetivo)

# Inversão do sinal dos coeficientes da função objetivo para maximização
for i in range(num_variaveis):
    coef_funcao_objetivo[i] = -coef_funcao_objetivo[i]

# Montar o quadro Simplex
num_linhas = num_restricoes + 1  # Número de linhas = restrições + linha da função objetivo
num_colunas = num_variaveis + num_restricoes + 1  # Variáveis + folgas + coluna do resultado
quadro_simplex = []  # Inicialização do quadro simplex

# Criação da matriz zerada
linha_vazia = [0] * num_colunas
for _ in range(num_linhas):
    quadro_simplex.append(linha_vazia[:])  # Clona a linha_vazia para evitar referência

# Copiar os coeficientes das restrições no quadro simplex
for i in range(num_restricoes):
    for j in range(num_variaveis):
        quadro_simplex[i][j] = matriz_restricoes[i][j]

# Copiar os valores constantes (lado direito das restrições)
for i in range(num_restricoes):
    quadro_simplex[i][num_colunas - 1] = vetor_constantes[i]

# Copiar os coeficientes da função objetivo para a última linha
for j in range(num_variaveis):
    quadro_simplex[num_restricoes][j] = coef_funcao_objetivo[j]

# Adicionar matriz identidade para as variáveis de folga
for i in range(num_restricoes):
    quadro_simplex[i][num_variaveis + i] = 1  # Variáveis de folga

# Títulos das colunas (x1, x2, f1, f2, ...)
nomes_colunas = []
for i in range(num_variaveis):
    nomes_colunas.append(f'x{i + 1}')  # Variáveis de decisão
for i in range(num_restricoes):
    nomes_colunas.append(f'f{i + 1}')  # Variáveis de folga

# Títulos das linhas (f1, f2, ..., função objetivo)
nomes_linhas = [f'f{i + 1}' for i in range(num_restricoes)]

# Iteração Simplex
print("Quadro Inicial do Simplex:")
for linha in quadro_simplex:
    print(linha)

# Variável de controle de iterações
num_iteracao = 0

# Obter os coeficientes da linha Z (linha da função objetivo)
coeficientes_z = quadro_simplex[num_restricoes][:num_variaveis + num_restricoes]
menor_coef_z = min(coeficientes_z)

# Enquanto houver coeficiente negativo em Z, continuar as iterações
while menor_coef_z < 0:
    # Escolher a coluna pivô (menor valor negativo na linha Z)
    coluna_pivo = coeficientes_z.index(menor_coef_z)

    # Determinar a linha pivô (teste da razão entre constantes e coluna pivô)
    razoes = []
    for i in range(num_restricoes):
        if quadro_simplex[i][num_colunas - 1] < 0 or quadro_simplex[i][coluna_pivo] <= 0:
            razoes.append(float('inf'))  # Evita divisão por zero ou valores negativos
        else:
            razao = quadro_simplex[i][num_colunas - 1] / quadro_simplex[i][coluna_pivo]
            razoes.append(razao)

    # Linha pivô é a menor razão válida
    menor_razao = min(razoes)
    linha_pivo = razoes.index(menor_razao)

    # Elemento pivô
    elemento_pivo = quadro_simplex[linha_pivo][coluna_pivo]

    # Normalizar a linha pivô (dividir por elemento pivô)
    for j in range(num_colunas):
        quadro_simplex[linha_pivo][j] /= elemento_pivo

    # Escalonar as outras linhas
    coeficientes_coluna_pivo = [quadro_simplex[i][coluna_pivo] for i in range(num_linhas)]
    for i in range(num_linhas):
        if i != linha_pivo:
            fator = coeficientes_coluna_pivo[i]
            for j in range(num_colunas):
                quadro_simplex[i][j] -= fator * quadro_simplex[linha_pivo][j]

    # Atualizar título da linha para a nova variável básica
    nomes_linhas[linha_pivo] = nomes_colunas[coluna_pivo]

    # Imprimir o quadro atualizado
    num_iteracao += 1
    print(f"\nQuadro Simplex - Iteração {num_iteracao}:")
    for linha in quadro_simplex:
        print(linha)

    # Atualizar os coeficientes de Z e encontrar o próximo menor valor
    coeficientes_z = quadro_simplex[num_restricoes][:num_variaveis + num_restricoes]
    menor_coef_z = min(coeficientes_z)

# Imprimir a solução final
print("\nSolução Final:")
for i, nome_variavel in enumerate(nomes_colunas):
    valor_variavel = 0
    for j, nome_linha in enumerate(nomes_linhas):
        if nome_variavel == nome_linha:
            valor_variavel = quadro_simplex[j][num_colunas - 1]
    print(f"{nome_variavel} = {valor_variavel}")

# Valor máximo da função objetivo
valor_maximo_z = quadro_simplex[num_restricoes][num_colunas - 1]
print(f"Valor máximo de Z = {valor_maximo_z}")
