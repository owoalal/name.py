import os
import glob
import json
import subprocess
import re
import psutil
import requests
import webbrowser
import urllib.parse
import platform  # Added missing import
from datetime import datetime, timedelta
from collections import defaultdict, Counter
import traceback

# COMPLETE ERROR_DB DICTIONARY FIRST
ERROR_DB = {
    "0": {"name": "STATUS_SUCCESS", "description": "Operation completed successfully", "severity": "INFO",
          "common_causes": ["Normal operation"], "troubleshooting": ["No action required"]},
    "1": {"name": "ERROR_INVALID_FUNCTION", "description": "Incorrect function", "severity": "ERROR",
          "common_causes": ["Invalid API call", "Corrupted system files"],
          "troubleshooting": ["Run sfc /scannow", "Check application compatibility"]},
    "2": {"name": "ERROR_FILE_NOT_FOUND", "description": "System cannot find the file specified", "severity": "ERROR",
          "common_causes": ["Missing files", "Corrupted installation"],
          "troubleshooting": ["Reinstall application", "Check file paths"]},
    "3": {"name": "ERROR_PATH_NOT_FOUND", "description": "System cannot find the path specified", "severity": "ERROR",
          "common_causes": ["Invalid directory", "Network path issues"],
          "troubleshooting": ["Verify paths", "Check network connectivity"]},
    "5": {"name": "ERROR_ACCESS_DENIED", "description": "Access is denied", "severity": "ERROR",
          "common_causes": ["Insufficient permissions", "File in use"],
          "troubleshooting": ["Run as administrator", "Check file permissions"]},
    "6": {"name": "ERROR_INVALID_HANDLE", "description": "Handle is invalid", "severity": "ERROR",
          "common_causes": ["Programming error", "System corruption"],
          "troubleshooting": ["Update application", "System file check"]},
    "8": {"name": "ERROR_NOT_ENOUGH_MEMORY", "description": "Not enough storage available", "severity": "CRITICAL",
          "common_causes": ["Memory leak", "Insufficient RAM"],
          "troubleshooting": ["Add more RAM", "Close unnecessary programs", "Check for memory leaks"]},
    "9": {"name": "ERROR_INVALID_BLOCK", "description": "Storage control block destroyed", "severity": "CRITICAL",
          "common_causes": ["Memory corruption", "Hardware failure"],
          "troubleshooting": ["Memory test", "Hardware diagnostics"]},
    "10": {"name": "ERROR_BAD_ENVIRONMENT", "description": "Environment is incorrect", "severity": "WARNING",
           "common_causes": ["Environment variable issues"],
           "troubleshooting": ["Check environment variables", "Restart system"]},
    "11": {"name": "ERROR_BAD_FORMAT", "description": "Attempt to load program with incorrect format",
           "severity": "ERROR", "common_causes": ["32/64-bit mismatch", "Corrupted executable"],
           "troubleshooting": ["Check architecture compatibility", "Reinstall program"]},
    "14": {"name": "ERROR_OUTOFMEMORY", "description": "Not enough storage available", "severity": "CRITICAL",
           "common_causes": ["Memory exhaustion", "Memory fragmentation"],
           "troubleshooting": ["Increase virtual memory", "Add physical RAM", "Close applications"]},
    "15": {"name": "ERROR_INVALID_DRIVE", "description": "System cannot find the drive specified", "severity": "ERROR",
           "common_causes": ["Drive disconnected", "Drive letter changed"],
           "troubleshooting": ["Check drive connections", "Verify drive letters"]},
    "18": {"name": "ERROR_NO_MORE_FILES", "description": "No more files found", "severity": "INFO",
           "common_causes": ["End of file list"], "troubleshooting": ["Normal operation"]},
    "21": {"name": "ERROR_NOT_READY", "description": "Device is not ready", "severity": "WARNING",
           "common_causes": ["Hardware not ready", "Driver issues"],
           "troubleshooting": ["Check device status", "Update drivers"]},
    "23": {"name": "ERROR_CRC", "description": "Data error (cyclic redundancy check)", "severity": "CRITICAL",
           "common_causes": ["Disk corruption", "Hardware failure"],
           "troubleshooting": ["Run chkdsk", "Replace drive", "Check cables"]},
    "32": {"name": "ERROR_SHARING_VIOLATION", "description": "Process cannot access file because it is being used",
           "severity": "WARNING", "common_causes": ["File in use", "Lock not released"],
           "troubleshooting": ["Close applications", "Restart system", "Check file locks"]},
    "33": {"name": "ERROR_LOCK_VIOLATION",
           "description": "Process cannot access file because another process has locked it", "severity": "WARNING",
           "common_causes": ["File locked by process"],
           "troubleshooting": ["Identify locking process", "Close applications"]},
    "39": {"name": "ERROR_DISK_FULL", "description": "Disk is full", "severity": "CRITICAL",
           "common_causes": ["No disk space"],
           "troubleshooting": ["Free disk space", "Clean temporary files", "Move files to other drives"]},
    "50": {"name": "ERROR_NOT_SUPPORTED", "description": "Request not supported", "severity": "ERROR",
           "common_causes": ["Feature not available", "Driver limitations"],
           "troubleshooting": ["Update drivers", "Check system requirements"]},
    "53": {"name": "ERROR_BAD_NETPATH", "description": "Network path not found", "severity": "ERROR",
           "common_causes": ["Network connectivity", "Server unavailable"],
           "troubleshooting": ["Check network connection", "Verify server status"]},
    "55": {"name": "ERROR_NETWORK_BUSY", "description": "Network resource busy", "severity": "WARNING",
           "common_causes": ["Network congestion"], "troubleshooting": ["Retry operation", "Check network load"]},
    "64": {"name": "ERROR_NETNAME_DELETED", "description": "Specified network name no longer available",
           "severity": "ERROR", "common_causes": ["Network disconnection"],
           "troubleshooting": ["Reconnect to network", "Check network settings"]},
    "65": {"name": "ERROR_NETWORK_ACCESS_DENIED", "description": "Network access denied", "severity": "ERROR",
           "common_causes": ["Authentication failure", "Permissions"],
           "troubleshooting": ["Check credentials", "Verify permissions"]},
    "67": {"name": "ERROR_BAD_NET_NAME", "description": "Network name cannot be found", "severity": "ERROR",
           "common_causes": ["Invalid network path"],
           "troubleshooting": ["Verify network path", "Check DNS resolution"]},
    "87": {"name": "ERROR_INVALID_PARAMETER", "description": "Parameter is incorrect", "severity": "ERROR",
           "common_causes": ["Programming error", "Invalid input"],
           "troubleshooting": ["Check application parameters", "Update software"]},
    "112": {"name": "ERROR_DISK_FULL", "description": "Not enough space on disk", "severity": "CRITICAL",
            "common_causes": ["Disk full"], "troubleshooting": ["Free disk space", "Clean temporary files"]},
    "122": {"name": "ERROR_INSUFFICIENT_BUFFER", "description": "Data area passed too small", "severity": "ERROR",
            "common_causes": ["Buffer overflow", "Programming error"],
            "troubleshooting": ["Update application", "Check system resources"]},
    "123": {"name": "ERROR_INVALID_NAME", "description": "Filename, directory name, or volume label syntax incorrect",
            "severity": "ERROR", "common_causes": ["Invalid characters", "Path too long"],
            "troubleshooting": ["Check filename validity", "Shorten paths"]},
    "127": {"name": "ERROR_PROC_NOT_FOUND", "description": "Specified procedure could not be found",
            "severity": "ERROR", "common_calls": ["Missing DLL functions"],
            "troubleshooting": ["Reinstall application", "Update system libraries"]},
    "183": {"name": "ERROR_ALREADY_EXISTS", "description": "Cannot create file when it already exists",
            "severity": "WARNING", "common_causes": ["File already exists"],
            "troubleshooting": ["Delete existing file", "Use different filename"]},
    "193": {"name": "ERROR_BAD_EXE_FORMAT", "description": "Not valid Win32 application", "severity": "ERROR",
            "common_causes": ["Corrupted executable", "Architecture mismatch"],
            "troubleshooting": ["Reinstall application", "Check system architecture"]},
    "259": {"name": "ERROR_NO_MORE_ITEMS", "description": "No more data available", "severity": "INFO",
            "common_causes": ["End of enumeration"], "troubleshooting": ["Normal operation"]},
    "995": {"name": "ERROR_OPERATION_ABORTED", "description": "I/O operation aborted", "severity": "WARNING",
            "common_causes": ["Operation cancelled", "System shutdown"],
            "troubleshooting": ["Retry operation", "Check system state"]},
    "996": {"name": "ERROR_IO_INCOMPLETE", "description": "Overlapped I/O event not in signaled state",
            "severity": "WARNING", "common_causes": ["Async operation pending"],
            "troubleshooting": ["Wait for completion", "Check I/O status"]},
    "997": {"name": "ERROR_IO_PENDING", "description": "Overlapped I/O operation in progress", "severity": "INFO",
            "common_causes": ["Async operation"], "troubleshooting": ["Wait for completion"]},
    "1114": {"name": "ERROR_DLL_INIT_FAILED", "description": "DLL initialization routine failed",
             "severity": "CRITICAL", "common_causes": ["DLL corruption", "Missing dependencies"],
             "troubleshooting": ["Reinstall application", "Register DLLs", "Check dependencies"]},
    "1115": {"name": "ERROR_SHUTDOWN_IN_PROGRESS", "description": "Shutdown in progress", "severity": "INFO",
             "common_causes": ["System shutdown"], "troubleshooting": ["Wait for shutdown completion"]},
    "1117": {"name": "ERROR_IO_DEVICE", "description": "I/O device error", "severity": "CRITICAL",
             "common_causes": ["Hardware failure", "Driver issues"],
             "troubleshooting": ["Check hardware connections", "Update drivers", "Replace device"]},
    "1200": {"name": "ERROR_BAD_DEVICE", "description": "Invalid device name", "severity": "ERROR",
             "common_causes": ["Device not found"],
             "troubleshooting": ["Check device name", "Verify device installation"]},
    "1450": {"name": "ERROR_NO_SYSTEM_RESOURCES", "description": "Insufficient system resources",
             "severity": "CRITICAL", "common_causes": ["Resource exhaustion"],
             "troubleshooting": ["Close applications", "Increase system resources", "Restart system"]},
    "1460": {"name": "ERROR_TIMEOUT", "description": "Operation timed out", "severity": "WARNING",
             "common_causes": ["Slow response", "Network issues"],
             "troubleshooting": ["Increase timeout", "Check network connectivity"]},
    "1722": {"name": "RPC_S_SERVER_UNAVAILABLE", "description": "RPC server unavailable", "severity": "ERROR",
             "common_causes": ["Service not running", "RPC issues"],
             "troubleshooting": ["Start required services", "Check RPC configuration"]},
    "41": {"name": "Kernel-Power", "description": "System rebooted without clean shutdown", "severity": "CRITICAL",
           "common_causes": ["Power supply failure", "Overheating", "Driver incompatibility", "System instability",
                             "Memory issues"],
           "troubleshooting": ["Check PSU", "Monitor temperatures", "Update BIOS", "Reset overclocking", "Test memory",
                               "Check power connections"]},
    "1001": {"name": "Windows Error Reporting", "description": "Blue screen crash reported", "severity": "CRITICAL",
             "common_causes": ["Driver conflicts", "Hardware failures", "System service exceptions", "Memory issues"],
             "troubleshooting": ["Analyze minidumps", "Update drivers", "Test hardware", "Check temperatures",
                                 "Review recent changes"]},
    "1000": {"name": "Application Error", "description": "Application crash or fault", "severity": "WARNING",
             "common_causes": ["Software bugs", "Corrupted files", "Missing dependencies", "Resource exhaustion"],
             "troubleshooting": ["Update application", "Check Windows Updates", "Compatibility mode",
                                 "Check resources"]},
    "7034": {"name": "Service Control Manager", "description": "Service terminated unexpectedly", "severity": "WARNING",
             "common_causes": ["Service dependencies", "Corrupted files", "Resource issues", "Service conflicts"],
             "troubleshooting": ["Check dependencies", "Review logs", "Restart services", "Check resources"]},
    "6008": {"name": "EventLog", "description": "Previous system shutdown was unexpected", "severity": "CRITICAL",
             "common_causes": ["Power failure", "System crash", "Hardware issues"],
             "troubleshooting": ["Check power supply", "Review crash logs", "Hardware diagnostics"]},
    "6009": {"name": "EventLog", "description": "System started", "severity": "INFO", "common_causes": ["Normal boot"],
             "troubleshooting": ["No action required"]},
    "6013": {"name": "EventLog", "description": "System uptime", "severity": "INFO",
             "common_causes": ["Normal operation"], "troubleshooting": ["No action required"]},
    "10016": {"name": "DistributedCOM", "description": "DCOM permission error", "severity": "WARNING",
              "common_causes": ["Permission issues", "Service configuration"],
              "troubleshooting": ["Configure DCOM permissions", "Check service accounts"]},
    "10028": {"name": "DistributedCOM", "description": "DCOM server start failure", "severity": "ERROR",
              "common_causes": ["Service startup issues"],
              "troubleshooting": ["Check service configuration", "Verify permissions"]},
    "4634": {"name": "Security", "description": "Account logged off", "severity": "INFO",
             "common_causes": ["Normal logoff"], "troubleshooting": ["No action required"]},
    "4624": {"name": "Security", "description": "Account successfully logged on", "severity": "INFO",
             "common_causes": ["Normal logon"], "troubleshooting": ["No action required"]},
    "4625": {"name": "Security", "description": "Account failed to log on", "severity": "WARNING",
             "common_causes": ["Wrong credentials", "Account locked"],
             "troubleshooting": ["Check credentials", "Unlock account"]},
    "0x0000000A": {"name": "IRQL_NOT_LESS_OR_EQUAL",
                   "description": "Kernel accessed pageable memory at inappropriate IRQL", "severity": "CRITICAL",
                   "common_causes": ["Faulty RAM", "Driver issues", "Hardware conflicts", "Overclocking"],
                   "troubleshooting": ["Memory test", "Reset BIOS", "Update drivers", "Check hardware"]},
    "0x0000001E": {"name": "KMODE_EXCEPTION_NOT_HANDLED", "description": "Kernel-mode exception not handled",
                   "severity": "CRITICAL",
                   "common_causes": ["Hardware failure", "Driver corruption", "System file corruption", "Overclocking"],
                   "troubleshooting": ["Hardware diagnostics", "Memory test", "Update BIOS", "System file check",
                                       "CPU stress test"]},
    "0x00000050": {"name": "PAGE_FAULT_IN_NONPAGED_AREA", "description": "Invalid system memory referenced",
                   "severity": "CRITICAL", "common_causes": ["Defective RAM", "Driver issues", "Antivirus conflicts"],
                   "troubleshooting": ["Memory test", "Update drivers", "Disable antivirus temporarily"]},
    "0x0000007E": {"name": "SYSTEM_THREAD_EXCEPTION_NOT_HANDLED", "description": "System thread exception not handled",
                   "severity": "CRITICAL",
                   "common_causes": ["Faulty hardware", "Driver issues", "Corrupted system files", "Graphics issues"],
                   "troubleshooting": ["Memory diagnostics", "Update drivers", "System file check", "Disk check",
                                       "Minimal hardware test"]},
    "0x0000007F": {"name": "UNEXPECTED_KERNEL_MODE_TRAP",
                   "description": "Hardware malfunction or system software error", "severity": "CRITICAL",
                   "common_causes": ["Hardware failure", "Overheating", "Overclocking", "Power issues"],
                   "troubleshooting": ["Hardware diagnostics", "Temperature check", "Reset overclocking",
                                       "Check power supply"]},
    "0x000000D1": {"name": "DRIVER_IRQL_NOT_LESS_OR_EQUAL", "description": "Driver accessed improper memory address",
                   "severity": "CRITICAL",
                   "common_causes": ["Faulty drivers", "Hardware conflicts", "System file corruption",
                                     "Security software"],
                   "troubleshooting": ["Update drivers", "Check Device Manager", "Memory diagnostics",
                                       "Disable antivirus", "Driver verifier"]},
    "0x000000BE": {"name": "ATTEMPTED_WRITE_TO_READONLY_MEMORY",
                   "description": "Driver attempted to write to read-only memory", "severity": "CRITICAL",
                   "common_causes": ["Faulty drivers", "Memory corruption"],
                   "troubleshooting": ["Update drivers", "Memory test", "System file check"]},
    "0x000000C2": {"name": "BAD_POOL_CALLER", "description": "Kernel pool corruption", "severity": "CRITICAL",
                   "common_causes": ["Driver issues", "System file corruption"],
                   "troubleshooting": ["Update drivers", "System file check", "Driver verifier"]},
    "0x000000C5": {"name": "DRIVER_CORRUPTED_EXPOOL", "description": "Driver corrupted system pool",
                   "severity": "CRITICAL", "common_causes": ["Driver corruption", "Memory issues"],
                   "troubleshooting": ["Update drivers", "Memory test", "System diagnostics"]},
    "0x000000D8": {"name": "DRIVER_USED_EXCESSIVE_PTES", "description": "Driver used excessive system PTEs",
                   "severity": "CRITICAL", "common_causes": ["Driver memory leak", "System resource exhaustion"],
                   "troubleshooting": ["Update drivers", "Increase system resources", "Driver diagnostics"]},
    "0x000000EA": {"name": "THREAD_STUCK_IN_DEVICE_DRIVER", "description": "Device driver stuck in infinite loop",
                   "severity": "CRITICAL", "common_causes": ["Graphics driver issues", "Hardware problems"],
                   "troubleshooting": ["Update graphics drivers", "Check display hardware", "Temperature monitoring"]},
    "0x000000F4": {"name": "CRITICAL_OBJECT_TERMINATION", "description": "Critical system process terminated",
                   "severity": "CRITICAL", "common_causes": ["System corruption", "Malware", "Hardware failure"],
                   "troubleshooting": ["Malware scan", "System file check", "Hardware diagnostics", "System restore"]},
    "0x00000124": {"name": "WHEA_UNCORRECTABLE_ERROR", "description": "Hardware error detected", "severity": "CRITICAL",
                   "common_causes": ["CPU failure", "Memory failure", "Overheating", "Power issues"],
                   "troubleshooting": ["Hardware diagnostics", "Temperature check", "Memory test", "CPU test",
                                       "Check power supply"]},
    "0x0000009F": {"name": "DRIVER_POWER_STATE_FAILURE",
                   "description": "Driver failed to complete power state transition", "severity": "CRITICAL",
                   "common_causes": ["Power management issues", "Driver problems"],
                   "troubleshooting": ["Update drivers", "Check power settings", "Disable power management"]},
    "0x000000A5": {"name": "ACPI_BIOS_ERROR", "description": "ACPI BIOS error", "severity": "CRITICAL",
                   "common_causes": ["BIOS issues", "ACPI problems"],
                   "troubleshooting": ["Update BIOS", "Check ACPI settings", "Hardware compatibility"]},
    "0x00000133": {"name": "DPC_WATCHDOG_VIOLATION", "description": "DPC routine exceeded time limit",
                   "severity": "CRITICAL", "common_causes": ["Driver issues", "Hardware problems"],
                   "troubleshooting": ["Update drivers", "Hardware diagnostics", "Check interrupts"]},
    "0x0000013A": {"name": "KERNEL_MODE_HEAP_CORRUPTION", "description": "Kernel heap corruption detected",
                   "severity": "CRITICAL", "common_causes": ["Driver corruption", "Memory issues"],
                   "troubleshooting": ["Update drivers", "Memory test", "System diagnostics"]},
    "0x0000014C": {"name": "THREAD_TERMINATE_HELD_MUTEX", "description": "Thread terminated while holding mutex",
                   "severity": "CRITICAL", "common_causes": ["Driver issues", "System corruption"],
                   "troubleshooting": ["Update drivers", "System file check", "Hardware test"]},
    "0x00000154": {"name": "SYSTEM_SCAN_AT_RAISED_IRQL_CAUGHT_IMPROPER_DRIVER_UNLOAD",
                   "description": "Driver unloaded improperly", "severity": "CRITICAL",
                   "common_causes": ["Driver issues"],
                   "troubleshooting": ["Update drivers", "Driver verifier", "System diagnostics"]},
    "0x0000015E": {"name": "BUGCODE_NDIS_DRIVER", "description": "Network driver error", "severity": "CRITICAL",
                   "common_causes": ["Network driver issues"],
                   "troubleshooting": ["Update network drivers", "Network diagnostics", "Hardware check"]},
    "0x0000016C": {"name": "INVALID_RUNDOWN_PROTECTION_FLAGS", "description": "Invalid rundown protection flags",
                   "severity": "CRITICAL", "common_causes": ["Driver issues", "System corruption"],
                   "troubleshooting": ["Update drivers", "System file check", "Hardware diagnostics"]},
    "0x0000019C": {"name": "WIN32K_SECURITY_FAILURE", "description": "Win32k security failure", "severity": "CRITICAL",
                   "common_causes": ["Security issues", "System corruption"],
                   "troubleshooting": ["System file check", "Security scan", "System restore"]},
    "0x000001A0": {"name": "TTM_FATAL_ERROR", "description": "Terminal timeout manager fatal error",
                   "severity": "CRITICAL", "common_causes": ["System issues", "Driver problems"],
                   "troubleshooting": ["Update drivers", "System diagnostics", "Hardware check"]},
    "0x000001C4": {"name": "DRIVER_VERIFIER_DETECTED_VIOLATION", "description": "Driver verifier detected violation",
                   "severity": "CRITICAL", "common_causes": ["Driver issues"],
                   "troubleshooting": ["Update drivers", "Driver verifier analysis", "Remove problematic drivers"]},
    "0x000001C5": {"name": "IO_THREAD_CREATION_FAILED", "description": "I/O thread creation failed",
                   "severity": "CRITICAL", "common_causes": ["Resource exhaustion", "System corruption"],
                   "troubleshooting": ["Increase resources", "System file check", "Memory test"]},
    "0x000001CA": {"name": "SYSTEM_THREAD_EXCEPTION_NOT_HANDLED_M",
                   "description": "System thread exception not handled", "severity": "CRITICAL",
                   "common_causes": ["Driver issues", "Hardware problems"],
                   "troubleshooting": ["Update drivers", "Hardware diagnostics", "System check"]},
    "0x000001CC": {"name": "PAGE_FAULT_IN_FREED_SPECIAL_POOL", "description": "Page fault in freed special pool",
                   "severity": "CRITICAL", "common_causes": ["Driver corruption", "Memory issues"],
                   "troubleshooting": ["Update drivers", "Memory test", "Driver verifier"]},
    "0x000001D3": {"name": "WDF_VIOLATION", "description": "Windows Driver Framework violation", "severity": "CRITICAL",
                   "common_causes": ["WDF driver issues"],
                   "troubleshooting": ["Update WDF drivers", "Driver diagnostics", "System check"]},
    "0x000001D5": {"name": "DRIVER_PNP_WATCHDOG", "description": "PnP driver watchdog timeout", "severity": "CRITICAL",
                   "common_causes": ["PnP driver issues"],
                   "troubleshooting": ["Update PnP drivers", "Hardware check", "System diagnostics"]},
    "0x000001D8": {"name": "SYSTEM_SCAN_AT_RAISED_IRQL_CAUGHT_IMPROPER_DRIVER",
                   "description": "Improper driver behavior at raised IRQL", "severity": "CRITICAL",
                   "common_causes": ["Driver issues"],
                   "troubleshooting": ["Update drivers", "Driver verifier", "System diagnostics"]},
    "0x000001DB": {"name": "UART_LIVEDUMP_SECONDARY_DATA", "description": "UART live dump secondary data",
                   "severity": "CRITICAL", "common_causes": ["Hardware issues"],
                   "troubleshooting": ["Hardware diagnostics", "System check"]},
    "0x000001DC": {"name": "INVALID_SLOT_ALLOCATOR_FLAGS", "description": "Invalid slot allocator flags",
                   "severity": "CRITICAL", "common_causes": ["System corruption"],
                   "troubleshooting": ["System file check", "Memory test", "System restore"]},
    "0x000001E3": {"name": "BLUETOOTH_ERROR_RECOVERY_LIVEDUMP", "description": "Bluetooth error recovery",
                   "severity": "WARNING", "common_causes": ["Bluetooth issues"],
                   "troubleshooting": ["Update Bluetooth drivers", "Reset Bluetooth", "Hardware check"]},
    "0x000001E7": {"name": "INVALID_CALLBACK_STACK_ADDRESS", "description": "Invalid callback stack address",
                   "severity": "CRITICAL", "common_causes": ["Driver issues", "System corruption"],
                   "troubleshooting": ["Update drivers", "System file check", "Memory test"]},
    "0x000001E8": {"name": "INVALID_KERNEL_STACK_ADDRESS", "description": "Invalid kernel stack address",
                   "severity": "CRITICAL", "common_causes": ["System corruption", "Memory issues"],
                   "troubleshooting": ["Memory test", "System file check", "Hardware diagnostics"]},
    "0x000001E9": {"name": "INVALID_AFFINITY_SET", "description": "Invalid affinity set", "severity": "CRITICAL",
                   "common_causes": ["System issues"],
                   "troubleshooting": ["System diagnostics", "Hardware check", "Update drivers"]},
    "0x000001EA": {"name": "INVALID_IDLE_STATE", "description": "Invalid idle state", "severity": "CRITICAL",
                   "common_causes": ["Power management issues"],
                   "troubleshooting": ["Update drivers", "Check power settings", "BIOS update"]},
    "0x000001EB": {"name": "INVALID_PUSH_LOCK_FLAGS", "description": "Invalid push lock flags", "severity": "CRITICAL",
                   "common_causes": ["System corruption"],
                   "troubleshooting": ["System file check", "Memory test", "System restore"]},
    "0x000001EC": {"name": "INVALID_LOCK_SEQUENCE", "description": "Invalid lock sequence", "severity": "CRITICAL",
                   "common_causes": ["Driver issues"],
                   "troubleshooting": ["Update drivers", "Driver verifier", "System diagnostics"]},
    "0x000001ED": {"name": "INVALID_MDLCOMPLETE_FLAGS", "description": "Invalid MDL complete flags",
                   "severity": "CRITICAL", "common_causes": ["Driver issues"],
                   "troubleshooting": ["Update drivers", "System diagnostics", "Hardware check"]},
    "0x000001EE": {"name": "INVALID_MDL_RANGE", "description": "Invalid MDL range", "severity": "CRITICAL",
                   "common_causes": ["Driver issues", "Memory corruption"],
                   "troubleshooting": ["Update drivers", "Memory test", "System check"]},
    "0x000001EF": {"name": "VHD_BOOT_INITIALIZATION_FAILED", "description": "VHD boot initialization failed",
                   "severity": "CRITICAL", "common_causes": ["VHD issues", "Boot problems"],
                   "troubleshooting": ["Check VHD integrity", "Boot repair", "System restore"]},
    "0x000001F0": {"name": "DYNAMIC_ADD_PROCESSOR_MISMATCH", "description": "Dynamic processor add mismatch",
                   "severity": "CRITICAL", "common_causes": ["Hardware configuration"],
                   "troubleshooting": ["Check hardware configuration", "BIOS update", "System diagnostics"]},
    "0x000001F1": {"name": "INVALID_EXTENDED_PROCESSOR_STATE", "description": "Invalid extended processor state",
                   "severity": "CRITICAL", "common_causes": ["Processor issues"],
                   "troubleshooting": ["CPU diagnostics", "BIOS update", "Hardware check"]},
    "0x000001F2": {"name": "INVALID_CALLBACK_FUNCTION", "description": "Invalid callback function",
                   "severity": "CRITICAL", "common_causes": ["Driver issues"],
                   "troubleshooting": ["Update drivers", "System diagnostics", "Driver verifier"]},
    "0x000001F3": {"name": "INVALID_IMAGE_WIN32K_SYS", "description": "Invalid Win32k system image",
                   "severity": "CRITICAL", "common_causes": ["System corruption"],
                   "troubleshooting": ["System file check", "Windows repair", "System restore"]},
    "0x000001F4": {"name": "TELEMETRY_ASSERTS_LIVEDUMP", "description": "Telemetry asserts live dump",
                   "severity": "WARNING", "common_causes": ["System monitoring"],
                   "troubleshooting": ["System diagnostics", "Check telemetry settings"]},
    "0x000001F5": {"name": "INVALID_FIBER_SWITCH_TARGET", "description": "Invalid fiber switch target",
                   "severity": "CRITICAL", "common_causes": ["System issues"],
                   "troubleshooting": ["System diagnostics", "Update drivers", "Hardware check"]},
    "0x000001F6": {"name": "INVALID_PLXSEC_CONTEXT", "description": "Invalid PLX security context",
                   "severity": "CRITICAL", "common_causes": ["Security issues"],
                   "troubleshooting": ["Security diagnostics", "System check", "Update drivers"]},
    "0x000001F7": {"name": "INVALID_STALKER_VALUE", "description": "Invalid stalker value", "severity": "CRITICAL",
                   "common_causes": ["System corruption"],
                   "troubleshooting": ["System file check", "Memory test", "System restore"]},
    "0x000001F8": {"name": "INVALID_DMA_PROTECTION_FLAGS", "description": "Invalid DMA protection flags",
                   "severity": "CRITICAL", "common_causes": ["Hardware issues"],
                   "troubleshooting": ["Hardware diagnostics", "Update drivers", "System check"]},
    "0x000001F9": {"name": "INVALID_HIBERNATE_ZERO_FLAGS", "description": "Invalid hibernate zero flags",
                   "severity": "CRITICAL", "common_causes": ["Hibernation issues"],
                   "troubleshooting": ["Disable hibernation", "System diagnostics", "Power settings"]},
    "0x000001FA": {"name": "INVALID_MEMORY_ALLOCATION_FLAGS", "description": "Invalid memory allocation flags",
                   "severity": "CRITICAL", "common_causes": ["Memory management"],
                   "troubleshooting": ["Memory test", "System diagnostics", "Update drivers"]},
    "0x000001FB": {"name": "INVALID_MEMORY_REFERENCE", "description": "Invalid memory reference",
                   "severity": "CRITICAL", "common_causes": ["Memory corruption"],
                   "troubleshooting": ["Memory test", "System file check", "Hardware diagnostics"]},
    "0x000001FC": {"name": "INVALID_THREAD_REFERENCE", "description": "Invalid thread reference",
                   "severity": "CRITICAL", "common_causes": ["System issues"],
                   "troubleshooting": ["System diagnostics", "Update drivers", "Memory test"]},
    "0x000001FD": {"name": "INVALID_PROCESS_DETACH_ATTEMPT", "description": "Invalid process detach attempt",
                   "severity": "CRITICAL", "common_causes": ["Process management"],
                   "troubleshooting": ["System diagnostics", "Update software", "System check"]},
    "0x000001FE": {"name": "INVALID_MDL_FLAGS", "description": "Invalid MDL flags", "severity": "CRITICAL",
                   "common_causes": ["Driver issues"],
                   "troubleshooting": ["Update drivers", "System diagnostics", "Hardware check"]},
    "0x000001FF": {"name": "INVALID_PARAMETER_MIX", "description": "Invalid combination of parameters passed",
                   "severity": "CRITICAL", "common_causes": ["Programming error", "System corruption"],
                   "troubleshooting": ["Update software", "System file check", "Debug application"]}
}

