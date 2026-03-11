print("Hello Digitális Projektek!")
devices = ["laptop", "monitor", "printer", "router", "other"]

def data_input():
    device = input(f"Milyen eszközöd van? Az alábbiak közül válassz: {devices}: ")
    if device not in devices:
        print("Érvénytelen eszköz!")
        return data_input()
    num_devices = int(input(f"Hány darab {device} van?: "))
    distance = float(input(f"Milyen távolságra vagy a {device}től (méterben; ha nem egész, akkor \".\"-zel add meg a tizedes jegyet)?: "))
    #power = float(input(f"Milyen teljesítményű a {device}?"))
    #frequency = float(input(f"Milyen frekvenciájú a {device}?"))
    muT = float(input(f"Milyen mágneses térerősségű a {device} (muT-ben)?: "))
    return device, num_devices, distance, muT

if __name__ == "__main__":
    device, num_devices, distance, muT = data_input()
    print(f"A {device} távolsága: {distance} m, a mágneses térerősség: {muT} muT")

