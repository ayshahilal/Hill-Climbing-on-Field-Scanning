import numpy as np
import random
import pygame
import matplotlib.pyplot as plt

x_start1 = 8
y_start1 = 0

x_start2 = 4
y_start2 = 8

x_start3 = 4
y_start3 = 4

P = 200 # popülasyon büyüklügü
G = 500 # jenerasyon sayısı
u = 81  # N*N


# Drone'larin yolunu ekrana cizen fonksiyon
def plotting(drone_path, x_start, y_start, d):
    the_xs = np.zeros((d,u+1))  # +1 bitis noktasini eklemek icin
    the_ys = np.zeros((d,u+1))
    # her bir drone icin x ve y leri matrisin ilgili yerine kaydet
    for k in range(0, d):
        # her drone icin baslangic noktasini tekrar guncelle
        x = x_start
        y = y_start
        # u (n*n)
        for i in range(0, u):
            the_xs[k][i] = x
            the_ys[k][i] = y
            select = drone_path[k][i]
            # hareketten sonraki x ve y koordinatlarini bul
            x, y = direction_finder(x, y, select)
        # baslangica geri donmesi icin dizinin sonuna bitis noktasi (x_start,y_start) verilir
        the_xs[k][u] = x_start
        the_ys[k][u] = y_start

    # Ekrana yolu ciz
    # Drone sayisina gore drone'lari beraber yada tek ciz
    if d==1 or d==2 or d==3 or d==4:
        plt.plot(the_xs[0,:], the_ys[0,:])
    if d==2 or d==3 or d==4:
        plt.plot(the_xs[1, :], the_ys[1, :])
    if d==3 or d==4:
        plt.plot(the_xs[2, :], the_ys[2, :])
    if d==4:
        plt.plot(the_xs[3, :], the_ys[3, :])
    plt.title('Jenerasyon Sayisi: {}'.format(G))
    plt.xlim([0, 8])
    plt.ylim([0, 8])
    plt.show()


def plot_w(G, watch_mu, a):

    plt.title('{}. drone icin Jenerasyon-Fitness degeri degisimi'.format(a+1))
    plt.plot(G, watch_mu)
    plt.xlabel("Jenerasyon sayisi (G)")
    plt.ylabel("Fitness degeri (w)")
    #plt.xlim([0, G])
    plt.show()


# Taranmis alani gosteren fonksiyon
def GUI(drone_path, x_start, y_start, d):
    matrix = np.zeros((9, 9))
    # Renkleri belirle
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GREEN = (170, 255, 30)
    RED = (255, 0, 0)
    renk = (154,73,99)
    renk2 = (100, 0, 255)
    # Width, height ve margin leri belirle
    WIDTH = 20
    HEIGHT = 20
    MARGIN = 5

    # İlgili drone icin kayitli olan yonlere gore (drone_path[]) ugradigi noktaları 9*9 luk matriste 1 yapar ve matrisi return eder
    if d == 1:
        matrix1 = draw(drone_path[0], x_start, y_start)
    if d == 2:
        matrix2 = draw(drone_path[1], x_start, y_start)
    if d == 3:
        matrix3 = draw(drone_path[2], x_start, y_start)
    if d == 4:
        matrix4 = draw(drone_path[3], x_start, y_start)

    # Initialize pygame
    pygame.init()

    # Set the HEIGHT and WIDTH of the screen
    WINDOW_SIZE = [230, 230]
    screen = pygame.display.set_mode(WINDOW_SIZE)

    # Set title of screen
    if d == 1:
        pygame.display.set_caption("DRONE 1 AREA")
    if d == 2:
        pygame.display.set_caption("DRONE 2 AREA")
    if d == 3:
        pygame.display.set_caption("DRONE 3 AREA")
    if d == 4:
        pygame.display.set_caption("DRONE 4 AREA")

    # Loop until the user clicks the close button.
    done = False
    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()

    # -------- Main Program Loop -----------
    while not done:
        for event in pygame.event.get():  # User did something
            if event.type == pygame.QUIT:  # If user clicked close
                done = True  # Flag that we are done so we exit this loop

        # Set the screen background
        screen.fill(BLACK)
        # Draw the grid
        if d == 1:
            temp_color = GREEN
            matrix = matrix1
        if d == 2:
            temp_color = renk
            matrix = matrix2
        if d == 3:
            temp_color = RED
            matrix = matrix3
        if d == 4:
            temp_color = renk2
            matrix = matrix4

        for row in range(9):
            for column in range(9):
                color = WHITE
                if matrix[row][column] == 1:
                    color = temp_color
                pygame.draw.rect(screen,
                                color,
                                [(MARGIN + WIDTH) * column + MARGIN,
                                (MARGIN + HEIGHT) * row + MARGIN,
                                WIDTH,
                                HEIGHT])
        # Limit to 60 frames per second
        clock.tick(60)
        # Go ahead and update the screen with what we've drawn.
        pygame.display.flip()
    # Be IDLE friendly. If you forget this line, the program will 'hang'
    # on exit.
    pygame.quit()


