"""Segundo projeto de FP
Francisco Sousa Uva - LEIC-T
ist1106340
francisco.uva@tecnico.ulisboa.pt
11/11/2022
"""

""" TAD gerador
TAD utilizado para representar a seed de um gerador de números pseudoaleatórios

Representação interna: lista

Operações básicas: 
Construtores: cria_gerador, cria_copia_gerador
Seletores: obtem_estado
Modificadores: define_estado, atualiza_estado
Reconhecedor: eh_gerador
Teste: geradores_iguais
Transformador: gerador_para_str

Funções de alto nível: gera_numero_aleatorio, gera_carater_aleatorio
"""
def cria_gerador(bits, seed):
    """Cria um gerador de números pseudoaleatório

    Argumetos:
        bits (inteiro): número de bits do gerador
        seed (inteiro): estado incial do gerador

    Retorna:
        lista: gerador na representacao interna
    """
    if not (isinstance(bits, int) and isinstance(seed, int)
    and (bits == 32 or bits == 64) and seed > 0):
        raise ValueError("cria_gerador: argumentos invalidos")
    
    if (bits == 32 and seed > 2 ** 32) or (bits == 64 and seed > 2 ** 64):
        raise ValueError("cria_gerador: argumentos invalidos")
    
    return [bits, seed]


def cria_copia_gerador(gerador):
    """Cria uma cópia de um gerador"""
    return gerador.copy()


def obtem_estado(gerador):
    """Retorna o estado atual de um gerador"""
    return gerador[1]


def define_estado(gerador, seed):
    """Define o estado para um gerador"""
    gerador[1] = seed
    return seed


def atualiza_estado(gerador):
    """Atualiza o estado de um gerador, através do algoritmo xorshift"""
    if gerador[0] == 32:
        gerador[1] ^= ( gerador[1] << 13 ) & 0xFFFFFFFF
        gerador[1] ^= ( gerador[1] >> 17 ) & 0xFFFFFFFF
        gerador[1] ^= ( gerador[1] << 5 ) & 0xFFFFFFFF
    
    elif gerador[0] == 64:
        gerador[1] ^= ( gerador[1] << 13 ) & 0xFFFFFFFFFFFFFFFF
        gerador[1] ^= ( gerador[1] >> 7 ) & 0xFFFFFFFFFFFFFFFF
        gerador[1] ^= ( gerador[1] << 17 ) & 0xFFFFFFFFFFFFFFFF
    
    define_estado(gerador, gerador[1])
    
    return gerador[1]
        
        
def eh_gerador(argumento):
    """Verifica se o argumento de entrada é um gerador"""
    if not isinstance(argumento, list):
        return False
    
    if not (isinstance(argumento[0], int) and
    isinstance(argumento[1], int) and (argumento[0] == 32 or argumento[0] == 64)
    and 0 < argumento[1] and len(argumento) == 2):
        return False
    
    if (argumento[0] == 32 and argumento[1] > 2 ** 32) \
    or (argumento[0] == 64 and argumento[1] > 2 ** 64):
        return False
    
    return True


def geradores_iguais(gerador1, gerador2):
    """Verifica se os geradores de entrada são iguais"""
    if gerador1[0] == gerador2[0] and gerador1[1] == gerador2[1]:
        return True
    
    return False


def gerador_para_str(gerador):
    """Passa um gerador para uma cadeia de carateres"""
    return "xorshift" + str(gerador[0]) + "(s=" + str(gerador[1]) + ")"


def mod(seed, numero):
    """Divisão inteira dos dois valores de entrada"""
    return seed % numero


def gera_numero_aleatorio(gerador, n):
    """Gera um número aleatório entre 1 e n"""
    return 1 + mod(atualiza_estado(gerador), n)


def gera_carater_aleatorio(gerador ,c):
    """Gera um carater aleatório entre A e c"""
    return chr(mod(atualiza_estado(gerador), ord(c) - 64) + 65)
    # mod retorna o indice do carater aleatório da cadeia entre A e c, +65 para 
    # obter o código ASCII


