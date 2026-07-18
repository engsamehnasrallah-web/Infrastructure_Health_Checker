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

### **monitor.py**
Responsible for:

- CPU monitoring
- Memory monitoring
- Disk monitoring
- Hostname detection
- Local IP detection
- Internet connectivity check
- Linux service monitoring
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

### Next Refactoring Goal

As the project grows, monitoring responsibilities will be separated into dedicated collector modules to improve maintainability.

### Planned Refactoring

Upcoming versions will separate infrastructure collectors into dedicated modules:

- Resource Collector
- Network Collector
- Service Collector
- Report Generator