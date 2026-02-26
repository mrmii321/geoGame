# GameObject System Documentation

## Overview

The game engine now uses a clean Object-Oriented Programming (OOP) inheritance system for all gameplay objects. This eliminates conditional type-checking and allows easy extension with new object types.

## Architecture

### Base Class: GameObject

All game objects inherit from `GameObject`, which provides:
- World position (grid-based)
- pygame Rect hitbox
- Rendering functionality
- `update()` method
- `on_player_collision(player)` method
- Visibility checking

### Behavioral Subclasses

#### SolidObject
- Base class for platforms and blocks
- Handles landing on top vs. side collision
- Kills player on side/bottom collision

#### HazardObject
- Base class for hazards (spikes, saws, etc.)
- Kills player on any contact

#### TriggerObject
- Base class for trigger-based objects
- Activates once when player touches
- Resets when player leaves
- Subclasses override `apply_effect(player)`

#### PortalObject
- Base class for portals that modify player state
- Activates once per pass-through
- Subclasses override `apply_effect(player)`

### Specific Object Types

#### Block (SolidObject)
- Standard platform
- Green color
- Solid collision

#### Spike (HazardObject)
- Kills player on contact
- Red color

#### JumpPad (TriggerObject)
- Launches player upward
- Purple color
- Jump power: -15

#### JumpOrb (TriggerObject)
- Gives player a jump when space is pressed
- Yellow color
- Jump power: -12

#### GravityPortal (PortalObject)
- Flips gravity direction
- Blue color
- Inverts player gravity and jump strength

#### SpeedPortal (PortalObject)
- Changes player speed
- Orange color
- Configurable speed multiplier

## JSON Format

### New Format (with object types)
```json
{
    "object": "Spike",
    "x": 15,
    "y": 9,
    "width": 1,
    "height": 1
}
```

### Backward Compatibility
Objects without an "object" field default to Block:
```json
{
    "x": 10,
    "y": 10,
    "width": 20,
    "height": 1
}
```

### Special Parameters
Some objects support additional parameters:
```json
{
    "object": "SpeedPortal",
    "x": 50,
    "y": 8,
    "width": 1,
    "height": 2,
    "speed_multiplier": 2.5
}
```

## Object Factory

The `ObjectFactory` class handles object instantiation:

```python
from main.objects.object_factory import ObjectFactory

# Create from JSON data
obj_data = {"object": "Spike", "x": 10, "y": 5, "width": 1, "height": 1}
spike = ObjectFactory.create(obj_data)
```

### Registering New Object Types

```python
from main.objects.object_factory import ObjectFactory
from main.objects.game_object import HazardObject

class Lava(HazardObject):
    def __init__(self, grid_x, grid_y, width_cells=1, height_cells=1):
        super().__init__(grid_x, grid_y, width_cells, height_cells)
        self.colour = (255, 100, 0)

# Register the new type
ObjectFactory.register_object("Lava", Lava)
```

## Adding New Object Types

### Step 1: Create the Class

```python
from main.objects.game_object import TriggerObject

class Trampoline(TriggerObject):
    def __init__(self, grid_x, grid_y, width_cells=1, height_cells=1):
        super().__init__(grid_x, grid_y, width_cells, height_cells)
        self.colour = (0, 255, 0)
        self.bounce_power = -20
    
    def apply_effect(self, player):
        player.y_vel = self.bounce_power
```

### Step 2: Register in ObjectFactory

Edit `object_factory.py`:
```python
from main.objects.object_types import Block, Spike, JumpPad, Trampoline

class ObjectFactory:
    OBJECT_MAP = {
        "Block": Block,
        "Spike": Spike,
        "JumpPad": JumpPad,
        "Trampoline": Trampoline,  # Add here
        # ...
    }
```

### Step 3: Use in JSON

```json
{
    "object": "Trampoline",
    "x": 25,
    "y": 10,
    "width": 2,
    "height": 1
}
```

## Collision System

The collision system now uses polymorphism:

```python
# In player update loop
for obj in objects:
    if obj.on_player_collision(player):
        # Player died
        return self.die()
```

Each object type implements its own collision behavior:
- **SolidObject**: Checks landing vs. side collision
- **HazardObject**: Always kills on contact
- **TriggerObject**: Applies effect once per touch
- **PortalObject**: Applies effect once per pass-through

## Benefits

1. **No Type Checking**: No more `if obj.type == "spike"` conditionals
2. **Polymorphic Behavior**: Each object handles its own collision logic
3. **Easy Extension**: Add new objects by subclassing
4. **Clean Code**: Behavior lives in the object class, not the main loop
5. **Scalable**: Factory pattern allows unlimited object types

## Migration Guide

### Old System
```python
if platform.type == "spike":
    player.die()
elif platform.type == "jump_pad":
    player.y_vel = -15
```

### New System
```python
if obj.on_player_collision(player):
    player.die()
```

The object itself handles the behavior internally.
