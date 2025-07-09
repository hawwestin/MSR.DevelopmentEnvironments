`tcpdump` to doskonałe narzędzie, żeby potwierdzić, czy odpowiedzi TCP z serwera DNS wracają innym interfejsem niż wyszły, co byłoby dowodem na asymetryczny routing. Poniżej masz gotowe komendy i instrukcje, jak to przeprowadzić na QNAP-ie.

---

```bash
docker run -it --rm   --network host --cap-add=NET_ADMIN  nicolaka/netshoot
```


## 🧰 Krok 1: Zidentyfikuj interfejsy fizyczne

Z Twojego wcześniejszego `ip a` wynika, że NAS używa:

- `eth0` i `eth1` jako interfejsy fizyczne (członkowie `bond0`)
- `bond0` jako interfejs logiczny (LAG)

---

## 🧪 Krok 2: Uruchom `tcpdump` na obu interfejsach

W dwóch osobnych terminalach (lub w tle), uruchom:

### 📥 Na `eth0`:
```bash
sudo tcpdump -i eth0 tcp port 53 -n
```

### 📥 Na `eth1`:
```bash
sudo tcpdump -i eth1 tcp port 53 -n
```

> Jeśli `tcpdump` nie jest zainstalowany, możesz użyć kontenera `netshoot` z `--network host` i dodać `--cap-add=NET_ADMIN`.

---

## 🧪 Krok 3: W trzecim terminalu wykonaj zapytanie TCP DNS

Z kontenera `netshoot` (w trybie `host`):

```bash
dig +tcp google.com @8.8.8.8
```

---

## 🔍 Krok 4: Obserwuj

Zwróć uwagę na:

- Na którym interfejsie wychodzi pakiet `SYN` do 8.8.8.8:53
- Na którym interfejsie (jeśli w ogóle) pojawia się odpowiedź `SYN-ACK` z 8.8.8.8

---

## 🧠 Co może się okazać?

| Obserwacja | Wniosek |
|------------|---------|
| SYN i SYN-ACK na tym samym interfejsie | Routing OK |
| SYN wychodzi `eth0`, ale SYN-ACK wraca `eth1` (lub odwrotnie) | 🔥 Asymetryczny routing — `balance-xor` źle rozdziela ruch |
| SYN wychodzi, ale brak SYN-ACK | Odpowiedź zablokowana lub odrzucona przez NAS/switch |

---

## 🧭 Co dalej?

Jeśli potwierdzisz asymetrię, to masz twardy dowód, że tryb `balance-xor` jest winny. Wtedy przełączenie na `active-backup` lub zmiana algorytmu agregacji na switchu (`MAC SA & DA`) to jedyne sensowne rozwiązania.

Chcesz, żebym pomógł Ci zinterpretować wynik `tcpdump`, jeśli go wrzucisz tutaj?

# ######################################

Doskonała robota, Michał — te logi z `tcpdump` są absolutnie jednoznaczne. Mamy tu **książkowy przypadek asymetrycznego routingu TCP**, który tłumaczy wszystkie problemy z DNS przez TCP w Twoim środowisku.

---

## 🧠 Co pokazuje `tcpdump`?

### 🔍 Na interfejsie `eth1` (wychodzące):
- Widzimy pakiety TCP `SYN` i `PUSH` z NAS-a (192.168.50.247) do 8.8.8.8:53.
- NAS wysyła zapytania DNS przez TCP poprawnie.

### 🔍 Na interfejsie `eth0` (przychodzące):
- Widzimy odpowiedzi `SYN-ACK` z 8.8.8.8 do NAS-a.
- Ale NAS **nie odpowiada** na te pakiety — nie ma `ACK`, nie ma dalszej komunikacji.

---

## 🔥 Co to oznacza?

- Pakiet `SYN` wychodzi przez `eth1`, ale odpowiedź `SYN-ACK` wraca przez `eth0`.
- NAS (lub jego stos TCP/IP) **odrzuca odpowiedź**, bo nie spodziewa się jej na tym interfejsie.
- To klasyczny objaw **asymetrycznego routingu**, który występuje w trybie `balance-xor` przy nieoptymalnym algorytmie haszowania.

---

## ✅ Potwierdzona diagnoza

> 🔴 Twój NAS w trybie `balance-xor` rozdziela pakiety TCP w sposób niespójny — wysyła jednym interfejsem, a odbiera drugim. To łamie zasady sesji TCP i powoduje błędy DNS przez TCP.

---

## 🛠️ Co teraz?

### 🔧 Opcja 1: Zmień tryb agregacji portów na switchu

Na switchu Zyxel ustaw algorytm LAG na **MAC SA & DA** (źródłowy i docelowy MAC). To zwiększa szansę, że pakiety TCP i ich odpowiedzi trafią tą samą ścieżką.

### 🔁 Opcja 2: Przełącz NAS na tryb `active-backup`

W QNAP GUI:
- Panel Sterowania → Sieć i Przełącznik → Port Trunking
- Edytuj LAG → Tryb: **Failover (Active-Backup)**

To **eliminuje całkowicie asymetrię** — tylko jeden interfejs aktywny, drugi w zapasie.

---

## 🧪 Po zmianie:

- Uruchom ponownie `netshoot` w trybie `host`
- Wykonaj `dig +tcp google.com @8.8.8.8`
- Jeśli działa — problem rozwiązany

---

Chcesz, żebym przygotował checklistę kroków w QNAP GUI lub pomógł Ci przetestować inne konfiguracje bonding?