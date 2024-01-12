"""
Primeiro Projeto de FP

Nome: Francisco Monteiro Pául de Sousa Uva
Nº IST: 106340
Curso: LEIC-T
Contacto: francisco.uva@tecnico.ulisboa.pt
Data: 26 / 10 / 2022
"""

def limpa_texto(texto):
    """Remove os carateres brancos de um texto

    Argumentos:
        texto (str): texto "não limpo"

    Retorna:
        str: texto limpo
    """
    
    texto = " ".join(texto.split())
    
    return texto


def corta_texto(texto, largura):
    """Corta o texto para a primeira parte do texto ter o tamanho da largura
    da linha ou menor, mas com o máximo de palavras possíveis

    Argumentos:
        texto (str): texto não cortado
        largura (int): tamanho da linha

    Retorna:
        tuple: tuplo de 2 cadeias de caráteres, em que a primeira é o texto com
        a largura pretendida e a segunda o resto do texto de entrada
    """
    
    if largura < len(texto): # verifica se tem que cortar
        
        # se o carater de indice 'largura' for um espaco corta aí o texto
        if texto[largura - 1] == " " or texto[largura] == " ": 
            a, b = texto[:largura], texto[largura:]
        
        else:
            # vai procurar um espaco de indice 'i' para cortar
            for i in reversed(range(1, largura)): 
                
                if texto[i] == " ":
                    a, b = texto[:i+1], texto[i+1:]
                    break
    else:
        return (texto.strip(), '')
   
    return a.rstrip(), b.lstrip()


def espacos_fim(texto, espacos):
    """Adiciona espaços no fim de uma linha até chegar ao tamanho pretendido

    Argumentos:
        texto (str): texto sem os espaços a adiconar espaços no fim
        espacos (int): numero de espaços a adiconar no fim do texto

    Retorna:
        str: texto com espaços adicionados no fim
    """
    
    for j in range(espacos): 
            texto += " "
    
    return texto


def insere_espacos(texto, largura):
    """Insere uniformemente espaços entre as palavras necessários, até um texto
    ter o tamanho pretendido

    Argumentos:
        texto (str): texto limpo sem os espaços a adiconar entre as palavras
        largura (int): tamanho pretendido do texto

    Retorna:
        str: texto com o tamanho pretendido
    """
    
    # numero de espacos que vão estar presentes
    espacos = largura - len(texto.replace(" ", "")) 
    texto = texto.split()
    
    if len(texto) >= 2:
        
        # resto do número de espaços a adicionar
        resto_espacos = espacos % (len(texto) - 1) 
        # numero mínimo de espaços entre palavras
        espacos //= (len(texto) - 1) 
        
        # insere o número igual de espaços entre palavras
        for j in range(1, 2 * len(texto) - 1, 2): 
            texto.insert(j, espacos * " ")
        
        # insere o número de espaços restantes uniformemente
        for j in range(1, 3 * resto_espacos, 3): 
            texto.insert(j, " ")
    
    else:

        espacos_fim(texto, espacos)
    
    return "".join(texto)



def justifica_texto(texto, largura):
    """Verifica os argumentos de entrada e a partir de um texto com caráteres
    brancos, "limpa" o texto e corta o texto em várias linhas para adicionar
    espaços para ficarem todas com o mesmo tamanho

    Argumentos:
        texto (str): texto "não limpo" 
        largura (int): tamanho pretendido das linhas do texto

    Retorna:
        tuple: tuplo de cadeias de caráteres todas com o mesmo tamanho
    """
    
    if not (isinstance(texto, str) and isinstance(largura, int) 
    and largura > 0 and len(texto) > 0):
        raise ValueError("justifica_texto: argumentos invalidos")
    
    texto = limpa_texto(texto)
    lst = texto.split()

    for i in range(len(lst)):
        if len(lst[i]) > largura:
            raise ValueError("justifica_texto: argumentos invalidos")

    corta, j, justificado = corta_texto(texto, largura), 1, ()

    if largura < len(texto):
        # corta o texto ate a ultima linha ter iguais ou menos carateres 
        # que a largura
        while len(corta[j]) > largura: 
            corta = corta[:j] + corta_texto(corta[j], largura) 
            j += 1
        
        for j in range(0, len(corta)-1):
            justificado += (insere_espacos(corta[j], largura),)
        
        # adiciona os espacos à última linha no fim
        justificado += (espacos_fim(corta[len(corta)-1],
                                    largura - len(corta[len(corta)-1])), )

    else:
        justificado = (espacos_fim(texto, largura - len(texto)),)
    
    return justificado

#------------------------------------------------------------------------------

