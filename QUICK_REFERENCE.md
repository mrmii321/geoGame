# Quick Reference: GameObject System

## Available Object Types

| Object | Type | Color | Behavior |
|--------|------|-------|----------|
| Block | SolidObject | Green | Standard platform, solid collision |
| Spike | HazardObject | Red | Kills player on contact |
| JumpPad | TriggerObject | Purple | Launches player upward (-15) |
| JumpOrb | TriggerObject | Yellow | Jump when space pressed (-12) |
| GravityPortal | PortalObject | Blue | Flips gravity direction |
| SpeedPortal | PortalObject | Orange | Changes player speed |

## JSON Examples

### Basic Block
```json
{"object": "Block", "x": 10, "y": 10, "width": 5, "height": 1}
```

### Spike
```json
{"object": "Spike", "x": 15, "y": 9, "width": 1, "height": 1}
```

### Jump Pad
```json
{"object": "JumpPad", "x": 20, "y": 10, "width": 2, "height": 1}
```

### Speed Portal (with custom multiplier)
```json
{"object": "SpeedPortal", "x": 50, "y": 8, "width": 1, "height": 2, "speed_multiplier": 2.5}
```

## Creating Custom Objects

### 1. Choose Base Class
- `SolidObject` - for platforms
- `HazardObject` - for instant-kill objects
- `TriggerObject` - for objects that activate on touch
- `PortalObject` - for state-changing portals

### 2. Implement Class
```python
from main.objects.game_object import TriggerObject

class MyObject(TriggerObject):
    def __init__(self, grid_x, grid_y, width_cells=1, height_cells=1):
        super().__init__(grid_x, grid_y, width_cells, height_cells)
        self.colour = (255, 0, 255)  # Set color
    
    def apply_effect(self, player):
        # Your custom behavior here
        player.y_vel = -20
```

### 3. Register in Factory
Add to `object_factory.py`:
```python
OBJECT_MAP = {
    # ...
    "MyObject": MyObject,
}
```

### 4. Use in JSON
```json
{"object": "MyObject", "x": 30, "y": 8, "width": 1, "height": 1}
```

## Key Methods to Override

### on_player_collision(player)
- Called every frame when player touches object
- Return `True` to kill player
- Return `False` to keep player alive

### apply_effect(player)
- Only for TriggerObject and PortalObject
- Called once when triggered
- Modify player properties here

### update()
- Called every frame
- Use for animated objects

### draw(surface, camera_x)
- Override for custom rendering
- Default draws a colored rectangle

## Player Properties You Can Modify

```python
player.y_vel          # Vertical velocity
player.speed          # Horizontal speed
player.gravity        # Gravity strength
player.jump_strength  # Jump power
player.on_ground      # Ground state
```

## Converting Old JSON Files

Run the conversion script:
```bash
python src/main/convert_json.py src/main/objects.json
```

This adds `"object": "Block"` to all existing entries.
