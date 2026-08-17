import math
from itertools import combinations


def svm(x, y, margin_turu="h"):

    if margin_turu != "h":
        print("Bu geometrik surum yalnizca hard margin icindir.")
        return None

    tolerans = 0.000001

    def carpim(a, b):
        return a[0] * b[0] + a[1] * b[1]

    def uygun_mu(w, b):
        for i in range(len(x)):
            margin = y[i] * (carpim(w, x[i]) + b)

            if margin < 1 - tolerans:
                return False

        return True

    adaylar = []

    # İki zıt sınıf noktasını destek vektörü kabul eden adaylar
    for i in range(len(x)):
        for j in range(i + 1, len(x)):

            if y[i] == y[j]:
                continue

            if y[i] == -1:
                negatif = x[i]
                pozitif = x[j]
            else:
                negatif = x[j]
                pozitif = x[i]

            dx = pozitif[0] - negatif[0]
            dy = pozitif[1] - negatif[1]

            uzaklik_kare = dx * dx + dy * dy

            if uzaklik_kare == 0:
                continue

            w = [
                2 * dx / uzaklik_kare,
                2 * dy / uzaklik_kare
            ]

            b = -1 - carpim(w, negatif)

            if uygun_mu(w, b):
                norm_kare = w[0] * w[0] + w[1] * w[1]
                adaylar.append((norm_kare, w, b))

    # Üç noktayı destek vektörü kabul eden adaylar
    for secim in combinations(range(len(x)), 3):

        matris = []
        sonuc = [1.0, 1.0, 1.0]

        for i in secim:
            matris.append([
                y[i] * x[i][0],
                y[i] * x[i][1],
                y[i]
            ])

        cozum = uc_bilinmeyenli_coz(matris, sonuc)

        if cozum is None:
            continue

        w = [cozum[0], cozum[1]]
        b = cozum[2]

        if uygun_mu(w, b):
            norm_kare = w[0] * w[0] + w[1] * w[1]
            adaylar.append((norm_kare, w, b))

    if len(adaylar) == 0:
        print("Veriler hard margin ile dogrusal ayrilamiyor.")
        return None

    # Hard-margin SVM: uygun adaylar arasından ||w||² en küçük olan seçilir
    adaylar.sort(key=lambda aday: aday[0])

    w = adaylar[0][1]
    b = adaylar[0][2]

    def karar(nokta):
        return carpim(w, nokta) + b

    print("Tam geometrik hard margin cozumu bulundu")
    print("w:", w)
    print("b:", b)
    print()

    print("Margin degerleri:")

    destekler = []

    for i in range(len(x)):
        margin = y[i] * karar(x[i])

        print(x[i], "margin:", round(margin, 6))

        if abs(margin - 1) < 0.0001:
            destekler.append(i)

    print()
    print("Destek vektorleri:")

    for i in destekler:
        print(x[i], "sinif:", y[i])

    print()

    dogru = 0

    for i in range(len(x)):

        if karar(x[i]) >= 0:
            tahmin = 1
        else:
            tahmin = -1

        if tahmin == y[i]:
            dogru += 1

        print(x[i], "gercek:", y[i], "tahmin:", tahmin)

    basari = dogru / len(x) * 100

    print()
    print("Basari:", basari)

    grafik_ciz(x, y, w, b, destekler)

    return w, b


def uc_bilinmeyenli_coz(a, sonuc):

    matris = []

    for i in range(3):
        matris.append([
            float(a[i][0]),
            float(a[i][1]),
            float(a[i][2]),
            float(sonuc[i])
        ])

    for sutun in range(3):

        pivot = sutun

        for satir in range(sutun + 1, 3):
            if abs(matris[satir][sutun]) > abs(matris[pivot][sutun]):
                pivot = satir

        if abs(matris[pivot][sutun]) < 0.000000001:
            return None

        matris[sutun], matris[pivot] = matris[pivot], matris[sutun]

        bolen = matris[sutun][sutun]

        for j in range(sutun, 4):
            matris[sutun][j] = matris[sutun][j] / bolen

        for satir in range(3):

            if satir == sutun:
                continue

            katsayi = matris[satir][sutun]

            for j in range(sutun, 4):
                matris[satir][j] -= katsayi * matris[sutun][j]

    return [
        matris[0][3],
        matris[1][3],
        matris[2][3]
    ]


