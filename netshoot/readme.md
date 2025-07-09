## testowanie MacVLAN z `netshoot`

### 1. Uruchom kontener `netshoot` w tej samej sieci `macvlan`

```bash
docker run -it --rm \
  --network docker-static-bond0 \
  --ip 192.168.50.98 \
  nicolaka/netshoot
```

>  Uwaga: upewnij się, że adres IP `192.168.50.98` nie jest zajęty w Twojej sieci LAN.

Or use host net
```bash
docker run -it --rm   --network host --cap-add=NET_ADMIN  nicolaka/netshoot
```

---

### 2.  Wewnątrz kontenera `netshoot` wykonaj testy

#### ✅ Sprawdź UDP DNS:
```bash
dig google.com @8.8.8.8
```

#### ❌ Sprawdź TCP DNS:
```bash
dig +tcp google.com @8.8.8.8
```

#### 📡 Sprawdź porty:
```bash
nc -vz 8.8.8.8 53
```

#### 🔁 Sprawdź trasę:
```bash
traceroute 8.8.8.8
```

#### 📊 Sprawdź fragmentację i MTU:
```bash
ping -M do -s 1472 8.8.8.8
```

---

## 🧠 Co nam to powie?

| Wynik | Wniosek |
|-------|---------|
| ✅ UDP działa, ❌ TCP nie | Problem z routingiem TCP w `macvlan`/`bond0` |
| ❌ Oba nie działają | Problem z dostępem do Internetu z `macvlan` |
| ✅ Oba działają | Problem leży w konfiguracji Pi-hole, nie sieci |

---

## 🧩 Co dalej?

Jeśli TCP DNS nie działa również z `netshoot`, to mamy twardy dowód, że `balance-xor` + `macvlan` + Twój switch **nie radzą sobie z routingiem TCP**. Wtedy warto:

- Przełączyć bonding na `active-backup` (tryb 1),
- Lub zrezygnować z `macvlan` i użyć `host` lub `bridge` z port forwardingiem,
- Lub dodać dodatkowy interfejs `bridge` tylko dla Pi-hole.

---
