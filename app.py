import streamlit as st
import streamlit.components.v1 as components

# Page Configuration
st.set_page_config(
    page_title="AEROGUARD Command Center",
    page_icon="🛸",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom Styling to make Streamlit container full width & dark
st.markdown("""
<style>
    .stApp {
        background-color: #050811 !important;
        padding: 0rem !important;
    }
    .block-container {
        padding: 0rem !important;
        max-width: 100% !important;
    }
    iframe {
        border: none !important;
    }
</style>
""", unsafe_allow_html=True)

# Full Exact UI Rendered via Custom Responsive Canvas
html_dashboard = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        body {
            margin: 0;
            padding: 15px;
            background: linear-gradient(rgba(5, 8, 17, 0.7), rgba(5, 8, 17, 0.85)), 
                        url("https://images.unsplash.com/photo-1518709268805-4e9042af9f23?q=80&w=2000&auto=format&fit=crop");
            background-size: cover;
            background-position: center;
            font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
            color: #fff;
            height: 100vh;
            box-sizing: border-box;
            overflow-x: hidden;
        }

        .glass-card {
            background: rgba(13, 20, 36, 0.75);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border: 1px solid rgba(56, 189, 248, 0.3);
            border-radius: 12px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
        }

        .header-bar {
            background: rgba(10, 16, 28, 0.85);
            border: 1px solid rgba(56, 189, 248, 0.3);
            border-radius: 10px;
        }

        .badge-red {
            background-color: rgba(239, 68, 68, 0.2);
            border: 1px solid #ef4444;
            color: #f87171;
        }

        .badge-pill {
            background: rgba(15, 23, 42, 0.8);
            border: 1px solid rgba(56, 189, 248, 0.4);
        }
    </style>
</head>
<body>

    <!-- TOP HEADER -->
    <div class="flex items-center justify-between p-3 mb-4 header-bar">
        <div class="flex items-center space-x-3">
            <span class="px-3 py-1 text-xs font-bold rounded-full badge-red flex items-center">
                <span class="w-2 h-2 mr-2 bg-red-500 rounded-full animate-ping"></span>
                Emergency Mode Active
            </span>
        </div>

        <div class="flex items-center space-x-2 badge-pill px-6 py-2 rounded-lg">
            <span class="text-xl">🛸</span>
            <h1 class="text-lg font-extrabold tracking-wider text-sky-400">AEROGUARD Command Center</h1>
            <span class="text-xs text-gray-400 bg-slate-800 px-2 py-0.5 rounded ml-2">detection.py (AI Teampy)</span>
        </div>

        <div class="flex items-center space-x-4 text-xs text-gray-300">
            <div class="badge-pill px-3 py-1.5 rounded flex items-center space-x-2">
                <span>⚡ Temporary Operations Center</span>
            </div>
            <div class="badge-pill px-3 py-1.5 rounded">
                <span>🕒 Mission: 12:33 AM</span>
            </div>
        </div>
    </div>

    <!-- MAIN GRID CONTAINER -->
    <div class="grid grid-cols-12 gap-4 h-[calc(100vh-90px)]">
        
        <!-- LEFT: GIS MAP GRID -->
        <div class="col-span-4 glass-card p-4 flex flex-col justify-between relative overflow-hidden">
            <div class="flex justify-between items-center mb-2">
                <div>
                    <h2 class="text-sm font-semibold text-gray-200">GIS Satellite Tracking & Search Grid</h2>
                    <p class="text-xs text-gray-400">Member 2 (Folium)</p>
                </div>
                <span class="text-gray-400 text-xs">⋮</span>
            </div>
            
            <!-- Map Visualization Box -->
            <div class="relative w-full h-full rounded-lg overflow-hidden border border-sky-500/20 bg-slate-900/80">
                <img src="https://images.unsplash.com/photo-1524661135-423995f22d0b?q=80&w=1000&auto=format&fit=crop" class="w-full h-full object-cover opacity-60" alt="Map">
                
                <!-- Hexagon Overlays -->
                <div class="absolute inset-0 flex items-center justify-center">
                    <div class="border border-sky-400/50 bg-sky-500/10 px-3 py-1 rounded text-xs text-sky-300 font-mono">SEARCHED ZONE</div>
                </div>
                
                <div class="absolute top-4 left-4 bg-slate-900/90 p-1.5 rounded border border-gray-700 text-xs font-bold">
                    <div>+</div>
                    <hr class="border-gray-700 my-1">
                    <div>-</div>
                </div>
            </div>
        </div>

        <!-- CENTER: THERMAL VISION & TELEMETRY -->
        <div class="col-span-5 flex flex-col space-y-4">
            
            <!-- Thermal Feed Box -->
            <div class="glass-card p-4 flex-1 flex flex-col justify-between">
                <div class="flex justify-between items-center mb-2">
                    <div>
                        <h2 class="text-sm font-semibold text-gray-200">Thermal Vision & Target Detection Feed</h2>
                        <p class="text-xs text-gray-400">Member 3 (AI Team)</p>
                    </div>
                    <span class="text-gray-400 text-xs">⋮</span>
                </div>

                <!-- Video Frame Simulation -->
                <div class="relative w-full h-56 rounded-lg overflow-hidden bg-black border border-red-500/30 flex items-center justify-center">
                    <img src="https://images.unsplash.com/photo-1578632767115-351597cf2477?q=80&w=1000&auto=format&fit=crop" class="w-full h-full object-cover grayscale opacity-70" alt="Thermal">
                    
                    <!-- Detection Box Overlay -->
                    <div class="absolute border-2 border-red-500 bg-red-500/10 p-2 rounded text-center">
                        <span class="bg-red-600 text-white text-[10px] px-1 font-bold">RESCUE WORKER: 92%</span>
                    </div>

                    <div class="absolute bottom-2 left-2 right-2 bg-slate-900/90 border border-red-500/40 p-1.5 rounded text-[11px] font-mono text-red-400">
                        SURVIVOR DETECTED: 92% CONFIDENCE<br>LOCATION: 18.52° N, 73.85° E
                    </div>
                </div>
            </div>

            <!-- Telemetry Graph Box -->
            <div class="glass-card p-4 h-36 flex flex-col justify-between">
                <div class="flex justify-between items-center">
                    <h2 class="text-sm font-semibold text-gray-200">Telemetry Log</h2>
                    <span class="text-xs text-gray-400 border border-gray-700 px-2 py-0.5 rounded">Live Graphs Log</span>
                </div>
                <div class="w-full h-20 bg-slate-900/50 rounded border border-sky-500/20 flex items-end p-2 space-x-1">
                    <div class="bg-sky-500/60 w-full h-[40%] rounded-t"></div>
                    <div class="bg-sky-500/60 w-full h-[70%] rounded-t"></div>
                    <div class="bg-sky-500/60 w-full h-[30%] rounded-t"></div>
                    <div class="bg-sky-500/60 w-full h-[85%] rounded-t"></div>
                    <div class="bg-sky-500/60 w-full h-[60%] rounded-t"></div>
                </div>
            </div>
        </div>

        <!-- RIGHT: 3D HARDWARE TWIN & TRIAGE LOG -->
        <div class="col-span-3 flex flex-col space-y-4">
            
            <!-- 3D Drone Twin -->
            <div class="glass-card p-4 flex-1 flex flex-col justify-between">
                <div class="flex justify-between items-center mb-2">
                    <div>
                        <h2 class="text-sm font-semibold text-gray-200">3D Hardware Twin & Payload</h2>
                        <p class="text-xs text-gray-400">Member 4 (DD Team)</p>
                    </div>
                    <span class="text-gray-400 text-xs">⋮</span>
                </div>

                <div class="w-full h-44 bg-slate-900/60 rounded-lg border border-sky-500/30 flex items-center justify-center p-2">
                    <img src="https://png.pngtree.com/png-vector/20230318/ourmid/pngtree-drone-camera-tactical-png-image_6650800.png" class="max-h-full object-contain filter drop-shadow-[0_0_10px_rgba(56,189,248,0.5)]" alt="Drone">
                </div>
            </div>

            <!-- Triage Log -->
            <div class="glass-card p-4 h-44 flex flex-col justify-between">
                <div class="flex justify-between items-center mb-1">
                    <div>
                        <h2 class="text-sm font-semibold text-gray-200">Triage Log</h2>
                        <p class="text-xs text-gray-400">Member 5/Integration</p>
                    </div>
                </div>

                <div class="text-[11px] font-mono w-full">
                    <div class="flex justify-between bg-red-500/20 text-red-300 p-1 rounded mb-1 border border-red-500/30">
                        <span>RED</span>
                        <span>12:43 PM</span>
                        <span>18.52° N</span>
                    </div>
                    <div class="flex justify-between bg-amber-500/20 text-amber-300 p-1 rounded mb-1 border border-amber-500/30">
                        <span>AMBER</span>
                        <span>12:33 PM</span>
                        <span>18.52° N</span>
                    </div>
                    <div class="flex justify-between bg-emerald-500/20 text-emerald-300 p-1 rounded border border-emerald-500/30">
                        <span>GREEN</span>
                        <span>12:31 PM</span>
                        <span>18.52° N</span>
                    </div>
                </div>
            </div>

        </div>

    </div>

</body>
</html>
"""

# Render Full Height Application Canvas
components.html(html_dashboard, height=720, scrolling=False)