def calcula_quocientes(votos, deputados):
    """A partir de um número de votos, calcula o quociente entre o número de
    votos e todos os números naturais até ao número de deputados inclusivé

    Argumentos:
        votos (dict): dicionário com a chave sendo um círculo eleitoral e o
        valor do número de votos
        
        deputados (int): número total de deputados a ser eleitos nesse círculo
        eleitoral

    Retorna:
        dict: dicionário com a chave sendo o círrculo eleitoral e os valores os
        quocientes
    """
    
    quocientes = votos.copy()
    
    for key in quocientes.keys():
        lst = []
        
        for div in range(1, deputados + 1):
            # calcula o quociente e adiciona à lista
            lst.append(quocientes[key] / div) 
        
        quocientes[key] = lst # substitui na cópia do dicionário
    
    return quocientes


def atribui_mandatos(votos, deputados):
    """Recebe os votos apurados num círculo eleitoral, calcula os quocientes
    dos votos e atribui os deputados a cada partido de acordo com o Método
    de Hondt

    Argumentos:
        votos (dict): dicionário com a chave sendo um círculo eleitoral e o 
        valor do número de votos
        
        deputados (int): número de deputados a atribuir
        
    Retorna:
        list: lista com os partidos que obtiveram cada mandato
    """
    
    def reverse_lookup(d, value):
        """Procura as chaves de um valor num dicionário, caso não exista devolve
        uma lista vazia

        Argumentos:
            d (dict): dicionário com as chaves a procurar
            value (int): valor que se pretende encontrar a chave

        Retorna:
            list: lista das chaves que têm esse valor
        """
        
        lista = [] # chaves com o valor
        keys = list(d.keys())
        
        for key in reversed(keys):
            
            for i in range(len(d[key])):
                
                if d[key][i] == value:
                    lista.append(key)
                    quocientes[key].remove(value)
                    break
        
        return lista
    
    sorted_lst, votos_sorted, j = sorted(votos), {}, 0
    for srt in sorted_lst:
        votos_sorted[srt] = votos[srt]
        j += 1
    quocientes, lst, res = calcula_quocientes(votos_sorted, deputados), [], []
    
    for key in quocientes.keys():
        lst += quocientes[key]
    
    #ordena do maior para o menor os quocientes que vão ser usados
    lst_quocientes = sorted(lst, reverse = True)[:deputados] 
        
    for quo in lst_quocientes: # cria a lista do resultado 
        res += reverse_lookup(quocientes, quo) 
    
    
    return res[:deputados]


def obtem_partidos(info):
    """Através da informação das eleições num território com vários círculos
    eleitorais, devolve uma lista com os nomes dos partidos por ordem
    alfabética

    Argumentos:
        info (dict): dicionário com as informações das eleições num território

    Retorna:
        list: lista com os nomes dos partidos por ordem alfabética
    """
    
    lst = []
    
    for key in info.keys():
        lst += (list(info[key]["votos"].keys())) # lista de partidos 
    
    lst = list(dict.fromkeys(lst)) # retira as entradas repetidas
    lst.sort()
    
    return lst


def obtem_resultado_eleicoes(info):
    """Verifica os argumentos de entrada, e calcula os resultados de uma eleição
    num território através do Método de Hondt

    Argumentos:
        info (dict): dicionário com as informações das eleições num território

    Retorna:
        list: lista de tuplos com o nome do partido, número de deputados 
        eleitos e número total de votos
    """

    if not (isinstance(info, dict) and len(info) > 0):
        raise ValueError("obtem_resultado_eleicoes: argumento invalido")
    
    mandatos, res = [], []
    
    for key in info.keys():
        if not (isinstance(info[key], dict) and isinstance(key, str)):
            raise ValueError("obtem_resultado_eleicoes: argumento invalido")
        keys = list(info[key].keys())
        if not (len(keys) == 2):
            raise ValueError("obtem_resultado_eleicoes: argumento invalido")
        if not (keys[0] == "deputados" and keys[1] == "votos"
        and isinstance(info[key]["deputados"], int) and info[key]["deputados"] > 0
        and isinstance(info[key]["votos"], dict) and len(info[key]["votos"]) > 0):
            raise ValueError("obtem_resultado_eleicoes: argumento invalido")
        
        for key2 in info[key]["votos"].keys():
            
            if not (isinstance(info[key]["votos"][key2], int)
            and isinstance(key2, str) and info[key]["votos"][key2] > 0 
            and len(key2) > 0):
                raise ValueError("obtem_resultado_eleicoes: argumento invalido")
        
        mandatos += atribui_mandatos(info[key]["votos"], info[key]["deputados"])
        
    for partido in obtem_partidos(info):
        
        count = 0
        
        for mandato in mandatos:
            
            if partido == mandato:
                count += 1 # número de deputados eleitos
        
        soma = 0
        
        for key in info.keys():
            
            if partido in list(info[key]["votos"].keys()):
                # soma dos votos de todos os circulos eleitorais
                soma += info[key]["votos"][partido] 
        
        res += [(partido, count, soma)]
    
        for i in range(0, len(res)):  
            for j in range(0, len(res)-i-1):  
                if (res[j][2] > res[j + 1][2]):  
                    temp = res[j]  
                    res[j]= res[j + 1]  
                    res[j + 1]= temp  
    
    return list(reversed(res))