try:
    import win32evtlog
    import win32evtlogutil
    import win32api
    import win32con
    import win32service
    import win32security
    import win32net
    import win32file
    import win32gui
    import win32process
    import wmi
    WIN32_AVAILABLE = True
except ImportError:
    WIN32_AVAILABLE = False
    print("⚠️  Win32 modules not available. Some features will be limited.")






def get_system_info():
    """Collect comprehensive system information"""
    info = {}
    try:
        # Basic system info
        info['os'] = f"{os.name} {platform.system()} {platform.release()}"
        info['processor'] = platform.processor()
        info['architecture'] = platform.architecture()[0]

        # Memory information
        mem = psutil.virtual_memory()
        info['memory'] = {
            'total': f"{mem.total / (1024 ** 3):.2f} GB",
            'available': f"{mem.available / (1024 ** 3):.2f} GB",
            'used_percent': f"{mem.percent}%"
        }

        # Disk information
        disks = []
        for part in psutil.disk_partitions():
            usage = psutil.disk_usage(part.mountpoint)
            disks.append({
                'device': part.device,
                'mountpoint': part.mountpoint,
                'fstype': part.fstype,
                'total': f"{usage.total / (1024 ** 3):.2f} GB",
                'used': f"{usage.used / (1024 ** 3):.2f} GB",
                'free': f"{usage.free / (1024 ** 3):.2f} GB",
                'percent': f"{usage.percent}%"
            })
        info['disks'] = disks

        # Network information
        nets = []
        for name, addrs in psutil.net_if_addrs().items():
            net_info = {'interface': name, 'addresses': []}
            for addr in addrs:
                net_info['addresses'].append({
                    'family': addr.family.name,
                    'address': addr.address,
                    'netmask': addr.netmask,
                    'broadcast': addr.broadcast
                })
            nets.append(net_info)
        info['networks'] = nets

        # Windows-specific info
        if WIN32_AVAILABLE:
            try:
                c = wmi.WMI()
                info['bios'] = c.Win32_BIOS()[0].Caption
                info['motherboard'] = c.Win32_BaseBoard()[0].Product
                info['cpu'] = c.Win32_Processor()[0].Name
                info['gpu'] = [gpu.Caption for gpu in c.Win32_VideoController()]
            except Exception:
                pass

    except Exception as e:
        info['error'] = f"System info collection failed: {str(e)}"

    return info


