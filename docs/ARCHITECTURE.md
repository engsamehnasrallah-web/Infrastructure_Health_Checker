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
- Docker Monitoring
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

As the project grows, monitoring components will be separated into dedicated modules:

- System Collector
- Network Collector
- Service Collector
- Docker Collector
- Report Generator