"""TAD coordenada
TAD que é utilizado para representar uma coordenada num campo de minas

Representação interna: tuplo

Operações básicas: 
Construtor: cria_coordenada
Seletores: obtem_coluna, obtem_linha
Reconhecedor: eh_coordenada
Teste: coordeandas_iguais
Transformador: coordeanda_para_str, str_para_coordendada

Funções de alto nível: obtem_coordenadas_vizinhas, obtem_coordenada_aleatoria
"""
def cria_coordenada(coluna , linha):
    """cria uma coordenada que está num campo de minas

    Argumentos:
        coluna (carater): coluna da coordenada de um campo de minas
        linha (inteiro): linha da coordenada de um campo de minas

    Retorna:
        tuplo: coordenada na representação interna
    """
    if not (isinstance(coluna, str) and len(coluna) == 1 
    and isinstance(linha, int) and 64 < ord(coluna) < 91 and 0 < linha < 100):
        raise ValueError("cria_coordenada: argumentos invalidos")
    
    return (coluna, linha)


def obtem_coluna(coordenada):
    """Retorna a coluna de uma coordenada"""
    return coordenada[0]


def obtem_linha(coordenada):
    """Retorna a linha de uma coordenada"""
    return coordenada[1]


def eh_coordenada(argumento):
    """Verifica se o argumento de entrada é uma coordenada"""
    
    if not (isinstance(argumento, tuple) and len(argumento) == 2
    and isinstance(obtem_coluna(argumento), str) 
    and isinstance(obtem_linha(argumento), int)
    and len(obtem_coluna(argumento)) == 1
    and 64 < ord(obtem_coluna(argumento)) < 91 
    and 0 < obtem_linha(argumento) < 100):
        return False
    
    return True


def coordenadas_iguais(coordenada1, coordenada2):
    """Verifica se duas coordenadas são iguais"""
    if (obtem_coluna(coordenada1) == obtem_coluna(coordenada2) 
    and obtem_linha(coordenada1) == obtem_linha(coordenada2)):
        return True
    
    return False


def coordenada_para_str(coordenada):
    """Passa uma coordeanda para uma cadeia de carateres"""
    if obtem_linha(coordenada) < 10:
        return obtem_coluna(coordenada) + "0" + str(obtem_linha(coordenada))
    
    return obtem_coluna(coordenada) + str(obtem_linha(coordenada))


def str_para_coordenada(cadeia):
    """Passa uma cadeia de carateres para a representação interna da 
    coordenada"""
    return cria_coordenada(cadeia[0], int(cadeia[1:]))


def obtem_coordenadas_vizinhas(coordenada):
    """Retrona um tuplo com as coordenadas vizinhas de uma coordenada"""
    lst_j, lst_i = [-1, 0, 1, 1, 1, 0, -1, -1], [-1, -1, -1, 0, 1, 1, 1, 0]
    # as listas são usadas para a soma da coluna e da linha da coordenada de
    # modo a obter as coordenadas vizinhas
    res = []
    
    for i, j in zip(lst_i, lst_j):
        
        if (64 < ord(obtem_coluna(coordenada)) + j < 91
        and 0 < obtem_linha(coordenada) + i < 100):
            
            res.append(cria_coordenada(chr(ord(obtem_coluna(coordenada)) + j),
                                       obtem_linha(coordenada) + i))
    
    return tuple(res)


def obtem_coordenada_aleatoria(coordenada, gerador):
    """Gera uma coordenada aleatória"""
    coord = cria_coordenada(
        gera_carater_aleatorio(gerador, obtem_coluna(coordenada)),
        gera_numero_aleatorio(gerador, obtem_linha(coordenada)))
    
    return coord


"""TAD parcela
TAD para representar as parcelas de um campo do jogo das minas

Representação interna: dicionário

Operações básicas: 
Construtores: cria_parcela, cria_copia_parcela
Modificadores: limpa_parcela, marca_parcela, desmarca_parcela, esconde_mina
Reconhecedores: eh_parcela, eh_parcela_tapada, eh_parcela_marcada, 
                eh_parcela_limpa, eh_parcela_minada
Teste: parcelas_iguais
Transformadores: parcela_para_str

Função de alto nível: alterna_bandeira
"""
def cria_parcela():
    """Cria uma parcela

    Retorna:
        dicionário: parcela na sua representação interna
    """
    return {"tapada": True, "marcada": False, "limpa": False, "minada": False}


def cria_copia_parcela(parcela):
    """Cria uma cópia de uma parcela"""
    return parcela.copy()


