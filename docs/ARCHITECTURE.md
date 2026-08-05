# Project Architecture

Current Architecture

```
main.py
  │
  ▼
monitor.py
```

## Current Responsibilities

### **main.py**

- Application entry point
- Configuration loading
- Collector orchestration

### **collectors/**

Responsible for:

- CPU monitoring
- Memory monitoring
- Disk monitoring
- Hostname detection
- Local IP detection
- Internet connectivity check
- Linux service monitoring
- Docker monitoring
- TCP listening ports monitoring
- Operating system monitoring
- Network interface monitoring

### **config/**

Responsible for:

- Configuration loading
- Centralized constants
- Application settings

### **utils/**

Responsible for:

- Shared helper functions
- Common console formatting

---

### Next Refactoring Goal

Introduce Report models and Reporter modules for exporting monitoring results.

### Planned Refactoring

- Report Model
- JSON Reporter
- HTML Reporter
- Health Score Engine