"""Task management module."""

class TaskManager:
    """Manages tasks."""
    
    def __init__(self):
        self.tasks = []
    
    def create_task(self, title: str, description: str) -> dict:
        """Create a new task."""
        task = {
            "id": len(self.tasks) + 1,
            "title": title,
            "description": description,
            "completed": False
        }
        self.tasks.append(task)
        return task
    
    def complete_task(self, task_id: int) -> bool:
        """Mark a task as completed."""
        for task in self.tasks:
            if task["id"] == task_id:
                task["completed"] = True
                return True
        return False
