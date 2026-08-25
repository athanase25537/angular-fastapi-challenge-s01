import json
from pathlib import Path

import json
from pathlib import Path


def make_interface_file_nameinterface_name(name: str, ) -> str:
    title = name[0].lower()
    for i in range(1, len(name)):
        title += name[i] if name[i].islower() else f"-{name[i].lower()}"
    
    return title


def write_typescript(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", encoding="utf-8") as file:
        file.write(content)
    
        
def generate(data: dict):
     
    for interface_name, interface_value in data.items():
        if "properties" in interface_value and "required" in interface_value:
            properties = interface_value["properties"]
            required = interface_value["required"]
            
            data_to_write = {}
            
            for key, value in properties.items():
                if"type" in value:
                    d = { key: value["type"] } if key in required else { key: value["type"] + " | null" }
                    data_to_write.update(d)

            write_typescript(
                Path(f"generated/interfaces/{make_interface_file_nameinterface_name(interface_name)}.ts"),
                "export interface " + interface_name + " {\n" + "\n".join(f"  {name}: {type};" for name, type in data_to_write.items()) + "\n}"
            )



def load_openapi(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def write_typescript(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", encoding="utf-8") as file:
        file.write(content)


def main():
    openapi = load_openapi("openapi.json")

    schemas = openapi["components"]["schemas"]
    
    schemasToTransform = { key: value for key, value in schemas.items() if key not in ["HTTPValidationError", "ValidationError"] }
    
    generate(schemasToTransform)


if __name__ == "__main__":
    main()