def grafik_ciz(x, y, w, b, destekler):

    minx = min(nokta[0] for nokta in x)
    maxx = max(nokta[0] for nokta in x)
    miny = min(nokta[1] for nokta in x)
    maxy = max(nokta[1] for nokta in x)

    boslukx = (maxx - minx) * 0.25
    bosluky = (maxy - miny) * 0.25

    if boslukx == 0:
        boslukx = 1

    if bosluky == 0:
        bosluky = 1

    minx -= boslukx
    maxx += boslukx
    miny -= bosluky
    maxy += bosluky

    genislik = 800
    yukseklik = 600
    kenar = 60

    cizim_genisligi = genislik - 2 * kenar
    cizim_yuksekligi = yukseklik - 2 * kenar

    # X ve Y eksenlerinde aynı piksel/birim ölçeğini kullan.
    # Böylece veri uzayında 90° olan açı grafikte de 90° görünür.
    x_aralik = maxx - minx
    y_aralik = maxy - miny

    olcek = min(
        cizim_genisligi / x_aralik,
        cizim_yuksekligi / y_aralik
    )

    merkez_x = (minx + maxx) / 2
    merkez_y = (miny + maxy) / 2

    yeni_x_aralik = cizim_genisligi / olcek
    yeni_y_aralik = cizim_yuksekligi / olcek

    minx = merkez_x - yeni_x_aralik / 2
    maxx = merkez_x + yeni_x_aralik / 2
    miny = merkez_y - yeni_y_aralik / 2
    maxy = merkez_y + yeni_y_aralik / 2

    def svgx(deger):
        return kenar + (deger - minx) * olcek

    def svgy(deger):
        return yukseklik - kenar - (deger - miny) * olcek

    svg = []

    svg.append(
        '<svg xmlns="http://www.w3.org/2000/svg" '
        'width="800" height="600">'
    )

    svg.append('<rect width="100%" height="100%" fill="white"/>')

    svg.append(
        '<text x="400" y="35" text-anchor="middle" '
        'font-size="24">Optimal Hard Margin SVM</text>'
    )

    svg.append(
        '<defs>'
        '<clipPath id="alan">'
        f'<rect x="{kenar}" y="{kenar}" '
        f'width="{cizim_genisligi}" '
        f'height="{cizim_yuksekligi}"/>'
        '</clipPath>'
        '</defs>'
    )

    svg.append(
        f'<rect x="{kenar}" y="{kenar}" '
        f'width="{cizim_genisligi}" '
        f'height="{cizim_yuksekligi}" '
        'fill="none" stroke="black" stroke-width="2"/>'
    )

    w1 = w[0]
    w2 = w[1]

    def dogru_ciz(seviye, kesikli):

        if abs(w2) > 0.000001:

            x1 = minx
            x2 = maxx

            y1 = (seviye - w1 * x1 - b) / w2
            y2 = (seviye - w1 * x2 - b) / w2

            sx1 = svgx(x1)
            sy1 = svgy(y1)
            sx2 = svgx(x2)
            sy2 = svgy(y2)

        elif abs(w1) > 0.000001:

            xdeger = (seviye - b) / w1

            sx1 = svgx(xdeger)
            sx2 = svgx(xdeger)
            sy1 = svgy(miny)
            sy2 = svgy(maxy)

        else:
            return

        if kesikli:
            ekstra = 'stroke-dasharray="10,8"'
            kalinlik = 2
        else:
            ekstra = ""
            kalinlik = 4

        svg.append(
            f'<line x1="{sx1}" y1="{sy1}" '
            f'x2="{sx2}" y2="{sy2}" '
            f'stroke="black" stroke-width="{kalinlik}" '
            f'{ekstra} clip-path="url(#alan)"/>'
        )

    dogru_ciz(0, False)
    dogru_ciz(1, True)
    dogru_ciz(-1, True)

    # Karar doğrusuna gerçekten dik olan doğruyu çiz.
    # Bir negatif destek vektöründen başlayıp pozitif marjin çizgisine
    # w yönünde dik izdüşüm alınır.
    negatif_destek_indeksi = None

    for i in destekler:
        if y[i] == -1:
            negatif_destek_indeksi = i
            break

    if negatif_destek_indeksi is not None:

        negatif_destek = x[negatif_destek_indeksi]

        w_norm_kare = w1 * w1 + w2 * w2

        if w_norm_kare > 0:

            # Negatif destek vektörü için:
            # w·x + b = -1
            #
            # Pozitif marjin çizgisine ulaşmak için değer +2 artmalıdır.
            # Bu nedenle w yönünde 2 / ||w||² kadar ilerlenir.
            izdususum = [
                negatif_destek[0] + 2 * w1 / w_norm_kare,
                negatif_destek[1] + 2 * w2 / w_norm_kare
            ]

            ax = svgx(negatif_destek[0])
            ay = svgy(negatif_destek[1])

            bx = svgx(izdususum[0])
            by = svgy(izdususum[1])

            svg.append(
                f'<line x1="{ax}" y1="{ay}" '
                f'x2="{bx}" y2="{by}" '
                'stroke="green" stroke-width="3"/>'
            )

            # Çizilen yeşil doğrunun yönü w'dir.
            dik_yonu = (w1, w2)

            # Karar doğrusunun yön vektörü.
            karar_yonu = (w2, -w1)

            dik_norm = math.hypot(dik_yonu[0], dik_yonu[1])
            karar_norm = math.hypot(karar_yonu[0], karar_yonu[1])

            nokta_carpim = (
                dik_yonu[0] * karar_yonu[0]
                + dik_yonu[1] * karar_yonu[1]
            )

            cos_degeri = nokta_carpim / (dik_norm * karar_norm)
            cos_degeri = max(-1.0, min(1.0, cos_degeri))

            aci_derece = math.degrees(math.acos(cos_degeri))

            if aci_derece > 90:
                aci_derece = 180 - aci_derece

            print("Hesaplanan aci:", round(aci_derece, 6), "derece")

            # Dik açı işareti karar doğrusu üzerindeki orta noktada çizilir.
            orta_x = (
                negatif_destek[0] + izdususum[0]
            ) / 2

            orta_y = (
                negatif_destek[1] + izdususum[1]
            ) / 2

            mx = svgx(orta_x)
            my = svgy(orta_y)

            # Eşit ölçek kullanıldığı için veri yönleri doğrudan
            # ekran yönlerine çevrilebilir. SVG'de y ekseni ters olduğu
            # için yalnızca y bileşeninin işareti değiştirilir.
            karar_ekran_x = karar_yonu[0]
            karar_ekran_y = -karar_yonu[1]

            dik_ekran_x = dik_yonu[0]
            dik_ekran_y = -dik_yonu[1]

            karar_ekran_norm = math.hypot(
                karar_ekran_x,
                karar_ekran_y
            )

            dik_ekran_norm = math.hypot(
                dik_ekran_x,
                dik_ekran_y
            )

            ux = karar_ekran_x / karar_ekran_norm
            uy = karar_ekran_y / karar_ekran_norm

            vx = dik_ekran_x / dik_ekran_norm
            vy = dik_ekran_y / dik_ekran_norm

            kare = 24

            p1x = mx + ux * kare
            p1y = my + uy * kare

            p2x = p1x + vx * kare
            p2y = p1y + vy * kare

            p3x = mx + vx * kare
            p3y = my + vy * kare

            svg.append(
                f'<polyline points="{mx},{my} {p1x},{p1y} '
                f'{p2x},{p2y} {p3x},{p3y}" '
                'fill="none" stroke="green" stroke-width="3"/>'
            )

            svg.append(
                f'<text x="{mx + 34}" y="{my - 14}" '
                'font-size="20" font-weight="bold" '
                f'fill="green">{aci_derece:.2f}°</text>'
            )

            svg.append(
                f'<text x="{mx + 12}" y="{my + 38}" '
                'font-size="16" fill="green">'
                'Marjinler arasindaki en kisa dik uzaklik'
                '</text>'
            )

            # İzdüşüm noktası veri noktası değildir; küçük yeşil işaretle gösterilir.
            svg.append(
                f'<circle cx="{bx}" cy="{by}" r="5" '
                'fill="green" stroke="black" stroke-width="1"/>'
            )

    for i in range(len(x)):

        px = svgx(x[i][0])
        py = svgy(x[i][1])

        if y[i] == -1:
            renk = "blue"
        else:
            renk = "red"

        if i in destekler:
            yaricap = 11
            kenar_kalinligi = 4
        else:
            yaricap = 8
            kenar_kalinligi = 1

        svg.append(
            f'<circle cx="{px}" cy="{py}" '
            f'r="{yaricap}" fill="{renk}" '
            f'stroke="black" stroke-width="{kenar_kalinligi}"/>'
        )

        svg.append(
            f'<text x="{px + 12}" y="{py - 12}" '
            f'font-size="14">{y[i]:+d}</text>'
        )

    svg.append("</svg>")

    with open("svm_grafik.svg", "w", encoding="utf-8") as dosya:
        dosya.write("\n".join(svg))

    print()
    print("Grafik olusturuldu: svm_grafik.svg")


x = [
    [1, 6],
    [2, 4],
    [2, 3],  # Sınıf -1
    [3, 4.5],
    [4.5, 5.5],
    [5, 7],  # Sınıf +1
]

y = [-1, -1, -1, 1, 1, 1]


sonuc = svm(x, y, "h")

if sonuc is not None:
    w, b = sonuc