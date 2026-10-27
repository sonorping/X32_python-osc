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