def get_recent_events(log_names=["System", "Application"], hours=48):
    """Retrieve recent events from specified logs"""
    if not WIN32_AVAILABLE:
        return {}

    events_by_log = defaultdict(list)
    cutoff_time = datetime.now() - timedelta(hours=hours)

    for log_name in log_names:
        hand = None  # Initialize handle
        try:
            # Attempt to open the event log
            hand = win32evtlog.OpenEventLog(None, log_name)
            flags = win32evtlog.EVENTLOG_BACKWARDS_READ | win32evtlog.EVENTLOG_SEQUENTIAL_READ
            total_events = 0

            while True:
                events = win32evtlog.ReadEventLog(hand, flags, 0)
                if not events:
                    break

                for event in events:
                    if event.TimeGenerated < cutoff_time:
                        break
                    if event.EventType in [win32con.EVENTLOG_ERROR_TYPE, win32con.EVENTLOG_WARNING_TYPE]:
                        event_data = {
                            'event_id': event.EventID & 0xFFFF,
                            'source': event.SourceName,
                            'time': event.TimeGenerated.strftime("%Y-%m-%d %H:%M:%S"),
                            'message': win32evtlogutil.SafeFormatMessage(event, log_name),
                            'severity': "ERROR" if event.EventType == win32con.EVENTLOG_ERROR_TYPE else "WARNING"
                        }
                        events_by_log[log_name].append(event_data)
                        total_events += 1
                        if total_events > 1000:  # Safety limit
                            break
        except Exception as e:
            events_by_log[log_name].append({
                'error': f"Error reading {log_name} log: {str(e)}"
            })
        finally:
            # Only close if handle was successfully created
            if hand is not None:
                try:
                    win32evtlog.CloseEventLog(hand)
                except Exception as e:
                    events_by_log[log_name].append({
                        'error': f"Error closing {log_name} log: {str(e)}"
                    })

    return dict(events_by_log)


