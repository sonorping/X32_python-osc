import mido
from pythonosc import udp_client

X32_IP = "192.168.1.10"                     # Match your X32 IP
X32_PORT = 10023                            # Default port X32 uses for OSC
IAC_NAME_FRONT = "IAC Driver"               # Requirement
IAC_NAME = "X32-Bridge"                     # Match your IAC bus name
IAC_BUS = f"{IAC_NAME_FRONT} {IAC_NAME}"    # variable concatenation for complete IAC bus name

client = udp_client.SimpleUDPClient(X32_IP, X32_PORT)

# Listen to the virtual IAC bus
with mido.open_input(IAC_BUS) as inport:
    print(f"Listening for MainStage MIDI on {IAC_BUS}")
    for msg in inport:
        if msg.type == 'program_change':
            cue_index = msg.program  # 0 to 99 corresponds to Cue 1 to 100
            client.send_message("/-action/gocue", cue_index)
            print(f"Loaded X32 Cue: {cue_index + 1} (Sent value: {cue_index})")

#                       The +1 language went here^
