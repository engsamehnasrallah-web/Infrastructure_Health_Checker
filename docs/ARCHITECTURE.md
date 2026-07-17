# Project Architecture

Current Architecture

```
main.py
  │
  ▼
monitor.py
```

Responsibilites

- **main.py** -> Application entry point
- **monitor.py** -> Collects and displays infrastructure metrics

---

Future Architecture

```
main.py
│
├── collectors/
├── models/
├── reporters/
└── config/
```

the architecture will envolve as new monitoring modules are introduced.