# yonleri ve baslangic noktasi belirli olan drone icin x ve y koordinatlarini bulur ve gezdigi hucreyi 1 yapar
def draw(B, x_start, y_start):
    matrix = np.zeros((9, 9))
    x = x_start
    y = y_start
    # baslangic noktasini ugranildi olarak 1 yap
    matrix[x][y] = 1
    # u ((N*N)-1) kadar giderek her bir yon sonucu gidilen noktayi bul, drone'u hareket ettir
    for i in range(0, u):
        # drone'un gidecegi yon'u alir
        select = B[i]
        # hareketten sonraki x ve y koordinatlarini bul
        x, y = direction_finder(x, y, select)
        # gezdigi hucreyi 1 yap
        matrix[x][y] = 1

    return matrix


# kopyalanan ve %mu kadar degistirilen P tane yol icin drone'u hareket ettiren fonksiyon
def generate_random_path(individuals, x_start, y_start):
    fitness1 = np.zeros(P)
    fitness2 = np.zeros(P)
    # P yol icin ayri ayri fitness fonks hesapla
    for i in range(0, P):
        x = x_start
        y = y_start
        # her bir yol icin matrisi sifirla
        matrix = np.zeros((9, 9))
        # drone'un baslangic noktasini matriste 1 yap
        matrix[x][y] = 1
        # Drone'un yolunu belirlemek icin u uzunlugundaki yonleri iceren matrisi (individuals[][]) gez
        for j in range(0, u):
            # hareketin yonunu al
            select = individuals[i][j]
            flag = 0

            # matrisin disina cikip cikmadigini is_there_an_obstacle() fonskiyonu ile kontrol et
            while is_there_an_obstacle(x, y, select):
                # disari cikmaya calisirsa baska bir random hareket sec
                select = random.randint(1, 8)
                flag = 1
            # hareketten sonraki x ve y koordinatlarini bul
            x, y = direction_finder(x, y, select)
            # gezdigi hucreyi 1 yap
            matrix[x][y] = 1

            # disari cikmaya calistiysa flag=1 dir; yonleri iceren matristeki degisikligi guncelle
            if flag == 1:
                individuals[i][j] = select
        # max-gezdigi hucre sayisi
        f1 = sum(map(sum, matrix)) / 81
        # fitness dizisine daha sonra en iyisini bulabilmek icin kaydedilir
        fitness1[i] = f1
        route = individuals[i]
        # acilar arasi donuslerin maliyeti cost() da hesaplanir
        # min cost iyi oldugu icin minimize edilmek icin asagidaki islem yapilir
        f2 = 100/cost(route)
        # fitness2 dizisine daha sonra en iyisini bulabilmek icin kaydedilir
        fitness2[i] = f2

    return fitness1, fitness2, individuals


# P yolun arasindan fitness fonksiyonlarına bakarak en iyisini bulur
def find_best(B, best_w, f1, f2, mu, individuals):
    mu_start = 0.01
    mu_dec = 0.99   # azalma oranı
    mu_inc = 1.01  # artma oranı
    tk_max = 5
    tk = 1
    w = -1

    # fitness degerlerinden ortalama bir deger uret, en yuksek olani w) ve indexini (index) bul
    for i in range(P):
        x = (f1[i] + f2[i]) / 2
        if x > w:
            w = x       # fitnessların en iyisini w da tut
            index = i   # index'ini tut

    # mevcut iyiden (best_w) daha iyi mi karsilastir, daha iyiyse best_w yu ve en iyi yolu guncelle
    if w > best_w:
        tk = 0
        best_w = w
        B = individuals[index]

        if mu <= mu_start:
            mu = mu * mu_dec     # mutasyon oranini azalt
        else:
            mu = mu_start       # mu_start'tan buyukse ve iyilesme varsa mu_start'tan tekrar başlasın
    # iyilesme yoksa / daha iyi yol bulamadiysa tk yi arttir ve mutasyon oraninin arttir
    else:
        tk += 1
        mu = mu * mu_inc        # mutasyon oranini arttir

    # tk_max kez mevcut yol'dan daha iyi yol bulunamadiysa baslangic yolunu random bir yolla degistir, mutasyon oranini bastan baslat
    if tk == tk_max:
        tk = 0
        mu = mu_start
        B = np.zeros(u)
        # Random bir yon dizisi belirle
        for i in range(0, u):
            n = random.randint(1, 8)  # 1-8 arasi sayilarla doldur
            B.append(n)

    return B, mu, best_w, index


# cost ne kadar buyukse okadar kotu donus yapiyor, iyilik fonksiyonu: min cost
def cost(route):
    cost = 0
    for i in range(0, 80):
        # donusleri ters yonde yapiyorsa cost'u fazla arttir
        if (abs(route[i] - route[i + 1])) == 4:
            cost += 4
        # degilse cost'u 1 hareket yaptigi icin 1 arttir
        else:
            cost += 1

    return cost


