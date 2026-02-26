from main.objects.object_types import Block, Spike, JumpPad, JumpOrb, GravityPortal, SpeedPortal


class ObjectFactory:
    """Factory for creating game objects from JSON data"""
    
    # Map object names to classes
    OBJECT_MAP = {
        "Block": Block,
        "Spike": Spike,
        "JumpPad": JumpPad,
        "JumpOrb": JumpOrb,
        "GravityPortal": GravityPortal,
        "SpeedPortal": SpeedPortal,
    }
    
    @staticmethod
    def create(obj_data):
        """Create a game object from JSON data"""
        obj_type = obj_data.get("object", "Block")  # Default to Block for backward compatibility
        
        # Get the class from the map
        obj_class = ObjectFactory.OBJECT_MAP.get(obj_type, Block)
        
        # Extract position and size
        grid_x = obj_data.get("x", 0)
        grid_y = obj_data.get("y", 0)
        width = obj_data.get("width", 1)
        height = obj_data.get("height", 1)
        
        # Handle special parameters for specific objects
        if obj_type == "SpeedPortal":
            speed_multiplier = obj_data.get("speed_multiplier", 2.0)
            return obj_class(grid_x, grid_y, width, height, speed_multiplier)
        
        return obj_class(grid_x, grid_y, width, height)
    
    @staticmethod
    def register_object(name, obj_class):
        """Register a new object type"""
        ObjectFactory.OBJECT_MAP[name] = obj_class