def analyze_events(events):
    """Analyze events and match against error database"""
    analyzed_events = []
    for log_name, log_events in events.items():
        for event in log_events:
            if 'error' in event:
                analyzed_events.append(event)
                continue

            event_id_str = str(event['event_id'])
            hex_id = f"0x{event['event_id']:08X}"

            # Check both decimal and hex representations
            error_info = None
            if event_id_str in ERROR_DB:
                error_info = ERROR_DB[event_id_str].copy()
            elif hex_id in ERROR_DB:
                error_info = ERROR_DB[hex_id].copy()

            if error_info:
                error_info['raw'] = event
                error_info['log'] = log_name
                analyzed_events.append(error_info)
            else:
                # Unknown event
                analyzed_events.append({
                    'name': 'UNKNOWN_EVENT',
                    'description': 'Unrecognized event ID',
                    'severity': 'WARNING',
                    'common_causes': ['New or uncommon error'],
                    'troubleshooting': ['Research event ID online', 'Check system logs'],
                    'raw': event,
                    'log': log_name
                })

    return analyzed_events


def find_dump_files():
    """Locate all crash dump files in common locations"""
    dump_files = []
    locations = [
        os.path.join(os.environ['SystemRoot'], 'Minidump'),
        os.path.join(os.environ['SystemRoot'], 'MEMORY.DMP'),
        os.path.join(os.environ['USERPROFILE'], 'AppData', 'Local', 'CrashDumps'),
        os.path.join(os.environ['SystemRoot'], 'LiveKernelReports')
    ]

    for location in locations:
        if os.path.exists(location):
            for root, _, files in os.walk(location):
                for file in files:
                    if file.endswith(('.dmp', '.DMP')):
                        dump_files.append(os.path.join(root, file))

    return dump_files


