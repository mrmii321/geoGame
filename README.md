# GeoGame - Geometry Dash Style Game Engine

A professional, extensible game engine built with Python and Pygame featuring a clean Object-Oriented Programming architecture.

## 🎮 Features

- **Clean OOP Architecture** - Inheritance-based GameObject system
- **Polymorphic Behavior** - No type checking, pure polymorphism
- **Factory Pattern** - JSON-driven object instantiation
- **Easy Extension** - Add new objects in 3 simple steps
- **Multiple Object Types** - Blocks, Spikes, Jump Pads, Orbs, Portals
- **Level System** - JSON-based level format
- **Particle Effects** - Dynamic particle system
- **Menu System** - Main menu and level selection

## 🚀 Quick Start

### Prerequisites
- Python 3.7+
- Pygame

### Installation
```bash
pip install pygame
```

### Run the Game
```bash
python src/app.py
```

### Verify System Integrity
```bash
python src/main/verify_migration.py
```

## 📁 Project Structure

```
geoGame/
├── src/
│   ├── main/
│   │   ├── objects/          # GameObject system
│   │   │   ├── game_object.py      # Base classes
│   │   │   ├── object_types.py     # Specific objects
│   │   │   ├── object_factory.py   # Factory pattern
│   │   │   ├── floor_terrain.py    # Floor object
│   │   │   └── particle.py         # Particle system
│   │   ├── playerDir/        # Player logic
│   │   ├── controller/       # Input handling
│   │   ├── mainMenu/         # Menu system
│   │   ├── screenDir/        # Display management
│   │   ├── game_state.py     # Game state manager
│   │   ├── objects.json      # Level data
│   │   └── constants.py      # Game constants
│   └── app.py                # Entry point
└── [Documentation Files]
```

## 🎯 Available Object Types

| Object | Type | Behavior |
|--------|------|----------|
| **Block** | SolidObject | Standard platform |
| **Spike** | HazardObject | Kills on contact |
| **JumpPad** | TriggerObject | Launches player upward |
| **JumpOrb** | TriggerObject | Jump when space pressed |
| **GravityPortal** | PortalObject | Flips gravity |
| **SpeedPortal** | PortalObject | Changes player speed |

## 🛠️ Adding New Objects

### 1. Create the Class
```python
# In src/main/objects/object_types.py
class Trampoline(TriggerObject):
    def __init__(self, grid_x, grid_y, width_cells=1, height_cells=1):
        super().__init__(grid_x, grid_y, width_cells, height_cells)
        self.colour = (0, 255, 0)
    
    def apply_effect(self, player):
        player.y_vel = -20
```

### 2. Register in Factory
```python
# In src/main/objects/object_factory.py
OBJECT_MAP = {
    # ...
    "Trampoline": Trampoline,
}
```

### 3. Use in JSON
```json
{"object": "Trampoline", "x": 25, "y": 10, "width": 2, "height": 1}
```

That's it! No game loop changes needed.

## 📖 Documentation

- **[EXECUTIVE_SUMMARY.md](EXECUTIVE_SUMMARY.md)** - Project overview and metrics
- **[MIGRATION_COMPLETE.md](MIGRATION_COMPLETE.md)** - Migration details and verification
- **[GAMEOBJECT_SYSTEM.md](GAMEOBJECT_SYSTEM.md)** - Complete technical documentation
- **[QUICK_REFERENCE.md](QUICK_REFERENCE.md)** - Developer quick reference
- **[CLASS_HIERARCHY.md](CLASS_HIERARCHY.md)** - Architecture diagrams
- **[TUTORIAL_NEW_OBJECTS.md](TUTORIAL_NEW_OBJECTS.md)** - Step-by-step tutorials

## 🎮 Controls

- **SPACE** - Jump
- **ESC** - Return to menu (during gameplay)
- **ENTER** - Select menu option
- **UP/DOWN** - Navigate menu

## 🏗️ Architecture

### GameObject Hierarchy
```
GameObject (base)
├── SolidObject → Block
├── HazardObject → Spike
├── TriggerObject → JumpPad, JumpOrb
└── PortalObject → GravityPortal, SpeedPortal
```

### Design Patterns
- **Inheritance** - Clean class hierarchy
- **Polymorphism** - Dynamic behavior dispatch
- **Factory Pattern** - Object creation abstraction
- **Template Method** - Base class structure

### SOLID Principles
✓ Single Responsibility
✓ Open/Closed
✓ Liskov Substitution
✓ Interface Segregation
✓ Dependency Inversion

## 🧪 Testing

### Automated Verification
```bash
python src/main/verify_migration.py
```

### Manual Testing
1. Launch game
2. Select level
3. Test player movement
4. Verify collisions
5. Test all object types

## 📊 System Status

| Component | Status |
|-----------|--------|
| GameObject System | ✓ Complete |
| Factory Pattern | ✓ Integrated |
| Polymorphic Collision | ✓ Working |
| Legacy Code | ✓ Removed |
| Documentation | ✓ Complete |
| Verification | ✓ All checks pass |

## 🔧 Utilities

### JSON Converter
Convert old JSON format to new format:
```bash
python src/main/convert_json.py input.json output.json
```

### Migration Verification
Verify system integrity:
```bash
python src/main/verify_migration.py
```

## 📝 JSON Level Format

```json
[
    [
        {"object": "Block", "x": 10, "y": 10, "width": 5, "height": 1},
        {"object": "Spike", "x": 15, "y": 9, "width": 1, "height": 1},
        {"object": "JumpPad", "x": 20, "y": 10, "width": 2, "height": 1},
        {"object": "GravityPortal", "x": 30, "y": 8, "width": 1, "height": 2}
    ]
]
```

## 🎓 Learning Resources

- **Beginners:** Start with QUICK_REFERENCE.md
- **Developers:** Read GAMEOBJECT_SYSTEM.md
- **Adding Objects:** Follow TUTORIAL_NEW_OBJECTS.md
- **Architecture:** Study CLASS_HIERARCHY.md

## 🚀 Future Enhancements

The system supports easy addition of:
- Collectible coins
- Checkpoints
- Moving platforms
- Rotating hazards
- Teleporters
- Power-ups
- Custom animations
- Sound effects

## 📄 License

[Your License Here]

## 👥 Contributors

[Your Name/Team]

## 🙏 Acknowledgments

Built with Python and Pygame
Inspired by Geometry Dash

---

**Status:** Production Ready ✓
**Quality:** Enterprise Grade ✓
**Architecture:** Professional OOP ✓

🎮 **Happy Gaming!**
