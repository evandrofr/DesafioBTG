import time
import os

def segmentos_cruzam(s0, s1):
    """
    s0 e s1 são listas com duas duplas dizendo as coordenadas das
    extremidades dos segmentos de retas no formato [(x0,y0),(x1,y1)]
    """
    dx0 = s0[1][0]-s0[0][0]
    dx1 = s1[1][0]-s1[0][0]
    dy0 = s0[1][1]-s0[0][1]
    dy1 = s1[1][1]-s1[0][1]
    p0 = dy1*(s1[1][0]-s0[0][0]) - dx1*(s1[1][1]-s0[0][1])
    p1 = dy1*(s1[1][0]-s0[1][0]) - dx1*(s1[1][1]-s0[1][1])
    p2 = dy0*(s0[1][0]-s1[0][0]) - dx0*(s0[1][1]-s1[0][1])
    p3 = dy0*(s0[1][0]-s1[1][0]) - dx0*(s0[1][1]-s1[1][1])
    return (p0*p1<=0) & (p2*p3<=0)


def ponto_dentro_poligono(ponto, poligono):
    """
    Cria uma semireta horizontal a partir do ponto dado e verifica seu cruzamento
    com os segmentos de reta que formam o poligono.
    Caso o haja um número impar de cruzamentos o ponto está dentro do poligono,
    caso o número seja par, está fora.
    Limitação: pode cometer erros se o cruzamento ocorrer no vertice do poligono.

    Ponto no formato de tupla (x, y)
    Poligono no formato de lista de tuplas [(x0,y0), (x1,y1), ... , (x_n, y_n)] 
    """
    seg = [(ponto[0], ponto[1]), (ponto[0]  + 360, ponto[1])] # Segmento horizontal "infinito"
    cont = 0
    for idx, p in enumerate(poligono):
        s = [(poligono[idx-1][0], poligono[idx-1][1]), (poligono[idx][0], poligono[idx][1])]
        if segmentos_cruzam(s, seg):
            cont += 1
    return cont%2 == 1

# Pegando os pontos do contorno
with open("PSATCMG_CAMARGOS.bln") as file:
    size = file.readline()
    contorno = []

    for line in file.readlines():
        data = line.split(",")
        contorno.append((float(data[0]),float(data[1])))



inicio = time.time()
# Pegando os pontos de um dia
with open("forecast_files/ETA40_p011221a021221.dat") as file:
    pontos_eta_arquivo1 = []
    for line in file.readlines():
        data = line.split()
        pontos_eta_arquivo1.append( ( float(data[0]), float(data[1]), float(data[2])) )

fim = time.time()
duracao = fim - inicio
print(f"Duração de um arquivo: {round(duracao, 3)}")


inicio = time.time()
# Pegando os pontos de todos os arquivos dentro da pasta forecast
pasta = "./forecast_files"
pontos_eta = {}
for diretorio, subpastas, arquivos in os.walk(pasta):
    for idx, arquivo in enumerate(arquivos):
        pontos = []
        path = os.path.join(diretorio, arquivo)
        with open(path) as file:
            for line in file.readlines():
                data = line.split()
                pontos.append( ( float(data[0]), float(data[1]), float(data[2])) )
        pontos_eta[idx] = pontos
fim = time.time()
duracao = fim - inicio
print(f"Duração de todos arquivos: {round(duracao, 3)}")



inicio_loop = time.time()
prec_total_list = []
for idx, pontos in pontos_eta.items():

    inicio = time.time()
    prec_total = 0
    for lat, long, prec in pontos:
        p = (lat, long)
        if ponto_dentro_poligono(p, contorno):
            prec_total += prec
    prec_total_list.append(round(prec_total, 3))

    fim = time.time()
    duracao = fim - inicio
    print(f"Duração de calculo de precipitação para um dia: {round(duracao, 3)}")


fim_loop = time.time()
duracao_loop = fim_loop - inicio_loop
print(f"Duração de calculo de precipitação para todos os dias: {round(duracao_loop, 3)}")

print("Precipitação dentro do contorno para cada dia: ")
print(prec_total_list)









