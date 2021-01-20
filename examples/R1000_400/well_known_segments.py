
'''
This table is created from all the 'LOAD' lines MLOAD
files in the DFS tape AutoArchaeologist.
'''

WELL_KNOWN_SEGMENTS = {
    0x813: "MODULE_NAMES",
    0x819: "PROCESSOR_MANAGER",
    0xC13: "MACHINE_INTERFACE_MODULE_NAMES",
    0xC19: "TAG_STORE_MANAGER",
    0x1013: "FILLER",
    0x1019: "BYTE_BUFFER",
    0x1413: "MODEM_DEFINITIONS",
    0x1419: "DEBUGGER_PORT_MANAGER",
    0x1813: "MODEM_STREAMS",
    0x1819: "EXCEPTIONS",
    0x1C13: "PACKET_DEFINITIONS",
    0x1C19: "SUBSTRATE",
    0x2013: "KERNEL_DEBUGGER_IO_MODULE_NAMES",
    0x2019: "RECEIVE_BUFFER",
    0x2413: "DEBUGGER_PORT_DEFINITIONS",
    0x2419: "R1000",
    0x2813: "DEBUGGER_IOP_DEFS",
    0x2819: "TYPE_ANALYZER",
    0x2C13: "PORT_SEQUENCE_NUMBER",
    0x2C19: "_KERNEL_DEBUGGER_IO",
    0x3013: "VIRT_MEM_DEFS",
    0x3019: "MISCELLANEOUS_MODULE_NAMES",
    0x3413: "MACHINE",
    0x3419: "UNCHECKED_LRM_GENERICS",
    0x3813: "IO_DEFINITIONS",
    0x3819: "STORAGE_MANAGER",
    0x3C13: "TRACE",
    0x3C19: "IO_EXCEPTIONS",
    0x4013: "MULTIPLEXING",
    0x4019: "PURE_ELEMENT_TABLE_SORT_GENERIC",
    0x4413: "PACKETIZE_WITH_COUNT",
    0x4419: "STRING_SORT_GENERIC",
    0x4813: "ABSTRACT_PORT",
    0x4C0A: "BITOPS",
    0x4C13: "SEGMENTED_HEAP_INTERFACE",
    0x4C19: "MINMAX",
    0x5013: "MODEM",
    0x5019: "ENUMERATION_OPS",
    0x5C19: "TIME_UTILITY",
    0x6019: "COMMAND_SCANNER",
    0x6409: "STRING_UTILITIES",
    0x6419: "INPUT_OUTPUT_BUFFERING",
    0x6813: "_MACHINE_INTERFACE",
    0x1A813: "ABSTRACT_TYPES_MODULE_NAMES",
    0x1AC13: "PURE_ELEMENT_SEQUENCE_MAP_GENERIC",
    0x1B013: "PURE_ELEMENT_MAP_GENERIC",
    0x1B413: "PURE_ELEMENT_HEAP_QUEUE_GENERIC",
    0x1B813: "ADAPTIVE_BALANCED_STRING_TREE_GENERIC",
    0x1BC13: "ADAPTIVE_BALANCED_TREE_GENERIC",
    0x1C013: "TYPE_UTILITIES",
    0x1C413: "LIST_GENERIC",
    0x1C813: "QUEUE_GENERIC",
    0x1CC13: "FAST_FIFO_HEAP_SET_GENERIC",
    0x1D013: "COMPACT_HEAP_SET_GENERIC",
    0x1D413: "UNBOUNDED_LENGTH_STRING_GENERIC",
    0x1DC13: "UNCHECKED_DEALLOCATION",
    0x1E013: "CACHED_PROTECTED_PURE_ELEMENT_MAP_GENERIC",
    0x1E413: "PURE_ELEMENT_QUEUE_GENERIC",
    0x1E813: "PURE_ELEMENT_HEAP_MAP_GENERIC",
    0x1EC13: "PURE_ELEMENT_HEAP_STRING_MAP_GENERIC",
    0x1F013: "LRU_STACK",
    0x1F413: "STACK_GENERIC",
    0x1F813: "CACHED_PROTECTED_PURE_ELEMENT_HEAP_MAP_GENERIC",
    0x1FC13: "SIMPLE_HASH",
    0x21013: "COMPACT_HEAP_MAP_GENERIC",
    0x21413: "MANAGED_UNBOUNDED_STRING_GENERIC",
    0x21813: "PURE_ELEMENT_STRING_MAP_GENERIC",
    0x21C13: "TABLE_GENERIC",
    0x22013: "PURE_ELEMENT_HEAP_SET_GENERIC",
    0x22413: "HEAP_MANAGER",
    0x22813: "HEAP_STORAGE_MANAGER",
    0x22C13: "PURE_ELEMENT_HEAP_SEQUENCE_MAP_GENERIC",
    # 0x35809 ",
    0x36809: "KERNEL_DEBUGGER",
    0x70C13: "CONDITION_OUTPUT",
    0x71013: "COMM",
    0x71413: "STANDARD_COMM_PRIMITIVES",
    0x71C13: "COMM_FILE",
    0x72013: "UNCHECKED_CONVERSION",
    0x72413: "IO",
    0x72813: "RUNTIME_TYPE_STRUCTURE",
    0x72C13: "REGULAR_EXPRESSION",
    0x73013: "LONG_FLOATS",
    0x73413: "CHECK_TYPE_PACKAGE",
    0x73813: "IO_EXCEPTION_FLAVORS",
    0x8DC08: "STRING_UTILITIES",
    0x8E013: "STRING_TABLE",
    0x8E413: "PURE_ELEMENT_DUAL_STRING_MAP_GENERIC",
    0x8E808: "STRING_UTILITIES",
    0x8E813: "PURE_ELEMENT_STACK_GENERIC",
    0x8EC13: "HEAP_STRING_TABLE",
    0x8F013: "PURE_ELEMENT_SET_GENERIC",
    0x90C13: "PURE_ELEMENT_LIST_GENERIC",
    0x91013: "_ABSTRACT_TYPES",
    0x92013: "INTERNAL_DEBUGGING_UTILITIES",
    0x92413: "LOG",
    0x92813: "ERROR_REPORTING",
    0x94413: "RECOVERY",
    0x94C13: "MAP_VPS_TO_VOLUMES",
    0x95013: "_OS_UTILITIES",
    0x9B413: "MACHINE_CODE",
    0x9B813: "SYSTEM",
    0x9C813: "KERNEL_ELABORATOR",
    0xA5009: "BIT_OPERATIONS",
    0xACC13: "_KERNEL_DEBUGGER",
    0xB2013: "COPYRIGHT_NOTICE",
    0xB2413: "_MISCELLANEOUS",
    0xBF813: "ELABORATOR_DATABASE_MODULE_NAMES",
    0xBFC13: "CROSS_DEVELOPMENT",
    0xC0013: "COMMAND_INTERPRETER",
    0xC0413: "EEDB_USER_INTERFACE_GENERIC",
    0xC0813: "EEDB_USER_INTERFACE",
    0xC0C13: "EEDB_IO",
    # 0xC101",
    0xC1413: "EEDB_UTILITIES",
    0xC1813: "ENVIRONMENT_ELABORATOR_DATABASE",
    0xC1C13: "SHUTDOWN_COUPLER",
    0xC2013: "TAPE_CODE_SEGMENT_INTERFACE",
    0xC2413: "TAPE_MLOAD_INTERFACE",
    0xC2813: "EEDB_BOOTSTRAP",
    0xC2C13: "EEDB_TAPE",
    0xC3013: "VERSION_STRING",
    0xC3413: "EEDB_MAIN",
    0xC3813: "_ELABORATOR_DATABASE",
    0xC7C0A: "R1000_UTILITIES",
    0xC800A: "R1000_UTILITIES",
    0xC840A: "_KERNEL_DEBUGGER",
    0xC880A: "R1000_UTILITIES",
    0xC8C0A: "_KERNEL_DEBUGGER",
    0xC900A: "_KERNEL_DEBUGGER",
    0xC980A: "_ENVIRONMENT_DEBUGGER",
    0xCA40A: "_ENVIRONMENT_DEBUGGER",
    0xDEC12: "REPRESENTATION",
    0xDF812: "PROGRAM",
    0xE1412: "PROFILE",
    0xE6812: "CURRENT_EXCEPTION",
    0xE6C12: "LIST_GENERIC",
    0xED413: "KERNEL_MODULE_NAMES",
    0xED813: "TYPE_DESCRIPTION",
    0xEDC13: "BLOCK_DEFS",
    0xEE013: "UNIQUE_NUMBER_GENERATOR",
    0xEE413: "SPACE_DEFS",
    0xEE813: "CONTEXT_FOR_PAGE_DISPLAY",
    0xEEC13: "IOP_DEFS",
    0xEF013: "WAIT_SERVICE",
    0xEF413: "TRIGGER",
    0xEF813: "SHORT_TERM_LOCK_MANAGER",
    0xEFC13: "PACKET_ID_ALLOCATOR",
    0xF0013: "PAGE_POOL",
    0xF0413: "SIMPLE_STRINGS",
    # 0xF0813 ",
    0xF0C13: "CALENDAR_UTILITIES",
    0xF1013: "MEMORY_ECC_ERROR",
    0xF1413: "TAPE_DEFINITIONS",
    0xF1813: "COPY_BYTES",
    0xF1C13: "TAPE_DRIVER",
    0xF2013: "PORT_DEFINITIONS",
    0xF2413: "ARRAY_LIST_MANAGER",
    0xF2813: "ARRAY_HEAP_MANAGER",
    0xF2C13: "ARRAY_QUEUE_MANAGER",
    0xF3013: "LOG_RECORD_BUFFER",
    0xF3413: "BARRIER_REMOVER",
    0xF3813: "MATH_FUNCTIONS",
    0xF3C13: "TABLE_PRINTER",
    0xF4013: "BLOCK_TO_SECTOR_MAPPING",
    0xF4413: "STABLE_STORAGE_DEFINITIONS",
    0xF4813: "DISK_Q_MANAGER",
    0xF4C13: "DISK_IO_WITH_WAIT",
    0xF5013: "BLOCK_TO_PAGE_MAPPING",
    0xF5413: "STABLE_STORAGE",
    0xF5813: "ARRAY_SHELL_SORT",
    0xF5C13: "BAD_BLOCK_MANAGER",
    0xF6013: "TWIG_MANAGER",
    0xF6413: "BTREE_MANAGER",
    0xF6813: "BARRIER_MANAGER",
    0xF6C13: "RAF_MANAGER",
    0xF7013: "ACTION_MANAGER",
    0xF7413: "TREE_STRUCTURE_PRINTER",
    0xF7813: "VOLUME_MANAGER",
    0xF7C12: "OS_UTILITIES_MODULE_NAMES",
    0xF7C13: "BLOCK_GETTER",
    0xF8012: "OPERATOR_IF_DEFS",
    0xF8013: "GHOST_LOG_MANAGER",
    0xF8412: "ANSI_TAPE_LABELS_DEFS",
    0xF8413: "ARRAY_HASH_TABLE_MANAGER_ELEMENT_HASHER",
    0xF8812: "CHAINED_ANSI_LABELS_DEFS",
    0xF8813: "ARRAY_HASH_TABLE_MANAGER_VALUE_HASHER",
    0xF8C12: "RATIONAL_TAPE_LABELS_DEFS",
    0xF8C13: "INCREMENT",
    0xF9013: "HASH_FUNCTIONS",
    0xF9413: "MEDIUM_TERM_SCHEDULER",
    0xF9813: "BAD_BLOCK_LIST_RECOVERY",
    0xF9C13: "GET_DISCRETE_VALUE_GENERIC",
    0xFA012: "LIST_MANAGER",
    0xFA013: "BYTE_STRING_CONVERSIONS",
    0xFA413: "X25_BARRIER_MANAGER",
    0xFA813: "PORT_DRIVER",
    0xFAC13: "PORT_MANAGER",
    0xFB013: "SIMPLE_PORT_IO",
    0xFB413: "CONSOLE_MANAGER",
    0xFB813: "HASHED_TYPE_DESCRIPTOR_MANAGER",
    0xFBC13: "CONFIGURATOR",
    0xFC012: "MATH_FUNCTIONS",
    0xFC013: "CONTEXT_FOR_BLOCK_DISPLAY",
    0xFC412: "SIMPLE_STRINGS",
    0xFC413: "SEGMENT_MANAGER",
    0xFC812: "CHARACTER_STRINGS",
    0xFC813: "ARRAY_TABLE_LOOKUP",
    0xFCC13: "CATALOG_MANAGER",
    0xFD013: "PAGE_TO_SECTION_MAPPING",
    0xFD413: "SPACE_MANAGER",
    0xFD813: "CALENDAR",
    0xFDC13: "ENVIRONMENT_ELABORATOR",
    0xFE013: "ERROR_LOG_THROTTLE",
    0xFE413: "GET_DISCRETE_VALUE_WITH_DEFAULT_GENERIC",
    0xFEC13: "MANAGED_SET",
    0xFF013: "MANAGED_QUEUE",
    0xFF413: "X25_BACKOFF_TIMER",
    0xFF813: "X25_DEFINITIONS",
    0xFFC13: "MCP_PACKET_DEFS",
    0x100013: "MCP_DEFINITIONS",
    0x100413: "X25_MESSAGE",
    0x100813: "MCP_PACKET",
    0x100C13: "MCP_GENERIC",
    0x101013: "X25_LINE",
    0x101413: "X25_INTERNAL_DEFINITIONS",
    0x101813: "X25_CIRCUIT",
    0x101C13: "X25_DRIVER",
    0x102413: "TCP_IP_DRIVER",
    0x102813: "ENP_DRIVER",
    0x10CC12: "FAMILY_ID_CONVERSION",
    0x10D012: "HEAP_MANAGER",
    0x10E012: "ANSI_STANDARD_DISCREPANCIES",
    0x10E812: "TAPE_ACCESS_CONTROL",
    0x114012: "DATABASE",
    0x114C12: "BREAK_MANAGER",
    0x115012: "ITEMS",
    0x117012: "INTERPRETER",
    0x117812: "KERNEL_IO",
    0x117C12: "TRANSPORT_GENERIC",
    0x118012: "REMOTE",
    0x11A408: "BACKUP_DATA",
    0x11BC08: "BACKUP_DATA_BASE",
    0x11C008: "BUFFERED_READS",
    0x11C808: "BACKUP_LOCK",
    0x11CC08: "BUFFERED_WRITES",
    0x11D408: "ANSI_RECORDS",
    0x11E013: "KERNEL_COMMAND_INTERPRETER",
    0x11EC13: "_KERNEL",
    0x12E412: "ABSTRACT_PROGRAM",
    0x12E812: "WORDS",
    0x12EC12: "EXCEPTION_NAME",
    0x12FC12: "BREAK_MANAGER",
    0x130012: "ITEMS",
    0x130412: "TASK_STATE_CACHE",
    0x130C12: "DATABASE",
    0x131012: "CONVERT_NAME",
    0x131C12: "PURE_MAP_GENERIC",
    0x132C12: "RESIDENT_MEMORY_STATUS",
    0x133412: "DEBUG",
    0x133C12: "INTERPRETER",
    0x134412: "KERNEL_IO",
    0x134812: "TRANSPORT_GENERIC",
    0x134C12: "REMOTE",
    0x135012: "LIST_GENERIC",
    0x135412: "CURRENT_EXCEPTION",
    0x15FC13: "MACHINE_CODE",
    0x160013: "SYSTEM",
    0x162413: "RUNTIME_STANDARD",
    0x163C13: "ENVIRONMENT_ELABORATOR_DATABASE",
    0x164013: "_ELABORATOR_DATABASE",
    0x169C13: "KERNEL_ELABORATOR",
    0x1A7808: "SIMPLE_STATUS",
    0x1C0013: "TCP_IP_DRIVER",
    0x1C0813: "KERNEL_COMMAND_INTERPRETER",
    0x1C0C13: "_KERNEL",
    0x1DA009: "RUNTIME_STANDARD",
    0x208409: "R1000_UTILITIES",
    0x208809: "R1000_UTILITIES",
    0x21A008: "KERNEL_CURRENT_EXCEPTION",
    0x227808: "LIBRARIES",
    0x227C08: "KERNEL_CURRENT_EXCEPTION",
    0x228008: "MONITOR",
    0x228408: "INTERPRETER",
    0x228C08: "LIBRARIES",
    0x229008: "INTERPRETER",
    0x229408: "MONITOR",
    0x229808: "KERNEL_CURRENT_EXCEPTION",
    0x259408: "CONTROL",
    0x25AC08: "CONTROL",
    0x2EC008: "BOUNDED",
    0x2EC808: "BOUNDED_LENGTH_STRING_GENERIC",
    0x2ED408: "BOUNDED_LENGTH_STRING_GENERIC",
    0x2ED808: "BOUNDED",
    0x2EFC08: "BOUNDED_LENGTH_STRING_GENERIC",
    0x2F0008: "BOUNDED",
    0x365808: "KERNEL",
    0x367808: "KERNEL_DEBUGGER",
    0x367C08: "KERNEL_DEBUGGER",
    0x3CB809: "CHECKED_TAPE",
    0x3CBC09: "GET_D",
    0x3CC009: "ANSI_TAPE_LABELS_LAYOUT",
    0x46D408: "COMMAND_INTERFACE",
    0x46E008: "NAME_REGISTRATION",
    0x46E408: "LIBRARIES",
    0x46E808: "RUNTIME",
    0x46EC08: "CONTROL",
    0x46F008: "BREAK_INTERFACE",
    0x46F408: "DEBUGGER",
    0x46F808: "MONITOR",
    0x46FC08: "INIT",
    0x470008: "KERNEL",
    0x471408: "COMMAND_INTERFACE",
    0x471C08: "NAME_REGISTRATION",
    0x472008: "LIBRARIES",
    0x472408: "BREAK_INTERFACE",
    0x472808: "DEBUGGER",
    0x472C08: "MONITOR",
    0x473008: "INIT",
    0x473408: "KERNEL",
    0x473808: "RUNTIME",
    0x473C08: "CONTROL",
    0x486C08: "HISTOGRAM",
    0x489008: "HOST",
    0x489C08: "HISTOGRAM",
    0x48A008: "HOST",
    0x493408: "HISTOGRAM_INTERFACE",
    0x493C08: "HISTOGRAM_INTERFACE",
    0x62AC08: "OPERATOR_IF",
    0x7ED808: "UNCHECKED_CONVERSIONS",
    0x8C2408: "BACKUP",
    0x8CFC08: "CHAINED_ANSI_LABELS",
    0x8D0008: "RATIONAL_TAPE_LABELS",
    0x8D0408: "LOW_LEVEL_STANDARD_LABELS",
    0x914008: "ANSI_TAPE_LABELS",
    0x914808: "TAPE_LOCK",
    0x9B1008: "INTERNAL_UNCHECKED_CONVERSION",
    0xA6F411: "REMOTE_PARAMETER",
    0xA6F811: "SCAN",
    0xA6FC11: "DEBUG_ERROR",
    0xA70411: "DEBUG",
    0xA70811: "RESIDENT_MEMORY_STATUS",
    0xA70C11: "ENVIRONMENT_DEBUGGER_MODULE_NAMES",
    0xA71411: "DEBUG_ACTION",
    0xA71C11: "LOCATION",
    0xA72011: "EXCEPTION_NAME",
    0xA73411: "ABSTRACT_PROGRAM",
    0xA73811: "PURE_ELEMENT_TABLE_SORT_GENERIC",
    0xA73C11: "MANAGED_PURE_ELEMENT_LIST_GENERIC",
    0xA74011: "MACHINE_HISTOGRAM_STRUCTURES",
    0xA74411: "WORDS",
    0xA74811: "DEBUG_TABLE",
    0xA77011: "PURE_MAP_GENERIC",
    0xA86411: "ARRAY_LIST_MANAGER",
    0xA86811: "ARRAY_HEAP_MANAGER",
    0xA86C11: "ARRAY_SHELL_SORT",
    0xA87011: "PACK",
    0xA87811: "DISPLAY_BYTE_STRING",
    0xAA1811: "KERNEL_DEBUGGER_MODULE_NAMES",
    0xAA2411: "SCAN",
    0xAA2811: "DEBUG_ERROR",
    0xAA2C11: "REPRESENTATION",
    0xAA3011: "DEBUG",
    0xAA3811: "PROGRAM",
    0xAA3C11: "KERNEL_IO",
    0xAA4011: "DEBUG_ACTION",
    0xAA4411: "TRANSPORT_GENERIC",
    0xAA4811: "REMOTE_PARAMETER",
    0xAA4C11: "REMOTE",
    0xAA5411: "EXCEPTION_NAME",
    0xAA5811: "PROFILE",
    0xAA5C11: "ABSTRACT_PROGRAM",
    0xAA6011: "LOCATION",
    0xAA6411: "HISTOGRAM",
    0xAA6811: "HOST",
    0xAA6C11: "DEBUG_TABLE",
    0xAA7011: "CONVERT_NAME",
    0xAA7411: "BREAK_MANAGER",
    0xAA7811: "RUNTIME",
    0xAA7C11: "ITEMS",
    0xAA8011: "TASK_STATE_CACHE",
    0xAA8411: "COMMAND_INTERFACE",
    0xAA8811: "DATABASE",
    0xAA9011: "BREAK_INTERFACE",
    0xAA9411: "NAME_REGISTRATION",
    0xAAA411: "INIT",
    0xAAB411: "KERNEL_PRIORITY",
    0xAAB811: "HISTORY",
    0xB39011: "CONVERT_CHARS_BYTES",
    0xB3E811: "CONVERT_NAME",
    0xB3EC11: "TASK_STATE_CACHE",
    0xB9600A: "SHORT_TERM_SEMAPHORE",
    0xBDE411: "REMOTE_PARAMETER",
    0xBDE811: "ENVIRONMENT_DEBUGGER_MODULE_NAMES",
    0xBDEC11: "SCAN",
    0xBDF011: "DEBUG_ERROR",
    0xBDF411: "REPRESENTATION",
    0xBDF811: "PROGRAM",
    0xBDFC11: "DEBUG_ACTION",
    0xBE0411: "LOCATION",
    0xBE0811: "DEBUG_TABLE",
    0xBE0C11: "PROFILE",
    0xBE1811: "PURE_ELEMENT_TABLE_SORT_GENERIC",
    0xBE1C11: "MANAGED_PURE_ELEMENT_LIST_GENERIC",
    0xBE2011: "MACHINE_HISTOGRAM_STRUCTURES",
    0xC5F411: "KERNEL_DEBUGGER_MODULE_NAMES",
    0xC60411: "SCAN",
    0xC60811: "PROGRAM",
    0xC61011: "LOCATION",
    0xC61411: "DEBUG",
    0xC61811: "DEBUG_ERROR",
    0xC61C11: "REPRESENTATION",
    0xC62011: "DEBUG_ACTION",
    0xC62411: "DEBUG_TABLE",
    0xC62811: "KERNEL_IO",
    0xC62C11: "CONVERT_NAME",
    0xC63011: "EXCEPTION_NAME",
    0xC63411: "TASK_STATE_CACHE",
    0xC63811: "BREAK_MANAGER",
    0xC63C11: "TRANSPORT_GENERIC",
    0xC64011: "REMOTE_PARAMETER",
    0xC64411: "REMOTE",
    0xC64811: "COMMAND_INTERFACE",
    0xC64C11: "PROFILE",
    0xC65011: "ABSTRACT_PROGRAM",
    0xC65411: "HISTOGRAM",
    0xC65811: "HOST",
    0xC65C11: "RUNTIME",
    0xC66011: "ITEMS",
    0xC66411: "DATABASE",
    0xC66C11: "BREAK_INTERFACE",
    0xC67011: "NAME_REGISTRATION",
    0xC68011: "INIT",
    0xC68C11: "HISTORY",
    0xC69011: "KERNEL_PRIORITY",
    0xC6A811: "KERNEL_DEBUGGER_MODULE_NAMES",
    0xFAEC08: "ALLOWS_DEALLOCATION",
}