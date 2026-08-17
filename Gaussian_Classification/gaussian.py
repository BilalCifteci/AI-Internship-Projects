import math


def gaussian_classification(x, y):

    siniflar = []

    for etiket in y:
        if etiket not in siniflar:
            siniflar.append(etiket)

    sinif_verileri = {}

    for sinif in siniflar:
        sinif_verileri[sinif] = []

    for i in range(len(x)):
        sinif_verileri[y[i]].append(x[i])

    ozellik_sayisi = len(x[0])

    #iki boyutlu veriler icin
    if ozellik_sayisi != 2:
        raise ValueError("Grafik icin veriler iki ozellikli olmalidir.")

    def ortalama(liste):
        toplam = 0

        for sayi in liste:
            toplam = toplam + sayi

        return toplam / len(liste)

    def varyans(liste, ort):
        toplam = 0

        for sayi in liste:
            toplam = toplam + (sayi - ort) ** 2

        return toplam / len(liste)

    bilgiler = {}

    # Her sinifin ortalama, varyans ve prior degerlerini buluyoruz
    for sinif in siniflar:

        ortalamalar = []
        varyanslar = []

        for j in range(ozellik_sayisi):

            degerler = []

            for nokta in sinif_verileri[sinif]:
                degerler.append(nokta[j])

            ort = ortalama(degerler)
            var = varyans(degerler, ort)

            if var == 0:
                var = 0.000001

            ortalamalar.append(ort)
            varyanslar.append(var)

        prior = len(sinif_verileri[sinif]) / len(x)

        bilgiler[sinif] = {
            "ortalama": ortalamalar,
            "varyans": varyanslar,
            "prior": prior
        }

    def gaussian(deger, ort, var):

        birinci_kisim = 1 / math.sqrt(
            2 * math.pi * var
        )

        ikinci_kisim = math.exp(
            -((deger - ort) ** 2) / (2 * var)
        )

        return birinci_kisim * ikinci_kisim

    def tahmin(nokta):

        en_iyi_sinif = None
        en_buyuk = None

        for sinif in siniflar:

            sonuc = math.log(
                bilgiler[sinif]["prior"]
            )

            for i in range(ozellik_sayisi):

                olasilik = gaussian(
                    nokta[i],
                    bilgiler[sinif]["ortalama"][i],
                    bilgiler[sinif]["varyans"][i]
                )

                if olasilik < 0.000000000001:
                    olasilik = 0.000000000001

                sonuc = sonuc + math.log(olasilik)

            if en_buyuk is None or sonuc > en_buyuk:
                en_buyuk = sonuc
                en_iyi_sinif = sinif

        return en_iyi_sinif

    print("Sinif bilgileri")
    print()

    for sinif in siniflar:

        print("Sinif:", sinif)
        print(
            "Merkez:",
            bilgiler[sinif]["ortalama"]
        )
        print(
            "Varyans:",
            bilgiler[sinif]["varyans"]
        )
        print(
            "Standart sapma:",
            [
                math.sqrt(bilgiler[sinif]["varyans"][0]),
                math.sqrt(bilgiler[sinif]["varyans"][1])
            ]
        )
        print(
            "Prior:",
            bilgiler[sinif]["prior"]
        )
        print()

    dogru = 0

    for i in range(len(x)):

        sonuc = tahmin(x[i])

        print(
            x[i],
            "gercek:",
            y[i],
            "tahmin:",
            sonuc
        )

        if sonuc == y[i]:
            dogru = dogru + 1

    basari = dogru / len(x) * 100

    print()
    print("Basari orani:", basari)

    
    # Grafik kismi

    minx = x[0][0]
    maxx = x[0][0]
    miny = x[0][1]
    maxy = x[0][1]

    for sinif in siniflar:

        merkez_x = bilgiler[sinif]["ortalama"][0]
        merkez_y = bilgiler[sinif]["ortalama"][1]

        std_x = math.sqrt(
            bilgiler[sinif]["varyans"][0]
        )

        std_y = math.sqrt(
            bilgiler[sinif]["varyans"][1]
        )

        if merkez_x - 3 * std_x < minx:
            minx = merkez_x - 3 * std_x

        if merkez_x + 3 * std_x > maxx:
            maxx = merkez_x + 3 * std_x

        if merkez_y - 3 * std_y < miny:
            miny = merkez_y - 3 * std_y

        if merkez_y + 3 * std_y > maxy:
            maxy = merkez_y + 3 * std_y

    for nokta in x:

        if nokta[0] < minx:
            minx = nokta[0]

        if nokta[0] > maxx:
            maxx = nokta[0]

        if nokta[1] < miny:
            miny = nokta[1]

        if nokta[1] > maxy:
            maxy = nokta[1]

    boslukx = (maxx - minx) * 0.15
    bosluky = (maxy - miny) * 0.15

    if boslukx == 0:
        boslukx = 1

    if bosluky == 0:
        bosluky = 1

    minx = minx - boslukx
    maxx = maxx + boslukx
    miny = miny - bosluky
    maxy = maxy + bosluky

    genislik = 800
    yukseklik = 600
    kenar = 60

    cizim_genisligi = genislik - 2 * kenar
    cizim_yuksekligi = yukseklik - 2 * kenar

    def svgx(deger):
        oran = (deger - minx) / (maxx - minx)
        return kenar + oran * cizim_genisligi

    def svgy(deger):
        oran = (deger - miny) / (maxy - miny)

        return (
            yukseklik
            - kenar
            - oran * cizim_yuksekligi
        )

    def svg_uzunluk_x(deger):
        return deger / (maxx - minx) * cizim_genisligi

    def svg_uzunluk_y(deger):
        return deger / (maxy - miny) * cizim_yuksekligi

    svg = []

    svg.append(
        '<svg xmlns="http://www.w3.org/2000/svg" '
        'width="800" height="600">'
    )

    svg.append(
        '<rect width="100%" height="100%" fill="white"/>'
    )

    svg.append(
        '<text x="400" y="35" text-anchor="middle" '
        'font-size="24">Gaussian Classification</text>'
    )

    svg.append(
        f'<rect x="{kenar}" y="{kenar}" '
        f'width="{cizim_genisligi}" '
        f'height="{cizim_yuksekligi}" '
        'fill="none" stroke="black" stroke-width="2"/>'
    )

    renkler = [
        "royalblue",
        "tomato",
        "green",
        "purple",
        "orange"
    ]


    for sinif_indexi in range(len(siniflar)):

        sinif = siniflar[sinif_indexi]
        renk = renkler[sinif_indexi % len(renkler)]

        merkez_x = bilgiler[sinif]["ortalama"][0]
        merkez_y = bilgiler[sinif]["ortalama"][1]

        std_x = math.sqrt(
            bilgiler[sinif]["varyans"][0]
        )

        std_y = math.sqrt(
            bilgiler[sinif]["varyans"][1]
        )

        svg_merkez_x = svgx(merkez_x)
        svg_merkez_y = svgy(merkez_y)

        for kat in [3, 2, 1]:

            yaricap_x = svg_uzunluk_x(
                kat * std_x
            )

            yaricap_y = svg_uzunluk_y(
                kat * std_y
            )

            svg.append(
                f'<ellipse cx="{svg_merkez_x}" '
                f'cy="{svg_merkez_y}" '
                f'rx="{yaricap_x}" '
                f'ry="{yaricap_y}" '
                f'fill="none" '
                f'stroke="{renk}" '
                f'stroke-width="2" '
                f'stroke-dasharray="8,5"/>'
            )

    
        svg.append(
            f'<line x1="{svg_merkez_x - 7}" '
            f'y1="{svg_merkez_y}" '
            f'x2="{svg_merkez_x + 7}" '
            f'y2="{svg_merkez_y}" '
            f'stroke="{renk}" stroke-width="4"/>'
        )

        svg.append(
            f'<line x1="{svg_merkez_x}" '
            f'y1="{svg_merkez_y - 7}" '
            f'x2="{svg_merkez_x}" '
            f'y2="{svg_merkez_y + 7}" '
            f'stroke="{renk}" stroke-width="4"/>'
        )

        svg.append(
            f'<text x="{svg_merkez_x + 10}" '
            f'y="{svg_merkez_y - 10}" '
            f'font-size="14">'
            f'Merkez {sinif}</text>'
        )


    for i in range(len(x)):

        px = svgx(x[i][0])
        py = svgy(x[i][1])

        sinif_indexi = siniflar.index(y[i])
        renk = renkler[sinif_indexi % len(renkler)]

        svg.append(
            f'<circle cx="{px}" cy="{py}" '
            f'r="7" fill="{renk}" '
            f'stroke="black"/>'
        )

        svg.append(
            f'<text x="{px + 9}" y="{py - 9}" '
            f'font-size="13">{y[i]}</text>'
        )

    svg.append("</svg>")

    dosya = open(
        "gaussian_grafik.svg",
        "w",
        encoding="utf-8"
    )

    dosya.write("\n".join(svg))
    dosya.close()

    print()
    print("Grafik olusturuldu: gaussian_grafik.svg")

    return tahmin


x = [
    [1, 2],
    [2, 3],
    [2, 1],
    [6, 5],
    [7, 7],
    [8, 6]
]

y = [-1, -1, -1, 1, 1, 1]


model = gaussian_classification(x, y)

print()
print("Yeni nokta tahmini")

yeni_nokta = [7, 5]

sonuc = model(yeni_nokta)

print(
    yeni_nokta,
    "sinifi:",
    sonuc
)