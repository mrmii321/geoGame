# Tutorial: Adding New Object Types

This tutorial shows you exactly how to add new gameplay objects to your game engine.

## Example 1: Adding a Trampoline (Simple)

### Step 1: Create the Class

Add to `src/main/objects/object_types.py`:

```python
class Trampoline(TriggerObject):
    """Super bouncy trampoline"""
    def __init__(self, grid_x, grid_y, width_cells=1, height_cells=1):
        super().__init__(grid_x, grid_y, width_cells, height_cells)
        self.colour = (0, 255, 0)  # Bright green
        self.bounce_power = -20  # Stronger than jump pad
    
    def apply_effect(self, player):
        player.y_vel = self.bounce_power
```

### Step 2: Register in Factory

Edit `src/main/objects/object_factory.py`:

```python
from main.objects.object_types import Block, Spike, JumpPad, JumpOrb, GravityPortal, SpeedPortal, Trampoline

class ObjectFactory:
    OBJECT_MAP = {
        "Block": Block,
        "Spike": Spike,
        "JumpPad": JumpPad,
        "JumpOrb": JumpOrb,
        "GravityPortal": GravityPortal,
        "SpeedPortal": SpeedPortal,
        "Trampoline": Trampoline,  # Add this line
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

Done! The trampoline now works in your game.

---

## Example 2: Adding a Coin (Collectible)

### Step 1: Create the Class

Add to `src/main/objects/object_types.py`:

```python
class Coin(TriggerObject):
    """Collectible coin"""
    def __init__(self, grid_x, grid_y, width_cells=1, height_cells=1):
        super().__init__(grid_x, grid_y, width_cells, height_cells)
        self.colour = (255, 215, 0)  # Gold
        self.collected = False
        self.value = 1
    
    def apply_effect(self, player):
        if not self.collected:
            self.collected = True
            # You could add: player.coins += self.value
    
    def draw(self, surface, camera_x):
        # Only draw if not collected
        if not self.collected:
            super().draw(surface, camera_x)
```

### Step 2: Register in Factory

```python
"Coin": Coin,  # Add to OBJECT_MAP
```

### Step 3: Use in JSON

```json
{
    "object": "Coin",
    "x": 15,
    "y": 8,
    "width": 1,
    "height": 1
}
```

---

## Example 3: Adding a Moving Platform (Advanced)

### Step 1: Create the Class

Add to `src/main/objects/object_types.py`:

```python
class MovingPlatform(SolidObject):
    """Platform that moves horizontally"""
    def __init__(self, grid_x, grid_y, width_cells=1, height_cells=1, 
                 move_distance=5, move_speed=2):
        super().__init__(grid_x, grid_y, width_cells, height_cells)
        self.colour = (100, 150, 200)  # Light blue
        self.start_x = self.rect.x
        self.move_distance = move_distance * GRID_SIZE
        self.move_speed = move_speed
        self.direction = 1
    
    def update(self):
        # Move platform
        self.rect.x += self.move_speed * self.direction
        
        # Reverse direction at boundaries
        if self.rect.x >= self.start_x + self.move_distance:
            self.direction = -1
        elif self.rect.x <= self.start_x:
            self.direction = 1
```

### Step 2: Register in Factory

```python
"MovingPlatform": MovingPlatform,  # Add to OBJECT_MAP
```

### Step 3: Handle Custom Parameters in Factory

Edit the `create()` method in `object_factory.py`:

```python
@staticmethod
def create(obj_data):
    obj_type = obj_data.get("object", "Block")
    obj_class = ObjectFactory.OBJECT_MAP.get(obj_type, Block)
    
    grid_x = obj_data.get("x", 0)
    grid_y = obj_data.get("y", 0)
    width = obj_data.get("width", 1)
    height = obj_data.get("height", 1)
    
    # Handle special parameters
    if obj_type == "SpeedPortal":
        speed_multiplier = obj_data.get("speed_multiplier", 2.0)
        return obj_class(grid_x, grid_y, width, height, speed_multiplier)
    
    elif obj_type == "MovingPlatform":  # Add this
        move_distance = obj_data.get("move_distance", 5)
        move_speed = obj_data.get("move_speed", 2)
        return obj_class(grid_x, grid_y, width, height, move_distance, move_speed)
    
    return obj_class(grid_x, grid_y, width, height)
```

### Step 4: Update Game Loop

Edit `game_state.py` to call update on objects:

```python
def update(self):
    # ... existing code ...
    
    # Update all objects
    for obj in self.objects:
        obj.update()
    
    # ... rest of code ...
