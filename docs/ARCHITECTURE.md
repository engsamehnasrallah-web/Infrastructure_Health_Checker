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

Responsible for:

- Application entry point
- Execute collectors

### **collectors/system.py**

Responsible for:

- Hostname detection
- Local IP detection
- Internet connectivity
- Operating system information

### **collectors/cpu.py**

Responsible for:

- CPU monitoring
- CPU information
- Per-core statistics

### **collectors/network.py**

Responsible for:

- Network interfaces
- TCP listening ports

### **collectors/services.py**

Responsible for:

- Linux services monitoring

### **collectors/docker.py**

Responsible for:

- Docker monitoring
---

### Next Refactoring Goal

Improve code reusability by introducing shared utility modules and centralized configuration management.

### Planned Refactoring

- Shared Utilities Module
- Configuration Manager
- Report Generator
- HTML Reporter
- JSON Reporter