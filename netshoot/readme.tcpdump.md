Investigate issues with Pihole on QNAP node. Things to check
- network BOND configuration
- PIHOLE configuration post upgrade 5 to 6 
- QNAP internal things 
`tcpdump` is an excellent tool to confirm whether TCP responses from the DNS server return via a different interface than they were sent, which would be evidence of asymmetric routing. Below are ready-made commands and instructions on how to perform this on a QNAP.

---

```bash
docker run -it --rm   --network host --cap-add=NET_ADMIN  nicolaka/netshoot
```

## 🧰 Step 1: Identify physical interfaces

From your earlier `ip a`, it appears that the NAS uses:

- `eth0` and `eth1` as physical interfaces (members of `bond0`)
- `bond0` as a logical interface (LAG)

---

## 🧪 Step 2: Run `tcpdump` on both interfaces

In two separate terminals (or in the background), run:

### 📥 On `eth0`:
```bash
sudo tcpdump -i eth0 tcp port 53 -n
```

### 📥 On `eth1`:
```bash
sudo tcpdump -i eth1 tcp port 53 -n
```

> If `tcpdump` is not installed, you can use the `netshoot` container with `--network host` and add `--cap-add=NET_ADMIN`.

---

## 🧪 Step 3: Perform a TCP DNS query in a third terminal

From the `netshoot` container (in `host` mode):

```bash
dig +tcp google.com @8.8.8.8
```

---

## 🔍 Step 4: Observe

Pay attention to:

- Which interface sends the `SYN` packet to 8.8.8.8:53
- Which interface (if any) receives the `SYN-ACK` response from 8.8.8.8

---

## 🧠 What might you find?

| Observation | Conclusion |
|-------------|------------|
| SYN and SYN-ACK on the same interface | Routing is OK |
| SYN leaves `eth0`, but SYN-ACK returns on `eth1` (or vice versa) | 🔥 Asymmetric routing — `balance-xor` is misrouting traffic |
| SYN is sent, but no SYN-ACK is received | Response is blocked or rejected by NAS/switch |

---

## 🧭 Next steps?

If you confirm asymmetry, you have solid proof that the `balance-xor` mode is the culprit. Switching to `active-backup` or changing the aggregation algorithm on the switch (`MAC SA & DA`) are the only viable solutions.


# ######################################

These `tcpdump` logs are absolutely conclusive. We have a **textbook case of asymmetric TCP routing**, which explains all the DNS over TCP issues in your environment.

---

## 🧠 What does `tcpdump` show?

### 🔍 On the `eth1` interface (outgoing):
- We see TCP `SYN` and `PUSH` packets from the NAS (192.168.50.247) to 8.8.8.8:53.
- The NAS is sending DNS queries over TCP correctly.

### 🔍 On the `eth0` interface (incoming):
- We see `SYN-ACK` responses from 8.8.8.8 to the NAS.
- But the NAS **does not respond** to these packets — no `ACK`, no further communication.

---

## 🔥 What does this mean?

- The `SYN` packet leaves via `eth1`, but the `SYN-ACK` response returns via `eth0`.
- The NAS (or its TCP/IP stack) **rejects the response** because it does not expect it on this interface.
- This is a classic symptom of **asymmetric routing**, which occurs in `balance-xor` mode with a suboptimal hashing algorithm.

---

## ✅ Confirmed diagnosis

> 🔴 Your NAS in `balance-xor` mode is splitting TCP packets inconsistently — sending via one interface and receiving via another. This breaks TCP session rules and causes DNS over TCP errors.

---

## 🛠️ What now?

### 🔧 Option 1: Change port aggregation mode on the switch

On the Zyxel switch, set the LAG algorithm to **MAC SA & DA** (source and destination MAC). This increases the likelihood that TCP packets and their responses follow the same path.

### 🔁 Option 2: Switch the NAS to `active-backup` mode

In the QNAP GUI:
- Control Panel → Network & Virtual Switch → Port Trunking
- Edit LAG → Mode: **Failover (Active-Backup)**

This **completely eliminates asymmetry** — only one interface is active, the other is on standby.

---

## 🧪 After the change:

- Restart `netshoot` in `host` mode
- Perform `dig +tcp google.com @8.8.8.8`
- If it works — problem solved

---

# Cclussions after GPT session
Non of the above was the main culprit. during upgrade pihole from 5 to 6 they added and by default enable IPV6. 
After disabling this feature Pihole log stopped logging issues. 