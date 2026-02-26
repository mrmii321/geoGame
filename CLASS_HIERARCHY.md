# GameObject Class Hierarchy

```
                                GameObject
                                    |
                    +---------------+---------------+---------------+
                    |               |               |               |
              SolidObject     HazardObject    TriggerObject   PortalObject
                    |               |               |               |
                    |               |               |               |
                  Block           Spike      +------+------+   +----+----+
                                             |             |   |         |
                                         JumpPad      JumpOrb  Gravity  Speed
                                                                Portal   Portal
```

## Class Responsibilities

### GameObject (Abstract Base)
- Position (grid_x, grid_y)
- Size (width_cells, height_cells)
- Hitbox (pygame.Rect)
- Color
- Drawing
- Visibility checking
- `on_player_collision(player)` - Override in subclasses

### SolidObject
**Purpose:** Objects the player can stand on
**Behavior:** 
- Landing on top: Player stands on it
- Hitting from side/bottom: Player dies
**Example:** Platforms, blocks

### HazardObject
**Purpose:** Objects that kill the player
**Behavior:** 
- Any contact: Player dies
**Example:** Spikes, saws, lava

### TriggerObject
**Purpose:** Objects that activate when touched
**Behavior:**
- Touch: Calls `apply_effect(player)` once
- Leave: Resets trigger
- Touch again: Activates again
**Example:** Jump pads, orbs, collectibles

### PortalObject
**Purpose:** Objects that change player state
**Behavior:**
- Pass through: Calls `apply_effect(player)` once
- Leave: Resets activation
- Pass through again: Activates again
**Example:** Gravity portals, speed portals, game mode portals

## Method Flow

### Every Frame:
```
game_state.update()
  └─> player.update(floor, objects, camera_x)
       └─> collision.check_objects(objects)
            └─> for each object:
                 └─> object.on_player_collision(player)
                      └─> [Object-specific behavior]
```

### SolidObject Flow:
```
on_player_collision(player)
  └─> Check if colliding
       ├─> Landing on top?
       │    └─> Set player on ground, return False
       └─> Hitting side/bottom?
            └─> Return True (kill player)
```

### HazardObject Flow:
```
on_player_collision(player)
  └─> Check if colliding
       └─> Yes? Return True (kill player)
```

### TriggerObject Flow:
```
on_player_collision(player)
  └─> Check if colliding AND not triggered
       ├─> Yes? Call apply_effect(player), set triggered=True
       └─> Not colliding? Set triggered=False
  └─> Return False (never kills)
```

### PortalObject Flow:
```
on_player_collision(player)
  └─> Check if colliding AND not activated
       ├─> Yes? Call apply_effect(player), set activated=True
       └─> Not colliding? Set activated=False
  └─> Return False (never kills)
```

## Adding New Behavioral Categories

Want a new category? Just subclass GameObject:

```python
class CollectibleObject(GameObject):
    """Objects that can be collected"""
    def __init__(self, grid_x, grid_y, width_cells=1, height_cells=1):
        super().__init__(grid_x, grid_y, width_cells, height_cells)
        self.collected = False
    
    def on_player_collision(self, player):
        if not self.collected:
            world_rect = pygame.Rect(player.display_x, player.y, 
                                     player.width, player.height)
            if world_rect.colliderect(self.rect):
                self.collect(player)
                self.collected = True
        return False
    
    def collect(self, player):
        """Override in subclass"""
        pass
    
    def draw(self, surface, camera_x):
        if not self.collected:
            super().draw(surface, camera_x)
```

Then create specific collectibles:

```python
class Coin(CollectibleObject):
    def __init__(self, grid_x, grid_y, width_cells=1, height_cells=1):
        super().__init__(grid_x, grid_y, width_cells, height_cells)
        self.colour = (255, 215, 0)
        self.value = 1
    
    def collect(self, player):
        # Add to player's score or coin count
        pass
```

Register and use:
```python
ObjectFactory.register_object("Coin", Coin)
```

```json
{"object": "Coin", "x": 15, "y": 8, "width": 1, "height": 1}
```

## Design Patterns Used

1. **Inheritance** - Class hierarchy for shared behavior
2. **Polymorphism** - Each object handles its own collision
3. **Factory Pattern** - ObjectFactory creates objects from JSON
4. **Template Method** - Base classes define structure, subclasses fill in details
5. **Strategy Pattern** - Different collision strategies per object type

## Benefits of This Design

✅ **Open/Closed Principle** - Open for extension, closed for modification
✅ **Single Responsibility** - Each class has one job
✅ **Liskov Substitution** - Any GameObject can be used interchangeably
✅ **Dependency Inversion** - Game loop depends on GameObject abstraction
✅ **Don't Repeat Yourself** - Shared code in base classes

This is clean, professional, scalable OOP architecture! 🎮
