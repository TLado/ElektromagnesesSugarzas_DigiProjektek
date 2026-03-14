devices_and_values = {"laptop": 10, "monitor": 9, "printer": 3, "router": 5, "other": 4} # teljesen véletlenszerű értékek és eszközök dummyknak
DISTANCE_WHEN_MEASURED = 0.1 # ilyen messziről mértük meg az eszközt (méter), amiből az alapvető térerősségértéket kaptuk

def data_input():
    device = input(f"Milyen eszközöd van? Az alábbiak közül válassz: {devices_and_values.keys()}: ")
    if device not in devices_and_values.keys():
        print("Érvénytelen eszköz!")
        return data_input()
    num_devices = int(input(f"Hány darab {device} van?: "))
    distance = float(input(f"Milyen távolságra vagy a {device}től (méterben; ha nem egész, akkor \".\"-zel add meg a tizedes jegyet)?: "))
    #power = float(input(f"Milyen teljesítményű a {device}?"))
    #frequency = float(input(f"Milyen frekvenciájú a {device}?"))
    # muT = float(input(f"Milyen mágneses térerősségű a {device} (muT-ben)?: "))
    return device, num_devices, distance

def tererosseg_szamitas(device, num_devices, distance):
    tererosseg_mutato = devices_and_values[device] * num_devices * (DISTANCE_WHEN_MEASURED / distance)**3
    return tererosseg_mutato

if __name__ == "__main__":
    device, num_devices, distance = data_input()
    print(f"A {device} távolsága: {distance} m, a mágneses térerősség közvetlen közelről: {devices_and_values[device]} muT")
    print(f"A tererosseg_mutato: {tererosseg_szamitas(device, num_devices, distance)}")

