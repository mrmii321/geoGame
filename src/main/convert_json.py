import json
import sys

def convert_json_to_new_format(input_file, output_file):
    """
    Convert old JSON format to new GameObject format.
    Old format: {"x": 10, "y": 10, "width": 1, "height": 1}
    New format: {"object": "Block", "x": 10, "y": 10, "width": 1, "height": 1}
    """
    try:
        with open(input_file, 'r') as f:
            data = json.load(f)
        
        # Convert each level
        for level in data:
            for obj in level:
                # Add "object" field if it doesn't exist
                if "object" not in obj:
                    obj["object"] = "Block"
        
        # Write to output file
        with open(output_file, 'w') as f:
            json.dump(data, f, indent=4)
        
        print(f"Successfully converted {input_file} to {output_file}")
        print(f"Converted {sum(len(level) for level in data)} objects across {len(data)} levels")
        
    except FileNotFoundError:
        print(f"Error: File {input_file} not found")
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON in {input_file}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python convert_json.py <input_file> [output_file]")
        print("Example: python convert_json.py objects.json objects_new.json")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else input_file.replace('.json', '_converted.json')
    
    convert_json_to_new_format(input_file, output_file)
