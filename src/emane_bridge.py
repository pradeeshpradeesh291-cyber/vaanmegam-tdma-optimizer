import json
import sys
import os

# Ensure Python can find tdma_optimizer in the same directory
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from tdma_optimizer import build_topology_graphs, optimize_tdma_schedule, verify_schedule

def generate_emane_tdma_xml(node_to_slot, output_path="config/emane_schedule.xml"):
    """
    Converts Python node-to-slot assignments into an EMANE TDMA Radio Model schedule XML format.
    """
    total_slots = max(node_to_slot.values()) + 1 if node_to_slot else 0
    
    # Create config directory if it doesn't exist
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    xml_lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<!DOCTYPE emaneevent SYSTEM "file:///usr/share/emane/dtd/tdmascheduleevent.dtd">',
        '<emaneevent module="tdmaschedule">',
        '  <tdmaschedule>',
        f'    <structure frames="1" slots="{total_slots}">',
        '      <slot index="0" duration="1000"/> <!-- 1ms slot duration -->',
        '    </structure>',
        '    <schedules>'
    ]
    
    # Sort nodes numerically for clean XML output
    sorted_nodes = sorted(node_to_slot.keys(), key=lambda x: int(''.join(filter(str.isdigit, x)) or 0))
    
    for node in sorted_nodes:
        slot = node_to_slot[node]
        node_id = int(''.join(filter(str.isdigit, node)) or 0)
        xml_lines.append(f'      <entry nem="{node_id}">')
        xml_lines.append(f'        <frequency slot="{slot}" channel="0"/>')
        xml_lines.append(f'        <tx slot="{slot}"/>')
        xml_lines.append(f'        <rx slot="{slot}"/>')
        xml_lines.append('      </entry>')
        
    xml_lines.extend([
        '    </schedules>',
        '  </tdmaschedule>',
        '</emaneevent>'
    ])
    
    xml_content = "\n".join(xml_lines)
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(xml_content)
        
    print("==================================================")
    print("      EMANE INTEGRATION BRIDGE GENERATOR          ")
    print("==================================================")
    print(f"Total Unique Slots Scheduled : {total_slots}")
    print(f"Schedule File Generated      : {output_path}")
    print("==================================================")
    print("Verification: Schedule successfully transformed to XML.")

def main():
    if len(sys.argv) < 2:
        print("Usage: python src/emane_bridge.py '<JSON_COORDINATES_STRING>'")
        sys.exit(1)
        
    json_input = sys.argv[1]
    
    try:
        nodes_dict = json.loads(json_input)
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON input: {e}")
        sys.exit(1)
        
    G1, G2 = build_topology_graphs(nodes_dict, communication_range=500.0)
    node_to_slot = optimize_tdma_schedule(G2)
    
    if not verify_schedule(G2, node_to_slot):
        print("Schedule verification failed! Cannot export to EMANE.")
        sys.exit(1)
        
    # Generate XML in config/ folder relative to root
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    output_xml = os.path.join(project_root, "config", "emane_schedule.xml")
    
    generate_emane_tdma_xml(node_to_slot, output_path=output_xml)

if __name__ == "__main__":
    main()
