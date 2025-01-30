import typer
from rich.console import Console
from rich.panel import Panel
from rich.progress import track
import subprocess
import webbrowser
import time
import os

app = typer.Typer()
console = Console()

def show_banner():
    """แสดง Banner ของโปรแกรม"""
    console.print(Panel.fit(
        "[bold green]Excel Processor[/bold green] - ระบบประมวลผล Excel อัจฉริยะ\n"
        "เวอร์ชัน 0.1.0 | พัฒนาโดย ZanKinZuiTH",
        title="🚀 ยินดีต้อนรับ",
        border_style="green"
    ))

@app.command()
def start(
    port: int = typer.Option(8501, help="พอร์ตที่ต้องการใช้งาน"),
    browser: bool = typer.Option(True, help="เปิดเบราว์เซอร์อัตโนมัติ")
):
    """เริ่มต้นใช้งานแอพพลิเคชัน"""
    show_banner()
    
    # แสดงสถานะการเริ่มต้น
    for _ in track(range(3), description="กำลังเริ่มต้นระบบ..."):
        time.sleep(0.5)
    
    # เปิดเบราว์เซอร์
    if browser:
        webbrowser.open(f"http://localhost:{port}")
    
    # รัน Streamlit
    console.print("\n[bold green]✓[/bold green] ระบบพร้อมใช้งานแล้ว!")
    console.print(f"[bold]เข้าใช้งานได้ที่:[/bold] http://localhost:{port}")
    subprocess.run(["streamlit", "run", "ui.py", "--server.port", str(port)])

@app.command()
def setup():
    """ตั้งค่าระบบเริ่มต้น"""
    show_banner()
    
    with console.status("[bold green]กำลังตั้งค่าระบบ...[/bold green]"):
        # สร้างโฟลเดอร์ที่จำเป็น
        os.makedirs("temp", exist_ok=True)
        os.makedirs("output", exist_ok=True)
        os.makedirs("templates", exist_ok=True)
        
        # ติดตั้งไลบรารีเพิ่มเติม
        subprocess.run(["pip", "install", "-e", "."])
        
        time.sleep(1)
    
    console.print("\n[bold green]✓[/bold green] ตั้งค่าระบบเรียบร้อยแล้ว!")

@app.command()
def version():
    """แสดงเวอร์ชันของโปรแกรม"""
    console.print("[bold]Excel Processor[/bold] เวอร์ชัน 0.1.0")

if __name__ == "__main__":
    app() 