def check_system_health():
    """Perform basic system health checks"""
    health = {}

    # Disk health
    health['disks'] = []
    for disk in psutil.disk_partitions():
        try:
            usage = psutil.disk_usage(disk.mountpoint)
            health['disks'].append({
                'device': disk.device,
                'mountpoint': disk.mountpoint,
                'total': usage.total,
                'used': usage.used,
                'free': usage.free,
                'percent': usage.percent,
                'status': 'OK' if usage.percent < 90 else 'WARNING'
            })
        except Exception:
            pass

    # Memory health
    mem = psutil.virtual_memory()
    health['memory'] = {
        'total': mem.total,
        'available': mem.available,
        'used': mem.used,
        'percent': mem.percent,
        'status': 'OK' if mem.percent < 90 else 'WARNING'
    }

    # CPU health
    health['cpu'] = {
        'usage': psutil.cpu_percent(interval=1),
        'status': 'OK' if psutil.cpu_percent(interval=1) < 90 else 'WARNING'
    }

    # Temperature (if available)
    health['temperatures'] = []
    if hasattr(psutil, "sensors_temperatures"):
        temps = psutil.sensors_temperatures()
        for name, entries in temps.items():
            for entry in entries:
                health['temperatures'].append({
                    'sensor': name,
                    'label': entry.label,
                    'current': entry.current,
                    'high': entry.high,
                    'critical': entry.critical,
                    'status': 'OK' if entry.current < entry.high else 'WARNING'
                })

    return health