def limpa_parcela(parcela):
    """Limpa uma parcela e retorna a parcela"""
    parcela["tapada"], parcela["limpa"], parcela["marcada"] = False, True, False
    return parcela


def marca_parcela(parcela):
    """Marca uma parcela e retorna a parcela"""
    parcela["marcada"], parcela["limpa"], parcela["tapada"] = True, False, False
    return parcela


def desmarca_parcela(parcela):
    """Desmarca uma parcela e retorna a parcela"""
    parcela["marcada"], parcela["tapada"], parcela["limpa"] = False, True, False
    return parcela


def esconde_mina(parcela):
    """Esconde uma mina na parcela e retorna a parcela"""
    parcela["minada"] = True
    return parcela


def eh_parcela(argumento):
    """Verifica se o argumento de entrada é uma parcela"""
    if isinstance(argumento, dict):
        
        for b in argumento:    
            
            if isinstance(argumento[b], bool) and len(argumento) == 4 \
            and b in argumento:
                return True
    
    return False


def eh_parcela_tapada(parcela):
    """Verifica se uma parcela está tapada"""
    return parcela["tapada"]


def eh_parcela_marcada(parcela):
    """Verifica se uma parcela está marcada"""
    return parcela["marcada"]


def eh_parcela_limpa(parcela):
    """Verifica se uma parcela está limpa"""
    return parcela["limpa"]


def eh_parcela_minada(parcela):
    """Verifica se uma parcela está minada"""
    return parcela["minada"]


def parcelas_iguais(parcela1, parcela2):
    """Verifica se duas parcelas são iguais"""
    if parcela1 == parcela2:
        return True
    return False


def parcela_para_str(parcela):
    """Passa uma parcela para uma cadeia de carateres"""
    if eh_parcela_marcada(parcela):
        return "@"
    
    elif eh_parcela_tapada(parcela):
        return "#"
    
    elif eh_parcela_limpa(parcela) and not eh_parcela_minada(parcela):
        return "?"
    
    elif eh_parcela_limpa(parcela) and eh_parcela_minada(parcela):
        return "X"
    
    
def alterna_bandeira(parcela):
    """Alterna a bandeira de uma parcela, ou seja, marca ou desmarca uma 
    parcela"""
    if eh_parcela_marcada(parcela):
        desmarca_parcela(parcela)
        return True
    
    elif eh_parcela_tapada(parcela):
        marca_parcela(parcela)
        return True
    
    return False


"""TAD campo
TAD para representar um campo do jogo das minas

Representação interna: Dicionário

Operações básicas: 
Construtores: cria_campo, cria_copia_campo
Seletores: obtem_ultima_coluna obtem_ultima_linha, obtem_parcela, 
           obtem_coordenadas, obtem_numero_minas_vizinhas
Reconhecedores: eh_campo, eh_coordenada_do_campo
Teste: campos_iguais
Transformador: campo_para_str

Funções de alto nível: coloca_minas, limpa_campo
"""
def cria_campo(coluna, linha):
    """Cria um campo do jogo das minas na representação interna

    Argumentos:
        coluna (carater): última colua do campo
        linha (inteiro): última linha do campo

    Retorna:
        dicionário: campo na representação interna
    """
    campo = {}
    
    if not (isinstance(coluna, str) and isinstance(linha, int) 
    and len(coluna) == 1 and 64 < ord(coluna) < 91 and 0 < linha < 100):
        raise ValueError("cria_campo: argumentos invalidos")
    
    for col in range(65, ord(coluna) + 1):
        
        for lin in range(1, linha + 1):
            
            campo[(chr(col), lin)] = cria_parcela()
    
    return campo


def cria_copia_campo(campo):
    """Cria uma cópia de um campo"""
    copia = {}
    
    for coordenada in campo:
        
        copia[coordenada] = cria_copia_parcela(campo[coordenada])
    
    return copia


def obtem_ultima_coluna(campo):
    """Retorna a última coluna de um campo"""
    return list(campo.keys())[-1][0]


def obtem_ultima_linha(campo):
    """Retorna a última linha de um campo"""
    return list(campo.keys())[-1][1]


def obtem_parcela(campo, coordenada):
    """Retorna a parcela de uma coordenada de um campo"""
    return campo[coordenada]


