SERVICE_MAP = {
    22: "SSH",
    53: "DNS",
    80: "HTTP",
    443: "HTTPS",
    631: "IPP",
    3306: "MySQL",
    5432: "PostgreSQL",
    25: "SMTP",
    110: "POP3",
    143: "IMAP",
    465: "SMTPS",
    587: "SMTP Submission",
    993: "IMAPS",
    995: "POP3S",
    21: "FTP",
    20: "FTP Data",
    23: "Telnet",
    3389: "RDP",
    8080: "HTTP-Alt",
    27017: "MongoDB",
    6379: "Redis"
}

STATUS_MAP = {
                "active": "Running ✅",
                "inactive": "Stopped ❌",
                "failed": "Failed ❌",
                "unknown": "Not Installed ⚠️"
            }
