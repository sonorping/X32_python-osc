# X32_python-osc
Converting MainStage program change midi commands into OSC cue change commands for the X32

**************************************************

The X32 listens for OSC on port 10023 by default. 
There is no need for any check boxes on the Setup->Midi Control tab.
There is nothing to change on Show Control->Midi
Just turn on the X32 and it is ready to recieve.

**************************************************

You will need the X32 IP address
You will need to create an IAC bus

**************************************************

MainStage prefs to check.

MIDI->Display->Program Change Range 1...128

In Layout (Concert level), devices (controllers, pitch bend, modulation, sustain etc.) must be changed from excepting all midi info from all channels, else there will be MIDI loops created.

**************************************************

This finds the network interface(s) in use and the IP address associated

networksetup -listallnetworkservices | tail -n +2 | while read -r service; do
  ip=$(networksetup -getinfo "$service" | awk -F': ' '/^IP address:/ {print $2}')
  device=$(networksetup -listallhardwareports | awk -v s="$service" '$0 ~ "Hardware Port: "s {getline; print $2}')
  if [ -n "$ip" ]; then
    printf "%-25s %-10s %s\n" "$service" "($device)" "$ip"
  fi
done

**********************************************

Option B: Lightweight Python Background Script (Free & Zero-Latency)
If you prefer not to purchase third-party bridging software, 
run a lightweight script using python-osc and mido:Pythonimport mido
from pythonosc import udp_client

X32_IP = "192.168.1.50"  # Match your X32 IP
X32_PORT = 10023

client = udp_client.SimpleUDPClient(X32_IP, X32_PORT)

# Listen to the virtual IAC bus
with mido.open_input('IAC Driver Bus 1') as inport:
    print("Listening for MainStage MIDI on IAC Driver Bus 1...")
    for msg in inport:
        if msg.type == 'program_change':
            scene_index = msg.program  # 0 to 99 corresponds to Scenes 1 to 100
            client.send_message("/-action/loadscene", scene_index)
            print(f"Loaded X32 Scene: {scene_index + 1} (Sent value: {scene_index})")
            
Step 4: Configure MainStage Patch Settings
In MainStage, select your Patch in the left sidebar.
Open the Patch Settings inspector at the bottom.
Select the MIDI Out tab.
Check Send Program Change:
Destination / Device: Select IAC Driver Bus 1.
Channel: Channel 1.
Program: Set the desired scene offset (e.g., 0 loads Scene 1, 1 loads Scene 2).

When you switch patches in MainStage, the MIDI PC is transmitted over the IAC bus, intercepted by your bridge, translated to native OSC, and sent over Ethernet to instantly recall the scene on the X32.

************************************************

what would i need to install on my macos to enable the use of this python script?


To run the Python bridge script on macOS, you only need Python 3 and two third-party packages (python-osc and mido with its MIDI port backend).

1. Check or Install Python 3
Open Terminal (press Cmd + Space, type Terminal, and hit Enter). Check if Python 3 is installed:

  Bash
  python3 --version

If it returns a version (e.g., Python 3.11.x or higher): You are ready to proceed.

If it prompts to install Xcode Command Line Tools: 
Click Install in the popup and wait for it to complete.
If Python is not installed: Download and install the official macOS installer from python.org or install it via Homebrew (brew install python).

***********************************************

2. Set Up a Virtual Environment & Install Libraries
Modern macOS versions require installing Python packages inside an isolated virtual environment to prevent externally-managed-environment errors.

In Terminal, create a project folder and install the required modules:

  Bash
  # 1. Create and navigate into a working folder
  mkdir -p ~/x32-bridge && cd ~/x32-bridge
  
  # 2. Create a virtual environment named "env"
  python3 -m venv env
  
  # 3. Activate the environment
  source env/bin/activate

  # 4. Install the OSC and MIDI packages (including python-rtmidi for CoreMIDI support)
  pip install python-osc mido python-rtmidi

Why python-rtmidi? While mido handles message parsing, it relies on an underlying backend like python-rtmidi to physically read and write to macOS CoreMIDI ports (such as the IAC Driver).

3. Verify Your MIDI Ports
To ensure the script will find your IAC Driver Bus 1, run a quick one-line check in Terminal:

  Bash
  python3 -c "import mido; print(mido.get_input_names())"

You should see a list containing 'IAC Driver Bus 1' (or the exact name you configured in macOS Audio MIDI Setup). 
If the string is formatted differently (e.g., 'IAC Driver: Bus 1'), update the string in the script to match.

4. Save and Run the Script
In the same folder, save the bridge code to a file named bridge.py:

  Bash
  nano bridge.py
  
Paste the script, then press Ctrl + O, Enter to save, and Ctrl + X to exit.

Run the script:

  Bash
  python3 bridge.py
  
To run it in future sessions, just navigate to the folder and activate the environment:

  Bash
  cd ~/x32-bridge
  source env/bin/activate
  python3 bridge.py
