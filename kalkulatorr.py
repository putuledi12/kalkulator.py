import re
import pandas as pd
import numpy as np
import math

riwayat = []

def sin(x):
    return np.sin(np.radians(x))

def cos(x):
    return np.cos(np.radians(x))

def tan(x):
    return np.tan(np.radians(x))

def sec(x):
    nilai = cos(x)
    if np.isclose(nilai, 0):
        raise ValueError("Secan tidak terdefinisi")
    return 1 / nilai

def cosec(x):
    nilai = sin(x)
    if np.isclose(nilai, 0):
        raise ValueError("Cosecan tidak terdefinisi")
    return 1 / nilai

def cot(x):
    nilai = sin(x)
    if np.isclose(nilai, 0):
        raise ValueError("Cotangen tidak terdefinisi")
    return cos(x) / nilai

def asin(x):
    return np.degrees(np.arcsin(x))

def acos(x):
    return np.degrees(np.arccos(x))

def atan(x):
    return np.degrees(np.arctan(x))

def multi_func(func, args):
    if len(args) == 1 and isinstance(args[0], (list, tuple, np.ndarray)):
        return func(args[0])
    return func(args)

def custom_sum(*args):
    return multi_func(sum, args)

def custom_mean(*args):
    return multi_func(np.mean, args)

def custom_median(*args):
    return multi_func(np.median, args)

def custom_max(*args):
    return multi_func(max, args)

def custom_min(*args):
    return multi_func(min, args)

fungsi = {
    "sin": sin,
    "cos": cos,
    "tan": tan,
    "sec": sec,
    "cosec": cosec,
    "cot": cot,
    "asin": asin,
    "acos": acos,
    "atan": atan,
    "sinh": np.sinh,
    "cosh": np.cosh,
    "tanh": np.tanh,
    "abs": abs,
    "ceil": math.ceil,
    "floor": math.floor,
    "round": round,
    "sqrt": np.sqrt,
    "log": np.log10,
    "ln": np.log,
    "fact": math.factorial,
    "sum": custom_sum,
    "mean": custom_mean,
    "median": custom_median,
    "max": custom_max,
    "min": custom_min,
    "pi": np.pi,
    "e": np.e
}

def hitung(rumus):
    rumus = rumus.replace("^", "**")

    if not re.fullmatch(r"[a-zA-Z0-9_+\-*/%().,\s\[\]]+", rumus):
        raise ValueError("Karakter tidak valid")

    token = r"[a-zA-Z_]\w*|\d+(?:\.\d*)?|\.\d+|\*\*|[()+\-*/%,\[\]]"
    tokens = re.findall(token, rumus)

    if "".join(tokens).replace(" ", "") != re.sub(r"\s+", "", rumus):
        raise ValueError("Format rumus tidak valid")

    for nama in re.findall(r"[a-zA-Z_]\w*", rumus):
        if nama not in fungsi:
            raise ValueError("Fungsi tidak dikenal: " + nama)

    pola_fungsi = r"\b(sin|cos|tan|sec|cosec|cot|asin|acos|atan|sinh|cosh|tanh|abs|ceil|floor|round|sqrt|log|ln|fact|sum|mean|median|max|min)\b"

    rumus = re.sub(
        pola_fungsi,
        lambda m: "fungsi['" + m.group() + "']",
        rumus
    )

    for nama in ["pi", "e"]:
        rumus = re.sub(
            r"\b" + nama + r"\b",
            "fungsi['" + nama + "']",
            rumus
        )

    lingkungan = {
        "__builtins__": {},
        "fungsi": fungsi
    }

    hasil = eval(rumus, lingkungan, {})

    if isinstance(hasil, (list, np.ndarray)):
        hasil = np.array(hasil)
        if not np.all(np.isfinite(hasil)):
            raise ValueError("Hasil tidak terdefinisi")
    else:
        if not np.isfinite(hasil):
            raise ValueError("Hasil tidak terdefinisi")

    return hasil


def kalkulator():
    print("\n" + "=" * 50)
    print("         SCIENTIFIC CALCULATOR (EXTENDED)")
    print("=" * 50)

    print("\nOPERASI DASAR & STATISTIK")
    print("+  -  *  /  %  **")
    print("sum(a,b,c)   mean(a,b,c)   median(a,b,c)")
    print("max(a,b,c)   min(a,b,c)")

    print("\nTRIGONOMETRI & INVERS")
    print("sin   cos   tan   sec   cosec   cot")
    print("asin  acos  atan  sinh  cosh    tanh")

    print("\nOPERASI LAINNYA")
    print("sqrt  log   ln    fact  abs")
    print("ceil  floor round pi    e")
    
    print("\n" + "-" * 50)
    print("CONTOH CARA INPUT:")
    print("• Operasi Dasar   : 5 + 3 * 2")
    print("• Pangkat         : 2 ** 3  (atau  2^3)")
    print("• Trigonometri    : sin(30)")
    print("• Statistik       : mean(10, 20, 30)  atau  sum([1, 2, 3])")
    print("• Akar & Faktorial: sqrt(25)  atau  fact(5)")
    print("=" * 50)

    while True:
        rumus = input("\nMasukkan perhitungan: ")

        try:
            hasil = hitung(rumus)

            if isinstance(hasil, np.ndarray):
                hasil_tampil = []
                for x in hasil:
                    if isinstance(x, (int, np.integer)) or (isinstance(x, float) and x.is_integer()):
                        hasil_tampil.append(int(x))
                    else:
                        r = round(float(x), 10)
                        hasil_tampil.append(int(r) if r.is_integer() else r)
            elif isinstance(hasil, (np.integer, int)):
                hasil_tampil = int(hasil)
            else:
                f_val = float(hasil)
                if f_val.is_integer():
                    hasil_tampil = int(f_val)
                else:
                    hasil_tampil = round(f_val, 10)
                    if isinstance(hasil_tampil, float) and hasil_tampil.is_integer():
                        hasil_tampil = int(hasil_tampil)

            print("\nHASIL")
            print("=", hasil_tampil)

            riwayat.append({
                "Perhitungan": rumus,
                "Hasil": str(hasil_tampil)
            })

        except ZeroDivisionError:
            print("Error: Tidak bisa dibagi nol!")
        except (ValueError, TypeError, OverflowError) as error:
            print("Error:", error)
        except Exception:
            print("Error: Format perhitungan tidak valid!")

        pilihan = input("\nApakah Anda ingin melanjutkan perhitungan? (y/n): ").strip().lower()
        if pilihan != 'y':
            print("\nKalkulator ditutup.")
            break

    if riwayat:
        data = pd.DataFrame(riwayat)
        print("\nRIWAYAT PERHITUNGAN")
        print(data.to_string(index=False))

kalkulator()