# Alanin disina cikmasini engelleyen fonskiyon
def is_there_an_obstacle(x, y, direction):
    # x,y den (direction) yonunde hareket ettiginde gittigi koordinatlari bul
    x, y = direction_finder(x, y, direction)
    # Eger alanin disina cikiyorsa True don
    if x < 0 or x > 8:
        return True
    if y < 0 or y > 8:
        return True
    return False


# x ve y nin hareket sonucu degerlerini gunceller ve dondurur
def direction_finder(x, y, direction):
    if direction == 1:
        return x - 1, y
    elif direction == 2:
        return x - 1, y - 1
    elif direction == 3:
        return x, y - 1
    elif direction == 4:
        return x + 1, y - 1
    elif direction == 5:
        return x + 1, y
    elif direction == 6:
        return x + 1, y + 1
    elif direction == 7:
        return x, y + 1
    elif direction == 8:
        return x - 1, y + 1


# Verilen diziyi P kere kopyalar ve %mu kadar degisiklik yapar
def create_P_path(B, mu):
    # degisiklik yapilmasi icin uretilecek random path
    Path = np.zeros((P, u))
    # P tane diziyi kaydetmek icin P*u uzunlugunda matris
    individuals = np.zeros((P, u))

    # B baslangic dizisini P kere kopyala
    for i in range(0, P):
        individuals[i] = B  # P diziyi individuals'a kopyala

    # degisiklik yaparken kullanilmasi icin P tane path uret (1-8 arasi sayilardan olusan)
    for i in range(0, P):
        for j in range(0, u):
            # 1-8 arasi sayilarla doldur ve kaydet
            n = random.randint(1, 8)
            Path[i][j] = n

    # her bir path icin (P tane u uzunlugunda) 0-1 arası rastgele degerler uret
    # check_mu = np.random.random_sample(size=P)
    check_mu = np.random.random_sample((P, u))

    # %mu kadar degisiklik yap
    # check_mu daki degerlerin mu'dan kucuk olup olmadigini kontrol et
    for i in range(0, P):
        for j in range(0, u):
            if check_mu[i][j] < mu:  # mu'dan kucukse degistir
                individuals[i][j] = Path[i][j]

    return individuals


if __name__ == "__main__":
    x_s = []
    y_s = []
    x_s.append(x_start1)
    x_s.append(x_start2)
    x_s.append(x_start3)
    y_s.append(y_start1)
    y_s.append(y_start2)
    y_s.append(y_start3)

    d = int(input("Kac drone'la tarama yapilsin?(1-2-4)"))
    drone_path = np.zeros((d, u))
    x = int(input("Bir baslangic noktasi secin (1-2-3)"))

    watch_w = np.zeros(G)
    list = list(range(0, G))    # w-G grafigini olusturmak icin 0-G arasi sayilardan olusan dizi

    if d>4 or d<1 or x>3 or x<1:
        print("Yanlis secim yaptiniz")
        exit()

    # Drone sayisi kadar islem yap
    for a in range(0, d):
        mu = 0.01  # değişim oranı
        best_w = 0
        B = []  # baslangic icin uretilecek random path
        # rastgele baslangic icin (N*N)-1 uzunlukta random path uret
        for i in range(0, u):
            n = random.randint(1, 8)  # 1-8 arasi sayilarla doldur
            B.append(n)

        # G iterasyon
        for k in range(0, G):
            # Baslangic dizisini P kere kopyalar ve %mu kadar degisiklik yapar
            individuals = create_P_path(B, mu)
            # kopyalanan ve %mu kadar degistirilen P tane yol icin drone'u hareket ettirir, fitness degerlerini dondurur
            fitness1, fitness2, individuals = generate_random_path(individuals, x_s[x-1], y_s[x-1])
            # P yolun arasindan fitness fonksiyonlarına bakarak en iyisini bulur ve dondurur
            B, mu, best_w, index = find_best(B, best_w, fitness1, fitness2, mu, individuals)
            # Mevcut drone icin G iterasyon boyunca bulunan en iyi w degerini watch_w dizisinde tutar
            watch_w[k] = best_w

        # Her drone icin bulunan en iyi yol drone_path[][] e kaydedilir
        drone_path[a] = B

        #print("Fitness Function:  w={} index={} mu={}".format(best_w, index, mu))
        print("Best Route is", B)

        # Jenerasyon (G) sayisina gore w (iyilik fonksiyonu) degisimini her drone icin ayri ayri grafikler
        plot_w(list, watch_w, a)

    print("----{} ITERASYON YAPILDI----".format(G))
    # Gidilen yolu cizdir
    plotting(drone_path, x_s[x-1], y_s[x-1], d)
    # Taranmis alani goster
    for i in range(1, d+1):
        GUI(drone_path, x_s[x-1], y_s[x-1], i)
