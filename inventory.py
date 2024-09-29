import tkinter as tk

class Inventory:
    """
    Inventory class to manage a character's items.
    """ 
    def __init__(self, root):
        self.items = {}
        self.inventory_window = None
        self.root = root # Keep a reference to the main application window.
        
    def add_item(self, item, quantity=1):
        """
        Add an item to the inventory
        
        :param item: Item name
        :param quantity: Quantity of the item
        """
        if item in self.items:
            self.items[item] += quantity
        else:
            self.items[item] = quantity
            
    def remove_item(self, item, quantity=1):
        """
        Remove an item from the inventory.
        
        :param item: Item name
        :param quantity: Quantity to remove
        """
        if item in self.items:
            self.items[item] -= quantity
            if self.items[item] <= 0:
                del self.items[item]
                
    def get_items(self):
        """
        Get all items in the inventory.
        
        :return: Dictionary of items and quantities
        """
        return self.items 
    
    def toggle_inventory(self, event):
        """
        Toggle the inventory window on and off when the 'i' key is pressed.
        """
        if self.inventory_window is None:
            self.show_inventory_overlay()
        else:
            self.hide_inventory_overlay()
            
    def show_inventory_overlay(self):
        """
        Show the inventory in a new window (overlay).
        """
        self.inventory_window = tk.Toplevel(self.root)
        self.inventory_window.title("Inventory")
        self.inventory_window.geometry("300x200")
        
        # Create a label for each item in the inventory
        inventory_label = tk.Label(self.inventory_window, text="Inventory", font=("Arial", 16))
        inventory_label.pack(pady=10)
        
        items = self.get_items()
        if items:
            for item in items:
                item_label = tk.Label(self.inventory_window, text=item)
                item_label.pack()
        else:
            empty_label = tk.Label(self.inventory_window, text="Inventory is empty")
            empty_label.pack()
            
        # Close the inventory window when it is destroyed
        self.inventory_window.protocol("WM_DELETE_WINDOW", self.hide_inventory_overlay)
        
    def hide_inventory_overlay(self):
        """
        Hide the inventory window and set it to None.
        """
        if self.inventory_window is not None:
            self.inventory_window.destroy() 
            self.inventory_window = None