def obtem_coordenadas(campo, estado):
    """Retorna um tuplo com as coordenadas no estado introduzido"""
    lst = list(campo.keys())
    res = lst.copy()
    
    for coord in lst:
        
        if not obtem_parcela(campo, coord)[estado[:-1]]:
            res.remove(coord)
    
    return tuple(sorted(res, key = lambda x: x[1]))


def obtem_numero_minas_vizinhas(campo, coordenada):
    """Obtém o número de minas vizinhas a uma coordenada de um campo"""
    tup, num = obtem_coordenadas_vizinhas(coordenada), 0
    
    for coord in tup:
        
        if eh_coordenada_do_campo(campo, coord):
            
            if eh_parcela_minada(obtem_parcela(campo, coord)):
                num += 1
    
    return num


def eh_campo(argumento):
    """Verifica se o argumento introduzido é um campo"""
    if isinstance(argumento, dict):
        
        for coord in argumento:
            
            if not (0 < len(argumento) < 2575 and eh_coordenada(coord)
            and eh_parcela(obtem_parcela(argumento, coord))):
                return False
        
        if len(argumento) != 0:    
            return True
    
    return False


def eh_coordenada_do_campo(campo, coordenada):
    """Verifica se uma coordenada está dentro de um campo"""
    if obtem_coluna(coordenada) <= obtem_ultima_coluna(campo) \
    and obtem_linha(coordenada) <= obtem_ultima_linha(campo):
        return True
    
    return False


def campos_iguais(campo1, campo2):
    """Verifica se dois campos são iguais"""
    if campo1 == campo2:
        return True
    
    return False


def campo_para_str(campo):
    """Passa um campo para uma cadeia de carateres"""
    campo_str = "   "
    
    for coluna in range(65, ord(obtem_ultima_coluna(campo)) + 1):
        
        campo_str += chr(coluna)
    
    campo_str += "\n  +" + "-" * (ord(obtem_ultima_coluna(campo)) - 64) + "+\n"
    
    for linha in range(1, obtem_ultima_linha(campo) + 1):
        
        if linha < 10:
            campo_str += "0"
        
        campo_str += str(linha) + "|"
        
        for coluna in range(65, ord(obtem_ultima_coluna(campo)) + 1):
            
            parcela = parcela_para_str(
                      obtem_parcela(campo, cria_coordenada(chr(coluna), linha)))
            
            if parcela == "?":
                parcela = obtem_numero_minas_vizinhas(
                          campo, cria_coordenada(chr(coluna), linha))
                
                if parcela == 0:
                    campo_str += " "
                
                else:
                    campo_str += str(parcela)
            
            else:
                campo_str += parcela
        
        campo_str += "|\n"
    
    campo_str += "  +" + "-" * (ord(obtem_ultima_coluna(campo)) - 64) + "+"
    
    return campo_str


def coloca_minas(campo, coordenada, gerador, minas):
    """Coloca um certo número de minas de forma pseudoaleatória num campo"""
    minadas = []
    
    while len(minadas) < minas:
        
        coord_rndm = obtem_coordenada_aleatoria(
            cria_coordenada(obtem_ultima_coluna(campo), 
                            obtem_ultima_linha(campo)), gerador)
        
        if coord_rndm not in obtem_coordenadas_vizinhas(coordenada) \
        and coord_rndm != coordenada and coord_rndm not in minadas:
            esconde_mina(obtem_parcela(campo, coord_rndm))
            minadas.append(coord_rndm)
    
    return campo


def limpa_campo(campo, coordenada):
    """Limpa uma parcela e se as vizinhas não tiverem mina escondida limpa 
    iterativamente as vizinhas """
    for coord in (coordenada,) + obtem_coordenadas_vizinhas(coordenada):
        if eh_coordenada_do_campo(campo, coord):
            if not eh_parcela_minada(obtem_parcela(campo, coord)) \
            and not eh_parcela_limpa(obtem_parcela(campo, coord)) \
            and eh_parcela_tapada(obtem_parcela(campo, coord)):
                if obtem_numero_minas_vizinhas(campo, coord) == 0:    
                    limpa_parcela(obtem_parcela(campo, coord))
                    limpa_campo(campo, coord)
                else:
                    limpa_parcela(obtem_parcela(campo, coord))
    return campo