#------------------------------------------------------------------------------

def produto_interno(a, x):
    """Calcula o produto interno de dois vetores

    Argumentos:
        a (tuple): vetor 1
        x (tuple): vetor 1

    Retorna:
        float: produto interno dos vetores
    """
    
    produto = 0
    
    for i in range(len(a)): 
        produto += a[i] * x[i] 
 
    return float(produto)

def verifica_convergencia(a, c, x, e):
    """Verifica a convergência de uma matriz, de acordo com uma precisão e uma
    uma estimativa dos valores das variáveis a calcular

    Argumentos:
        a (tuple): matriz quadrada
        c (tuple): constantes da matriz
        x (tuple): estimativa das soluções da matriz
        e (float): precisão

    Retorna:
        bool: se verificar a convergência retorna True, se não verificar
        retorna False
    """
    
    for i in range(len(a)):
        # verifica se o erro é maior à precisão
        if abs(produto_interno(a[i], x) - c[i]) > e: 
            return False 
         
    return True 


def altera_ordem(a, i, j): # troca a linha i com a linha j
    """Altera a ordem das linhas de uma matriz

    Argumentos:
        a (tuple): matriz
        i (int): indice da linha a trocar
        j (int): indice da linha a trocar

    Retorna:
        tuple: matriz com as linhas trocadas
    """
    
    if i < j:
        a = a[:i] + (a[j],) + a[i+1:j] + (a[i],) + a[j+1:] 
    
    else:
        a = a[:j] + (a[i],) + a[j+1:i] + (a[j],) + a[i+1:]
    
    return a


def retira_zeros_diagonal(a, c):
    """Retira os zeros da diagonal de uma matriz trocando a ordem das suas
    linhas

    Argumentos:
        a (tuple): matriz quadrada
        c (tuple): vetor das constantes

    Retorna:
        tuple: matriz sem zeros na diagonal e o vetor das constantes com as
        linhas trocadas
    """

    for i in range(len(a)):
        if a[i][i]== 0:
            
            for j in range(len(a)): 
                # verifica se contém um 0 na coluna 'i' ou na coluna 'j' da matriz
                if a[j][i] != 0 and a[i][j] != 0: 
                    a, c = altera_ordem(a, i, j), altera_ordem(c, i, j)
                    break
    
    return a, c


def eh_diagonal_dominante(a):
    """Verifica se a matriz tem a diagonal dominante

    Argumentos:
        a (tuple): matriz quadrada

    Retorna:
        bool: True se é diagonal dominante, False se não é
    """
    
    for i in range(len(a)): 
        soma = 0
        
        # calcula a soma dos valores absolutos da linha
        for j in range(len(a)): 
            soma += abs(a[i][j]) 
        
        # verifica a condição para ser diagonal dominante
        if soma - abs(a[i][i]) > abs(a[i][i]): 
            return False
    
    return True


def resolve_sistema(a, c, e):
    """Verifica os argumentos de entrada e resolve um sistema de equações
    lineares através da sua matriz pelo Método de Jacobi

    Argumentos:
        a (tuple): matriz quadrada do sistemea de equações
        c (tuple): vetor das constantes do sistema equações
        e (float): precisão pretendida para a solução do sistema de equações

    Returns:
        tuple: vetor solução do sistema de equações lineares
    """
    
    if not (isinstance(a, tuple) and isinstance(c, tuple) 
    and isinstance(e, float) and len(a) > 0):
        raise ValueError("resolve_sistema: argumentos invalidos")
    for i in a:
        if not (isinstance(i, tuple) and len(a) == len(c) and e > 0
        and len(i) ==  len(c)):
            raise ValueError("resolve_sistema: argumentos invalidos")
        for j in range(len(a)):
            if not isinstance(i[j], (float, int)):
                raise ValueError("resolve_sistema: argumentos invalidos")
        for C in c:
            if not isinstance(C, (float, int)):
                raise ValueError("resolve_sistema: argumentos invalidos")
    
    a, c = retira_zeros_diagonal(a, c)[0], retira_zeros_diagonal(a, c)[1]
    
    if not eh_diagonal_dominante(a):
        raise ValueError("resolve_sistema: matriz nao diagonal dominante")
    
    for i in range(len(a)):
        if a[i][i] == 0:
            raise ValueError("resolve_sistema: argumentos invalidos")
    
    
    x = (0,) * len(a) # vetor solução
    
    while not verifica_convergencia(a, c, x, e):
        y = x
        for i in range(len(a)): 
            # estimativa da iteração
            k = x[i] + (c[i] - produto_interno(a[i], y)) / a[i][i] 
            # coloca a estimativa 'k' no vetor 'x' (solucao ate ao momento)
            x = x[:i] + (k,) + x[i+1:] 

    return x