def analyze_drivers():
    """Analyze driver status and versions"""
    if not WIN32_AVAILABLE:
        return []

    drivers = []
    try:
        c = wmi.WMI()
        for driver in c.Win32_SystemDriver():
            drivers.append({
                'name': driver.Name,
                'description': driver.Description,
                'state': driver.State,
                'status': driver.Status,
                'start_mode': driver.StartMode,
                'path': driver.PathName
            })
    except Exception:
        pass

    return drivers


def generate_report(analyzed_events, dump_files, system_info, system_health, drivers):
    """Generate comprehensive diagnostic report"""
    report = []
    report.append("=" * 80)
    report.append("PC CRASH DIAGNOSTIC REPORT")
    report.append("=" * 80)
    report.append(f"Generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append("\n")

    # System overview
    report.append("[SYSTEM OVERVIEW]")
    report.append(f"OS: {system_info.get('os', 'Unknown')}")
    report.append(f"CPU: {system_info.get('cpu', 'Unknown')}")
    report.append(f"Memory: {system_info.get('memory', {}).get('total', 'Unknown')}")
    if 'gpu' in system_info:
        report.append(f"GPU: {', '.join(system_info['gpu'])}")
    report.append("\n")

    # Critical errors
    critical_errors = [e for e in analyzed_events if e.get('severity') == 'CRITICAL']
    if critical_errors:
        report.append("[CRITICAL ERRORS DETECTED]")
        for error in critical_errors:
            report.append("\n" + "-" * 60)
            report.append(f"► [{error['log']}] Event ID: {error['raw']['event_id']} ({error['name']})")
            report.append(f"  Time: {error['raw']['time']}")
            report.append(f"  Source: {error['raw']['source']}")
            report.append(f"  Description: {error['description']}")
            report.append("  Common Causes:")
            for cause in error['common_causes']:
                report.append(f"    • {cause}")
            report.append("  Recommended Troubleshooting:")
            for step in error['troubleshooting']:
                report.append(f"    • {step}")
        report.append("\n")
    else:
        report.append("[✓] No critical errors detected in event logs")
        report.append("\n")

    # Dump files
    if dump_files:
        report.append("[CRASH DUMP FILES FOUND]")
        for dump in dump_files:
            report.append(f"  • {dump}")
        report.append("\n  Analyze these with WinDbg or use the following online tools:")
        report.append("  https://www.osronline.com/page.cfm?name=analyze")
        report.append("  https://www.nirsoft.net/utils/blue_screen_view.html")
        report.append("\n")

    # System health
    report.append("[SYSTEM HEALTH CHECK]")
    report.append(f"Memory Usage: {system_health['memory']['percent']}% - {system_health['memory']['status']}")
    report.append(f"CPU Usage: {system_health['cpu']['usage']}% - {system_health['cpu']['status']}")

    for disk in system_health['disks']:
        report.append(f"Disk ({disk['mountpoint']}): {disk['percent']}% used - {disk['status']}")

    if system_health['temperatures']:
        report.append("\n[TEMPERATURES]")
        for temp in system_health['temperatures']:
            status = f" - {temp['status']}" if temp['current'] > temp['high'] else ""
            report.append(f"  {temp['label']}: {temp['current']}°C (High: {temp['high']}°C){status}")

    # Driver analysis
    if drivers:
        report.append("\n[DRIVER STATUS]")
        problem_drivers = [d for d in drivers if d['state'] != "Running"]
        if problem_drivers:
            report.append(f"Found {len(problem_drivers)} drivers with issues:")
            for driver in problem_drivers[:5]:  # Limit to top 5
                report.append(f"  • {driver['name']} - State: {driver['state']}, Status: {driver['status']}")
        else:
            report.append("All drivers are running normally")

    # Additional recommendations
    report.append("\n[RECOMMENDED ACTIONS]")
    report.append("1. Run memory diagnostics: Press Win+R and type 'mdsched.exe'")
    report.append("2. Update all device drivers (especially graphics and chipset)")
    report.append("3. Check for Windows updates")
    report.append("4. Perform system file check: Open CMD as admin and run 'sfc /scannow'")
    report.append("5. Check disk for errors: Open CMD as admin and run 'chkdsk /f'")

    if critical_errors:
        report.append("\n[QUICK FIX ATTEMPTS]")
        report.append("You can try these automated fixes:")
        report.append("• Run driver verifier: verifier /standard /all")
        report.append("• Clean boot: msconfig -> Selective startup")
        report.append("• System restore: rstrui.exe")

    report.append("\n" + "=" * 80)
    return "\n".join(report)


def save_report(report, filename="crash_report.txt"):
    """Save report to file"""
    with open(filename, "w", encoding="utf-8") as f:
        f.write(report)
    return os.path.abspath(filename)


def main():
    print("PC Crash Analyzer - Comprehensive Diagnostic Tool")
    print("=" * 70)

    # Collect data
    print("\n[1/6] Collecting system information...")
    system_info = get_system_info()

    print("[2/6] Scanning event logs...")
    events = get_recent_events()

    print("[3/6] Analyzing events...")
    analyzed_events = analyze_events(events)

    print("[4/6] Searching for crash dumps...")
    dump_files = find_dump_files()

    print("[5/6] Checking system health...")
    system_health = check_system_health()

    print("[6/6] Analyzing drivers...")
    drivers = analyze_drivers()

    # Generate report
    report = generate_report(
        analyzed_events,
        dump_files,
        system_info,
        system_health,
        drivers
    )

    # Output results
    print("\n" + "=" * 70)
    print(report)
    print("=" * 70)

    # Save report
    report_path = save_report(report)
    print(f"\nReport saved to: {report_path}")

    # Offer to open online resources
    if any(e.get('severity') == 'CRITICAL' for e in analyzed_events):
        print("\nWould you like to search online for solutions? (y/n)")
        if input().lower() == 'y':
            for event in analyzed_events:
                if event.get('severity') == 'CRITICAL':
                    query = f"{event.get('name')} {event.get('raw', {}).get('event_id')} solution"
                    url = f"https://www.google.com/search?q={urllib.parse.quote(query)}"
                    webbrowser.open(url)


if __name__ == "__main__":
    import platform

    main()