"""Funções adicionais:
jogo_ganho, turno_jogador, minas
"""
def jogo_ganho(campo):
    """Verifica se ganhou o jogo"""
    limpas = len(obtem_coordenadas(campo, "limpas"))
    tamanho = (ord(obtem_ultima_coluna(campo)) - 64) * obtem_ultima_linha(campo)
    minadas = len(obtem_coordenadas(campo, "minadas"))
    
    if limpas == tamanho - minadas:
        return True
    
    return False


def turno_jogador(campo):
    """Função que premite ao jogador introduzir uma ação e executa essa mesma 
    ação, seja ela alternar a bandeira da coordenada introduzida, ou limpar essa
    coordenada"""
    acao = str(input("Escolha uma ação, [L]impar ou [M]arcar:"))
    while not (acao == "M" or acao == "L"):
        acao = str(input("Escolha uma ação, [L]impar ou [M]arcar:"))
    
    coordenada = str(input("Escolha uma coordenada:"))
    while not len(coordenada) == 3 or not 64 < ord(coordenada[0]) < 91 \
    or not 47 < ord(coordenada[1]) < 58 or not 48 < ord(coordenada[2]) < 58 \
    or not eh_coordenada_do_campo(campo, str_para_coordenada(coordenada)):
        coordenada = str(input("Escolha uma coordenada:"))
    
    if acao == "L":
        limpa_campo(campo, str_para_coordenada(coordenada))
        if eh_parcela_minada(obtem_parcela(campo, 
                                           str_para_coordenada(coordenada))):
            
            desmarca_parcela(obtem_parcela(campo, 
                                           str_para_coordenada(coordenada)))
            limpa_parcela(obtem_parcela(campo, 
                                        str_para_coordenada(coordenada)))
            return False
        
        return True
    
    elif acao == "M":
        alterna_bandeira(obtem_parcela(campo, str_para_coordenada(coordenada)))
        return True


def minas(carater, linha, n_minas, dimensao, seed):
    """Função que permite jogar ao jogo das minas

    Argumentos:
        carater (carater): ultima coluna do campo
        linha (inteiro): ultima linha do campo
        n_minas (inteiro): número de minas
        dimensao (inteiro): dimensão dos bits do gerador
        seed (inteiro): estado inicial do gerador

    Retorna:
        boolean: True se ganhar, False se perder
    """
    if not (isinstance(carater, str) and isinstance(linha, int) 
    and isinstance(n_minas, int) and isinstance(dimensao, int) and (seed, int)):
        raise ValueError("minas: argumentos invalidos")
    
    if not (len(carater) == 1 and 0 < linha < 100 and n_minas > 0 
    and (dimensao == 32 or dimensao == 64) and seed > 0 
    and n_minas < (ord(carater) - 64) * linha 
    and (ord(carater) - 64) * linha - n_minas > 9):
        raise ValueError("minas: argumentos invalidos")
    
    campo = cria_campo(carater, linha)
    gerador = cria_gerador(dimensao, seed)
    
    print("   [Bandeiras " + str(len(obtem_coordenadas(campo, "marcadas"))) \
          + "/" + str(n_minas) + "]")
    print(campo_para_str(campo))
    
    coordenada = str(input("Escolha uma coordenada:"))
    while not len(coordenada) == 3 or not 64 < ord(coordenada[0]) < 91 \
    or not 47 < ord(coordenada[1]) < 58 or not 48 < ord(coordenada[2]) < 58 \
    or not eh_coordenada_do_campo(campo, str_para_coordenada(coordenada)):
        coordenada = str(input("Escolha uma coordenada:"))
    
    coloca_minas(campo, str_para_coordenada(coordenada), gerador, n_minas)
    limpa_campo(campo, str_para_coordenada(coordenada))
    
    print("   [Bandeiras " + str(len(obtem_coordenadas(campo, "marcadas"))) \
          + "/" + str(n_minas) + "]")
    print(campo_para_str(campo))

    while turno_jogador(campo):
        
        print("   [Bandeiras " + str(len(obtem_coordenadas(campo, "marcadas")))\
          + "/" + str(n_minas) + "]")
        print(campo_para_str(campo))
        
        if jogo_ganho(campo):
            print("VITORIA!!!")
            return True
    
    print("   [Bandeiras " + str(len(obtem_coordenadas(campo, "marcadas"))) \
          + "/" + str(n_minas) + "]")
    print(campo_para_str(campo))
    
    print("BOOOOOOOM!!!")
    
    return False