```

### Step 5: Use in JSON

```json
{
    "object": "MovingPlatform",
    "x": 30,
    "y": 8,
    "width": 3,
    "height": 1,
    "move_distance": 10,
    "move_speed": 3
}
```

---

## Example 4: Adding a Checkpoint

### Step 1: Create the Class

```python
class Checkpoint(TriggerObject):
    """Saves player progress"""
    def __init__(self, grid_x, grid_y, width_cells=1, height_cells=1):
        super().__init__(grid_x, grid_y, width_cells, height_cells)
        self.colour = (0, 255, 255)  # Cyan
        self.activated = False
    
    def apply_effect(self, player):
        if not self.activated:
            self.activated = True
            # Save checkpoint position
            player.initial_state['display_x'] = player.display_x
            player.initial_state['y'] = player.y
            # Change color to show it's activated
            self.colour = (0, 150, 150)
```

### Step 2: Register and Use

```python
"Checkpoint": Checkpoint,  # In factory
```

```json
{"object": "Checkpoint", "x": 50, "y": 9, "width": 1, "height": 2}
```

---

## Example 5: Adding a Size Portal

### Step 1: Create the Class

```python
class SizePortal(PortalObject):
    """Changes player size"""
    def __init__(self, grid_x, grid_y, width_cells=1, height_cells=1, 
                 size_multiplier=0.5):
        super().__init__(grid_x, grid_y, width_cells, height_cells)
        self.colour = (255, 0, 255)  # Magenta
        self.size_multiplier = size_multiplier
    
    def apply_effect(self, player):
        player.width = int(player.width * self.size_multiplier)
        player.height = int(player.height * self.size_multiplier)
        player.rect.width = player.width
        player.rect.height = player.height
```

### Step 2: Handle in Factory

```python
elif obj_type == "SizePortal":
    size_multiplier = obj_data.get("size_multiplier", 0.5)
    return obj_class(grid_x, grid_y, width, height, size_multiplier)
```

### Step 3: Use in JSON

```json
{
    "object": "SizePortal",
    "x": 60,
    "y": 8,
    "width": 1,
    "height": 2,
    "size_multiplier": 0.5
}
```

---

## Quick Reference: Which Base Class?

| Want to create... | Use base class | Override method |
|-------------------|----------------|-----------------|
| Platform/Block | `SolidObject` | None needed |
| Instant-kill hazard | `HazardObject` | None needed |
| One-time trigger | `TriggerObject` | `apply_effect(player)` |
| State-changing portal | `PortalObject` | `apply_effect(player)` |
| Collectible item | `TriggerObject` | `apply_effect(player)` + `draw()` |
| Moving object | Any + `update()` | `update()` |
| Animated object | Any + `update()` | `update()` + `draw()` |

---

## Common Patterns

### Pattern 1: One-Time Effect
```python
class MyObject(TriggerObject):
    def __init__(self, ...):
        super().__init__(...)
        self.used = False
    
    def apply_effect(self, player):
        if not self.used:
            # Do something
            self.used = True
```

### Pattern 2: Conditional Effect
```python
class MyObject(TriggerObject):
    def apply_effect(self, player):
        if player.controller.is_pressed(pygame.K_SPACE):
            # Only activate when space pressed
            pass
```

### Pattern 3: Timed Effect
```python
class MyObject(TriggerObject):
    def __init__(self, ...):
        super().__init__(...)
        self.effect_timer = 0
    
    def apply_effect(self, player):
        self.effect_timer = 60  # 1 second at 60 FPS
    
    def update(self):
        if self.effect_timer > 0:
            self.effect_timer -= 1
            # Apply effect while timer is active
```

### Pattern 4: Custom Drawing
```python
class MyObject(GameObject):
    def draw(self, surface, camera_x):
        draw_rect = self.rect.copy()
        draw_rect.x -= camera_x
        # Custom drawing code
        pygame.draw.circle(surface, self.colour, 
                          draw_rect.center, draw_rect.width // 2)
```

---

## Testing Your New Object

1. Add it to a test level JSON
2. Load the level in game
3. Test collision behavior
4. Test visual appearance
5. Test edge cases (multiple triggers, etc.)

---

## Troubleshooting

**Object doesn't appear:**
- Check if "object" name matches factory registration
- Check if position is on screen
- Check if color is visible against background

**Collision doesn't work:**
- Verify `on_player_collision()` is implemented
- Check hitbox size (rect)
- Test with different approach angles

**Effect doesn't trigger:**
- For TriggerObject: Check if `apply_effect()` is implemented
- Check if trigger is resetting properly
- Add print statements for debugging

**Object not in factory:**
- Did you add import statement?
- Did you add to OBJECT_MAP?
- Did you spell the name correctly?

---

## Summary

Adding new objects is a 3-step process:
1. **Create class** - Inherit from appropriate base class
2. **Register in factory** - Add to OBJECT_MAP
3. **Use in JSON** - Add to level files

That's it! No changes to the game loop required. The system handles everything through polymorphism.

Happy creating! 🎮
