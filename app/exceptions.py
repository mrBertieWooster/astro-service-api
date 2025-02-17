class HoroscopeGenerationError(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)
        
class CalculatingPlanetsError(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

class OpenAIAPIError(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

class DatabaseError(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)
