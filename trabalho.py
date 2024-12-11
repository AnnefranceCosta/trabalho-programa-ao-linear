#Simplex - Forma Canônica
#Zmax / restrições <= / Não negatividade

#Entrada de dados
'''
Problema Exemplo:
Maximizar Z = 3x1 + 5x2
Sujeito a:
x1 <= 4
2x2 <= 12
2x1 + 3x2 <= 21
xi >= 0
'''
m=[[1, 0],[0, 2],[2, 3]] #matriz de coeficientes
b=[4, 12, 21]
z=[3, 5]

rest=len(b)
var=len(z)

#Inversão do sinal de Z (max)
for i in range (var):
    z[i]=-z[i]

#Montar quadro Simplex
lin=rest+1
col=var+rest+1
simplex=[]
a=[]
for i in range (col):
    a.append(0)
for i in range (lin):
    simplex.append(a[:])

#Copiar os coeficientes
for i in range (rest):
    for j in range (var):
        simplex[i][j]=m[i][j]
for i in range (rest):
    simplex[i][rest+var]=b[i]
for i in range (var):
    simplex[rest][i]=z[i]
#Matriz identidade
for i in range (rest):
    simplex[i][var+i]=1

#Títulos das linhas e das colunas
icol=[]
for i in range (var):
    icol.append('x'+str(i+1))
for i in range (var, var+rest):
    icol.append ('f'+str(i-var+1))
ilin=[]
for i in range (rest):
    ilin.append ('f'+str(i+1))

print(simplex)

#Interações
it=0
znova=simplex[rest][0:var+rest]
menor=min(znova)

while (menor<0):
    cpivo=znova.index(menor)
    pp=[]
    for i in range(rest):
        #garante que o pp não será negativo ou gere uma divisão por zero
        if (simplex[i][var+rest]<0 or simplex[i][cpivo]<=0):
            pp.append(999999)
        else:
            pp.append(simplex[i][var+rest]/simplex[i][cpivo])
    menorlinha=min(pp)
    lpivo=pp.index(menorlinha)
    np=simplex[lpivo][cpivo]

    C=[]
    #Escalonamento da linha pivo
    for i in range (col):
        simplex[lpivo][i]=simplex[lpivo][i]/np
    for i in range (lin):
        C.append(simplex[i][cpivo])
    
    #Escalonamento do restante do quadro
    for i in range (lin):
        if i != lpivo:
            for j in range (col):
                simplex[i][j]=simplex[i][j]-C[i]*simplex[lpivo][j]
    ilin[lpivo]=icol[cpivo]
    
    print(simplex)
    it+=1
    znova=simplex[rest][0:var+rest]
    menor=min(znova)
    
    #Imprimir a solução
    for i in range (len(icol)):
        cont=0
        for j in range (len(ilin)):
            if(icol[i]==ilin[j]):
                cont+=1
                pos=j
        if cont ==1:
            print (icol[i], '=', simplex[pos][col -1])
        else:
            print (icol[i], '=0')
        print ("Z =", simplex[lin-1][col-1])
        
        
